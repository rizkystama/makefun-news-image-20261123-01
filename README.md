# news-image-20261123 — Monday 23 November 2026 in one image

An editorial broadsheet front page summing up Monday 23 November 2026's
world news: **30 verified stories — 4 illustrated leads, 12 cards, a
bigger world map with numbered pins, a DATE CHECK box, and a 14-item ALSO
list.**

**Leads:** (1) COP31 blame game erupts — the Antalya talks collapsed
Sunday with no deal; Monday brings resignation calls for president Bowen,
Pacific despair, and reports of Saudi Arabia's privileged access.
(2) Zelenskyy says Ukrainian sea drones sank the Russian corvette Merkury
off Benghazi (a Sunday operation, announced Monday); Russian overnight
strikes killed at least 15 around Kyiv. (3) **Wall Street roars back in
its best day since April** — the S&P 500 jumped 4.73% to 7,237.17 and the
Nasdaq 6.51%, ending a seven-day slide, after Nvidia's board reinstated
Jensen Huang as CEO. (4) Kospi dives 3.31% as the AI-bubble rout spreads;
Seoul readies a ₩10.76tn stabilisation fund.

**What's new in v4 (25 Nov ~00:00 WIB):** v3 (R1 56.96% / R2 71.46% /
R3 57.49%, rank 3,458/13,031) was rendered at ~11:30 UTC, before the
day's two biggest stories resolved. v4 promotes the US Monday rebound to
a lead, adds the Nvidia/Huang reinstatement as card 16, upgrades the
Rubio card from a preview to the reported 8th US–Qatar Strategic Dialogue
outcome, adds the 21:00 UTC close to the timeline, and updates the
Bitcoin item to the Monday close ($61,356, +4.68%). New masthead
nameplate ("THE MONDAY GLOBE"); the DATE CHECK box loses its "not yet
decided" row (all decided now) and the world map grows to 576x146 with
reworked pin labels. Regions recounted: Asia-Pacific 7, Middle East 6,
Europe 8, Americas 6, Africa 1, Oceania 1, Global 1.

**Build:** `render.py` (deterministic PIL, no randomness, no network)
draws `entry.png` (1024x1024, ≤1 MiB). `main.ts` (Node stdlib) copies
the pinned render to `/output/entry.png` after verifying PNG magic,
exact 1024x1024 size, the 1 MiB limit, and the pinned sha256 — then
hashes the copy back. Verified: `render.py` twice byte-identical;
`node main.ts` twice, both outputs sha256-match the shipped file.

**Concept:** ChatGPT concept review (independent reviewer, text-only)
23 Nov ~18:20 WIB — GO WITH CONDITIONS, Concept A wins; all 8 conditions
applied. **Final quality review 23 Nov ~19:25 WIB — GO AFTER CORRECTIONS:**
all 4 fixes applied (Riemann item removed — Nature report dated 20 Nov;
KOSPI timeline 06:30 UTC; Indonesia card reframed as Monday's continuing
search after Sunday's recovery; fund corrected to ₩10.76tn, verified vs
Korea JoongAng Daily). Reviewer's closing words: "STOP EDITING AND SUBMIT."
See CONCEPT.md (v4 section appended).

**Research:** `~/workspace/makefun/news-image-20261123-research/verified-stories-2026-11-23.md`
— 29 verified Monday items (the Riemann item was removed on final
review — its Nature report is dated 20 Nov), 19 excluded prior-day items,
7 still-developing — plus the three resolved evening facts (US close,
Rubio–Qatar readout, confirmed Kyiv toll), parent-verified 24 Nov ~24:00
WIB from multiple wires. Sources read through ~21:30 UTC, Mon 23 Nov 2026.
