// Live run of HoursCheck on GenLayer Studio over real London places: every validator reads the OpenStreetMap element
// and the business's own page (its text and its schema.org hours). Writes docs/demo-run.json.
//
//   node scripts/demo.mjs <contract-address>
//
// OpenStreetMap data © OpenStreetMap contributors (ODbL); the pages are the businesses' own.

import { writeFileSync } from "fs";
import { createAccount, generatePrivateKey } from "genlayer-js";
import { client, fund, log, read, setContract, sleep, write } from "./studio.mjs";

const [CONTRACT] = process.argv.slice(2);
if (!CONTRACT) {
  console.error("usage: node scripts/demo.mjs <contract-address>");
  process.exit(1);
}
setContract(CONTRACT);
const account = createAccount(generatePrivateKey());
const C = client(account);
await fund(account.address, 1n);
await sleep(3000);
console.log("contract", CONTRACT, "checker", account.address);

const places = [
  ["348018690", "PizzaExpress, 450 Strand"],
  ["694510208", "Wagamama, Tower Hill"],
  ["299523381", "PizzaExpress, Baker Street"],
  ["332117740", "PizzaExpress, Euston Road"],
  ["14178896038", "PizzaExpress, Dean Street"],
  ["264515720", "PizzaExpress, High Holborn (no opening_hours on OSM)"],
  ["6381240591", "The Signal Box, Euston"],
  ["12477919501", "Oma, Borough"],
  ["1708718478", "Waitrose, Canary Wharf"],
  ["14396853783", "Kolach (no website on OSM)"],
];
const labels = {};
for (const [id, label] of places) {
  await write(C, "checker", "check", ["node", id]);
  const c = JSON.parse(await read(C, "get_check", [`node/${id}`]));
  labels[`node/${id}`] = label;
  console.log(`  -> node/${id} ${label}: ${c.status} | OSM ${c.osm_week || "-"} | page ${c.page?.week || "-"} (text ${c.page?.visible || "-"}; schema.org ${c.page?.structured || "-"})`);
}
// Refused, recording nothing: the same element again within 10 minutes, an element that does not exist, a bad type.
await write(C, "checker", "check", ["node", "348018690"], 0n, { expectError: true });
await write(C, "checker", "check", ["node", "99999999999"], 0n, { expectError: true });
await write(C, "checker", "check", ["shop", "1"], 0n, { expectError: true });

const queries = [
  ["node/348018690", "Fr", "22:45"], ["node/348018690", "Mo", "22:45"], ["node/348018690", "Su", "11:00"],
  ["node/694510208", "Sa", "22:30"], ["node/332117740", "Mo", "12:00"], ["node/6381240591", "Mo", "12:00"],
];
const answers = [];
for (const [el, day, time] of queries) {
  const a = await read(C, "is_open", [el, day, time]);
  answers.push({ element: el, day, time, answer: a });
  console.log(`  is_open(${el}, ${day}, ${time}) = ${a}`);
}
const out = {
  network: "studio", contract: CONTRACT, checker: account.address, labels, log, is_open: answers,
  checks: {}, to_fix: JSON.parse(await read(C, "to_fix", [0, 50])), stats: JSON.parse(await read(C, "stats")),
};
for (const el of Object.keys(labels)) out.checks[el] = JSON.parse(await read(C, "get_check", [el]));
writeFileSync(new URL("../docs/demo-run.json", import.meta.url), JSON.stringify(out, null, 2));
console.log("to_fix", JSON.stringify(out.to_fix.map((r) => [r.element, r.status])));
console.log("stats", JSON.stringify(out.stats));
console.log("wrote docs/demo-run.json");
