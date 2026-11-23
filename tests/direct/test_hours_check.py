"""Direct-mode tests for HoursCheck: OpenStreetMap opening hours checked against the business's own web page."""

import json
import re

import pytest

from tests.direct.conftest import CONTRACT_PATH, llm_json

OSM = "https://api.openstreetmap.org/api/0.6"
SITE = "https://www.example-cafe.co.uk/borough"
HOURS = "Mo-Fr 07:30-20:00; Sa 09:00-18:00; Su 12:00-18:00"
TEXT = ("<html><body><nav>Menu</nav><h1>Example Café, Borough</h1><h2>Opening hours</h2>"
        "<p>Monday 07:30 - 20:00 Tuesday 07:30 - 20:00 Wednesday 07:30 - 20:00 Thursday 07:30 - 20:00 Friday 07:30 - 20:00 "
        "Saturday 09:00 - 18:00 Sunday 12:00 - 18:00</p></body></html>")


def _ld(spec):
    return f'<script type="application/ld+json">{json.dumps({"@type": "CafeOrCoffeeShop", "openingHoursSpecification": spec})}</script>'


LD_SAME = _ld([{"dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:30", "closes": "20:00"},
               {"dayOfWeek": "https://schema.org/Saturday", "opens": "09:00", "closes": "18:00"},
               {"dayOfWeek": "Sunday", "opens": "12:00", "closes": "18:00"},
               {"dayOfWeek": "Monday", "opens": "10:00", "closes": "14:00", "validFrom": "2026-12-25", "validThrough": "2026-12-25"}])
LD_OTHER = _ld([{"dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "08:00", "closes": "17:00"}])


def _get(vm, url, body=None, status=200, raw=None):
    payload = raw.encode() if raw is not None else json.dumps(body).encode()
    vm.mock_web("^" + re.escape(url) + "$", {"method": "GET", "response": {
        "status": status, "headers": {"Content-Type": b"application/json"}, "body": payload}})


def _element(kind="node", eid=1001, version=7, oh=HOURS, tags=None, visible=True):
    t = {"amenity": "cafe", "name": "Example Café", "website": SITE, "addr:street": "Borough High Street"}
    if oh is not None:
        t["opening_hours"] = oh
    t.update(tags or {})
    t = {k: v for k, v in t.items() if v is not None}
    e = {"type": kind, "id": eid, "version": version, "timestamp": "2026-11-20T10:00:00Z", "uid": 1, "user": "m", "tags": t}
    if kind == "node":
        e.update(lat=51.503, lon=-0.090)
    else:
        e["nodes"] = [1, 2, 3, 1]
    if not visible:
        e = {"type": kind, "id": eid, "version": version, "visible": False}
    return e


def _setup(vm, kind="node", eid=1001, osm_status=200, page=TEXT, page_status=200, found=True, site_hours=HOURS, url=SITE, **el):
    vm.clear_mocks()
    _get(vm, f"{OSM}/{kind}/{eid}.json", {"elements": [_element(kind, eid, **el)]}, osm_status)
    _get(vm, url, status=page_status, raw=page)
    vm.mock_llm(r".*", llm_json({"found": found, "opening_hours": site_hours if found else "", "quote": "Monday 07:30 - 20:00 …"}))


def _at(vm, ts):
    """Move the clock. The harness's warp() does not reach a deployed contract's message datetime, so set it too."""
    import sys
    vm.warp(ts)
    gl = sys.modules.get("genlayer.gl")
    raw = getattr(gl, "message_raw", None)
    if isinstance(raw, dict):
        raw["datetime"] = ts


@pytest.fixture
def hc(direct_vm, direct_deploy, direct_alice):
    direct_vm.sender = direct_alice
    direct_vm.warp("2026-11-23T12:00:00Z")
    return direct_deploy(CONTRACT_PATH)


def _check(vm, hc, kind="node", eid="1001", **setup):
    _setup(vm, kind=kind, eid=int(eid), **setup)
    return hc.check(kind, eid)


# --- the eight statuses ------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("setup, status", [
    (dict(), "VERIFIED"),
    (dict(page=TEXT + LD_SAME), "VERIFIED"),  # both readings of the page agree with OSM
    (dict(page=LD_SAME + "<p>Welcome</p>", found=False), "VERIFIED"),  # schema.org alone
    (dict(oh="Mo-Su 08:00-17:00"), "DIFFERS"),
    (dict(oh=None), "MISSING"),
    (dict(oh="Mon-Fri 9am-5pm"), "UNPARSED"),
    (dict(page=TEXT + LD_OTHER), "SOURCE_CONFLICT"),
    (dict(found=False), "SOURCE_NO_HOURS"),
    (dict(site_hours="Mon to Fri 7.30am to 8pm"), "SOURCE_NO_HOURS"),  # the model's answer must be in the syntax
    (dict(page="", page_status=403), "SOURCE_UNREADABLE"),
    (dict(tags={"website": None}), "NO_SOURCE"),
    (dict(tags={"website": "not a url"}), "NO_SOURCE"),
])
def test_statuses(direct_vm, hc, setup, status):
    assert _check(direct_vm, hc, **setup) == status
    c = json.loads(hc.get_check("node/1001"))
    assert (c["status"], c["element"], c["version"], c["checked_at"]) == (status, "node/1001", 7, "2026-11-23T12:00:00")
    assert hc.status_of("node/1001") == status
    assert json.loads(hc.stats())["by_status"][status] == 1


def test_a_verified_check_records_every_reading(direct_vm, hc):
    assert _check(direct_vm, hc, page=TEXT + LD_SAME) == "VERIFIED"
    c = json.loads(hc.get_check("node/1001"))
    assert c["osm_week"] == HOURS and c["source"] == SITE and c["name"] == "Example Café"
    p = c["page"]
    assert (p["state"], p["week"], p["visible"], p["structured"]) == ("ok", HOURS, HOURS, HOURS)
    assert len(p["text_sha256"]) == 64 and p["chars"] > 60 and p["quote"].startswith("Monday")
    assert hc.verified_week("node/1001") == HOURS


def test_the_page_named_by_opening_hours_url_wins(direct_vm, hc):
    hours_page = "https://www.example-cafe.co.uk/hours"
    _setup(direct_vm, tags={"opening_hours:url": hours_page}, url=hours_page)
    assert hc.check("node", "1001") == "VERIFIED"
    assert json.loads(hc.get_check("node/1001"))["source"] == hours_page


def test_a_way_is_checked_too(direct_vm, hc):
    assert _check(direct_vm, hc, kind="way", eid="555") == "VERIFIED"
    assert hc.verified_week("way/555") == HOURS


# --- is_open -------------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("day, time, answer", [
    ("Mo", "07:29", "closed"), ("Mo", "07:30", "open"), ("Fr", "19:59", "open"), ("Fr", "20:00", "closed"),
    ("Sa", "12:00", "open"), ("Su", "11:00", "closed"), ("su", "12:30", "open"), ("Sunday", "17:59", "open"),
])
def test_is_open_answers_from_a_verified_week(direct_vm, hc, day, time, answer):
    _check(direct_vm, hc)
    assert hc.is_open("node/1001", day, time) == answer


