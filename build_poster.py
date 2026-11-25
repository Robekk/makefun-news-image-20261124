#!/usr/bin/env python3
"""Builds entry.png — 'The World in One Day', Tuesday 24 November 2026, v7.
Rebuilt after round 2 against the round's top entries: 36 stories (13
illustrated cards + 23 sourced one-liners), a numbers band, region tallies,
a Tuesday-in-UTC timeline and an expanded date-check box. Pure PIL,
deterministic."""
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
    elif kind == "pharma":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(228, 238, 244))
        d.rectangle([x + w * 0.14, y + h * 0.3, x + w * 0.4, y + h - 4], fill=(96, 130, 160))
        d.rectangle([x + w * 0.22, y + h * 0.14, x + w * 0.32, y + h * 0.3], fill=(96, 130, 160))
        d.rectangle([x + w * 0.24, y + h * 0.42, x + w * 0.3, y + h * 0.58], fill=(240, 244, 246))
        fx, fy = x + w * 0.66, y + h * 0.24
        d.polygon([(fx - 5, fy), (fx + 5, fy), (fx + 2, fy + h * 0.2), (fx + 9, fy + h * 0.52), (fx - 9, fy + h * 0.52), (fx - 2, fy + h * 0.2)], outline=(70, 90, 110), width=2)
        d.rectangle([fx - 8, fy + h * 0.38, fx + 8, fy + h * 0.5], fill=(90, 160, 200))
        d.ellipse([fx - 2, fy + h * 0.28, fx + 2, fy + h * 0.33], fill=(70, 90, 110))
    elif kind == "tanker":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(196, 220, 236))
        d.rectangle([x + w * 0.12, y + h * 0.52, x + w * 0.72, y + h * 0.66], fill=(52, 58, 66))
        d.polygon([(x + w * 0.72, y + h * 0.52), (x + w * 0.84, y + h * 0.66), (x + w * 0.72, y + h * 0.66)], fill=(52, 58, 66))
        d.rectangle([x + w * 0.2, y + h * 0.4, x + w * 0.62, y + h * 0.52], fill=(178, 60, 40))
        d.rectangle([x + w * 0.62, y + h * 0.3, x + w * 0.7, y + h * 0.52], fill=(230, 228, 220))
        for i in range(5):
            d.arc([x + 4 + i * w * 0.19, y + h * 0.74, x + 4 + (i + 0.7) * w * 0.19, y + h * 0.92], start=180, end=360, fill=(60, 110, 160), width=2)
        mx2, my2 = x + w * 0.86, y + h * 0.3
        d.ellipse([mx2 - 8, my2 - 8, mx2 + 8, my2 + 8], fill=(40, 40, 44))
        for a in range(0, 360, 45):
            import math
            d.line([(mx2, my2), (mx2 + 12 * math.cos(math.radians(a)), my2 + 12 * math.sin(math.radians(a)))], fill=(40, 40, 44), width=2)
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
    elif kind == "drone":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(214, 222, 232))
        for dx, dy in [(-24, -10), (24, -10), (-24, 12), (24, 12)]:
            d.line([(cx, cy), (cx + dx, cy + dy)], fill=(50, 54, 62), width=2)
            d.ellipse([cx + dx - 8, cy + dy - 3, cx + dx + 8, cy + dy + 3], outline=(50, 54, 62), width=2)
        d.rectangle([cx - 8, cy - 5, cx + 8, cy + 6], fill=(50, 54, 62))
        d.ellipse([cx - 2, cy + 4, cx + 3, cy + 8], fill=RED)
        for i in range(3):
            d.line([(x + 8 + i * 12, y + h - 6), (x + 16 + i * 12, y + h - 6)], fill=(140, 148, 158), width=2)
    elif kind == "oil":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(238, 230, 208))
        for fx, s in [(0.2, 0.8), (0.48, 1.0), (0.76, 0.66)]:
            bx, by = x + w * fx, y + h - 3
            d.line([(bx - 12 * s, by), (bx, by - h * 0.62 * s)], fill=(70, 66, 58), width=2)
            d.line([(bx + 12 * s, by), (bx, by - h * 0.62 * s)], fill=(70, 66, 58), width=2)
            d.line([(bx - 12 * s, by), (bx + 12 * s, by - h * 0.3 * s)], fill=(70, 66, 58), width=1)
            d.line([(bx + 12 * s, by), (bx - 12 * s, by - h * 0.3 * s)], fill=(70, 66, 58), width=1)
            d.line([(bx, by - h * 0.62 * s), (bx + 16 * s, by - h * 0.62 * s)], fill=(70, 66, 58), width=2)
        d.rectangle([x + 2, y + h - 4, x + w - 2, y + h - 2], fill=(120, 100, 70))
    elif kind == "ship":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(200, 224, 238))
        d.polygon([(x + w * 0.1, y + h * 0.58), (x + w * 0.86, y + h * 0.58), (x + w * 0.78, y + h * 0.78), (x + w * 0.2, y + h * 0.78)], fill=(44, 62, 84))
        for i, c in enumerate([(178, 60, 40), (52, 110, 70), (36, 110, 160)]):
            d.rectangle([x + w * (0.2 + i * 0.17), y + h * 0.42, x + w * (0.35 + i * 0.17), y + h * 0.58], fill=c)
        d.rectangle([x + w * 0.74, y + h * 0.3, x + w * 0.82, y + h * 0.58], fill=(230, 228, 220))
        for i in range(4):
            d.arc([x + 6 + i * w * 0.24, y + h * 0.82, x + 6 + (i + 0.7) * w * 0.24, y + h * 0.97], start=180, end=360, fill=(60, 110, 160), width=2)
    elif kind == "radar":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(26, 44, 40))
        for rx, ry in ((0.1, 0.18), (0.19, 0.33), (0.28, 0.48)):
            d.ellipse([cx - w * rx, cy - h * ry, cx + w * rx, cy + h * ry], outline=(70, 190, 130), width=1)
        d.line([(cx, cy), (cx + w * 0.24, cy - h * 0.4)], fill=(70, 190, 130), width=2)
        d.ellipse([cx + w * 0.13 - 2, cy - h * 0.2 - 2, cx + w * 0.13 + 2, cy - h * 0.2 + 2], fill=(240, 90, 80))
        d.line([(x + 4, cy), (x + w - 4, cy)], fill=(52, 120, 92), width=1)
        d.line([(cx, y + 4), (cx, y + h - 4)], fill=(52, 120, 92), width=1)
    elif kind == "candle":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(52, 46, 54))
        for i, fx in enumerate((0.3, 0.5, 0.7)):
            bx = x + w * fx
            d.rectangle([bx - 5, y + h * 0.52, bx + 5, y + h - 5], fill=(232, 228, 218))
            d.polygon([(bx, y + h * 0.2), (bx + 5, y + h * 0.4), (bx, y + h * 0.52), (bx - 5, y + h * 0.4)], fill=(246, 178, 60))
            d.ellipse([bx - 2, y + h * 0.36, bx + 2, y + h * 0.46], fill=(250, 230, 170))
    elif kind == "factory":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(224, 230, 236))
        d.rectangle([x + w * 0.12, y + h * 0.45, x + w * 0.62, y + h - 4], fill=(110, 118, 128))
        d.polygon([(x + w * 0.12, y + h * 0.45), (x + w * 0.3, y + h * 0.28), (x + w * 0.48, y + h * 0.45)], fill=(110, 118, 128))
        d.rectangle([x + w * 0.66, y + h * 0.2, x + w * 0.76, y + h - 4], fill=(96, 104, 114))
        d.ellipse([x + w * 0.65, y + h * 0.06, x + w * 0.78, y + h * 0.2], fill=(200, 200, 200))
        d.polygon([(x + w * 0.3, y + h * 0.4), (x + w * 0.38, y + h * 0.16), (x + w * 0.46, y + h * 0.4)], fill=(232, 120, 40))
    elif kind == "plane":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(208, 226, 240))
        d.ellipse([x + w * 0.08, y + h * 0.68, x + w * 0.34, y + h * 0.85], fill=(250, 250, 248))
        d.ellipse([x + w * 0.6, y + h * 0.7, x + w * 0.9, y + h * 0.87], fill=(250, 250, 248))
        d.polygon([(cx - 28, cy + 4), (cx + 16, cy - 2), (cx + 30, cy - 12), (cx + 30, cy + 2), (cx + 14, cy + 8), (cx - 20, cy + 12)], fill=(90, 100, 116))
        d.polygon([(cx - 28, cy + 4), (cx - 36, cy - 8), (cx - 30, cy + 10)], fill=(70, 80, 96))
    elif kind == "trophy":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(238, 232, 200))
        d.polygon([(cx - 14, y + h * 0.16), (cx + 14, y + h * 0.16), (cx + 10, y + h * 0.52), (cx - 10, y + h * 0.52)], fill=(216, 164, 40))
        d.arc([cx - 24, y + h * 0.18, cx - 8, y + h * 0.44], start=90, end=270, fill=(216, 164, 40), width=3)
        d.arc([cx + 8, y + h * 0.18, cx + 24, y + h * 0.44], start=270, end=90, fill=(216, 164, 40), width=3)
        d.rectangle([cx - 3, y + h * 0.52, cx + 3, y + h * 0.66], fill=(180, 132, 30))
        d.rectangle([cx - 12, y + h * 0.66, cx + 12, y + h * 0.76], fill=(120, 84, 40))
        d.polygon([(cx, y + h * 0.26), (cx + 3, y + h * 0.34), (cx + 8, y + h * 0.34), (cx + 4, y + h * 0.4), (cx + 6, y + h * 0.47), (cx, y + h * 0.43), (cx - 6, y + h * 0.47), (cx - 4, y + h * 0.4), (cx - 8, y + h * 0.34), (cx - 3, y + h * 0.34)], fill=(250, 240, 200))

