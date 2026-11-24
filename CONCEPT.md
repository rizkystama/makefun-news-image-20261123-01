# news-image-20261123 — Concept (DRAFT, pre ChatGPT concept review)

**Concept A: editorial broadsheet** (the proven structure: the 20261121 and
20261122 editions using it scored provisional top ~6%; leaders all use
masthead + number strip + region bar + UTC timeline + 3 illustrated leads +
small cards + map + ALSO list + DATE CHECK box). This entry follows that
structure with its own verified Monday story set.

**ChatGPT CONCEPT REVIEW 23 Nov ~18:20 WIB** (chatgpt.com/c/6b04133a-8554-83ec-81de-44539114fc09):
GO WITH CONDITIONS — Concept A wins; COP31 stays lead 1 (Monday fallout
framing); Merkury lead 2 (Sunday operation, announced Monday by Zelenskyy);
30 stories as coverage target with strict hierarchy (leads dominate; ~18
clearly communicated over 30 unreadable); 300px legibility is the biggest
risk (leads + masthead + date must survive at 300px). "Not approving
submission yet" — final review still to come.
Corrections applied from the review (verified against wires where flagged):
boy trapped HOURS DROPPED (14h vs 22h conflict — omit hours); Kyiv toll
"at least 15" (AFP) with "11 in Dymer" (Reuters); Indonesia card uses AP's
34 missing + forensic ID pending; Gaza "indicators of potential
contamination across >99%"; NHS "AI-assisted trial, not proof"; Seoul fund
worded "readies ₩10tn"; Hormuz card notes "IRGC said Sunday; reported
Monday (Tasnim)" + CLAIM tag; Iran 78 drones = Tehran's tally alone;
Rubio card drops the "seven conditions" number; Lowy scores kept with
(Lowy Institute) attribution; Belgium 429/~59,500 kept (Brussels Airport
sourced). Congo Ebola + SAPS 581 already excluded by parent verification.

**ChatGPT FINAL QUALITY REVIEW 23 Nov ~19:25 WIB** (same chat
c/6b04133a-8554-83ec-81de-44539114fc09): **GO AFTER CORRECTIONS** — "STOP
EDITING AND SUBMIT" once the 4 fixes are applied. 300px hierarchy PASS.
All 4 applied in v2: (1) Riemann item REMOVED (Nature report dated 20 Nov;
its Monday angle already sits in the Wang ALSO item); (2) KOSPI timeline
06:00 → 06:30 UTC (15:30 KST close); (3) Indonesia card reframed as
Monday's continuing search after Sunday's recovery + DATE CHECK green row
gains "Cikande search continues"; (4) fund corrected to ₩10.76tn,
verified vs Korea JoongAng Daily 23 Nov (Finance Minister Lee Hyoung-il,
est. 2020, never deployed, timing/size undecided), worded "prepares to
activate … deployment undecided".

**Stories: 29 verified Monday items** — 3 leads + 12 cards + 14 ALSO items.
Research: ~/workspace/makefun/news-image-20261123-research/verified-stories-2026-11-23.md
(researcher session ec25b97b; 30 verified, 19 excluded, 7 still-developing).
Parent spot-checks: Democrats-258 reached SUNDAY (Hubbard beat Foxx by ~330
after recount; Reuters 22 Nov) — NOT a Monday lead; Shenzhen trilateral was
Thu 19 Nov; Riemann claim Fri 20 Nov (certified Sat; Monday = Nature report
+ Wang essay); South Korea $1tn milestone Thu 19 Nov (Monday = Nov 1-20
customs data + Kospi slide); SAPS 581-women stats released Fri 20 Nov;
Congo Ebola passed 11,000 mid-Nov; Indonesia ship seizure disclosed Fri
20 Nov; UK Budget was 28 Oct. All sit in DATE CHECK as left out.

