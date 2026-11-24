#!/usr/bin/env python3
"""news-image-20261123 — v4 revision: deterministic front-page render.

v3 scored R1 56.96% / R2 71.46% / R3 57.49% — far from the top-50 prize
zone. v4 is a genuine design + content revision, not a tweak:

* FOUR leads across (was 3): COP31, Merkury/Kyiv, the US Monday rebound
  (NEW — the biggest genuinely-Monday story v3 missed), Kospi. Each lead
  card is 246px wide with a redesigned, simpler illustration, a 2-line
  serif headline and a ~200-char body (5 lines at 9pt); body placement is
  dynamic (it follows the headline length) with an adaptive line cap so
  text can never print past the card's bottom edge.
* Three items v3 left "not yet decided" are now RESOLVED (parent-verified
  24 Nov ~24:00 WIB from multiple wires):
  - US markets Monday close (21:00 UTC): S&P 500 +4.73% to 7,237.17 (best
    day since April 2025, ended a seven-day losing streak, exited
    correction); Nasdaq +6.51% to 24,089.56 (+1,471.82 points, the
    second-largest one-day points gain ever); Dow +3.01% to 49,595.31
    (+1,447.98); Russell 2000 +3.40% to 2,669.66. Driver: Nvidia's board
    unanimously reinstated Jensen Huang as CEO, eleven days after he
    resigned; NVDA +31.48% to $165.05, biggest one-day gain since 2003,
    roughly $950B market value added. VIX fell 25.83% to 26.62. Bitcoin
    $61,356 (+4.68%).
  - Rubio-Qatar readout: Rubio met Qatari PM Sheikh Mohammed bin
    Abdulrahman Al Thani at the State Department to launch the eighth
    U.S.-Qatar Strategic Dialogue; VP Vance met him separately at the
    White House. The Qatari PM told Al Jazeera the region cannot afford
    a new US-Iran escalation and Doha is pushing to revive stalled
    talks. No breakthrough, no new agreement announced.
  - Kyiv toll CONFIRMED: at least 15 killed in the Kyiv region (AFP):
    Dymer 11, Vyshneve supermarket 3 (+15 wounded incl. three children),
    Bila Tserkva 1. A seven-year-old boy and a 79-year-old woman were
    pulled alive from the Dymer rubble after about 22 hours; two people
    remained missing there. v3's "at least 15 / 11 in Dymer" was already
    correct; the rescue detail joins the DATE CHECK included row.
* New masthead nameplate ("THE MONDAY GLOBE") with the date kept huge;
  the red subline now teases all four leads.
* Stat strip: the Seoul fund stat (still in the Kospi lead body) is
  replaced by +31.48% NVIDIA in green — the day's most dramatic number.
* Timeline gains the 21:00 UTC US close.
* DATE CHECK loses the "not yet decided" row (all decided now) and
  narrows; the freed width goes to a BIGGER world map (576x146, was
  496x136) with 17 pins and reworked label offsets that fix real v3
  collisions (Tehran/Hormuz, Delhi/Tehran, Wellington/Canberra).
* Story count 30 (was 29): 4 leads + 12 cards + 14 ALSO. The Wall Street
  card is promoted to lead 3; the Nvidia card takes the last card slot
  (16). Rubio card upgraded from preview to reported outcome. Bitcoin
  ALSO item updated to the Monday close ($61,356, +4.68%).
* Regions recounted: Asia-Pacific 7, Middle East 6, Europe 8, Americas 6
  (Nvidia joins the Americas), Africa 1, Oceania 1, Global 1 = 30.

Story data: ~/workspace/makefun/news-image-20261123-research/
verified-stories-2026-11-23.md (v3's 29 verified Monday items) + the
resolved facts above. Every story, number and date comes from those two
sources; nothing is invented. Still excluded: SAPS 581-women and Congo
Ebola 11,000 (unverified in the sweep), Riemann proof claim (20 Nov).
Sources now read through ~21:30 UTC, Mon 23 Nov 2026.
Output: entry.png, 1024x1024, <=1 MiB. Deterministic: no randomness, no time.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
GREY = (107, 114, 128)
LIGHT = (232, 226, 208)
RED = (185, 28, 28)
DARKRED = (127, 29, 29)
NAVY = (30, 58, 95)
OCEAN = (220, 233, 242)
LAND = (232, 220, 195)
LANDLINE = (180, 168, 140)
GOLD = (217, 119, 6)
GREEN = (22, 101, 52)
AMBER = (146, 64, 14)
TEAL = (13, 100, 100)
SKY = (235, 228, 210)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(SANS, size)


F = {
    "band": font(SANS_B, 10),
    "name": font(SERIF_B, 22),
    "mast": font(SERIF_B, 50),
    "sub": font(SANS_B, 14),
    "stat_n": font(SANS_B, 26),
    "stat_l": font(SANS_B, 8),
    "reg": font(SANS_B, 10),
    "time": font(SANS_B, 10),
    "lead": font(SERIF_B, 18),
    "lead_s": font(SANS_B, 10),
    "lead_b": font(SANS, 9),
    "cap": font(SANS, 9),
    "cap_b": font(SANS_B, 9),
    "card_h": font(SANS_B, 10),
    "card_c": font(SANS, 7),
    "sect": font(SANS_B, 12),
    "list": font(SANS, 10),
    "list_b": font(SANS_B, 10),
    "dc": font(SANS, 9),
    "dc_b": font(SANS_B, 10),
    "foot": font(SANS, 8),
    "badge": font(SANS_B, 8),
    "pin": font(SANS_B, 8),
}


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(d, cx, y, text, fnt, fill=INK):
    d.text((cx - d.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def tag(d, x, y, text, color):
    w = d.textlength(text, font=F["badge"]) + 8
    d.rectangle([x, y, x + w, y + 12], fill=color)
    d.text((x + 4, y + 1.5), text, font=F["badge"], fill=(255, 255, 255))
    return w


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- top band 0-18
d.rectangle([0, 0, 1024, 18], fill=NAVY)
d.text((10, 3), "THE WORLD IN ONE DAY", font=F["band"], fill=(255, 255, 255))
r = "30 STORIES  ·  6 REGIONS + GLOBAL  ·  MONDAY 23 NOVEMBER 2026 NEWS EDITION"
d.text((1014 - d.textlength(r, font=F["band"]), 3), r, font=F["band"],
       fill=(255, 220, 130))

# ---------------------------------------------------------------- masthead 18-118
# New v4 nameplate: a distinct paper name above the huge date.
center(d, 512, 21, "·  THE MONDAY GLOBE  ·", F["name"], NAVY)
center(d, 512, 44, "Monday 23 November 2026", F["mast"])
center(d, 512, 98,
       "Wall Street roars back +4.73%  ·  COP31 blame game erupts  ·  "
       "Zelenskyy: Ukraine sank a corvette  ·  Kospi dives 3.31%",
       F["sub"], RED)
# Classic double rule under the masthead.
d.line([8, 114, 1016, 114], fill=INK, width=1)
d.rectangle([8, 117, 1016, 119], fill=INK)

# ---------------------------------------------------------------- stat strip 118-154
# v4: the Seoul fund stat moves out (still in the Kospi lead body);
# NVIDIA +31.48% in green takes the slot — the day's biggest number.
stats = [("15", "KILLED AROUND KYIV"),
         ("-3.31%", "KOSPI ON MONDAY"),
         ("700,000", "WOMEN IN NHS AI TRIAL"),
         ("429", "FLIGHTS AXED IN BELGIUM"),
         ("24", "BODY BAGS, INDONESIA FIRE"),
         ("+31.48%", "NVIDIA SHARES")]
for i, (n, lab) in enumerate(stats):
    x0 = 8 + i * 168
    col = GREEN if i == 5 else (RED if i in (0, 1) else INK)
    center(d, x0 + 84, 121, n, F["stat_n"], col)
    center(d, x0 + 84, 145, lab, F["stat_l"], GREY)
    if i:
        d.line([x0, 123, x0, 151], fill=GREY, width=1)
d.line([8, 154, 1016, 154], fill=INK, width=1)

# ---------------------------------------------------------------- region bar 156-174
# v4 recount (30 stories): AP 7, ME 6, EU 8, AM 6, AF 1, OC 1, GL 1.
regs = [("ASIA-PACIFIC", 7, (184, 120, 20)), ("MIDDLE EAST", 6, RED),
        ("EUROPE", 8, (60, 90, 140)), ("AMERICAS", 6, (13, 100, 100)),
        ("AFRICA", 1, (120, 90, 40)), ("OCEANIA", 1, (90, 60, 130)),
        ("GLOBAL", 1, NAVY)]
rx = 8
for name, n, col in regs:
    label = f"{name} {n}"
    w = d.textlength(label, font=F["reg"]) + 22
    d.rectangle([rx, 158, rx + w, 172], fill=col)
    d.text((rx + 11, 161), label, font=F["reg"], fill=(255, 255, 255))
    rx += w + 4
d.text((rx + 4, 161), "ONE DAY  ·  ONE PAGE", font=F["reg"], fill=GREY)

# ---------------------------------------------------------------- timeline 176-196
d.rectangle([8, 176, 1016, 196], fill=INK)
tl = ("THE DAY IN UTC   01:00 NHS TRIAL OPENS   ·   03:09 IRGC DRONE TALLY   ·   "
      "06:30 KOSPI -3.31%   ·   08:05 MERKURY SUNK   ·   "
      "19:00 RUBIO MEETS QATAR PM   ·   21:00 S&P +4.73%, NASDAQ +6.51%")
f = F["time"]
while d.textlength(tl, font=f) > 1000 and f.size > 8:
    f = font(SANS_B, f.size - 1)
center(d, 512, 180, tl, f, (255, 255, 255))

# ---------------------------------------------------------------- leads 200-410
# v4: FOUR leads across, 246px wide x 210 tall. Illustrations are redrawn
# for the narrower card; headlines are kept to 2 lines and bodies run to
# ~200 chars (5 lines at 9pt), placed dynamically below the headline with
# an adaptive line cap so nothing prints past the card's bottom edge.
LY0, LH, LW = 200, 210, 246
ILL_H = 76


def illo_cop31(ix, iy):
    # Empty chairs + cracked globe + NO DEAL stamp, 246x76.
    d.rectangle([ix, iy, ix + LW, iy + ILL_H], fill=(214, 232, 214))
    d.rectangle([ix + 10, iy + 46, ix + 64, iy + 68], fill=(120, 90, 60))
    d.rectangle([ix + 10, iy + 68, ix + 64, iy + 72], fill=(90, 65, 40))
    for fx in (22, 38, 54):
        d.rectangle([ix + fx - 6, iy + 26, ix + fx + 6, iy + 46],
                    fill=(150, 140, 120), outline=(90, 80, 60), width=1)
        d.rectangle([ix + fx - 3, iy + 32, ix + fx + 3, iy + 40],
                    fill=(214, 232, 214))
    d.ellipse([ix + 84, iy + 8, ix + 138, iy + 62], fill=(90, 140, 190),
              outline=NAVY, width=2)
    d.ellipse([ix + 96, iy + 18, ix + 112, iy + 32], fill=(120, 180, 120))
    d.ellipse([ix + 116, iy + 38, ix + 128, iy + 52], fill=(120, 180, 120))
    d.line([ix + 98, iy + 12, ix + 108, iy + 26, ix + 102, iy + 40,
            ix + 118, iy + 52], fill=RED, width=2)
    d.text((ix + 150, iy + 6), "COP31", font=font(SANS_B, 15), fill=NAVY)
    d.text((ix + 150, iy + 26), "ANTALYA", font=F["cap_b"], fill=INK)
    d.rectangle([ix + 148, iy + 44, ix + 236, iy + 68], outline=RED, width=3)
    d.text((ix + 154, iy + 49), "NO DEAL", font=font(SANS_B, 12), fill=RED)


def illo_merkury(ix, iy):
    # Night sea, capsized hull, drones, moon — 246x76.
    d.rectangle([ix, iy, ix + LW, iy + ILL_H], fill=(16, 28, 50))
    for sx, sy in [(24, 14), (70, 8), (120, 16), (170, 10), (210, 16)]:
        d.ellipse([ix + sx, iy + sy, ix + sx + 3, iy + sy + 3],
                  fill=(255, 255, 255))
    d.rectangle([ix, iy + 48, ix + LW, iy + ILL_H], fill=(30, 60, 95))
    d.polygon([(ix + 48, iy + 48), (ix + 190, iy + 48), (ix + 176, iy + 64),
               (ix + 62, iy + 64)], fill=(60, 65, 75),
              outline=(200, 200, 200))
    d.rectangle([ix + 104, iy + 42, ix + 134, iy + 48], fill=(60, 65, 75))
    for mx, my in [(32, 10), (88, 6), (150, 12), (200, 8)]:
        d.line([ix + mx, iy + my + 10, ix + mx + 12, iy + my], fill=GOLD,
               width=2)
        d.ellipse([ix + mx + 10, iy + my - 2, ix + mx + 15, iy + my + 3],
                  fill=GOLD)
    d.ellipse([ix + 222, iy + 6, ix + 240, iy + 24], fill=(230, 230, 210))


def illo_wallst(ix, iy):
    # Rising green chart + S&P print — 246x76.
    d.rectangle([ix, iy, ix + LW, iy + ILL_H], fill=(255, 255, 255))
    d.rectangle([ix + 8, iy + 8, ix + 148, iy + 68], fill=(250, 246, 238),
                outline=GREY, width=1)
    for gy in (22, 36, 50, 62):
        d.line([ix + 10, iy + gy, ix + 146, iy + gy], fill=(220, 215, 200),
               width=1)
    d.line([ix + 14, iy + 58, ix + 48, iy + 50, ix + 82, iy + 54,
            ix + 112, iy + 32, ix + 142, iy + 16], fill=GREEN, width=3)
    d.ellipse([ix + 138, iy + 12, ix + 146, iy + 20], fill=GREEN)
    d.text((ix + 158, iy + 6), "S&P 500", font=font(SANS_B, 13), fill=NAVY)
    d.text((ix + 158, iy + 24), "+4.73%", font=font(SANS_B, 19), fill=GREEN)
    d.text((ix + 158, iy + 46), "7,237.17", font=F["cap_b"], fill=INK)
    d.text((ix + 158, iy + 60), "NASDAQ +6.51%", font=font(SANS_B, 8),
           fill=GREEN)


def illo_kospi(ix, iy):
    # Falling red chart + Kospi print — 246x76.
    d.rectangle([ix, iy, ix + LW, iy + ILL_H], fill=(255, 255, 255))
    d.rectangle([ix + 8, iy + 8, ix + 148, iy + 68], fill=(250, 246, 238),
                outline=GREY, width=1)
    for gy in (22, 36, 50, 62):
        d.line([ix + 10, iy + gy, ix + 146, iy + gy], fill=(220, 215, 200),
               width=1)
    d.line([ix + 14, iy + 16, ix + 48, iy + 26, ix + 82, iy + 24,
            ix + 112, iy + 44, ix + 142, iy + 58], fill=RED, width=3)
    d.ellipse([ix + 138, iy + 54, ix + 146, iy + 62], fill=RED)
    d.text((ix + 158, iy + 6), "KOSPI", font=font(SANS_B, 15), fill=NAVY)
    d.text((ix + 158, iy + 26), "-3.31%", font=font(SANS_B, 19), fill=RED)
    d.text((ix + 158, iy + 48), "4,708.54", font=F["cap_b"], fill=INK)
    d.rectangle([ix + 158, iy + 62, ix + 184, iy + 74], fill=NAVY)
    d.rectangle([ix + 166, iy + 65, ix + 176, iy + 71], fill=(255, 255, 255))


ILLOS = {"cop31": illo_cop31, "merkury": illo_merkury,
         "wallst": illo_wallst, "kospi": illo_kospi}

LEADS = [
    {"kicker": "1  ·  ANTALYA, TÜRKIYE  ·  CLIMATE",
     "tag": "NO DEAL", "tag_color": RED,
     "headline": "COP31 blame game erupts as talks end in no deal",
     "body": ("Antalya collapsed Sunday after ~48 hours of overtime — no deal, "
              "no fossil-fuel mention. Monday: Bowen resignation calls, Pacific "
              "despair, Saudi-access reports. 90+ states signed a pledge. "
              "(Reuters)"),
     "illo": "cop31"},
    {"kicker": "2  ·  BENGHAZI & KYIV  ·  WAR",
     "tag": "REPORTED", "tag_color": GREEN,
     "headline": "Zelenskyy: Ukraine sank a Russian corvette off Libya",
     "body": ("Zelenskyy said Monday that seven sea drones sank the Merkury "
              "at berth; satellite images show it capsized. Russian strikes "
              "killed at least 15 around Kyiv. A boy, 7, was pulled alive "
              "after 22 hours. (Reuters, AFP)"),
     "illo": "merkury"},
    {"kicker": "3  ·  NEW YORK, USA  ·  MARKETS",
     "tag": "+4.73%", "tag_color": GREEN,
     "headline": "Wall Street roars back in its best day since April",
     "body": ("The S&P 500 jumped 4.73% to 7,237.17 and the Nasdaq 6.51%, "
              "ending a seven-day slide. Nvidia's board reinstated Jensen "
              "Huang as CEO; its shares rose 31.48%. The Dow added 3.01% "
              "and the VIX fell 25.83%. (AP, CNBC)"),
     "illo": "wallst"},
    {"kicker": "4  ·  SEOUL, S. KOREA  ·  MARKETS",
     "tag": "-3.31%", "tag_color": RED,
     "headline": "Kospi dives 3.31% as the AI-bubble rout spreads",
     "body": ("Seoul's index closed at 4,708.54, lowest since 13 January, "
              "after falling 5.1% intraday. Program trading halted for 5 "
              "minutes. Seoul prepares to activate a ₩10.76tn fund; "
              "deployment undecided. (Yonhap)"),
     "illo": "kospi"},
]

for i, L in enumerate(LEADS):
    x0 = 8 + i * (LW + 8)
    d.rectangle([x0, LY0, x0 + LW, LY0 + LH], outline=INK, width=2)
    ILLOS[L["illo"]](x0, LY0)
    d.text((x0 + 8, LY0 + 80), L["kicker"], font=F["lead_s"], fill=INK)
    tw = d.textlength(L["tag"], font=F["badge"]) + 8
    tag(d, x0 + LW - tw - 4, LY0 + 79, L["tag"], L["tag_color"])
    hlines = wrap(d, L["headline"], F["lead"], LW - 16)
    for j, ln in enumerate(hlines):
        d.text((x0 + 8, LY0 + 96 + j * 19), ln, font=F["lead"], fill=INK)
    by = LY0 + 96 + len(hlines) * 19 + 6
    # Safety net: never print past the card's bottom edge, however the
    # headline wraps. With 2-line headlines this allows 5 body lines.
    max_lines = max(3, (LY0 + LH - 8 - by) // 12)
    for j, ln in enumerate(wrap(d, L["body"], F["lead_b"], LW - 16)[:max_lines]):
        d.text((x0 + 8, by + j * 12), ln, font=F["lead_b"], fill=INK)

# ---------------------------------------------------------------- secondary cards 414-618
# v4: 12 cards, numbered 05-16. The Wall Street card is promoted to lead 3;
# the Nvidia card (chip icon) takes the last slot. Rubio card upgraded from
# a preview ("talks 19:00 UTC") to the reported outcome.
# Card text geometry (FIXED 25 Nov: v4's first render clipped every card's
# second body line against the bottom border). Card is 99px tall, border at
# y0+99; the icon area owns y0..y0+48 and cannot shrink (icon art already
# spans ~44px), so the text stack must fit y0+49..y0+97. DejaVu extent is
# size x (1901+483)/2048, i.e. 10pt = 11.64px, 7pt = 8.15px, 9pt digits =
# 8.35px (no descenders). Stack: number y0+49 (bottom y0+57.35) -> headline
# 10pt at y0+58 / y0+68 (line 2 bottom y0+79.64) -> body 7pt c1 y0+80 /
# c2 y0+88 (bottom y0+96.15) = 2.85px clearance above the border.
# Tightest gap is headline line 2 -> c1 (0.36px); headline leading overlap
# is 1.64px, the same as v3's proven 11pt/11px leading. Headline shrink is
# wrap-safe: a smaller font can only reduce a headline's line count.
cards = [
    ("NHS launches world's largest AI breast-screening trial",
     "EDITH: ~700,000 women, 30 sites;", "AI reads one of two readers (BBC)", "trial"),
    ("Gaza a 'toxic wasteland', Oxfam report finds",
     "Contamination signs across >99%;", "61m+ tonnes of debris (Oxfam)", "toxic"),
    ("Belgium strike grounds almost all flights",
     "429 flights axed at Brussels;", "Charleroi shut; ~59,500 hit", "plane"),
    ("Cikande search continues after factory fire",
     "24 body bags recovered Sunday;", "34 unaccounted for; ID pending", "fire"),
    ("Nepal PM Shah lands in Delhi",
     "₹15,000-crore aid; 8 MoUs signed;", "new Ayodhya–Janakpur train (ANI)", "flags"),
    ("China unveils 2030 eldercare plan",
     "Nursing beds 73% of care beds;", "as population shrinks (Reuters)", "elder"),
    ("Iran claims 78 US drones downed",
     "Tehran's tally alone since Feb;", "Pentagon unconfirmed — CLAIM", "drone"),
    ("US and Qatar launch 8th strategic dialogue",
     "Rubio and Vance met Qatar's PM;", "no breakthrough; Doha pushes talks", "talks"),
    ("Iran says two tankers hit mines",
     "IRGC: mines east of Hormuz;", "claim unverified — CLAIM (Tasnim)", "mine"),
    ("New Zealand hang on to draw Test",
     "Mitchell 49* saves Wellington;", "India declared 720/9 (ESPNcricinfo)", "cricket"),
    ("Lowy Index: India holds third",
     "US 78.9, China 73.6, India 40.5;", "gap narrowest since 2018 (Lowy)", "chart"),
    ("Nvidia reinstates Huang as CEO",
     "Board acts 11 days after exit;", "shares +31.48%, ~$950B added", "chip"),
]
CW, CH, GAP = 163, 99, 6
for idx, (h, c1, c2, kind) in enumerate(cards):
    col, row = idx % 6, idx // 6
    x0 = 8 + col * (CW + GAP)
    y0 = 414 + row * (CH + GAP)
    d.rectangle([x0, y0, x0 + CW, y0 + CH], outline=INK, width=1)
    d.rectangle([x0, y0, x0 + CW, y0 + 48], fill=SKY)
    ix, iy = x0 + 8, y0 + 3
    if kind == "trial":
        d.rectangle([ix + 44, iy + 6, ix + 104, iy + 42], fill=(255, 255, 255),
                    outline=NAVY, width=2)
        for ly in (14, 22, 30):
            d.line([ix + 52, iy + ly, ix + 96, iy + ly], fill=GREY, width=2)
        d.line([ix + 52, iy + 38, ix + 72, iy + 38], fill=GREEN, width=2)
        d.text((ix + 6, iy + 10), "AI", font=font(SANS_B, 20), fill=RED)
        d.ellipse([ix + 108, iy + 26, ix + 132, iy + 42], outline=NAVY, width=3)
        d.line([ix + 128, iy + 38, ix + 142, iy + 44], fill=NAVY, width=3)
    elif kind == "toxic":
        d.polygon([(ix + 74, iy + 2), (ix + 146, iy + 44), (ix + 2, iy + 44)],
                  fill=GOLD, outline=INK, width=2)
        d.text((ix + 68, iy + 14), "!", font=font(SANS_B, 24), fill=INK)
        d.rectangle([ix + 8, iy + 40, ix + 40, iy + 44], fill=RED)
    elif kind == "plane":
        d.polygon([(ix + 10, iy + 26), (ix + 60, iy + 26), (ix + 70, iy + 20),
                   (ix + 110, iy + 20), (ix + 140, iy + 26), (ix + 110, iy + 32),
                   (ix + 60, iy + 32)], fill=NAVY)
        d.polygon([(ix + 70, iy + 20), (ix + 86, iy + 4), (ix + 96, iy + 20)],
                  fill=NAVY)
        d.line([ix + 96, iy + 26, ix + 130, iy + 40], fill=NAVY, width=4)
        d.line([ix + 8, iy + 42, ix + 142, iy + 42], fill=RED, width=3)
    elif kind == "fire":
        d.rectangle([ix + 10, iy + 20, ix + 70, iy + 44], fill=NAVY)
        d.rectangle([ix + 80, iy + 10, ix + 88, iy + 44], fill=NAVY)
        d.rectangle([ix + 96, iy + 14, ix + 104, iy + 44], fill=NAVY)
        d.polygon([(ix + 116, iy + 44), (ix + 126, iy + 16), (ix + 136, iy + 44)],
                  fill=GOLD)
        d.polygon([(ix + 122, iy + 44), (ix + 128, iy + 28), (ix + 134, iy + 44)],
                  fill=RED)
    elif kind == "flags":
        d.polygon([(ix + 6, iy + 8), (ix + 66, iy + 8), (ix + 6, iy + 24)],
                  fill=(220, 40, 60))
        d.polygon([(ix + 6, iy + 24), (ix + 48, iy + 24), (ix + 6, iy + 40)],
                  fill=(200, 30, 50))
        d.rectangle([ix + 82, iy + 8, ix + 142, iy + 18], fill=(255, 153, 51))
        d.rectangle([ix + 82, iy + 18, ix + 142, iy + 29], fill=(255, 255, 255))
        d.rectangle([ix + 82, iy + 29, ix + 142, iy + 40], fill=(19, 136, 8))
        d.ellipse([ix + 106, iy + 20, ix + 118, iy + 27], outline=NAVY, width=2)
    elif kind == "elder":
        d.polygon([(ix + 20, iy + 26), (ix + 74, iy + 4), (ix + 128, iy + 26)],
                  fill=RED)
        d.rectangle([ix + 30, iy + 26, ix + 118, iy + 44], fill=(255, 255, 255),
                    outline=INK, width=1)
        d.rectangle([ix + 66, iy + 30, ix + 82, iy + 44], fill=NAVY)
        d.text((ix + 128, iy + 8), "73%", font=font(SANS_B, 14), fill=NAVY)
    elif kind == "drone":
        d.line([ix + 20, iy + 12, ix + 128, iy + 36], fill=INK, width=3)
        d.line([ix + 128, iy + 12, ix + 20, iy + 36], fill=INK, width=3)
        for cx, cy in [(20, 12), (128, 12), (20, 36), (128, 36)]:
            d.ellipse([ix + cx - 8, iy + cy - 3, ix + cx + 8, iy + cy + 3],
                      outline=INK, width=2)
        d.rectangle([ix + 62, iy + 18, ix + 86, iy + 30], fill=NAVY)
        d.text((ix + 96, iy + 34), "78", font=font(SANS_B, 12), fill=RED)
    elif kind == "talks":
        d.ellipse([ix + 8, iy + 8, ix + 78, iy + 34], fill=(255, 255, 255),
                  outline=NAVY, width=2)
        d.ellipse([ix + 70, iy + 18, ix + 140, iy + 44], fill=(220, 233, 242),
                  outline=NAVY, width=2)
        d.text((ix + 18, iy + 14), "US", font=font(SANS_B, 12), fill=NAVY)
        d.text((ix + 92, iy + 26), "QA", font=font(SANS_B, 12), fill=NAVY)
    elif kind == "mine":
        d.rectangle([ix, iy + 26, ix + 147, iy + 44], fill=OCEAN)
        d.ellipse([ix + 56, iy + 6, ix + 92, iy + 42], fill=INK)
        for sx, sy in [(74, 2), (74, 42), (52, 24), (96, 24)]:
            d.line([ix + sx, iy + sy, ix + sx, iy + sy + 4], fill=INK, width=3)
        for wx in range(6, 140, 22):
            d.arc([ix + wx, iy + 34, ix + wx + 18, iy + 44], 180, 360,
                  fill=NAVY, width=2)
    elif kind == "cricket":
        d.rectangle([ix, iy + 26, ix + 147, iy + 44], fill=(120, 180, 100))
        d.line([ix + 10, iy + 14, ix + 60, iy + 14], fill=(150, 110, 70), width=6)
        d.line([ix + 60, iy + 14, ix + 74, iy + 26], fill=(150, 110, 70), width=5)
        d.ellipse([ix + 96, iy + 6, ix + 108, iy + 18], fill=RED)
        for sx in (118, 126, 134):
            d.line([ix + sx, iy + 24, ix + sx, iy + 38], fill=GOLD, width=3)
        d.text((ix + 6, iy + 28), "720/9", font=font(SANS_B, 13),
               fill=(255, 255, 255))
    elif kind == "chart":
        for bx, bh, col in [(8, 40, NAVY), (44, 34, RED), (80, 22, TEAL)]:
            d.rectangle([ix + bx, iy + 44 - bh, ix + bx + 24, iy + 44], fill=col)
        d.text((ix + 112, iy + 6), "78.9", font=font(SANS_B, 11), fill=NAVY)
        d.text((ix + 112, iy + 20), "73.6", font=font(SANS_B, 11), fill=RED)
        d.text((ix + 112, iy + 34), "40.5", font=font(SANS_B, 11), fill=TEAL)
    elif kind == "chip":
        # Nvidia green chip + rising arrow (new v4 icon).
        d.rectangle([ix + 30, iy + 6, ix + 90, iy + 40], fill=(118, 185, 0),
                    outline=(40, 90, 0), width=2)
        d.rectangle([ix + 46, iy + 16, ix + 74, iy + 30], fill=(255, 255, 255))
        for py in (14, 24, 34):
            d.line([ix + 24, iy + py, ix + 30, iy + py], fill=(40, 90, 0),
                   width=2)
            d.line([ix + 90, iy + py, ix + 96, iy + py], fill=(40, 90, 0),
                   width=2)
        d.line([ix + 104, iy + 38, ix + 136, iy + 10], fill=GREEN, width=3)
        d.line([ix + 136, iy + 10, ix + 126, iy + 12], fill=GREEN, width=3)
        d.line([ix + 136, iy + 10, ix + 134, iy + 20], fill=GREEN, width=3)
    d.text((x0 + 5, y0 + 49), f"{idx + 5:02d}", font=F["cap_b"], fill=RED)
    for j, ln in enumerate(wrap(d, h, F["card_h"], CW - 10)[:2]):
        d.text((x0 + 5, y0 + 58 + j * 10), ln, font=F["card_h"], fill=INK)
    d.text((x0 + 5, y0 + 80), c1, font=F["card_c"], fill=GREY)
    d.text((x0 + 5, y0 + 88), c2, font=F["card_c"], fill=GREY)

# ---------------------------------------------------------------- map + date check 622-812
# v4: the map is BIGGER (576x146, was 496x136) because DATE CHECK lost its
# third row; pin label offsets reworked to fix v3 collisions.
MX0, MX1, MY0, MY1 = 8, 600, 622, 812
d.rectangle([MX0, MY0, MX1, MY1], outline=INK, width=2)
d.text((MX0 + 8, MY0 + 5), "WHERE IT HAPPENED", font=F["sect"], fill=INK)
d.text((MX1 - 150, MY0 + 7), "pins = story numbers", font=F["cap"], fill=GREY)
MAPX0, MAPY0, MAPW, MAPH = MX0 + 8, MY0 + 24, MX1 - MX0 - 16, 146
d.rectangle([MAPX0, MAPY0, MAPX0 + MAPW, MAPY0 + MAPH], fill=OCEAN)


def proj(lon, lat):
    return (MAPX0 + (lon + 180) / 360 * MAPW,
            MAPY0 + (90 - lat) / 180 * MAPH)


CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-80, 73), (-70, 62), (-60, 52), (-55, 47), (-65, 44), (-70, 42),
     (-75, 35), (-80, 32), (-81, 25), (-90, 21), (-97, 16), (-94, 17),
     (-86, 15), (-83, 9), (-79, 9), (-85, 13), (-92, 15), (-97, 16),
     (-105, 20), (-110, 23), (-114, 29), (-120, 34), (-124, 40), (-124, 48),
     (-130, 55), (-140, 60), (-155, 58), (-165, 60)],
    [(-79, 9), (-72, 12), (-64, 10), (-55, 6), (-50, 0), (-44, -3), (-35, -8),
     (-38, -15), (-40, -22), (-48, -28), (-52, -33), (-58, -38), (-62, -41),
     (-65, -45), (-68, -50), (-68, -55), (-72, -54), (-73, -45), (-73, -37),
     (-71, -30), (-70, -20), (-75, -15), (-79, -8), (-81, -3), (-80, 1)],
    [(-17, 15), (-10, 6), (-8, 4), (0, 6), (6, 4), (9, -1), (13, -12),
     (12, -18), (16, -28), (20, -35), (28, -33), (32, -29), (35, -23),
     (40, -15), (41, -10), (46, -11), (51, 11), (44, 11), (40, 15), (38, 18),
     (35, 20), (32, 31), (30, 31), (20, 32), (11, 34), (10, 37), (0, 36),
     (-6, 35), (-10, 31), (-15, 27), (-17, 21)],
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 53), (5, 58), (10, 58),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 70), (40, 68), (50, 69),
     (60, 69), (70, 72), (80, 73), (90, 75), (100, 77), (110, 74), (120, 73),
     (130, 72), (140, 72), (150, 70), (160, 70), (170, 67), (178, 65),
     (178, 62), (170, 60), (162, 56), (156, 51), (150, 45), (142, 42),
     (140, 35), (135, 34), (130, 33), (127, 35), (122, 38), (120, 32),
     (122, 28), (118, 25), (110, 20), (108, 12), (105, 9), (103, 1), (100, 7),
     (98, 12), (95, 16), (92, 21), (88, 22), (85, 19), (80, 15), (77, 8),
     (75, 12), (72, 20), (68, 23), (66, 25), (62, 25), (58, 26), (56, 27),
     (52, 26), (50, 29), (48, 30), (44, 29), (40, 31), (36, 36), (30, 36),
     (27, 37), (23, 36), (19, 40), (16, 42), (12, 44), (8, 44), (3, 43),
     (-2, 37), (-6, 36)],
    [(114, -22), (114, -30), (118, -35), (124, -33), (129, -32), (132, -32),
     (135, -35), (138, -35), (140, -38), (145, -38), (147, -42), (150, -37),
     (153, -30), (153, -27), (146, -19), (142, -15), (142, -11), (137, -12),
     (135, -15), (132, -12), (129, -15), (126, -14), (122, -17), (118, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (1, 52), (1, 51), (-3, 50)],
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (143, 43),
     (145, 44), (142, 44), (140, 40), (138, 37), (135, 34), (132, 33)],
    [(167, -45), (170, -42), (173, -39), (175, -37), (178, -38), (175, -41),
     (172, -43), (169, -46)],
]
for poly in CONTINENTS:
    d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
              outline=LANDLINE)

# pins: (num, lon, lat, label dx, dy) — v4 numbering (leads 1-4, cards 05-16).
# Label offsets chosen so neighbours don't collide: Brussels left of London,
# Beijing below-right of Seoul, Tehran above Hormuz, Canberra below-right
# of Wellington, Washington below-left of New York.
PINS = [
    ("1", 30.7, 36.9, -34, 10),
    ("2", 30.5, 50.5, 8, -14),
    ("2", 20.1, 32.1, 8, 8),
    ("3", -74.0, 40.7, 8, -14),
    ("4", 127.0, 37.5, 8, -14),
    ("05", 0.1, 52.2, 8, -14),
    ("06", 34.5, 31.5, 8, 8),
    ("07", 4.4, 50.8, -40, 6),
    ("08", 106.5, -6.2, -40, 8),
    ("09", 77.2, 28.6, 8, -16),
    ("10", 116.4, 39.9, 8, 8),
    ("11", 51.4, 35.7, 8, -16),
    ("12", -77.4, 38.9, -30, 10),
    ("13", 56.5, 26.5, 8, 8),
    ("14", 174.8, -41.3, -36, -14),
    ("15", 149.1, -35.3, 8, 8),
    ("16", -122.0, 37.4, 8, -14),
]
for num, lon, lat, dx, dy in PINS:
    px, py = proj(lon, lat)
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED, outline=(255, 255, 255))
    lx, ly = px + dx, py + dy
    w = d.textlength(num, font=F["pin"]) + 6
    d.line([px, py, lx + w / 2, ly + 6], fill=RED, width=1)
    d.rectangle([lx, ly, lx + w, ly + 12], fill=(255, 255, 255),
                outline=RED, width=1)
    d.text((lx + 3, ly + 1.5), num, font=F["pin"], fill=RED)
d.text((MAPX0, MY0 + 174),
       "No pin: 17-30 (ALSO list). 2 also at Benghazi, Libya.",
       font=F["cap"], fill=GREY)

# DATE CHECK (right) — v4: only TWO rows. The "not yet decided" row is gone
# because all three items are now decided (US close, Rubio readout, Kyiv toll).
DX0, DX1, DY0, DY1 = 608, 1016, 622, 812
d.rectangle([DX0, DY0, DX1, DY1], outline=INK, width=2)
d.text((DX0 + 8, DY0 + 5), "DATE CHECK — WHAT COUNTS AS 23 NOVEMBER",
       font=F["sect"], fill=INK)
dc_rows = [
    (RED, "LEFT OUT — EARLIER EVENTS",
     "Democrats' 258th House seat (Sun) · COP31 collapse itself (Sun) · "
     "Verstappen GP (Sat) · Chapo Isidro (Fri) · Alcaraz title (Sun) · "
     "Liverpool 4-0 Man Utd (Sun) · Shenzhen summit (Thu) · SAPS stats "
     "(Fri) · Ebola 11,000 (mid-Nov) · Ship seizure disclosed (Fri) · "
     "Riemann proof claim (Fri)"),
    (GREEN, "INCLUDED — MONDAY DEVELOPMENTS",
     "COP31 fallout · Merkury announcement (Sun operation, Mon claim) · "
     "Kyiv toll 15 · Dymer boy rescued after 22 hours · Kospi slide + "
     "Seoul fund · NHS trial launch · Belgium strike · Hormuz mine claim "
     "(Tasnim) · Cikande search continues · US rebound + Nvidia (Mon close)"),
]
y = DY0 + 25
for color, head, text in dc_rows:
    d.rectangle([DX0 + 8, y + 2, DX0 + 18, y + 12], fill=color)
    d.text((DX0 + 22, y), head, font=F["dc_b"], fill=color)
    y += 15
    for ln in wrap(d, text, F["dc"], DX1 - DX0 - 36):
        d.text((DX0 + 22, y), ln, font=F["dc"], fill=INK)
        y += 12
    y += 6
d.text((DX0 + 8, DY1 - 16), "Sources checked through ~21:30 UTC, Mon 23 Nov 2026.",
       font=F["cap"], fill=GREY)

# ---------------------------------------------------------------- ALSO list 816-980
d.text((8, 816), "ALSO ON MONDAY 23 NOVEMBER — 14 MORE STORIES",
       font=F["sect"], fill=INK)
d.line([8, 834, 1016, 834], fill=INK, width=1)
also = [
    "Bitcoin closes at $61,356 (+4.68%); Hayes warns of $55k",
    "Paolo Bulgari funeral held in Rome (died Sat)",
    "Thanksgiving travel: Delta's Sunday meltdown + storm watch",
    "US intel chief defends Trump calling Putin 'friend'",
    "West Bank medics attacks up 350%, rights group says",
    "Syria–EU talks progress; repatriation fears",
    "Taliban police protect Afghanistan's vanishing forests",
    "Meta's Alexandr Wang: superintelligence 'arriving'",
    "Trump to host a third crypto gala",
    "US envoy floats NATO-style guarantees for Ukraine",
    "Sudanese widowed mothers struggle amid war",
    "Europe's 'hot autumn' protests: economic symptom",
    "Taiwan shares slip 0.93%; Japan shut for holiday",
    "France hopefuls both question Ukraine aid",
]
for i, item in enumerate(also):
    col, row = i % 3, i // 3
    x0 = 8 + col * 336
    y0 = 842 + row * 28
    d.text((x0, y0), f"{i + 17:02d}", font=F["list_b"], fill=RED)
    for j, ln in enumerate(wrap(d, item, F["list"], 306)[:2]):
        d.text((x0 + 26, y0 + j * 12), ln, font=F["list"], fill=INK)

# ---------------------------------------------------------------- footer 984-1024
d.line([8, 984, 1016, 984], fill=INK, width=2)
d.text((8, 990),
       "Sources: Reuters · BBC · AP · AFP · Al Jazeera · ESPNcricinfo · Lowy Institute · Oxfam/CEOBS · official statements",
       font=F["foot"], fill=GREY)
d.text((8, 1002),
       "30 stories checked against reporting available on 23 Nov 2026 to ~21:30 UTC. Scenes are drawn illustrations, not photographs.",
       font=F["foot"], fill=GREY)
r1 = "REPORTED = carried by the day's wires   CLAIM = one side's account, labelled"
d.text((1014 - d.textlength(r1, font=F["foot"]), 990), r1, font=F["foot"],
       fill=GREY)
r2 = "HORMUZ = IRGC said Sun, reported Mon (Tasnim)"
d.text((1014 - d.textlength(r2, font=F["foot"]), 1002), r2, font=F["foot"],
       fill=GREY)

img.save("entry.png", format="PNG")
print("saved entry.png")
