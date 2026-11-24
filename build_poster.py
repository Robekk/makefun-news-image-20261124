#!/usr/bin/env python3
"""Builds entry.png — 'The World in One Day', Tuesday 24 November 2026.
Dense broadsheet: numbered, illustrated story cards + one-liners, a numbers
band, region tallies and a date-audit box. Pure PIL, deterministic."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (244, 239, 228)
INK = (24, 22, 18)
RED = (166, 28, 28)
NAVY = (24, 42, 74)
GREY = (96, 90, 80)
CARD = (252, 250, 244)
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, text, font, width, leading, fill=INK):
    for ln in wrap(d, text, font, width):
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
MX = 24
CW = W - 2 * MX  # 976

# ---------------- illustrations (tiny flat scenes) ----------------
def illo(kind, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=(150, 142, 126), width=1)
    cx, cy = x + w / 2, y + h / 2
    if kind == "chart":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(226, 240, 224))
        pts = [(x + 8, y + h - 10), (x + w * 0.35, y + h * 0.62), (x + w * 0.55, y + h * 0.7), (x + w * 0.8, y + h * 0.22)]
        d.line(pts, fill=(28, 128, 52), width=3)
        d.polygon([(x + w * 0.8, y + h * 0.22), (x + w * 0.8 - 12, y + h * 0.22 + 2), (x + w * 0.8 - 2, y + h * 0.22 + 12)], fill=(28, 128, 52))
        for i in range(4):
            d.line([(x + 8, y + h - 8 - i * (h - 16) / 3), (x + w - 8, y + h - 8 - i * (h - 16) / 3)], fill=(190, 205, 188), width=1)
    elif kind == "gaza":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(233, 226, 205))
        for bx, bw, bh in [(0.08, 0.16, 0.55), (0.3, 0.13, 0.42), (0.5, 0.18, 0.62), (0.74, 0.14, 0.48)]:
            d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h - 2], fill=(120, 112, 96))
        d.ellipse([x + w * 0.52, y + h * 0.08, x + w * 0.66, y + h * 0.3], fill=(150, 146, 138))
        d.ellipse([x + w * 0.58, y + h * 0.02, x + w * 0.74, y + h * 0.22], fill=(168, 164, 156))
    elif kind == "rocket":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(30, 44, 74))
        for sx, sy in [(0.15, 0.2), (0.7, 0.15), (0.85, 0.4), (0.3, 0.1), (0.55, 0.3)]:
            d.ellipse([x + w * sx, y + h * sy, x + w * sx + 3, y + h * sy + 3], fill=(240, 240, 230))
        d.polygon([(cx - 7, y + h * 0.62), (cx, y + h * 0.1), (cx + 7, y + h * 0.62)], fill=(235, 235, 230))
        d.rectangle([cx - 7, y + h * 0.62, cx + 7, y + h * 0.78], fill=(235, 235, 230))
        d.polygon([(cx - 7, y + h * 0.78), (cx, y + h * 0.97), (cx + 7, y + h * 0.78)], fill=(238, 130, 40))
        d.rectangle([x + w * 0.68, y + h * 0.3, x + w * 0.9, y + h * 0.38], fill=(200, 205, 215))
        d.line([(x + w * 0.79, y + h * 0.38), (x + w * 0.79, y + h * 0.55)], fill=(200, 205, 215), width=2)
    elif kind == "jet":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(206, 222, 236))
        d.line([(x + 6, y + h - 6), (x + w - 6, y + h - 6)], fill=(90, 130, 90), width=2)
        d.polygon([(cx - 26, cy + 2), (cx + 20, cy - 4), (cx + 30, cy + 2), (cx + 18, cy + 6), (cx - 14, cy + 8)], fill=(60, 66, 76))
        d.polygon([(cx - 26, cy + 2), (cx - 34, cy - 8), (cx - 28, cy + 8)], fill=(60, 66, 76))
        for i in range(3):
            d.arc([x + w - 44 - i * 3, y + 6 + i * 3, x + w - 14 + i * 3, y + 36 + i * 3], start=270, end=350, fill=RED, width=2)
    elif kind == "talks":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(238, 232, 214))
        cols = [(52, 90, 200), (240, 200, 40), (200, 40, 40), (240, 240, 240)]
        for i, c in enumerate(cols):
            fx = x + w * (0.14 + i * 0.22)
            d.line([(fx, y + 6), (fx, y + h - 8)], fill=(110, 100, 84), width=2)
            d.rectangle([fx, y + 6, fx + w * 0.15, y + 6 + h * 0.3], fill=c)
        d.rectangle([x + w * 0.1, y + h - 10, x + w * 0.9, y + h - 5], fill=(110, 84, 52))
    elif kind == "eu":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(36, 58, 128))
        import math
        for i in range(8):
            a = i * math.pi / 4
            sx, sy = cx + (w * 0.3) * math.cos(a) - 3, cy + (h * 0.32) * math.sin(a) - 3
            d.ellipse([sx, sy, sx + 6, sy + 6], fill=(246, 205, 60))
        d.line([(cx - w * 0.3, cy + h * 0.3), (cx + w * 0.3, cy - h * 0.3)], fill=RED, width=4)
    elif kind == "quake":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(228, 222, 204))
        d.polygon([(x + 4, y + h - 4), (x + w * 0.35, y + h * 0.2), (x + w * 0.55, y + h - 4)], fill=(140, 132, 114))
        d.polygon([(x + w * 0.45, y + h - 4), (x + w * 0.72, y + h * 0.3), (x + w - 4, y + h - 4)], fill=(120, 112, 94))
        pts = [(x + 6, cy), (x + w * 0.3, cy), (x + w * 0.42, cy - h * 0.28), (x + w * 0.54, cy + h * 0.28), (x + w * 0.66, cy), (x + w - 6, cy)]
        d.line(pts, fill=RED, width=2)
    elif kind == "nba":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(240, 226, 204))
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(224, 122, 44), outline=(120, 60, 20))
        d.arc([cx - 13, cy - 13, cx + 13, cy + 13], start=80, end=100, fill=(120, 60, 20), width=2)
        d.line([(cx - 13, cy), (cx + 13, cy)], fill=(120, 60, 20), width=1)
        d.rectangle([x + w - 34, y + 6, x + w - 8, y + 10], fill=(90, 90, 90))
        d.rectangle([x + w - 32, y + 10, x + w - 10, y + 20], outline=RED, width=2)
    elif kind == "factory":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(224, 230, 236))
        d.rectangle([x + w * 0.12, y + h * 0.45, x + w * 0.62, y + h - 4], fill=(110, 118, 128))
        d.polygon([(x + w * 0.12, y + h * 0.45), (x + w * 0.3, y + h * 0.28), (x + w * 0.48, y + h * 0.45)], fill=(110, 118, 128))
        d.rectangle([x + w * 0.66, y + h * 0.2, x + w * 0.76, y + h - 4], fill=(96, 104, 114))
        d.ellipse([x + w * 0.65, y + h * 0.06, x + w * 0.78, y + h * 0.2], fill=(200, 200, 200))
        d.polygon([(x + w * 0.8, y + h * 0.62), (x + w * 0.88, y + h * 0.34), (x + w * 0.96, y + h * 0.62)], fill=(28, 128, 52))
    elif kind == "skyline":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(214, 228, 240))
        for bx, bw, bh in [(0.08, 0.14, 0.5), (0.28, 0.16, 0.72), (0.5, 0.12, 0.58), (0.68, 0.18, 0.8)]:
            d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h - 2], fill=(70, 92, 118))
        d.text((x + w * 0.3, y + h * 0.3), "%", font=F(SANS_B, int(h * 0.5)), fill=RED)
    elif kind == "phones":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(232, 226, 240))
        d.rounded_rectangle([cx - 26, y + h * 0.18, cx - 4, y + h * 0.85], radius=4, fill=(70, 70, 120))
        d.rounded_rectangle([cx + 4, y + h * 0.18, cx + 26, y + h * 0.85], radius=4, fill=(150, 60, 90))
        d.polygon([(cx - 2, cy - 5), (cx + 8, cy), (cx - 2, cy + 5)], fill=INK)
    elif kind == "plane":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(208, 226, 240))
        d.ellipse([x + w * 0.08, y + h * 0.68, x + w * 0.34, y + h * 0.85], fill=(250, 250, 248))
        d.ellipse([x + w * 0.6, y + h * 0.7, x + w * 0.9, y + h * 0.87], fill=(250, 250, 248))
        d.polygon([(cx - 28, cy + 4), (cx + 16, cy - 2), (cx + 30, cy - 12), (cx + 30, cy + 2), (cx + 14, cy + 8), (cx - 20, cy + 12)], fill=(90, 100, 116))
        d.polygon([(cx - 28, cy + 4), (cx - 36, cy - 8), (cx - 30, cy + 10)], fill=(70, 80, 96))
    elif kind == "gavel":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(238, 230, 210))
        d.line([(cx - 16, cy - 12), (cx + 14, cy + 14)], fill=(120, 84, 40), width=5)
        d.rectangle([cx - 22, cy - 18, cx - 6, cy - 6], fill=(140, 100, 48))
        d.rectangle([cx + 8, cy + 8, cx + 24, cy + 20], fill=(140, 100, 48))
        d.rectangle([x + w * 0.2, y + h - 9, x + w * 0.8, y + h - 5], fill=(120, 84, 40))

# ---------------- masthead ----------------
d.text((MX, 8), "THE WORLD IN ONE DAY", font=F(SANS_B, 14), fill=RED)
r = "21 STORIES \u00b7 5 REGIONS \u00b7 ALL FROM THIS ONE DAY"
d.text((W - MX - d.textlength(r, font=F(SANS_B, 14)), 8), r, font=F(SANS_B, 14), fill=GREY)
d.line([(MX, 30), (W - MX, 30)], fill=INK, width=2)
t = "Tuesday 24 November 2026"
d.text(((W - d.textlength(t, font=F(SERIF_B, 66))) / 2, 34), t, font=F(SERIF_B, 66), fill=NAVY)
sub = "Asia markets roar as Huang returns to Nvidia \u00b7 Israeli strike kills three in Khan Younis \u00b7 China names the first foreign astronaut for its station"
d.text(((W - d.textlength(sub, font=F(SERIF_I, 16.5))) / 2, 110), sub, font=F(SERIF_I, 16.5), fill=RED)

# ---------------- numbers band ----------------
NY = 136
d.rectangle([MX, NY, W - MX, NY + 40], fill=NAVY)
stats = [("+9.1%", "TAIEX RECORD DAY"), ("53.7", "JAPAN FACTORY PMI"), ("+6.1%", "SINGAPORE Q3 GDP"),
         ("103.1", "KOREA SENTIMENT"), ("S$5bn", "STARHUB\u2013M1 MERGER"), ("128\u2013111", "BLAZERS BEAT 76ERS")]
sw = CW / 6
for i, (num, lab) in enumerate(stats):
    sx = MX + i * sw
    d.text((sx + (sw - d.textlength(num, font=F(SANS_B, 20))) / 2, NY + 2), num, font=F(SANS_B, 20), fill=(250, 244, 230))
    d.text((sx + (sw - d.textlength(lab, font=F(SANS_B, 9.5))) / 2, NY + 26), lab, font=F(SANS_B, 9.5), fill=(178, 192, 214))

# ---------------- region chips ----------------
RY = 182
chips = [("ASIA 13", (36, 110, 160)), ("AMERICAS 3", (150, 60, 120)), ("EUROPE 2", (52, 110, 70)),
         ("OCEANIA 2", (190, 120, 30)), ("MIDDLE EAST 1", (166, 28, 28))]
cx = MX
for lab, col in chips:
    wch = d.textlength(lab, font=F(SANS_B, 12)) + 22
    d.rectangle([cx, RY, cx + wch, RY + 20], fill=col)
    d.text((cx + 11, RY + 4), lab, font=F(SANS_B, 12), fill=(250, 248, 240))
    cx += wch + 10
note = "Every story dated Tue 24 Nov 2026 in some time zone"
d.text((W - MX - d.textlength(note, font=F(SERIF_I, 12)), RY + 3), note, font=F(SERIF_I, 12), fill=GREY)

# ---------------- cards ----------------
def card(x, y, w, h, num, ill, dateline, headline, body, source, pill, big=False):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=(178, 170, 154), width=1)
    ih = 56 if big else 33
    illo(ill, x + 6, y + 6, w - 12, ih)
    d.ellipse([x + 10, y + 10, x + 28, y + 28], fill=RED)
    nt = str(num)
    d.text((x + 19 - d.textlength(nt, font=F(SANS_B, 12)) / 2, y + 12), nt, font=F(SANS_B, 12), fill=(255, 255, 255))
    cy = y + 6 + ih + (5 if big else 4)
    d.text((x + 8, cy), dateline, font=F(SANS_B, 9.5 if not big else 10.5), fill=RED)
    pw = d.textlength(pill, font=F(SANS_B, 8.5)) + 10
    d.rectangle([x + w - 8 - pw, cy - 1, x + w - 8, cy + 12], outline=GREY, width=1)
    d.text((x + w - 8 - pw + 5, cy + 1), pill, font=F(SANS_B, 8.5), fill=GREY)
    cy += 14 if big else 13
    cy = block(d, x + 8, cy, headline, F(SERIF_B, 18 if big else 13.5), w - 16, 21 if big else 16.5)
    cy += 2
    cy = block(d, x + 8, cy, body, F(SANS, 11 if big else 10), w - 16, 14 if big else 12.5, fill=(52, 48, 42))
    if big:
        d.text((x + 8, y + h - 15), source, font=F(SERIF_I, 9.5), fill=GREY)
    else:
        d.text((x + 8, cy + 2), source, font=F(SERIF_I, 9.5), fill=GREY)
    return cy

# row 1 — three big cards
R1Y, R1H = 210, 190
CW3 = (CW - 20) // 3
card(MX, R1Y, CW3, R1H, 1, "chart", "HONG KONG \u00b7 MARKETS",
     "Huang's return sets Asia alight",
     "Nvidia reinstated Jensen Huang as CEO; Wall Street leapt and Asia followed \u2014 MSCI Asia-Pacific +4.6%, Seoul's Kospi +7.5%, Tokyo's Nikkei +4.5%.",
     "Reuters", "REPORTED", big=True)
card(MX + CW3 + 10, R1Y, CW3, R1H, 2, "gaza", "KHAN YOUNIS, GAZA \u00b7 WAR",
     "Israeli strike kills three in Gaza",
     "An airstrike killed at least three Palestinians near a police outpost in Khan Younis on Tuesday and wounded five others, local medics said.",
     "Reuters", "REPORTED", big=True)
card(MX + 2 * (CW3 + 10), R1Y, CW3, R1H, 3, "rocket", "JIUQUAN, CHINA \u00b7 SPACE",
     "First foreigner to fly to China's station",
     "China named the Shenzhou-24 crew: Tang Hongbo, Wu Yi and Pakistan's Muhammad Zeeshan Ali \u2014 first foreigner to visit Tiangong. Launch: Wednesday.",
     "Xinhua \u00b7 CMSA", "ON RECORD", big=True)

# rows 2-3 — five small cards each
CW5 = (CW - 32) // 5
R2Y, RSH = 408, 146
row2 = [
    ("jet", "ULLEUNG, S. KOREA", "Seoul scrambles jets at Russian planes",
     "Russian jets entered the air defence zone; islanders sheltered for 3 minutes.", "Yonhap", "REPORTED"),
    ("talks", "BERLIN", "Zelensky: ready for four-way talks",
     "Kyiv ready to meet Russia, the US and Europe at once \u2014 \u201cliterally tomorrow\u201d.", "AFP \u00b7 Ukrinform", "ON RECORD"),
    ("eu", "BRUSSELS", "EU proposes 22nd Russia sanctions",
     "Some 60 banks off SWIFT, 70 more shadow-fleet ships, a visa ban for ex-combatants.", "Reuters", "ON RECORD"),
    ("quake", "KOSHI, NEPAL", "M5.3 quake on the Nepal\u2013China border",
     "The 07:02 tremor was felt in India, Bhutan and Bangladesh. No casualties reported.", "USGS \u00b7 EMSC", "REPORTED"),
    ("nba", "PHILADELPHIA", "Avdija's 31 sinks the 76ers",
     "Portland hit 19 threes to win 128-111 and end the Sixers' five-game streak.", "AP", "REPORTED"),
]
for i, c in enumerate(row2):
    card(MX + i * (CW5 + 8), R2Y, CW5, RSH, 4 + i, *c)
R3Y = R2Y + RSH + 8
row3 = [
    ("factory", "TOKYO", "Japan factory PMI climbs to 53.7",
     "Chip demand lifts factories; services cool to 50.5, the composite a six-month low.", "S&P Global via Reuters", "ON RECORD"),
    ("skyline", "SINGAPORE", "Singapore GDP beats at 6.1%",
     "Q3 growth topped forecasts on AI demand; the 2026 outlook was raised to about 6%.", "Reuters", "ON RECORD"),
    ("phones", "SINGAPORE", "StarHub and M1 agree S$5bn merger",
     "The all-share deal cuts mobile operators from four to three; completion due H1 2027.", "CNA", "REPORTED"),
    ("plane", "DHAKA", "Hasina seeks a Dec 16 return",
     "The ousted PM, exiled in India, asks Dhaka to lay on a state-carrier flight home.", "Reuters", "REPORTED"),
    ("gavel", "CANBERRA", "Tech giants face 5% fines",
     "Platforms face fines of up to 5% of global revenue under a new safety bill.", "Reuters", "ON RECORD"),
]
for i, c in enumerate(row3):
    card(MX + i * (CW5 + 8), R3Y, CW5, RSH, 9 + i, *c)
print("cards end", R3Y + RSH)

# ---------------- also band: one-liners ----------------
AY = R3Y + RSH + 8
d.rectangle([MX, AY, W - MX, AY + 24], fill=INK)
d.text((MX + 10, AY + 5), "ALSO ON TUESDAY 24 NOVEMBER", font=F(SANS_B, 13), fill=BG)
liners = [
    (14, "SEOUL", "Consumer sentiment slips to 103.1, a seven-month low (Bank of Korea)."),
    (15, "SEOUL COURT", "Arrest warrant for an election official over forged June vote counts."),
    (16, "CANBERRA", "Singapore\u2013Australia: essential-supplies pact and a first CO2 storage treaty."),
    (17, "HONG KONG", "Wang Fuk Court fund: HK$300,000 per flat owner, HK$200,000 per life lost."),
    (18, "WELLINGTON", "RNZ's HR chief quits amid an NZ$11.8m deficit \u2014 third exec exit in two months."),
    (19, "TORONTO", "Leafs snap a nine-game skid, rallying from 2-0 down on Long Island."),
    (20, "BRIDGETOWN", "UN and Barbados call for talks on a global AI risk framework in a year."),
    (21, "TAIPEI", "Taiex leaps 9.15% intraday \u2014 a record 3,368 points \u2014 as TSMC hits its limit."),
]
LW2 = (CW - 16) // 2
ly = AY + 32
for r in range(4):
    row_end = ly
    for c in range(2):
        n, lab, txt = liners[r * 2 + c]
        lx = MX + c * (LW2 + 16)
        d.ellipse([lx, ly + 1, lx + 17, ly + 18], fill=RED)
        nt = str(n)
        d.text((lx + 8.5 - d.textlength(nt, font=F(SANS_B, 10)) / 2, ly + 3), nt, font=F(SANS_B, 10), fill=(255, 255, 255))
        tx = lx + 24
        d.text((tx, ly), lab, font=F(SANS_B, 11.5), fill=RED)
        row_end = max(row_end, block(d, tx, ly + 14, txt, F(SANS, 11), LW2 - 24, 14.5, fill=(52, 48, 42)))
    ly = row_end + 6
print("liners end", ly)

# ---------------- date audit + legend ----------------
DY = ly + 4
d.rectangle([MX, DY, W - MX, DY + 50], outline=RED, width=2)
d.rectangle([MX, DY, MX + 118, DY + 50], fill=RED)
d.text((MX + 10, DY + 7), "DATES", font=F(SANS_B, 15), fill=(255, 255, 255))
d.text((MX + 10, DY + 26), "AUDITED", font=F(SANS_B, 15), fill=(255, 255, 255))
audit = ("Left out \u2014 they happened on an earlier day: the Benghazi strike on Russia's Merkury (Sun 22 Nov) \u00b7 COP31's close "
         "(22 Nov) \u00b7 Senegal migrant boat (19 Nov) \u00b7 NATO's Starlift launch (17 Nov) \u00b7 \u2018El Chapo Isidro\u2019 capture (20\u201321 Nov) "
         "\u00b7 ICJ Rohingya ruling (19 Nov). Every story above happened, or was first reported, on Mon 23 \u2013 Tue 24 Nov.")
block(d, MX + 130, DY + 6, audit, F(SANS, 11), CW - 142, 14, fill=(52, 48, 42))
fy = DY + 58
d.text((MX, fy), "HOW SURE:  ON RECORD = official statement or release  \u00b7  REPORTED = carried by the wires named  \u00b7  Pictures drawn for this page, not photographs.",
       font=F(SANS_B, 10.5), fill=GREY)
print("footer at", fy)

img.save("entry.png", optimize=True)
print("saved")