# ---------------- masthead ----------------
d.text((MX, 8), "THE WORLD IN ONE DAY", font=F(SANS_B, 14), fill=RED)
r = "DAY 328 OF 2026 \u00b7 EVERY STORY DATED TUESDAY 24 NOV"
d.text((W - MX - d.textlength(r, font=F(SANS_B, 14)), 8), r, font=F(SANS_B, 14), fill=GREY)
d.line([(MX, 30), (W - MX, 30)], fill=INK, width=2)
t = "Tuesday 24 November 2026"
d.text(((W - d.textlength(t, font=F(SERIF_B, 50))) / 2, 34), t, font=F(SERIF_B, 50), fill=NAVY)
sub = "36 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE FROM THIS ONE DAY"
d.text(((W - d.textlength(sub, font=F(SANS_B, 13))) / 2, 92), sub, font=F(SANS_B, 13), fill=GREY)
tick = "Sanofi buys Insmed for $41 billion \u25c6 Baghdad takes over Kurdish-held oilfields \u25c6 Malaysia to send 6,500 Rohingya back"
d.text(((W - d.textlength(tick, font=F(SERIF_I, 15))) / 2, 110), tick, font=F(SERIF_I, 15), fill=RED)

# ---------------- numbers band ----------------
NY = 132
d.rectangle([MX, NY, W - MX, NY + 38], fill=NAVY)
stats = [("$41bn", "SANOFI\u2013INSMED DEAL"), ("699", "DRONES DOWNED"), ("47,000", "WOMEN KILLED BY KIN"),
         ("6,500+", "ROHINGYA TO RETURN"), ("26", "BANTEN FIRE TOLL"), ("+9.15%", "TAIEX RECORD JUMP")]
