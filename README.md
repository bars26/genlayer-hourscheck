# HoursCheck

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/license/mit/)

**OpenStreetMap opening hours, checked against the business's own web page by GenLayer validators: a reusable
`is_open` that answers only when the map and the business agree.**

Map apps, delivery and booking contracts, and agents all need "is this place open now?". OpenStreetMap's
`opening_hours` is the open answer, but it is edited by volunteers and often stale; the business's own page is the
authority, but it is free text. HoursCheck is an Intelligent Contract that checks one against the other and stores the
result on-chain, so any contract or app can ask `is_open(element, day, time)` and get "open" / "closed" only for hours
that match the business's own page, and "unknown" otherwise.

**Contract (GenLayer Studio):** [`0x83ff5c32EC6dB1075854C2B37A709a3e44498c40`](https://explorer-studio.genlayer.com/address/0x83ff5c32EC6dB1075854C2B37A709a3e44498c40)
(`node scripts/verify-code.mjs 0x83ff5c32EC6dB1075854C2B37A709a3e44498c40` checks it is byte-identical to `contracts/hours_check.py`).

## How a check works

`check(element_type, element_id)` (anyone; one element at most every 10 minutes):

1. **The element, from OpenStreetMap.** Every validator reads the element's current version from the OSM API: its
   `opening_hours`, its name and address, and the page it names (`opening_hours:url`, else `website`, else
   `contact:website`).
2. **The page, read twice.** Each validator fetches that page (rendered in a browser if a plain fetch is refused) and
   reads its hours two independent ways:
   - **the visible text:** the model transcribes the place's regular week in `opening_hours` syntax (it only
     transcribes; page text is fenced as data, and an answer outside the syntax counts as "no hours");
   - **the schema.org data:** code parses the page's JSON-LD `openingHoursSpecification` / `openingHours` (dated
     exceptions skipped, several different weeks on one page ignored).
3. **The comparison, in code.** All values become a canonical week of minute ranges (weekday ranges and lists, several
   ranges a day, past midnight, `off`, `24/7`, `;` and additional `,` rules; holidays ignored), compared exactly:

