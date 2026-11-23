#!/usr/bin/env python3
"""news-image-20261123 — deterministic front-page render.

Parent-direct build (20261121/20261122 precedent: parent builds directly).
Story data: ~/workspace/makefun/news-image-20261123-research/verified-stories-2026-11-23.md
(30 verified Monday items) + parent spot-checks (5 date traps caught:
Democrats-258 Sunday, Shenzhen Thu, Riemann Fri, Korea $1tn Thu, SAPS Fri).
Concept: ChatGPT-approved Concept A (editorial broadsheet), GO WITH
CONDITIONS 23 Nov ~18:20 WIB — COP31 lead 1 as Monday fallout, Merkury
lead 2 as a Sunday operation announced Monday, strict hierarchy for the
300px test (leads dominate; cards by headline+icon; ALSO list compact).
Review corrections applied: boy-rescue hours dropped (14h vs 22h conflict);
Kyiv "at least 15" (AFP) / "11 in Dymer" (Reuters); Indonesia AP 34 missing
+ forensic ID pending; Gaza "indicators of potential contamination";
NHS "AI-assisted trial"; Seoul fund "readies"; Hormuz CLAIM + Sun/Monday
note; Iran 78 drones Tehran-only; Rubio card drops "seven conditions".
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
    "mast": font(SERIF_B, 50),
    "sub": font(SANS_B, 14),
    "stat_n": font(SANS_B, 26),
    "stat_l": font(SANS_B, 8),
    "reg": font(SANS_B, 10),
    "time": font(SANS_B, 10),
    "lead": font(SERIF_B, 18),
    "lead_s": font(SANS_B, 10),
    "lead_b": font(SANS, 10),
    "cap": font(SANS, 9),
    "cap_b": font(SANS_B, 9),
    "card_h": font(SANS_B, 11),
    "card_c": font(SANS, 8),
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

# ---------------------------------------------------------------- masthead 18-78
center(d, 512, 24, "Monday 23 November 2026", F["mast"])
center(d, 512, 80,
       "COP31 blame game erupts  ·  Ukraine says it sank a Russian corvette  ·  Kospi dives 3.31%",
       F["sub"], RED)
d.rectangle([8, 98, 1016, 100], fill=INK)

# ---------------------------------------------------------------- stat strip 100-136
stats = [("15", "KILLED AROUND KYIV"),
         ("-3.31%", "KOSPI ON MONDAY"),
         ("700,000", "WOMEN IN NHS AI TRIAL"),
         ("429", "FLIGHTS AXED IN BELGIUM"),
         ("24", "BODY BAGS, INDONESIA FIRE"),
         ("₩10tn", "SEOUL STABILISATION FUND")]
for i, (n, lab) in enumerate(stats):
    x0 = 8 + i * 168
    center(d, x0 + 84, 103, n, F["stat_n"], RED if i in (0, 1, 5) else INK)
    center(d, x0 + 84, 129, lab, F["stat_l"], GREY)
    if i:
        d.line([x0, 105, x0, 135], fill=GREY, width=1)
d.line([8, 138, 1016, 138], fill=INK, width=1)

# ---------------------------------------------------------------- region bar 138-158
regs = [("ASIA-PACIFIC", 7, (184, 120, 20)), ("MIDDLE EAST", 6, RED),
        ("EUROPE", 8, (60, 90, 140)), ("AMERICAS", 5, (13, 100, 100)),
        ("AFRICA", 1, (120, 90, 40)), ("OCEANIA", 1, (90, 60, 130)),
        ("GLOBAL", 2, NAVY)]
rx = 8
for name, n, col in regs:
    label = f"{name} {n}"
    w = d.textlength(label, font=F["reg"]) + 22
    d.rectangle([rx, 140, rx + w, 156], fill=col)
    d.text((rx + 11, 143), label, font=F["reg"], fill=(255, 255, 255))
    rx += w + 4
d.text((rx + 4, 143), "ONE DAY  ·  ONE PAGE", font=F["reg"], fill=GREY)

# ---------------------------------------------------------------- timeline 158-178
d.rectangle([8, 160, 1016, 178], fill=INK)
tl = ("THE DAY IN UTC   01:00 NHS AI TRIAL OPENS   ·   03:09 IRGC DRONE TALLY   ·   "
      "06:00 KOSPI CLOSES -3.31%   ·   08:05 ZELENSKYY: MERKURY SUNK   ·   "
      "19:00 RUBIO MEETS QATAR PM")
f = F["time"]
while d.textlength(tl, font=f) > 1000 and f.size > 8:
    f = font(SANS_B, f.size - 1)
center(d, 512, 164, tl, f, (255, 255, 255))

# ---------------------------------------------------------------- leads 182-382
LY0, LH = 182, 200
LW = 330


def lead_card(x0):
    d.rectangle([x0, LY0, x0 + LW, LY0 + LH], outline=INK, width=2)

# --- lead 1: COP31 fallout (illustration: empty chairs + cracked globe + NO DEAL stamp)
x0 = 8
lead_card(x0)
ix0, iy0, iw, ih = x0, LY0, LW, 88
d.rectangle([ix0, iy0, ix0 + iw, iy0 + ih], fill=(214, 232, 214))
d.rectangle([ix0 + 16, iy0 + 52, ix0 + 110, iy0 + 76], fill=(120, 90, 60))
d.rectangle([ix0 + 16, iy0 + 76, ix0 + 110, iy0 + 80], fill=(90, 65, 40))
for fx in (36, 62, 88):
    d.rectangle([ix0 + fx - 7, iy0 + 30, ix0 + fx + 7, iy0 + 52],
                fill=(150, 140, 120), outline=(90, 80, 60), width=1)
    d.rectangle([ix0 + fx - 4, iy0 + 36, ix0 + fx + 4, iy0 + 46],
                fill=(214, 232, 214))
d.ellipse([ix0 + 200, iy0 + 12, ix0 + 260, iy0 + 72], fill=(90, 140, 190),
          outline=NAVY, width=2)
d.ellipse([ix0 + 214, iy0 + 24, ix0 + 232, iy0 + 40], fill=(120, 180, 120))
d.ellipse([ix0 + 236, iy0 + 44, ix0 + 250, iy0 + 60], fill=(120, 180, 120))
d.line([ix0 + 216, iy0 + 16, ix0 + 228, iy0 + 32, ix0 + 220, iy0 + 48,
        ix0 + 238, iy0 + 62], fill=RED, width=2)
d.ellipse([ix0 + 286, iy0 + 14, ix0 + 316, iy0 + 44], fill=(255, 255, 255),
          outline=INK, width=2)
d.line([ix0 + 301, iy0 + 29, ix0 + 301, iy0 + 19], fill=INK, width=2)
d.line([ix0 + 301, iy0 + 29, ix0 + 309, iy0 + 29], fill=INK, width=2)
d.text((ix0 + 124, iy0 + 8), "COP31", font=font(SANS_B, 16), fill=NAVY)
d.text((ix0 + 124, iy0 + 28), "ANTALYA", font=F["cap_b"], fill=INK)
d.rectangle([ix0 + 122, iy0 + 48, ix0 + 196, iy0 + 70], outline=RED, width=3)
d.text((ix0 + 128, iy0 + 52), "NO DEAL", font=font(SANS_B, 13), fill=RED)
d.text((x0 + 8, LY0 + 94), "1  ·  ANTALYA, TÜRKIYE  ·  CLIMATE", font=F["lead_s"],
       fill=INK)
tag(d, x0 + LW - 74, LY0 + 93, "NO DEAL", RED)
for j, ln in enumerate(wrap(d, "COP31 blame game erupts as the talks end with no deal",
                            F["lead"], LW - 16)):
    d.text((x0 + 8, LY0 + 110 + j * 20), ln, font=F["lead"], fill=INK)
body1 = ("Antalya collapsed Sunday — no deal, no fossil-fuel mention. "
         "Monday: resignation calls for president Bowen, Pacific despair, "
         "reports of Saudi Arabia's privileged access. 90+ states signed "
         "an electrification pledge. (Reuters, BBC)")
for j, ln in enumerate(wrap(d, body1, F["lead_b"], LW - 16)):
    d.text((x0 + 8, LY0 + 152 + j * 12), ln, font=F["lead_b"], fill=INK)

# --- lead 2: Merkury sinking + Kyiv toll (illustration: night sea, capsized hull, drones)
x0 = 346
lead_card(x0)
ix0, iy0, iw, ih = x0, LY0, LW, 88
d.rectangle([ix0, iy0, ix0 + iw, iy0 + ih], fill=(16, 28, 50))
for sx, sy in [(30, 18), (90, 10), (150, 22), (210, 12), (270, 20)]:
    d.ellipse([ix0 + sx, iy0 + sy, ix0 + sx + 3, iy0 + sy + 3],
              fill=(255, 255, 255))
d.rectangle([ix0, iy0 + 58, ix0 + iw, iy0 + ih], fill=(30, 60, 95))
# capsized hull: dark keel-up shape with a red waterline
d.polygon([(ix0 + 60, iy0 + 58), (ix0 + 240, iy0 + 58), (ix0 + 220, iy0 + 76),
           (ix0 + 80, iy0 + 76)], fill=(60, 65, 75), outline=(200, 200, 200))
d.rectangle([ix0 + 130, iy0 + 50, ix0 + 170, iy0 + 58], fill=(60, 65, 75))
for mx, my in [(40, 14), (110, 8), (200, 18), (260, 10)]:
    d.line([ix0 + mx, iy0 + my + 10, ix0 + mx + 12, iy0 + my], fill=GOLD,
           width=2)
    d.ellipse([ix0 + mx + 10, iy0 + my - 2, ix0 + mx + 15, iy0 + my + 3],
              fill=GOLD)
d.ellipse([ix0 + 286, iy0 + 8, ix0 + 310, iy0 + 32], fill=(230, 230, 210))
d.text((x0 + 8, LY0 + 94), "2  ·  BENGHAZI & KYIV  ·  WAR", font=F["lead_s"],
       fill=INK)
tag(d, x0 + LW - 78, LY0 + 93, "REPORTED", GREEN)
for j, ln in enumerate(wrap(d, "Zelenskyy: Ukraine sank a Russian corvette off Libya",
                            F["lead"], LW - 16)):
    d.text((x0 + 8, LY0 + 110 + j * 20), ln, font=F["lead"], fill=INK)
body2 = ("Seven sea drones sank the Merkury at berth, Zelenskyy said "
         "Monday; satellite images show it capsized. The strike was early "
         "Sunday. Overnight Russian strikes killed at least 15 around Kyiv; "
         "he urged the US to release paid-for Patriots. (Reuters, AFP)")
for j, ln in enumerate(wrap(d, body2, F["lead_b"], LW - 16)):
    d.text((x0 + 8, LY0 + 152 + j * 12), ln, font=F["lead_b"], fill=INK)

# --- lead 3: Kospi dive (illustration: falling chart + chip)
x0 = 684
lead_card(x0)
ix0, iy0, iw, ih = x0, LY0, LW, 88
d.rectangle([ix0, iy0, ix0 + iw, iy0 + ih], fill=(255, 255, 255))
d.rectangle([ix0 + 8, iy0 + 8, ix0 + 200, iy0 + 80], fill=(250, 246, 238),
            outline=GREY, width=1)
for gy in (24, 40, 56, 72):
    d.line([ix0 + 10, iy0 + gy, ix0 + 198, iy0 + gy], fill=(220, 215, 200),
           width=1)
d.line([ix0 + 14, iy0 + 16, ix0 + 60, iy0 + 28, ix0 + 100, iy0 + 24,
        ix0 + 140, iy0 + 48, ix0 + 186, iy0 + 70], fill=RED, width=3)
d.ellipse([ix0 + 182, iy0 + 66, ix0 + 190, iy0 + 74], fill=RED)
d.text((ix0 + 216, iy0 + 10), "KOSPI", font=font(SANS_B, 16), fill=NAVY)
d.text((ix0 + 216, iy0 + 30), "-3.31%", font=font(SANS_B, 20), fill=RED)
d.text((ix0 + 216, iy0 + 54), "4,708.54", font=F["cap_b"], fill=INK)
d.rectangle([ix0 + 216, iy0 + 68, ix0 + 248, iy0 + 84], fill=NAVY)
d.rectangle([ix0 + 226, iy0 + 73, ix0 + 238, iy0 + 79], fill=(255, 255, 255))
d.text((x0 + 8, LY0 + 94), "3  ·  SEOUL, SOUTH KOREA  ·  MARKETS",
       font=F["lead_s"], fill=INK)
tag(d, x0 + LW - 64, LY0 + 93, "-3.31%", RED)
for j, ln in enumerate(wrap(d, "Kospi dives 3.31% as the AI-bubble rout spreads",
                            F["lead"], LW - 16)):
    d.text((x0 + 8, LY0 + 110 + j * 20), ln, font=F["lead"], fill=INK)
body3 = ("Seoul's index closed at 4,708.54, its lowest since 13 January, "
         "after falling 5.1% intraday; Seoul readies a ₩10tn stabilisation "
         "fund. It extends Friday's US rout; US futures bounced Monday. "
         "(Yonhap, CNBC)")
for j, ln in enumerate(wrap(d, body3, F["lead_b"], LW - 16)):
    d.text((x0 + 8, LY0 + 152 + j * 12), ln, font=F["lead_b"], fill=INK)

# ---------------------------------------------------------------- secondary cards 386-600
cards = [
    ("NHS launches world's largest AI breast-screening trial",
     "EDITH: ~700,000 women, 30 sites;", "AI reads one of two readers (BBC)", "trial"),
    ("Gaza a 'toxic wasteland', Oxfam report finds",
     "Contamination signs across >99%;", "61m+ tonnes of debris (Oxfam)", "toxic"),
    ("Belgium strike grounds almost all flights",
     "429 flights axed at Brussels;", "~59,500 passengers hit (airport)", "plane"),
    ("Candy-factory fire: 24 body bags found",
     "Forensic ID pending; 34 missing;", "fire broke out Saturday (AP)", "fire"),
    ("Nepal PM Shah lands in Delhi",
     "\u20b915,000-crore aid; 8 MoUs signed;", "new Ayodhya\u2013Janakpur train (ANI)", "flags"),
    ("China unveils 2030 eldercare plan",
     "Nursing beds 73% of care beds;", "as population shrinks (Reuters)", "elder"),
    ("Iran claims 78 US drones downed",
     "Tehran's tally alone since Feb;", "Pentagon unconfirmed \u2014 CLAIM", "drone"),
    ("Rubio meets Qatar PM on Iran",
     "Washington talks 19:00 UTC;", "Tehran restates its terms (State Dept)", "talks"),
    ("Iran says two tankers hit mines",
     "IRGC: mines east of Hormuz;", "claim unverified \u2014 CLAIM (Tasnim)", "mine"),
    ("New Zealand hang on to draw Test",
     "Mitchell 49* saves Wellington;", "India declared 720/9 (ESPNcricinfo)", "cricket"),
    ("Lowy Index: India holds third",
     "US 78.9, China 73.6, India 40.5;", "gap narrowest since 2018 (Lowy)", "chart"),
    ("Wall Street's worst week since 2020",
     "Nasdaq -5.28% Fri; S&P in correction;", "futures bounce Monday (CNBC)", "market"),
]
CW, CH, GAP = 163, 104, 6
for idx, (h, c1, c2, kind) in enumerate(cards):
    col, row = idx % 6, idx // 6
    x0 = 8 + col * (CW + GAP)
    y0 = 386 + row * (CH + GAP)
    d.rectangle([x0, y0, x0 + CW, y0 + CH], outline=INK, width=1)
    d.rectangle([x0, y0, x0 + CW, y0 + 50], fill=SKY)
    ix, iy = x0 + 8, y0 + 6
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
    elif kind == "market":
        d.line([ix + 8, iy + 10, ix + 50, iy + 16, ix + 90, iy + 12,
                ix + 130, iy + 38], fill=RED, width=3)
        d.line([ix + 8, iy + 30, ix + 50, iy + 26, ix + 90, iy + 30,
                ix + 130, iy + 20], fill=GREEN, width=2)
        d.text((ix + 8, iy + 40), "-5.28%", font=font(SANS_B, 10), fill=RED)
        d.text((ix + 96, iy + 40), "+1.9%", font=font(SANS_B, 10), fill=GREEN)
    d.text((x0 + 5, y0 + 51), f"{idx + 4:02d}", font=F["cap_b"], fill=RED)
    for j, ln in enumerate(wrap(d, h, F["card_h"], CW - 10)[:2]):
        d.text((x0 + 5, y0 + 61 + j * 11), ln, font=F["card_h"], fill=INK)
    d.text((x0 + 5, y0 + 85), c1, font=F["card_c"], fill=GREY)
    d.text((x0 + 5, y0 + 95), c2, font=F["card_c"], fill=GREY)

# ---------------------------------------------------------------- map + date check 602-790
MX0, MX1, MY0, MY1 = 8, 520, 602, 790
d.rectangle([MX0, MY0, MX1, MY1], outline=INK, width=2)
d.text((MX0 + 8, MY0 + 5), "WHERE IT HAPPENED", font=F["sect"], fill=INK)
d.text((MX1 - 150, MY0 + 7), "pins = story numbers", font=F["cap"], fill=GREY)
MAPX0, MAPY0, MAPW, MAPH = MX0 + 8, MY0 + 24, MX1 - MX0 - 16, 136
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

# pins: (num, lon, lat, label dx, dy)
PINS = [
    ("1", 30.7, 36.9, -34, 10),
    ("2", 30.5, 50.5, 8, -14),
    ("2", 20.1, 32.1, 8, 8),
    ("3", 127.0, 37.5, 8, -14),
    ("04", 0.1, 52.2, 8, -14),
    ("05", 34.5, 31.5, 8, 8),
    ("06", 4.4, 50.8, 8, -14),
    ("07", 106.5, -6.2, -40, 8),
    ("08", 77.2, 28.6, -34, -16),
    ("09", 116.4, 39.9, 8, -14),
    ("10", 51.4, 35.7, 8, 8),
    ("11", -77.4, 38.9, -30, 10),
    ("12", 56.5, 26.5, 8, 8),
    ("13", 174.8, -41.3, -36, -14),
    ("14", 149.1, -35.3, 8, -14),
    ("15", -74.0, 40.7, 8, -14),
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
d.text((MAPX0, MY0 + 164),
       "No pin: 16-30 (ALSO list). 2 also at Benghazi, Libya.",
       font=F["cap"], fill=GREY)

# DATE CHECK (right)
DX0, DX1, DY0, DY1 = 528, 1016, 602, 790
d.rectangle([DX0, DY0, DX1, DY1], outline=INK, width=2)
d.text((DX0 + 8, DY0 + 5), "DATE CHECK \u2014 WHAT COUNTS AS 23 NOVEMBER",
       font=F["sect"], fill=INK)
dc_rows = [
    (RED, "LEFT OUT \u2014 EARLIER EVENTS",
     "Democrats' 258th House seat (Sun) \u00b7 COP31 collapse itself (Sun) \u00b7 "
     "Verstappen GP (Sat) \u00b7 Chapo Isidro (Fri) \u00b7 Alcaraz title (Sun) \u00b7 "
     "Liverpool 4-0 Man Utd (Sun) \u00b7 Shenzhen summit (Thu) \u00b7 SAPS stats "
     "(Fri) \u00b7 Ebola 11,000 (mid-Nov) \u00b7 Ship seizure disclosed (Fri)"),
    (GREEN, "INCLUDED \u2014 MONDAY DEVELOPMENTS",
     "COP31 fallout \u00b7 Zelenskyy's Merkury announcement (Sun operation, "
     "Mon claim) \u00b7 Kyiv toll rises to 15 \u00b7 Kospi slide + Seoul fund \u00b7 "
     "NHS trial launch \u00b7 Belgium strike \u00b7 Hormuz mine claim first "
     "reported Mon (Tasnim) \u00b7 Bulgari funeral"),
    (AMBER, "NOT YET DECIDED",
     "US market close (futures up; close ~21:00 UTC) \u00b7 Rubio\u2013Qatar "
     "readout (19:00 UTC) \u00b7 Kyiv toll may still rise \u00b7 Belgium airspace "
     "reopens 20:00 UTC"),
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
d.text((DX0 + 8, DY1 - 16), "Sources checked through ~11:30 UTC, Mon 23 Nov 2026.",
       font=F["cap"], fill=GREY)

# ---------------------------------------------------------------- ALSO list 794-978
d.text((8, 796), "ALSO ON MONDAY 23 NOVEMBER \u2014 15 MORE STORIES",
       font=F["sect"], fill=INK)
d.line([8, 814, 1016, 814], fill=INK, width=1)
also = [
    "Bitcoin wobbles near $61,000; Hayes warns of $55k",
    "Paolo Bulgari funeral held in Rome (died Sat)",
    "Thanksgiving travel: Delta's Sunday meltdown + storm watch",
    "US intel chief defends Trump calling Putin 'friend'",
    "West Bank medics attacks up 350%, rights group says",
    "Syria\u2013EU talks progress; repatriation fears",
    "Taliban police protect Afghanistan's vanishing forests",
    "Meta's Alexandr Wang: superintelligence 'arriving'",
    "Trump to host a third crypto gala",
    "US envoy floats NATO-style guarantees for Ukraine",
    "Sudanese widowed mothers struggle amid war",
    "Europe's 'hot autumn' protests: economic symptom",
    "Riemann proof claim: Nature weighs in Monday",
    "Taiwan shares slip 0.93%; Japan shut for holiday",
    "France hopefuls both question Ukraine aid",
]
for i, item in enumerate(also):
    col, row = i % 3, i // 3
    x0 = 8 + col * 336
    y0 = 826 + row * 28
    d.text((x0, y0), f"{i + 16:02d}", font=F["list_b"], fill=RED)
    for j, ln in enumerate(wrap(d, item, F["list"], 306)[:2]):
        d.text((x0 + 26, y0 + j * 12), ln, font=F["list"], fill=INK)

# ---------------------------------------------------------------- footer 982-1024
d.line([8, 984, 1016, 984], fill=INK, width=2)
d.text((8, 990),
       "Sources: Reuters \u00b7 BBC \u00b7 AP \u00b7 AFP \u00b7 Al Jazeera \u00b7 ESPNcricinfo \u00b7 Lowy Institute \u00b7 Oxfam/CEOBS \u00b7 official statements",
       font=F["foot"], fill=GREY)
d.text((8, 1002),
       "30 stories checked against reporting available on 23 Nov 2026 to ~11:30 UTC. Scenes are drawn illustrations, not photographs.",
       font=F["foot"], fill=GREY)
r1 = "REPORTED = carried by the day's wires   CLAIM = one side's account, labelled"
d.text((1014 - d.textlength(r1, font=F["foot"]), 990), r1, font=F["foot"],
       fill=GREY)
r2 = "HORMUZ = IRGC said Sun, reported Mon (Tasnim)"
d.text((1014 - d.textlength(r2, font=F["foot"]), 1002), r2, font=F["foot"],
       fill=GREY)

img.save("entry.png", format="PNG")
print("saved entry.png")