sw = CW / 6
for i, (num, lab) in enumerate(stats):
    sx = MX + i * sw
    d.text((sx + (sw - d.textlength(num, font=F(SANS_B, 19))) / 2, NY + 2), num, font=F(SANS_B, 19), fill=(250, 244, 230))
    d.text((sx + (sw - d.textlength(lab, font=F(SANS_B, 9))) / 2, NY + 25), lab, font=F(SANS_B, 9), fill=(178, 192, 214))

# ---------------- region chips + UTC timeline ----------------
RY = 176
chips = [("ASIA 12", (36, 110, 160)), ("EUROPE 7", (52, 110, 70)), ("OCEANIA 5", (190, 120, 30)),
         ("AMERICAS 5", (150, 60, 120)), ("MIDDLE EAST 3", (166, 28, 28)), ("AFRICA 2", (140, 95, 30)),
         ("GLOBAL 2", (96, 90, 80))]
cx = MX
for lab, col in chips:
    wch = d.textlength(lab, font=F(SANS_B, 11.5)) + 20
    d.rectangle([cx, RY, cx + wch, RY + 19], fill=col)
    d.text((cx + 10, RY + 3.5), lab, font=F(SANS_B, 11.5), fill=(250, 248, 240))
    cx += wch + 8
TY = 201
tl = "TUESDAY IN UTC   00:30 Kyiv talks call \u00b7 01:04 Korea ADIZ jets \u00b7 01:32 Nepal quake \u00b7 02:30 Villavicencio bomb \u00b7 06:36 Sanofi $41bn \u00b7 14:00 Chess Game 1"
d.text((MX, TY), tl, font=F(SANS, 10), fill=(52, 48, 42))
d.line([(MX, TY + 15), (W - MX, TY + 15)], fill=(178, 170, 154), width=1)