| Status | Meaning | `is_open` |
|---|---|---|
| `VERIFIED` | OSM's week equals the page's (and the page's two readings agree) | open / closed |
| `DIFFERS` | the page states another week than OSM: OSM is probably out of date | unknown |
| `MISSING` | OSM has no `opening_hours`; the page states a week | unknown |
| `UNPARSED` | OSM's value is outside the compared syntax; the page states a week | unknown |
| `SOURCE_CONFLICT` | the page's visible hours and its schema.org hours differ: nothing is decided | unknown |
| `SOURCE_NO_HOURS` | the page states no regular weekly hours | unknown |
| `SOURCE_UNREADABLE` | the page could not be read | unknown |
| `NO_SOURCE` | the element names no web page | unknown |

4. **Consensus.** Validators re-run the whole check and accept the leader's result only if they agree **exactly** on the
   status and every value it rests on: the element version, OSM's value and week, the page named, and the page's week
   from each reading (`same_reading`). The model's quote and the page's text hash are kept as the leader's evidence,
   not compared (pages carry per-request tokens). An element that does not exist, or an OSM outage, records nothing.

The model never decides a status. It transcribes one page; parsing, both comparisons and the status are deterministic.

## Using it from another contract or app

| View | Returns |
|---|---|
| `is_open(element, day, time)` | `"open"` / `"closed"` from a VERIFIED week (`day` `Mo`..`Su`, `time` `HH:MM` local at the place; ranges include their start, exclude their end, past-midnight hours count on the next day), else `"unknown"` |
| `verified_week(element)` | the VERIFIED week in `opening_hours` syntax, else `""` |
| `status_of(element)`, `checked_at(element)` | the latest status (or `UNCHECKED`) and when it was agreed; a consumer decides how old is too old |
| `get_check(element)`, `get_history(element)` | the full latest check (both readings, source, quote, page hash) and up to 8 earlier ones |
| `to_fix(offset, limit)` | elements whose OSM hours should change (`DIFFERS`, `MISSING`, `UNPARSED`) with the week the page states: a work list for mappers |
| `list_checks`, `stats`, `check_hours(value)` | paged summaries, counts by status (kept in storage, no loops), and how a value is parsed |

`element` is `"node/123"`, `"way/456"` or `"relation/789"`. Paged views return at most 100 rows.

Example consumers: a delivery escrow that refuses a booking outside verified hours; a map app that shows a "verified
against the business's site" badge; [HoursFix](https://github.com/bars26/genlayer-hoursfix), which pays mappers for
fixes, can take its work list from `to_fix`.

## Verified live, on ten London places

`scripts/demo.mjs` ran on GenLayer Studio on 2026-11-23 over real OpenStreetMap elements and the businesses' own pages.
Every value, quote, page hash and transaction is in [`docs/REPRODUCTION.md`](docs/REPRODUCTION.md).

| Place | OSM | Page (text = schema.org unless noted) | Status |
|---|---|---|---|
| PizzaExpress, 450 Strand | `Mo-We 11:30-22:30; Th-Sa 11:30-23:00; Su 11:30-22:00` | the same week | **VERIFIED** |
| Wagamama, Tower Hill | `Mo-Th 11:00-22:00; Fr-Sa 11:00-23:00; Su 11:00-21:00` | the same week | **VERIFIED** |
| PizzaExpress, Baker Street | `Mo-We 11:30-22:00; Th 11:30-22:30; Fr-Sa 11:30-23:00; Su 11:30-22:30` | the same week | **VERIFIED** |
| PizzaExpress, Euston Road | `Mo-Tu 11:31-23:00; We-Fr 11:30-23:30; Sa-Su 11:30-23:00` | `Mo-Tu 11:30-22:00; We-Th 11:30-22:30; Fr-Sa 11:30-23:00; Su 11:30-22:00` | **DIFFERS** |
| PizzaExpress, Dean Street | `Mo-Sa 11:30-23:00; Su 11:30-22:30` | `Mo-Th 11:30-22:30; Fr-Sa 11:30-23:00; Su 11:30-22:00` | **DIFFERS** |
| PizzaExpress, High Holborn | none | `Mo-Th 11:30-22:00; Fr-Sa 11:30-23:00; Su 11:30-22:00` | **MISSING** |
| The Signal Box, Euston | `Mo-Sa 08:00-22:00; Su 09:00-21:00` | text `Mo-Sa 08:00-22:00; Su 09:00-21:00`, schema.org `Mo-Sa 08:00-21:00; Su 09:00-20:00` | **SOURCE_CONFLICT** |
| Oma, Borough | `Mo-Fr 12:00-15:00,17:30-23:00; …` | no weekly hours shown to validators | **SOURCE_NO_HOURS** |
| Waitrose, Canary Wharf | `Mo-Fr 07:00-22:00; …` | the store page could not be read | **SOURCE_UNREADABLE** |
| Kolach, Bloomsbury | `Mo-Su 08:00-17:00` | no website on OSM | **NO_SOURCE** |

- `is_open`: 450 Strand Friday 22:45 **open**, Monday 22:45 **closed**, Sunday 11:00 **closed**; Wagamama Saturday 22:30
  **open**; Euston Road and The Signal Box **unknown** (not verified).
- `to_fix` listed Euston Road, Dean Street (DIFFERS) and High Holborn (MISSING) with the week each page states.
- Refused, recording nothing: the same element again within 10 minutes, an element that does not exist on OSM, and an
  element type that is not node/way/relation.
- Seven of the eight statuses occurred on real data; `UNPARSED` is covered by the tests.

## Run it

```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
genvm-lint check contracts/hours_check.py
python -m pytest tests/direct -q                  # 51 direct-mode tests, web and model mocked
npm install
node scripts/deploy.mjs                           # deploys to GenLayer Studio, prints the address
node scripts/demo.mjs <address>                   # the live run; writes docs/demo-run.json
node scripts/reproduction.mjs                     # renders docs/REPRODUCTION.md
node scripts/verify-code.mjs <address>
```

The tests cover every status (including schema.org alone, an `opening_hours:url` page, a way, and a model answer
outside the syntax), `is_open` at range edges and past midnight, the to-fix list, rechecks with history and status
counts, the 10-minute gap, missing or deleted elements and OSM outages (nothing recorded), and the parser.

## Limits

- `is_open` takes the **local** weekday and time at the place; HoursCheck stores no time zone.
- Only the regular week is compared: public holidays, seasonal or dated hours are outside the parser; schema.org data
  stating several weeks (a page listing several branches) counts as absent.
- The page is the business's own claim. If it is out of date, HoursCheck verifies the out-of-date week.
- A page is read as of the check; `checked_at` lets a consumer refuse old checks.
- Some sites refuse automated readers (Waitrose here), even rendered; their places stay `SOURCE_UNREADABLE`.
- GenLayer Studio. The source carries the same Bradbury header switch as our other contracts.

OpenStreetMap data © OpenStreetMap contributors, available under the Open Database License. The opening-hours parser
and page reading come from [HoursFix](https://github.com/bars26/genlayer-hoursfix).
