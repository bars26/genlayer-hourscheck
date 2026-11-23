// Renders docs/REPRODUCTION.md from docs/demo-run.json (written by scripts/demo.mjs).
//
//   node scripts/reproduction.mjs

import { readFileSync, writeFileSync } from "fs";

const run = JSON.parse(readFileSync(new URL("../docs/demo-run.json", import.meta.url), "utf8"));
const EXPLORER = "https://explorer-studio.genlayer.com";
const tx = (h) => (h ? `[${h.slice(0, 10)}…](${EXPLORER}/tx/${h})` : "");
const esc = (s) => String(s ?? "").replace(/\|/g, "\\|").replace(/\n/g, " ");
const code = (s) => (s ? `\`${esc(s)}\`` : "—");
const hashOf = (el) => run.log.find((r) => r.call === `check("node", "${el.split("/")[1]}")` && r.exec === "SUCCESS")?.hash;

const rows = Object.entries(run.checks).map(([el, c]) => {
  const p = c.page || {};
  return `| [${el}](https://www.openstreetmap.org/${el}) ${esc(run.labels[el])} v${c.version} | ${code(c.osm_week || c.osm_hours)} | ${code(p.visible)} | ${code(p.structured)} | **${c.status}** | ${tx(hashOf(el))} |`;
});
const evidence = Object.entries(run.checks).map(([el, c]) => {
  const p = c.page || {};
  return `- **${el}** (${esc(c.name)}): source ${c.source ? `<${c.source}>` : "none"}${p.text_sha256 ? `; page text sha256 \`${p.text_sha256}\` (${p.chars} characters)` : ""}${p.quote ? `; the model quoted *"${esc(p.quote).slice(0, 160)}"*` : ""}; checked ${c.checked_at} UTC.`;
});
const log = run.log.map((r) => `| \`${esc(r.call)}\` | ${r.status} | ${r.exec} | ${esc(r.refused ? `refused: ${r.refused}` : r.returned ?? "").slice(0, 140)} | ${tx(r.hash)} |`);

const md = `# HoursCheck: live run

Every check below was agreed by GenLayer validators on GenLayer Studio, each reading OpenStreetMap's public API and the
business's own page. Contract \`${run.contract}\` ([explorer](${EXPLORER}/address/${run.contract})); \`node scripts/verify-code.mjs ${run.contract}\`
checks the deployed code is byte-identical to \`contracts/hours_check.py\`. The places, their OSM data and their pages are
real (OpenStreetMap data © OpenStreetMap contributors, ODbL); the checks were run on ${Object.values(run.checks)[0].checked_at.slice(0, 10)}.

## Ten London places

Every value is the week HoursCheck reads (\`check_hours\`). "Page text" is the model's transcription of the visible page,
"schema.org" the page's machine-readable hours parsed in code; when both exist they must agree.

| Element | OSM | Page text (model) | Page schema.org (code) | Status | Tx |
|---|---|---|---|---|---|
${rows.join("\n")}

${evidence.join("\n")}

## Reading the results

\`is_open\` answers only from a VERIFIED week:

| Element | Day | Time | Answer |
|---|---|---|---|
${run.is_open.map((q) => `| ${q.element} | ${q.day} | ${q.time} | ${q.answer} |`).join("\n")}

\`to_fix(0, 50)\`, the list a mapper works from:

| Element | Status | OSM now | The page states |
|---|---|---|---|
${run.to_fix.map((r) => `| ${r.element} ${esc(r.name)} | ${r.status} | ${code(r.osm_hours)} | ${code(r.page_week)} |`).join("\n")}

\`stats()\`: \`${JSON.stringify(run.stats)}\`

## Every transaction

A refused call is still ACCEPTED by consensus; the contract outcome is the \`exec\` column (\`ERROR\` = refused, on purpose).
Checker wallet \`${run.checker}\` (Studio test account).

| Call | Consensus | exec | Returned / refused | Tx |
|---|---|---|---|---|
${log.join("\n")}
`;
writeFileSync(new URL("../docs/REPRODUCTION.md", import.meta.url), md);
console.log(`wrote docs/REPRODUCTION.md (${run.log.length} transactions)`);