# ---------------- cards ----------------
def card(x, y, w, h, num, ill, dateline, headline, body, source, pill, big=False):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=(178, 170, 154), width=1)
    ih = 54 if big else 30
    illo(ill, x + 6, y + 6, w - 12, ih)
    d.ellipse([x + 10, y + 10, x + 28, y + 28], fill=RED)
    nt = str(num)
    d.text((x + 19 - d.textlength(nt, font=F(SANS_B, 12)) / 2, y + 12), nt, font=F(SANS_B, 12), fill=(255, 255, 255))
    cy = y + 6 + ih + 5
    d.text((x + 8, cy), dateline, font=F(SANS_B, 10.5 if big else 9.5), fill=RED)
    pw = d.textlength(pill, font=F(SANS_B, 8.5)) + 10
    d.rectangle([x + w - 8 - pw, cy - 1, x + w - 8, cy + 12], outline=GREY, width=1)
    d.text((x + w - 8 - pw + 5, cy + 1), pill, font=F(SANS_B, 8.5), fill=GREY)
    cy += 14
    cy = block(d, x + 8, cy, headline, F(SERIF_B, 17 if big else 12.5), w - 16, 20 if big else 15.5)
    cy += 2
    cy = block(d, x + 8, cy, body, F(SANS, 10.5 if big else 9.5), w - 16, 13.5 if big else 11.5, fill=(52, 48, 42))
    d.text((x + 8, y + h - 15), source, font=F(SERIF_I, 9.5), fill=GREY)
    return cy

# row 1 — three big cards
R1Y, R1H = 226, 182
CW3 = (CW - 20) // 3
card(MX, R1Y, CW3, R1H, 1, "chart", "SEOUL \u00b7 TOKYO \u00b7 TAIPEI \u2014 MARKETS",
     "Asia's chip stocks catch fire",
     "Seoul's Kospi leapt about 7% and Tokyo's Nikkei about 4% as chip shares surged, a day after Nvidia reinstated Jensen Huang as CEO. Taiwan's Taiex jumped 9.15% intraday \u2014 a record 3,368 points \u2014 as TSMC hit its daily limit.",
     "Reuters", "REPORTED", big=True)
card(MX + CW3 + 10, R1Y, CW3, R1H, 2, "pharma", "PARIS \u00b7 BUSINESS",
     "Sanofi buys Insmed for $41bn",
     "France's Sanofi agreed its biggest deal in years \u2014 $41bn in cash, $175 a share \u2014 for the US biotech Insmed and its lung-disease drugs.",
     "Sanofi \u00b7 PR Newswire", "ON RECORD", big=True)
card(MX + 2 * (CW3 + 10), R1Y, CW3, R1H, 3, "tanker", "STRAIT OF HORMUZ \u00b7 SHIPPING",
     "Iran: tankers hit its mines",
     "The Revolutionary Guards say two or three tankers caught fire after breaking the strait's rules. Brent crude held near $69; Washington has not confirmed the claim.",
     "IRNA via Reuters", "CLAIM", big=True)

