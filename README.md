# news-image-20261123 — Monday 23 November 2026 in one image

An editorial broadsheet front page summing up Monday 23 November 2026's
world news: 30 verified stories — 3 illustrated leads, 12 cards, a world
map with numbered pins, a DATE CHECK box, and a 15-item ALSO list.

**Leads:** (1) COP31 blame game erupts — the Antalya talks collapsed
Sunday with no deal; Monday brings resignation calls for president Bowen,
Pacific despair, and reports of Saudi Arabia's privileged access.
(2) Zelenskyy says Ukrainian sea drones sank the Russian corvette Merkury
off Benghazi (a Sunday operation, announced Monday); Russian overnight
strikes killed at least 15 around Kyiv. (3) Kospi dives 3.31% as the
AI-bubble rout spreads; Seoul readies a ₩10tn stabilisation fund.

**Build:** `render.py` (deterministic PIL, no randomness, no network)
draws `entry.png` (1024x1024, 194,767 bytes). `main.ts` (Node stdlib)
copies the pinned render to `/output/entry.png` after verifying PNG magic,
exact 1024x1024 size, the 1 MiB limit, and the pinned sha256 — then hashes
the copy back. Verified: `render.py` twice byte-identical; `node main.ts`
twice, both outputs sha256-match the shipped file.

**Concept:** ChatGPT concept review (independent reviewer, text-only)
23 Nov ~18:20 WIB — GO WITH CONDITIONS, Concept A wins; all 8 conditions
applied (see CONCEPT.md). Final quality review after `makefun check`.

**Research:** `~/workspace/makefun/news-image-20261123-research/verified-stories-2026-11-23.md`
— 30 verified Monday items, 19 excluded prior-day items, 7 still-developing.
Sources read through ~11:30 UTC, Mon 23 Nov 2026.