def test_is_open_follows_hours_past_midnight(direct_vm, hc):
    late = "Fr-Sa 18:00-02:00"
    _check(direct_vm, hc, oh=late, site_hours=late, page="<p>Friday and Saturday 18:00 - 02:00, closed otherwise</p>" * 2)
    assert [hc.is_open("node/1001", d, t) for d, t in (("Fr", "23:00"), ("Sa", "01:30"), ("Su", "01:30"), ("Su", "02:00"), ("Th", "23:00"))] == \
        ["open", "open", "open", "closed", "closed"]


@pytest.mark.parametrize("setup", [dict(oh="Mo-Su 08:00-17:00"), dict(page=TEXT + LD_OTHER), dict(tags={"website": None})])
def test_is_open_is_unknown_unless_verified(direct_vm, hc, setup):
    _check(direct_vm, hc, **setup)
    assert hc.is_open("node/1001", "Mo", "12:00") == "unknown"
    assert hc.verified_week("node/1001") == ""


def test_is_open_of_an_unchecked_element_is_unknown(hc):
    assert hc.is_open("node/42", "Mo", "12:00") == "unknown"
    assert (hc.status_of("node/42"), hc.get_check("node/42"), hc.checked_at("node/42")) == ("UNCHECKED", "", "")


@pytest.mark.parametrize("day, time, reason", [("Xx", "12:00", "day must be"), ("Mo", "24:00", "time must be"), ("Mo", "9:00", "time must be")])
def test_is_open_refuses_bad_input(direct_vm, hc, day, time, reason):
    with direct_vm.expect_revert(reason):
        hc.is_open("node/1001", day, time)


# --- the to-fix list, rechecks and history --------------------------------------------------------------------------------