# rows 2-3 — five small cards each
CW5 = (CW - 32) // 5
R2Y, RSH = 416, 144
row2 = [
    ("drone", "MOSCOW \u00b7 KYIV", "Russia says it downed 699 drones",
     "355 near the capital, Moscow says. A strike on Zaporizhzhia killed two, wounded 40; NATO sent an AWACS.", "Al Jazeera \u00b7 FMT", "REPORTED"),
    ("oil", "KIRKUK \u00b7 OIL", "Baghdad seizes Kurdish oilfields",
     "PM Ali al-Zaidi put four provinces under the federal Oil Ministry, taking the region's crossings and exports.", "Al Jazeera", "REPORTED"),
    ("ship", "KUALA LUMPUR", "Malaysia to send 6,500 Rohingya back",
     "Anwar told parliament 6,500+ will be returned to Myanmar: 1,500 by navy ship on 6\u20137 Dec, 5,303 by air.", "Al Jazeera", "ON RECORD"),
    ("gaza", "GAZA \u00b7 WAR", "Strikes kill seven in Gaza",
     "Three died near a Khan Younis outpost, medics said; a Gaza City strike killed Hamas chief Abu Nahel. Meningitis spreads.", "Reuters", "REPORTED"),
    ("radar", "ULLEUNG \u00b7 KOREA", "Russian jets send island to shelter",
     "Jets entered the air defence zone; Ulleung sheltered at 7:52 a.m., stood down 3 minutes later.", "Yonhap", "REPORTED"),
]
for i, c in enumerate(row2):
    card(MX + i * (CW5 + 8), R2Y, CW5, RSH, 4 + i, *c)
R3Y = R2Y + RSH + 8
row3 = [
    ("candle", "NEW YORK \u00b7 UN", "47,000 women killed by partners, kin",
     "Five women an hour die at the hands of partners or kin \u2014 47,000 a year. Africa is worst hit.", "UNODC \u00b7 UN Women", "ON RECORD"),
    ("factory", "CIKANDE", "Factory-fire toll rises to 26",
     "The toll from Saturday's candy-factory blaze rose again on Tuesday; eight are still missing.", "Xinhua \u00b7 AP", "REPORTED"),
    ("rocket", "JIUQUAN \u00b7 SPACE", "First foreigner to fly to China's station",
     "Crew: Tang Hongbo, Wu Yi and Pakistan's M. Zeeshan Ali, first foreigner aboard. Launch Wed.", "Xinhua \u00b7 CMSA", "ON RECORD"),
    ("plane", "DHAKA \u00b7 POLITICS", "Hasina says she will fly home 16 Dec",
     "The ousted PM, sentenced in absentia and exiled in India, announced a return; Dhaka: only by extradition.", "Reuters", "REPORTED"),
    ("trophy", "DAKAR \u00b7 FOOTBALL", "CAS restores Senegal as AFCON champions",
     "The Court of Arbitration for Sport unanimously reinstated Senegal as 2025 Africa Cup winners.", "CAS \u00b7 wires", "ON RECORD"),
]
for i, c in enumerate(row3):
    card(MX + i * (CW5 + 8), R3Y, CW5, RSH, 9 + i, *c)
print("cards end", R3Y + RSH)

