# news-image-20261123 — Monday 23 November 2026 in one image

An editorial broadsheet front page summing up Monday 23 November 2026's
world news: 29 verified stories — 3 illustrated leads, 12 cards, a world
map with numbered pins, a DATE CHECK box, and a 14-item ALSO list.

**Leads:** (1) COP31 blame game erupts — the Antalya talks collapsed
Sunday with no deal; Monday brings resignation calls for president Bowen,
Pacific despair, and reports of Saudi Arabia's privileged access.
(2) Zelenskyy says Ukrainian sea drones sank the Russian corvette Merkury
off Benghazi (a Sunday operation, announced Monday); Russian overnight
strikes killed at least 15 around Kyiv. (3) Kospi dives 3.31% as the
AI-bubble rout spreads; Seoul readies a ₩10tn stabilisation fund.

**Build:** `render.py` (deterministic PIL, no randomness, no network)
draws `entry.png` (1024x1024, 195,730 bytes). `main.ts` (Node stdlib)
copies the pinned render to `/output/entry.png` after verifying PNG magic,
exact 1024x1024 size, the 1 MiB limit, and the pinned sha256 — then hashes
the copy back. Verified: `render.py` twice byte-identical; `node main.ts`
twice, both outputs sha256-match the shipped file.

**Concept:** ChatGPT concept review (independent reviewer, text-only)
23 Nov ~18:20 WIB — GO WITH CONDITIONS, Concept A wins; all 8 conditions
applied. **Final quality review 23 Nov ~19:25 WIB — GO AFTER CORRECTIONS:**
all 4 fixes applied (Riemann item removed — Nature report dated 20 Nov;
KOSPI timeline 06:30 UTC; Indonesia card reframed as Monday's continuing
search after Sunday's recovery; fund corrected to ₩10.76tn, verified vs
Korea JoongAng Daily). Reviewer's closing words: "STOP EDITING AND SUBMIT."
See CONCEPT.md.

**Research:** `~/workspace/makefun/news-image-20261123-research/verified-stories-2026-11-23.md`
— 30 verified Monday items (29 used; the Riemann item was removed on final
review — its Nature report is dated 20 Nov), 19 excluded prior-day items,
7 still-developing. Sources read through ~11:30 UTC, Mon 23 Nov 2026.