def test_to_fix_lists_what_mappers_should_correct(direct_vm, hc):
    _check(direct_vm, hc, eid="1", oh="Mo-Su 08:00-17:00")
    _check(direct_vm, hc, eid="2", oh=None)
    _check(direct_vm, hc, eid="3")
    _check(direct_vm, hc, eid="4", page=TEXT + LD_OTHER)
    rows = json.loads(hc.to_fix(0, 10))
    assert [(r["element"], r["status"], r["page_week"]) for r in rows] == [("node/1", "DIFFERS", HOURS), ("node/2", "MISSING", HOURS)]
    assert rows[0]["osm_hours"] == "Mo-Su 08:00-17:00" and rows[0]["source"] == SITE
    assert [r["element"] for r in json.loads(hc.list_checks(0, 10))] == ["node/1", "node/2", "node/3", "node/4"]
    assert json.loads(hc.list_checks(2, 1))[0]["element"] == "node/3"
    s = json.loads(hc.stats())
    assert (s["elements"], s["checks"], s["by_status"]["DIFFERS"], s["by_status"]["VERIFIED"]) == (4, 4, 1, 1)


def test_a_recheck_after_the_fix_moves_the_element_and_keeps_history(direct_vm, hc):
    assert _check(direct_vm, hc, oh="Mo-Su 08:00-17:00") == "DIFFERS"
    with direct_vm.expect_revert("at most every 10 minutes"):
        _check(direct_vm, hc)
    _at(direct_vm, "2026-11-23T12:10:00Z")
    assert _check(direct_vm, hc, version=8) == "VERIFIED"  # a mapper corrected OSM
    past = json.loads(hc.get_history("node/1001"))
    assert past == [{"checked_at": "2026-11-23T12:00:00", "version": 7, "status": "DIFFERS", "osm_week": "Mo-Su 08:00-17:00", "page_week": HOURS}]
    s = json.loads(hc.stats())
    assert (s["elements"], s["checks"], s["by_status"]["DIFFERS"], s["by_status"]["VERIFIED"]) == (1, 2, 0, 1)
    assert json.loads(hc.to_fix(0, 10)) == []
    assert hc.checked_at("node/1001") == "2026-11-23T12:10:00"


def test_history_keeps_the_last_eight(direct_vm, hc):
    for i in range(10):
        _at(direct_vm, f"2026-11-23T{12 + i:02d}:00:00Z")
        _check(direct_vm, hc, version=10 + i)
    past = json.loads(hc.get_history("node/1001"))
    assert len(past) == 8 and past[0]["version"] == 11 and past[-1]["version"] == 18


# --- refusals: nothing is recorded ----------------------------------------------------------------------------------------


@pytest.mark.parametrize("setup, reason", [
    (dict(osm_status=404), "does not exist on OpenStreetMap"),
    (dict(osm_status=410), "does not exist on OpenStreetMap"),
    (dict(visible=False), "does not exist on OpenStreetMap"),
    (dict(osm_status=503), "could not be read right now"),
])
def test_an_element_that_cannot_be_read_records_nothing(direct_vm, hc, setup, reason):
    with direct_vm.expect_revert(reason):
        _check(direct_vm, hc, **setup)
    assert hc.get_check("node/1001") == "" and json.loads(hc.stats())["checks"] == 0


@pytest.mark.parametrize("kind, eid, reason", [
    ("shop", "1", "element_type must be"), ("node", "abc", "element_id must be"), ("node", "0", "element_id must be"),
    ("node", "1234567890123", "element_id must be"),
])
def test_bad_elements_are_refused_before_any_reading(direct_vm, hc, kind, eid, reason):
    direct_vm.clear_mocks()
    with direct_vm.expect_revert(reason):
        hc.check(kind, eid)


def test_a_model_answer_that_is_not_json_records_nothing(direct_vm, hc):
    _setup(direct_vm)
    direct_vm.clear_mocks()
    _get(direct_vm, f"{OSM}/node/1001.json", {"elements": [_element()]})
    _get(direct_vm, SITE, raw=TEXT)
    direct_vm.mock_llm(r".*", "Monday to Friday, half past seven till eight")
    with pytest.raises(Exception):
        hc.check("node", "1001")
    assert hc.get_check("node/1001") == ""


# --- the parser (shared with HoursFix) -------------------------------------------------------------------------------------


@pytest.mark.parametrize("text, week", [
    (HOURS, HOURS),
    ("Mo-Fr 07:30-20:00, Sa 09:00-18:00; Su 12:00-18:00", HOURS),
    ("Mo,Tu,We,Th,Fr 07:30-20:00; Sa 09:00-18:00; Su 12:00-18:00; PH off", HOURS),
    ("24/7", "Mo-Su 00:00-24:00"),
    ("Mo-Su 10:00-14:00,17:00-23:00", "Mo-Su 10:00-14:00,17:00-23:00"),
    ("Mo-Su 09:00-17:00; Su off", "Mo-Sa 09:00-17:00; Su off"),
    ("Jan-Mar Mo 09:00-17:00", ""),
    ("sunrise-sunset", ""),
])
def test_check_hours(hc, text, week):
    assert hc.check_hours(text) == week