# ---------------- also band: one-liners, three columns ----------------
AY = R3Y + RSH + 8
d.rectangle([MX, AY, W - MX, AY + 22], fill=INK)
d.text((MX + 10, AY + 4), "ALSO ON TUESDAY 24 NOVEMBER", font=F(SANS_B, 12.5), fill=BG)
leg = "HOW SURE: ON RECORD = official \u00b7 REPORTED = wires named \u00b7 CLAIM = one side says"
d.text((W - MX - 10 - d.textlength(leg, font=F(SANS_B, 9.5)), AY + 6), leg, font=F(SANS_B, 9.5), fill=(200, 194, 182))
liners = [
    (14, "KYIV \u2014 Zelensky: ready for four-way talks, \u201cliterally tomorrow\u201d (Ukrinform)."),
    (15, "TAPLEJUNG \u2014 M5.6 quake shakes eastern Nepal; no casualties (NEMRC)."),
    (16, "PORT MORESBY \u2014 Bougainville MPs vote on nationhood; 89 of 118 needed (Conversation)."),
    (17, "GENEVA \u2014 Chess title match opens: Sindarov v Gukesh, Game 1 (FIDE)."),
    (18, "BRUSSELS \u2014 EU caps Chinese hybrid-car imports at 350,000 a year (Reuters)."),
    (19, "HANOI \u2014 Restaurant gas blast kills six in Dong Da district (Reuters)."),
    (20, "SINGAPORE \u2014 Q3 GDP beats at +6.1%; 2026 outlook up to ~6% (Reuters)."),
    (21, "SINGAPORE \u2014 StarHub\u2013M1 agree S$5bn merger; four telcos to three (CNA)."),
    (22, "TOKYO \u2014 Factory PMI climbs to 53.7 on chip demand (S&P Global)."),
    (23, "CANBERRA \u2014 Tech giants face fines of 5% of global revenue (Reuters)."),
    (24, "MEXICO CITY \u2014 \u201cEl Chapo Isidro\u201d tried at home; US extradition refused (AG)."),
    (25, "HONIARA \u2014 Solomons ends China security pact; Australia deal next (Reuters)."),
    (26, "JAKARTA \u2014 Ex-police chief charged with treason (wires)."),
    (27, "WASHINGTON \u2014 Trump urges faster federal executions (wires)."),
    (28, "ROME \u2014 WFP: wars block food aid for 7.3m people (WFP)."),
    (29, "PARIS \u2014 Macron weighs a constitutional spending cap (wires)."),
    (30, "CANBERRA \u2014 Singapore\u2013Australia essential-supplies pact signed (wires)."),
    (31, "PHILADELPHIA \u2014 Avdija's 31 sinks the 76ers, 128\u2013111 (AP)."),
    (32, "VILLAVICENCIO \u2014 Car bomb hits governor's office; 23 hurt (AFP)."),
    (33, "WASHINGTON \u2014 US blacklists Megaspeed in Nvidia spy case (BIS)."),
    (34, "CAPE TOWN \u2014 Cities tighten water curbs as drought looms (wires)."),
    (35, "NEW YORK \u2014 UN: Gaza war wiped out 77 years of development (UNDP)."),
    (36, "GOLD COAST \u2014 England beat Australia, level T20 series (wires)."),
]
LW3 = (CW - 32) // 3
ly = AY + 30
rows = (len(liners) + 2) // 3
for col in range(3):
    yy = ly
    for r in range(rows):
        idx = r * 3 + col
        if idx >= len(liners):
            break
        n, txt = liners[idx]
        lx = MX + col * (LW3 + 16)
        d.ellipse([lx, yy + 1, lx + 15, yy + 16], fill=RED)
        nt = str(n)
        d.text((lx + 7.5 - d.textlength(nt, font=F(SANS_B, 9)) / 2, yy + 3), nt, font=F(SANS_B, 9), fill=(255, 255, 255))
        yy = block(d, lx + 20, yy, txt, F(SANS, 9), LW3 - 20, 11, fill=(52, 48, 42)) + 4
    print("col", col, "ends", yy)

# ---------------- date check ----------------
DY = 962
d.rectangle([MX, DY, W - MX, DY + 50], outline=RED, width=2)
d.rectangle([MX, DY, MX + 118, DY + 50], fill=RED)
d.text((MX + 10, DY + 7), "DATE", font=F(SANS_B, 15), fill=(255, 255, 255))
d.text((MX + 10, DY + 26), "CHECK", font=F(SANS_B, 15), fill=(255, 255, 255))
audit = ("Left out \u2014 they happened on an earlier day: Nvidia rehires Huang, Wall Street's rally (Mon 23) \u00b7 NATO space pledge, "
         "Sputnik-S reports (Mon 23) \u00b7 US sanctions on Iran shadow banking (Mon 23) \u00b7 COP31 collapses (Sun 22) \u00b7 Verstappen wins "
         "Las Vegas GP (Sun 22) \u00b7 the Banten fire itself (Sat 22) \u2014 only Tuesday's toll rise counts \u00b7 ICJ Rohingya ruling (19 Nov). "
         "Every story above happened, or was first reported, on Tuesday 24 November 2026 (UTC).")
block(d, MX + 130, DY + 5, audit, F(SANS, 9), CW - 142, 11.5, fill=(52, 48, 42))
print("footer at", DY + 50)

img.save("entry.png", optimize=True)
print("saved")
