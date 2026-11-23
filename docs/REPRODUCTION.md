# HoursCheck: live run

Every check below was agreed by GenLayer validators on GenLayer Studio, each reading OpenStreetMap's public API and the
business's own page. Contract `0x83ff5c32EC6dB1075854C2B37A709a3e44498c40` ([explorer](https://explorer-studio.genlayer.com/address/0x83ff5c32EC6dB1075854C2B37A709a3e44498c40)); `node scripts/verify-code.mjs 0x83ff5c32EC6dB1075854C2B37A709a3e44498c40`
checks the deployed code is byte-identical to `contracts/hours_check.py`. The places, their OSM data and their pages are
real (OpenStreetMap data © OpenStreetMap contributors, ODbL); the checks were run on 2026-11-23.

## Ten London places

Every value is the week HoursCheck reads (`check_hours`). "Page text" is the model's transcription of the visible page,
"schema.org" the page's machine-readable hours parsed in code; when both exist they must agree.

| Element | OSM | Page text (model) | Page schema.org (code) | Status | Tx |
|---|---|---|---|---|---|
| [node/348018690](https://www.openstreetmap.org/node/348018690) PizzaExpress, 450 Strand v31 | `Mo-We 11:30-22:30; Th-Sa 11:30-23:00; Su 11:30-22:00` | `Mo-We 11:30-22:30; Th-Sa 11:30-23:00; Su 11:30-22:00` | `Mo-We 11:30-22:30; Th-Sa 11:30-23:00; Su 11:30-22:00` | **VERIFIED** | [0x176555e0…](https://explorer-studio.genlayer.com/tx/0x176555e03bbb6b5bf758dcc6f9dccc38c4b958837d9bb3a38d6ab52a06fe250a) |
| [node/694510208](https://www.openstreetmap.org/node/694510208) Wagamama, Tower Hill v19 | `Mo-Th 11:00-22:00; Fr-Sa 11:00-23:00; Su 11:00-21:00` | `Mo-Th 11:00-22:00; Fr-Sa 11:00-23:00; Su 11:00-21:00` | `Mo-Th 11:00-22:00; Fr-Sa 11:00-23:00; Su 11:00-21:00` | **VERIFIED** | [0xfa581d46…](https://explorer-studio.genlayer.com/tx/0xfa581d463f0e52a1c2929723a3b8e20536422e3f2d77b1553efd8596b8fa767e) |
| [node/299523381](https://www.openstreetmap.org/node/299523381) PizzaExpress, Baker Street v26 | `Mo-We 11:30-22:00; Th 11:30-22:30; Fr-Sa 11:30-23:00; Su 11:30-22:30` | `Mo-We 11:30-22:00; Th 11:30-22:30; Fr-Sa 11:30-23:00; Su 11:30-22:30` | `Mo-We 11:30-22:00; Th 11:30-22:30; Fr-Sa 11:30-23:00; Su 11:30-22:30` | **VERIFIED** | [0x0171eaa0…](https://explorer-studio.genlayer.com/tx/0x0171eaa0f62745d0e0081aa51bcc2450ae8d553142d6c768749ba227b34803df) |
| [node/332117740](https://www.openstreetmap.org/node/332117740) PizzaExpress, Euston Road v19 | `Mo-Tu 11:31-23:00; We-Fr 11:30-23:30; Sa-Su 11:30-23:00` | `Mo-Tu 11:30-22:00; We-Th 11:30-22:30; Fr-Sa 11:30-23:00; Su 11:30-22:00` | `Mo-Tu 11:30-22:00; We-Th 11:30-22:30; Fr-Sa 11:30-23:00; Su 11:30-22:00` | **DIFFERS** | [0xcf88127a…](https://explorer-studio.genlayer.com/tx/0xcf88127a13c1e63cec0f251c58c2d3551bb1fc992ea70277f504c779b0b7cbe6) |
| [node/14178896038](https://www.openstreetmap.org/node/14178896038) PizzaExpress, Dean Street v2 | `Mo-Sa 11:30-23:00; Su 11:30-22:30` | `Mo-Th 11:30-22:30; Fr-Sa 11:30-23:00; Su 11:30-22:00` | `Mo-Th 11:30-22:30; Fr-Sa 11:30-23:00; Su 11:30-22:00` | **DIFFERS** | [0x3b397de5…](https://explorer-studio.genlayer.com/tx/0x3b397de5d6006f8d61cfb422c85f7be08f4a42b31ce2c6e6f2a9a4bacd080908) |
| [node/264515720](https://www.openstreetmap.org/node/264515720) PizzaExpress, High Holborn (no opening_hours on OSM) v16 | — | `Mo-Th 11:30-22:00; Fr-Sa 11:30-23:00; Su 11:30-22:00` | `Mo-Th 11:30-22:00; Fr-Sa 11:30-23:00; Su 11:30-22:00` | **MISSING** | [0x569ffe78…](https://explorer-studio.genlayer.com/tx/0x569ffe7893a26fe326e9c319239b91c6b7be7caefa88d0bd57ca814f3a9c8743) |
| [node/6381240591](https://www.openstreetmap.org/node/6381240591) The Signal Box, Euston v10 | `Mo-Sa 08:00-22:00; Su 09:00-21:00` | `Mo-Sa 08:00-22:00; Su 09:00-21:00` | `Mo-Sa 08:00-21:00; Su 09:00-20:00` | **SOURCE_CONFLICT** | [0xec61f1dd…](https://explorer-studio.genlayer.com/tx/0xec61f1ddd877beaf0c68a672161091a25f63f1ee08013bc2234451bb283430db) |
| [node/12477919501](https://www.openstreetmap.org/node/12477919501) Oma, Borough v4 | `Mo-Fr 12:00-15:00,17:30-23:00; Sa 12:00-23:00; Su 12:00-22:00` | — | — | **SOURCE_NO_HOURS** | [0xe3e78d8d…](https://explorer-studio.genlayer.com/tx/0xe3e78d8df84cbad7d38f3bfce9ff486a5596ec763af9fb67ade332455577f849) |
| [node/1708718478](https://www.openstreetmap.org/node/1708718478) Waitrose, Canary Wharf v23 | `Mo-Fr 07:00-22:00; Sa 08:00-21:00; Su 12:00-18:00` | — | — | **SOURCE_UNREADABLE** | [0xa5eda50a…](https://explorer-studio.genlayer.com/tx/0xa5eda50a7cabe49619ee5e2b7fda40dfa29a03bb9934ec2c4dc239eb717c9201) |
| [node/14396853783](https://www.openstreetmap.org/node/14396853783) Kolach (no website on OSM) v3 | `Mo-Su 08:00-17:00` | — | — | **NO_SOURCE** | [0xf869a57b…](https://explorer-studio.genlayer.com/tx/0xf869a57b1ca3203d527e6062327438dfa5c13449a1a3c9b7af38295266f31fc0) |

- **node/348018690** (PizzaExpress): source <https://www.pizzaexpress.com/london-450-strand>; page text sha256 `ab250a56b0d510b6822c16d4ff5b903991cbb5e1a87625afb97e78a1635d4449` (2061 characters); the model quoted *"Monday 11:30 - 22:30 Tuesday 11:30 - 22:30 Wednesday 11:30 - 22:30 Thursday 11:30 - 23:00 Friday 11:30 - 23:00 Saturday 11:30 - 23:00 Sunday 11:30 - 22:00"*; checked 2026-11-23T12:55:59 UTC.
- **node/694510208** (Wagamama): source <https://www.wagamama.com/restaurants/london/tower-hill>; page text sha256 `0370175d4e3b43422035eddb6f42431fd034cc05a9d5a1a6497866196eb0daa5` (2370 characters); the model quoted *"monday 11:00 AM - 10:00 PM tuesday 11:00 AM - 10:00 PM wednesday 11:00 AM - 10:00 PM thursday 11:00 AM - 10:00 PM friday 11:00 AM - 11:00 PM saturday 11:00 AM -"*; checked 2026-11-23T12:56:27 UTC.
- **node/299523381** (PizzaExpress): source <https://www.pizzaexpress.com/london-baker-street>; page text sha256 `3530e0a37b34728e196ecf98dbac97a88a49f41b0e12e636136e32d6c9c6e584` (2782 characters); the model quoted *"Monday 11:30 - 22:00 Tuesday 11:30 - 22:00 Wednesday 11:30 - 22:00 Thursday 11:30 - 22:30 Friday 11:30 - 23:00 Saturday 11:30 - 23:00 Sunday 11:30 - 22:30"*; checked 2026-11-23T12:56:56 UTC.
- **node/332117740** (PizzaExpress): source <https://www.pizzaexpress.com/london-euston-road>; page text sha256 `3e269120c0d21716de7892f288a891cfe2b078aa98ae16eb8a48fbed519e5c98` (1997 characters); the model quoted *"Monday 11:30 - 22:00 Tuesday 11:30 - 22:00 Wednesday 11:30 - 22:30 Thursday 11:30 - 22:30 Friday 11:30 - 23:00 Saturday 11:30 - 23:00 Sunday 11:30 - 22:00"*; checked 2026-11-23T12:57:24 UTC.
- **node/14178896038** (PizzaExpress): source <https://www.pizzaexpress.com/london-dean-street>; page text sha256 `c4ad6147aa175a0358680d289f34593e69ffa22ae46bdd13a53acd358adfda29` (1889 characters); the model quoted *"Opening hours Monday 11:30 - 22:30 Tuesday 11:30 - 22:30 Wednesday 11:30 - 22:30 Thursday 11:30 - 22:30 Friday 11:30 - 23:00 Saturday 11:30 - 23:00 Sunday 11:30"*; checked 2026-11-23T12:57:52 UTC.
- **node/264515720** (PizzaExpress): source <https://www.pizzaexpress.com/london-high-holborn>; page text sha256 `a79cff6711ac0bde5a1128751061a7b1435c55bfac8376fa3b49a54f8f2f0572` (2294 characters); the model quoted *"Monday 11:30 - 22:00 Tuesday 11:30 - 22:00 Wednesday 11:30 - 22:00 Thursday 11:30 - 22:00 Friday 11:30 - 23:00 Saturday 11:30 - 23:00 Sunday 11:30 - 22:00"*; checked 2026-11-23T12:58:13 UTC.
- **node/6381240591** (The Signal Box): source <https://www.signalboxeuston.co.uk/>; page text sha256 `3284527621bc57a528579b66852f99831943a6524a06a568ccc06b3d6cad7d42` (4983 characters); the model quoted *"Monday 08:00 - 22:00 Tuesday 08:00 - 22:00 Wednesday 08:00 - 22:00 Thursday 08:00 - 22:00 Friday 08:00 - 22:00 Saturday 08:00 - 22:00 Sunday 09:00 - 21:00"*; checked 2026-11-23T12:58:48 UTC.
- **node/12477919501** (OMA): source <https://www.oma.london/>; page text sha256 `a5faa022cb492c96d8f7b562e424f480287257d4a98e93e507ca4cda108bf11c` (303 characters); checked 2026-11-23T12:59:16 UTC.
- **node/1708718478** (Waitrose): source <https://www.waitrose.com/find-a-store/canary-wharf>; checked 2026-11-23T12:59:44 UTC.
- **node/14396853783** (Kolach): source none; checked 2026-11-23T12:59:59 UTC.

## Reading the results

`is_open` answers only from a VERIFIED week:

| Element | Day | Time | Answer |
|---|---|---|---|
| node/348018690 | Fr | 22:45 | open |
| node/348018690 | Mo | 22:45 | closed |
| node/348018690 | Su | 11:00 | closed |
| node/694510208 | Sa | 22:30 | open |
| node/332117740 | Mo | 12:00 | unknown |
| node/6381240591 | Mo | 12:00 | unknown |

`to_fix(0, 50)`, the list a mapper works from:

| Element | Status | OSM now | The page states |
|---|---|---|---|
| node/332117740 PizzaExpress | DIFFERS | `Mo,Tu 11:31-23:00, We-Fr 11:30-23:30, Sa,Su 11:30-23:00` | `Mo-Tu 11:30-22:00; We-Th 11:30-22:30; Fr-Sa 11:30-23:00; Su 11:30-22:00` |
| node/14178896038 PizzaExpress | DIFFERS | `Mo-Sa 11:30-23:00; Su 11:30-22:30` | `Mo-Th 11:30-22:30; Fr-Sa 11:30-23:00; Su 11:30-22:00` |
| node/264515720 PizzaExpress | MISSING | — | `Mo-Th 11:30-22:00; Fr-Sa 11:30-23:00; Su 11:30-22:00` |

`stats()`: `{"by_status":{"DIFFERS":2,"MISSING":1,"NO_SOURCE":1,"SOURCE_CONFLICT":1,"SOURCE_NO_HOURS":1,"SOURCE_UNREADABLE":1,"UNPARSED":0,"VERIFIED":3},"checks":10,"elements":10}`

## Every transaction

A refused call is still ACCEPTED by consensus; the contract outcome is the `exec` column (`ERROR` = refused, on purpose).
Checker wallet `0xCebF5ceE979A74Bbae2B172791bDb0eB4e064443` (Studio test account).

| Call | Consensus | exec | Returned / refused | Tx |
|---|---|---|---|---|
| `check("node", "348018690")` | ACCEPTED | SUCCESS | VERIFIED | [0x176555e0…](https://explorer-studio.genlayer.com/tx/0x176555e03bbb6b5bf758dcc6f9dccc38c4b958837d9bb3a38d6ab52a06fe250a) |
| `check("node", "694510208")` | ACCEPTED | SUCCESS | VERIFIED | [0xfa581d46…](https://explorer-studio.genlayer.com/tx/0xfa581d463f0e52a1c2929723a3b8e20536422e3f2d77b1553efd8596b8fa767e) |
| `check("node", "299523381")` | ACCEPTED | SUCCESS | VERIFIED | [0x0171eaa0…](https://explorer-studio.genlayer.com/tx/0x0171eaa0f62745d0e0081aa51bcc2450ae8d553142d6c768749ba227b34803df) |
| `check("node", "332117740")` | ACCEPTED | SUCCESS | DIFFERS | [0xcf88127a…](https://explorer-studio.genlayer.com/tx/0xcf88127a13c1e63cec0f251c58c2d3551bb1fc992ea70277f504c779b0b7cbe6) |
| `check("node", "14178896038")` | ACCEPTED | SUCCESS | DIFFERS | [0x3b397de5…](https://explorer-studio.genlayer.com/tx/0x3b397de5d6006f8d61cfb422c85f7be08f4a42b31ce2c6e6f2a9a4bacd080908) |
| `check("node", "264515720")` | ACCEPTED | SUCCESS | MISSING | [0x569ffe78…](https://explorer-studio.genlayer.com/tx/0x569ffe7893a26fe326e9c319239b91c6b7be7caefa88d0bd57ca814f3a9c8743) |
| `check("node", "6381240591")` | ACCEPTED | SUCCESS | SOURCE_CONFLICT | [0xec61f1dd…](https://explorer-studio.genlayer.com/tx/0xec61f1ddd877beaf0c68a672161091a25f63f1ee08013bc2234451bb283430db) |
| `check("node", "12477919501")` | ACCEPTED | SUCCESS | SOURCE_NO_HOURS | [0xe3e78d8d…](https://explorer-studio.genlayer.com/tx/0xe3e78d8df84cbad7d38f3bfce9ff486a5596ec763af9fb67ade332455577f849) |
| `check("node", "1708718478")` | ACCEPTED | SUCCESS | SOURCE_UNREADABLE | [0xa5eda50a…](https://explorer-studio.genlayer.com/tx/0xa5eda50a7cabe49619ee5e2b7fda40dfa29a03bb9934ec2c4dc239eb717c9201) |
| `check("node", "14396853783")` | ACCEPTED | SUCCESS | NO_SOURCE | [0xf869a57b…](https://explorer-studio.genlayer.com/tx/0xf869a57b1ca3203d527e6062327438dfa5c13449a1a3c9b7af38295266f31fc0) |
| `check("node", "348018690")` | ACCEPTED | ERROR | refused: node/348018690 was checked at 2026-11-23 12:55:59 UTC; one element is checked at most every 10 minutes | [0x95a3e8df…](https://explorer-studio.genlayer.com/tx/0x95a3e8df085ad54f13f3f6ca6207c8cba7f8d6f0699e07a4ad03490a023d499d) |
| `check("node", "99999999999")` | ACCEPTED | ERROR | refused: node/99999999999 does not exist on OpenStreetMap (or was deleted) | [0x672da62f…](https://explorer-studio.genlayer.com/tx/0x672da62f193c0eb48517ededa044c3d99ad32b025011a73c2e1506919c767598) |
| `check("shop", "1")` | ACCEPTED | ERROR | refused: element_type must be node, way or relation | [0x817d5bcc…](https://explorer-studio.genlayer.com/tx/0x817d5bcc1185d4294ec7eacee0fa49c3d4fc29e866532375204782cb5328ae16) |