**Leads:** 1 COP31 Monday fallout — collapse was Sunday, Monday brings
resignation calls for president Bowen, Pacific despair, Saudi-access
reporting; 90+ countries signed an electrification pledge. 2 Ukraine —
Zelenskyy says sea drones sank the Russian corvette Merkury off Benghazi
(satellite images show it capsized) + Russian overnight strikes kill 15
around Kyiv; Zelenskyy urges US to release paid-for Patriot interceptors.
3 Kospi -3.31% (4,708.54, lowest since 13 Jan; -5.1% intraday; Seoul
announces a 10-trillion-won stabilisation fund; extends Friday's US rout).

**Cards (12):** NHS EDITH trial (world's largest AI breast-screening trial,
~700,000 women, 30 sites, £10m); Gaza "toxic wasteland" (Oxfam/CEOBS,
contamination indicators across >99%); Belgium strike (429 flights
cancelled at Brussels, ~59,500 passengers); Indonesia candy-factory fire
(24 dead confirmed, ~30 missing); Nepal PM in Delhi (₹15,000-crore aid,
8 MoUs, Ayodhya–Janakpur train); China 2030 eldercare/childcare plan;
Iran claims 78 US drones downed (CLAIM — Tehran's tally alone); Trump–Iran
Monday diplomacy (Rubio meets Qatar PM 19:00 UTC; Iran's 7 conditions);
Hormuz — Iran says two tankers hit naval mines (REPORTED); NZ draw
Wellington Test (India 720/9 dec); Lowy Asia Power Index (US 78.9,
China 73.6, India 40.5 holds third); Wall Street's worst week since 2020
(Nasdaq -5.28% Fri; S&P in correction; Monday futures bounce).

**ALSO (15):** Bitcoin near $61,000 (Hayes warns $55k); Bulgari funeral in
Rome; Thanksgiving travel (Delta Sunday meltdown + Monday storm watch);
US intel chief defends Trump calling Putin "friend"; West Bank medics
attacks +350%; Syria–EU talks; Taliban forest police; Meta's Alexandr Wang
(superintelligence "arriving"); Trump third crypto gala; US envoy floats
NATO-style Ukraine guarantees; Sudan widowed mothers; Europe "hot autumn"
protests; Riemann proof claim (Nature weighs in Monday); Taiwan -0.93%,
Japan shut; France hopefuls question Ukraine aid.

**Regions:** Asia-Pacific 10 · Middle East 7 · Europe 6 · Americas 4 ·
Africa 2 · Oceania 1 · Global 0 — recount at build time; bar shows the
final counts (6 regions + Global only if a Global item exists).

**Honesty devices:** DATE CHECK box (left-out prior-day events, included
Monday developments, not-yet-decided: US market close, Rubio–Qatar readout,
Kyiv toll); certainty tags REPORTED / CLAIM with footer legend; "Sources
read to ~11:30 UTC" line.

**Build:** render.py (deterministic PIL, no randomness/time) → entry.png
1024x1024, ≤1 MiB. main.ts copies the pinned render after sha256
verification. 300px thumbnail checked before submit.

## v4 revision (25 Nov ~00:00 WIB — built on Rizky's "Bangun v4 news-image malam ini")

**Why:** v3 scored R1 56.96% / R2 71.46% / **R3 57.49% (rank 3,458/13,031,
judged 23:00 WIB 24 Nov)** — far from the top-50 prize zone. The
diagnosis: v3 was rendered at ~11:30 UTC, before the day's two biggest
stories resolved, so it reads as an unfinished edition of the day. v4
fixes that with a genuine design + content revision, not a tweak.

**Resolved facts (parent-verified 24 Nov ~24:00 WIB, multiple wires):**
(1) US markets Monday close (21:00 UTC): S&P 500 +4.73% to 7,237.17
(best day since April 2025, ended a seven-day losing streak, exited
correction); Nasdaq +6.51% to 24,089.56 (+1,471.82 pts, second-largest
one-day points gain ever); Dow +3.01% to 49,595.31; Russell 2000 +3.40%.
Driver: Nvidia's board unanimously reinstated Jensen Huang as CEO,
eleven days after he resigned; NVDA +31.48% to $165.05, biggest one-day
gain since 2003, ~$950B market value added. VIX -25.83% to 26.62.
Bitcoin $61,356 (+4.68%). (2) Rubio–Qatar readout: Rubio met Qatari PM
Sheikh Mohammed bin Abdulrahman Al Thani at the State Department to
launch the 8th U.S.-Qatar Strategic Dialogue; VP Vance met him
separately at the White House; the Qatari PM told Al Jazeera the region
cannot afford a new US-Iran escalation and Doha is pushing to revive
stalled talks; no breakthrough, no new agreement. (3) Kyiv toll
CONFIRMED: at least 15 killed (Dymer 11, Vyshneve supermarket 3 + 15
wounded incl. three children, Bila Tserkva 1); a seven-year-old boy and
a 79-year-old woman were pulled alive from the Dymer rubble after about
22 hours; two people remained missing there.

**Changes:** FOUR leads across (COP31, Merkury, Wall Street rebound NEW,
Kospi), each 246px wide with a redesigned illustration, a 2-line serif
headline and a ~200-char body (5 lines at 9pt), body placed dynamically
below the headline with an adaptive line cap. The
Wall Street card is promoted to lead 3; the Nvidia card takes the last
card slot (16, new chip icon). Rubio card upgraded from preview to the
reported outcome. Timeline gains the 21:00 UTC close. Stat strip: the
Seoul fund stat (still in the Kospi lead body) is replaced by +31.48%
NVIDIA in green. New masthead nameplate ("THE MONDAY GLOBE"); the red
subline teases all four leads. DATE CHECK loses the "not yet decided"
row (all decided now) and narrows; the world map grows to 576x146 with
17 pins and reworked label offsets fixing v3 collisions (Tehran/Hormuz,
Delhi/Tehran, Wellington/Canberra). Bitcoin ALSO item updated to the
Monday close ($61,356, +4.68%). Sources read through ~21:30 UTC.

**Stories: 30** — 4 leads + 12 cards (05-16) + 14 ALSO (17-30).
**Regions recounted:** Asia-Pacific 7 · Middle East 6 · Europe 8 ·
Americas 6 (Nvidia joins the Americas) · Africa 1 · Oceania 1 · Global 1.
Rubio/Qatar stays Middle East (Iran-diplomacy substance, as in v3);
US-envoy item stays Europe (Ukraine topic); Bitcoin stays Global.
