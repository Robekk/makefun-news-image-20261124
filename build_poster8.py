#!/usr/bin/env python3
"""Builds entry.png — 'The World in One Day', Tuesday 24 November 2026, v8.
Layout copied from the round-2 runner-up (full-colour illustrated cards,
red-number caps headlines, tag + source lines); bottom block copied from
the round's #4 (world map with pins beside the ALSO list). Three colour
zones — Asia-Pacific / Europe-Africa-Middle East / Americas — run through
the zone bar, the card numbers, the map pins and the ALSO chips so the
whole page syncs. 38 stories. Pure PIL, deterministic."""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
BG = (246, 241, 230)
INK = (26, 24, 20)
RED = (166, 28, 28)
NAVY = (22, 38, 72)
GREY = (96, 90, 80)
ZA = (172, 32, 36)      # Asia-Pacific
ZB = (0, 108, 102)      # Europe · Africa · Middle East
ZC = (105, 55, 145)     # Americas
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


def wrap2(d, text, font, w_first, w_rest):
    words, lines, cur = text.split(), [], ""
    width = w_first
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
            width = w_rest
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

# ---------------- illustrations (tiny flat scenes, full-bleed) ----------------
def illo(kind, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=(150, 142, 126), width=1)
    cx, cy = x + w / 2, y + h / 2
    if kind == "chart":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(224, 240, 222))
        pts = [(x + 8, y + h - 10), (x + w * 0.35, y + h * 0.62), (x + w * 0.55, y + h * 0.7), (x + w * 0.8, y + h * 0.22)]
        d.line(pts, fill=(28, 128, 52), width=3)
        d.polygon([(x + w * 0.8, y + h * 0.22), (x + w * 0.8 - 12, y + h * 0.22 + 2), (x + w * 0.8 - 2, y + h * 0.22 + 12)], fill=(28, 128, 52))
        for i in range(4):
            d.line([(x + 8, y + h - 8 - i * (h - 16) / 3), (x + w - 8, y + h - 8 - i * (h - 16) / 3)], fill=(190, 205, 188), width=1)
    elif kind == "pharma":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(226, 238, 244))
        d.rectangle([x + w * 0.12, y + h * 0.3, x + w * 0.36, y + h - 3], fill=(96, 130, 160))
        d.rectangle([x + w * 0.2, y + h * 0.14, x + w * 0.28, y + h * 0.3], fill=(96, 130, 160))
        d.rectangle([x + w * 0.21, y + h * 0.42, x + w * 0.27, y + h * 0.58], fill=(240, 244, 246))
        fx, fy = x + w * 0.62, y + h * 0.2
        d.polygon([(fx - 6, fy), (fx + 6, fy), (fx + 2, fy + h * 0.22), (fx + 11, fy + h * 0.58), (fx - 11, fy + h * 0.58), (fx - 2, fy + h * 0.22)], outline=(70, 90, 110), width=2)
        d.rectangle([fx - 10, fy + h * 0.42, fx + 10, fy + h * 0.56], fill=(90, 160, 200))
        d.rectangle([x + w * 0.8, y + h * 0.34, x + w * 0.94, y + h * 0.48], fill=(250, 250, 248), outline=(150, 60, 60), width=1)
        d.rectangle([x + w * 0.855, y + h * 0.36, x + w * 0.885, y + h * 0.46], fill=(200, 50, 50))
        d.rectangle([x + w * 0.815, y + h * 0.395, x + w * 0.925, y + h * 0.425], fill=(200, 50, 50))
    elif kind == "tanker":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(190, 218, 236))
        d.rectangle([x + w * 0.1, y + h * 0.52, x + w * 0.7, y + h * 0.68], fill=(52, 58, 66))
        d.polygon([(x + w * 0.7, y + h * 0.52), (x + w * 0.83, y + h * 0.68), (x + w * 0.7, y + h * 0.68)], fill=(52, 58, 66))
        d.rectangle([x + w * 0.18, y + h * 0.38, x + w * 0.6, y + h * 0.52], fill=(178, 60, 40))
        d.rectangle([x + w * 0.6, y + h * 0.26, x + w * 0.68, y + h * 0.52], fill=(230, 228, 220))
        d.polygon([(x + w * 0.24, y + h * 0.38), (x + w * 0.3, y + h * 0.14), (x + w * 0.36, y + h * 0.38)], fill=(240, 130, 40))
        for i in range(5):
            d.arc([x + 4 + i * w * 0.19, y + h * 0.76, x + 4 + (i + 0.7) * w * 0.19, y + h * 0.94], start=180, end=360, fill=(60, 110, 160), width=2)
        mx2, my2 = x + w * 0.88, y + h * 0.3
        d.ellipse([mx2 - 8, my2 - 8, mx2 + 8, my2 + 8], fill=(40, 40, 44))
        for a in range(0, 360, 45):
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
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(210, 220, 232))
        for dx, dy in [(-26, -10), (26, -10), (-26, 12), (26, 12)]:
            d.line([(cx, cy), (cx + dx, cy + dy)], fill=(50, 54, 62), width=2)
            d.ellipse([cx + dx - 9, cy + dy - 3, cx + dx + 9, cy + dy + 3], outline=(50, 54, 62), width=2)
        d.rectangle([cx - 9, cy - 5, cx + 9, cy + 6], fill=(50, 54, 62))
        d.ellipse([cx - 2, cy + 4, cx + 3, cy + 8], fill=RED)
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
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(198, 224, 238))
        d.polygon([(x + w * 0.1, y + h * 0.58), (x + w * 0.86, y + h * 0.58), (x + w * 0.78, y + h * 0.78), (x + w * 0.2, y + h * 0.78)], fill=(44, 62, 84))
        for i, c in enumerate([(178, 60, 40), (52, 110, 70), (36, 110, 160)]):
            d.rectangle([x + w * (0.2 + i * 0.17), y + h * 0.42, x + w * (0.35 + i * 0.17), y + h * 0.58], fill=c)
        d.rectangle([x + w * 0.74, y + h * 0.3, x + w * 0.82, y + h * 0.58], fill=(230, 228, 220))
        for i in range(4):
            d.arc([x + 6 + i * w * 0.24, y + h * 0.82, x + 6 + (i + 0.7) * w * 0.24, y + h * 0.97], start=180, end=360, fill=(60, 110, 160), width=2)
    elif kind == "radar":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(26, 44, 40))
        for rx, ry in ((0.1, 0.2), (0.19, 0.36), (0.28, 0.52)):
            d.ellipse([cx - w * rx, cy - h * ry, cx + w * rx, cy + h * ry], outline=(70, 190, 130), width=1)
        d.line([(cx, cy), (cx + w * 0.24, cy - h * 0.42)], fill=(70, 190, 130), width=2)
        d.ellipse([cx + w * 0.13 - 2, cy - h * 0.22 - 2, cx + w * 0.13 + 2, cy - h * 0.22 + 2], fill=(240, 90, 80))
        d.line([(x + 4, cy), (x + w - 4, cy)], fill=(52, 120, 92), width=1)
        d.line([(cx, y + 4), (cx, y + h - 4)], fill=(52, 120, 92), width=1)
    elif kind == "candle":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(52, 46, 54))
        for fx in (0.3, 0.5, 0.7):
            bx = x + w * fx
            d.rectangle([bx - 5, y + h * 0.52, bx + 5, y + h - 4], fill=(232, 228, 218))
            d.polygon([(bx, y + h * 0.18), (bx + 5, y + h * 0.4), (bx, y + h * 0.52), (bx - 5, y + h * 0.4)], fill=(246, 178, 60))
            d.ellipse([bx - 2, y + h * 0.34, bx + 2, y + h * 0.45], fill=(250, 230, 170))
    elif kind == "factory":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(224, 230, 236))
        d.rectangle([x + w * 0.12, y + h * 0.45, x + w * 0.62, y + h - 4], fill=(110, 118, 128))
        d.polygon([(x + w * 0.12, y + h * 0.45), (x + w * 0.3, y + h * 0.28), (x + w * 0.48, y + h * 0.45)], fill=(110, 118, 128))
        d.rectangle([x + w * 0.66, y + h * 0.2, x + w * 0.76, y + h - 4], fill=(96, 104, 114))
        d.ellipse([x + w * 0.65, y + h * 0.06, x + w * 0.78, y + h * 0.2], fill=(200, 200, 200))
        d.polygon([(x + w * 0.3, y + h * 0.4), (x + w * 0.38, y + h * 0.16), (x + w * 0.46, y + h * 0.4)], fill=(232, 120, 40))
    elif kind == "gavel":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(238, 230, 210))
        d.line([(cx - 18, cy - 12), (cx + 16, cy + 14)], fill=(120, 84, 40), width=5)
        d.rectangle([cx - 26, cy - 19, cx - 8, cy - 6], fill=(140, 100, 48))
        d.rectangle([cx + 10, cy + 7, cx + 28, cy + 20], fill=(140, 100, 48))
        d.rectangle([x + w * 0.18, y + h - 9, x + w * 0.82, y + h - 5], fill=(120, 84, 40))
    elif kind == "bomb":
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(226, 220, 206))
        d.rectangle([x + w * 0.14, y + h * 0.34, x + w * 0.5, y + h - 3], fill=(128, 120, 106))
        d.rectangle([x + w * 0.56, y + h * 0.5, x + w * 0.78, y + h - 3], fill=(142, 134, 118))
        bx, by = x + w * 0.52, y + h * 0.3
        pts = []
        for i in range(12):
            a = i * math.pi / 6
            r = (w * 0.13) if i % 2 == 0 else (w * 0.06)
            pts.append((bx + r * math.cos(a), by + r * math.sin(a) * 0.8))
        d.polygon(pts, fill=(238, 130, 40))
        d.ellipse([bx - 6, by - 5, bx + 6, by + 5], fill=(250, 210, 90))
        d.ellipse([x + w * 0.6, y + h * 0.06, x + w * 0.76, y + h * 0.24], fill=(168, 164, 156))

# ---------------- masthead ----------------
d.text((MX, 8), "THE WORLD IN ONE DAY", font=F(SANS_B, 15), fill=RED)
r = "EVERY STORY DATED TUESDAY 24 NOV"
d.text((W - MX - d.textlength(r, font=F(SANS_B, 13)), 9), r, font=F(SANS_B, 13), fill=GREY)
d.line([(MX, 30), (W - MX, 30)], fill=INK, width=2)
t = "Tuesday 24 November 2026"
d.text(((W - d.textlength(t, font=F(SERIF_B, 54))) / 2, 34), t, font=F(SERIF_B, 54), fill=NAVY)
sub = "38 STORIES \u00b7 3 COLOUR ZONES \u00b7 EVERY ONE FROM THIS ONE DAY"
d.text(((W - d.textlength(sub, font=F(SANS_B, 13))) / 2, 98), sub, font=F(SANS_B, 13), fill=GREY)

# ---------------- zone bar (the 3 colours) ----------------
ZY = 118
zones = [("ASIA-PACIFIC 16", ZA, 16), ("EUROPE \u00b7 AFRICA \u00b7 MIDDLE EAST 12", ZB, 12), ("AMERICAS 10", ZC, 10)]
zx = MX
for lab, col, n in zones:
    zw = CW * n / 38
    d.rectangle([zx, ZY, zx + zw - 3, ZY + 20], fill=col)
    d.text((zx + (zw - 3 - d.textlength(lab, font=F(SANS_B, 11.5))) / 2, ZY + 4), lab, font=F(SANS_B, 11.5), fill=(252, 250, 244))
    zx += zw

# ---------------- UTC timeline ----------------
TY = 146
tx = MX
d.text((tx, TY), "TUESDAY IN UTC", font=F(SANS_B, 10.5), fill=RED)
tx += d.textlength("TUESDAY IN UTC", font=F(SANS_B, 10.5)) + 12
segs = [("00:30", "Kyiv talks"), ("01:04", "Korea ADIZ"), ("01:32", "Nepal quake"),
        ("02:30", "Villavicencio"), ("06:36", "Sanofi $41bn"), ("07:52", "Ulleung alert"), ("14:00", "Chess G1")]
for i, (tm, lab) in enumerate(segs):
    d.text((tx, TY), tm, font=F(SANS_B, 10.5), fill=INK)
    tx += d.textlength(tm, font=F(SANS_B, 10.5)) + 4
    d.text((tx, TY), lab, font=F(SANS, 10.5), fill=(52, 48, 42))
    tx += d.textlength(lab, font=F(SANS, 10.5)) + (10 if i < len(segs) - 1 else 0)
    if i < len(segs) - 1:
        d.text((tx, TY), "\u00b7", font=F(SANS, 10.5), fill=GREY)
        tx += 8

# ---------------- numbers band ----------------
NY = 166
d.line([(MX, NY), (W - MX, NY)], fill=INK, width=1)
stats = [("$41bn", "SANOFI\u2013INSMED DEAL"), ("699", "DRONES DOWNED"), ("47,000", "WOMEN KILLED BY KIN"),
         ("6,500+", "ROHINGYA TO RETURN"), ("26", "BANTEN FIRE TOLL"), ("23", "HURT IN VILLAVICENCIO")]
sw = CW / 6
for i, (num, lab) in enumerate(stats):
    sx = MX + i * sw
    d.text((sx + (sw - d.textlength(num, font=F(SANS_B, 21))) / 2, NY + 5), num, font=F(SANS_B, 21), fill=INK)
    d.text((sx + (sw - d.textlength(lab, font=F(SANS_B, 8.5))) / 2, NY + 31), lab, font=F(SANS_B, 8.5), fill=GREY)
d.line([(MX, NY + 44), (W - MX, NY + 44)], fill=INK, width=1)

# ---------------- cards (top-2 style) ----------------
def card2(x, y, w, num, zone, ill, headline, dek, tag, source, big=False):
    ih = 76 if big else 52
    illo(ill, x, y, w, ih)
    ty = y + ih + 5
    nf = F(SANS_B, 14 if big else 12)
    nt = str(num) + "."
    d.text((x, ty), nt, font=nf, fill=zone)
    nw = d.textlength(nt, font=nf) + 4
    hf = F(SANS_B, 15.5 if big else 11.5)
    lines = wrap2(d, headline, hf, w - nw, w)
    for i, ln in enumerate(lines):
        d.text((x + (nw if i == 0 else 0), ty), ln, font=hf, fill=INK)
        ty += 19 if big else 15
    ty += 1
    ty = block(d, x, ty, dek, F(SANS, 10 if big else 9), w, 13 if big else 11.5, fill=(52, 48, 42))
    ty += 3
    tc = RED if tag == "CLAIM" else INK
    d.text((x, ty), tag, font=F(SANS_B, 8.5), fill=tc)
    tw = d.textlength(tag, font=F(SANS_B, 8.5))
    d.text((x + tw + 4, ty), "\u2014 " + source, font=F(SANS, 8.5), fill=GREY)
    return ty

CW3 = (CW - 20) // 3
R1Y = 222
card2(MX, R1Y, CW3, 1, ZA, "chart", "ASIA'S CHIP STOCKS SURGE",
      "Kospi leapt about 7% and the Nikkei about 4% as chip shares caught fire; Taiwan's Taiex jumped 9.15% intraday \u2014 a record 3,368 points \u2014 as TSMC hit its daily limit.",
      "CONFIRMED", "Reuters \u00b7 CNBC", big=True)
card2(MX + CW3 + 10, R1Y, CW3, 2, ZB, "pharma", "SANOFI BUYS INSMED FOR $41 BILLION",
      "France's Sanofi agreed its biggest deal in years \u2014 $41bn in cash, $175 a share \u2014 for the US biotech Insmed and its lung-disease drugs.",
      "OFFICIAL", "Sanofi \u00b7 PR Newswire", big=True)
card2(MX + 2 * (CW3 + 10), R1Y, CW3, 3, ZB, "tanker", "IRAN CLAIMS TANKERS HIT MINES IN HORMUZ",
      "The Revolutionary Guards say two or three tankers caught fire after breaking the strait's rules; Washington has not confirmed. Brent held near $69.",
      "CLAIM", "IRNA via Reuters", big=True)

CW5 = (CW - 32) // 5
R2Y = 418
row2 = [
    (4, ZB, "drone", "RUSSIA SAYS IT DOWNED 699 DRONES",
     "355 near the capital, Moscow says; a strike on Zaporizhzhia killed two and wounded 40. NATO sent an AWACS after a drone crossed into Poland.", "CONFIRMED", "Al Jazeera \u00b7 FMT"),
    (5, ZB, "oil", "BAGHDAD SEIZES KURDISH-HELD OILFIELDS",
     "PM Ali al-Zaidi put four provinces under the federal Oil Ministry, taking the region's border crossings and oil exports.", "REPORTED", "Al Jazeera"),
    (6, ZA, "ship", "MALAYSIA TO RETURN 6,500 ROHINGYA",
     "Anwar told parliament 6,500+ will go back to Myanmar: 1,500 by navy ship on 6\u20137 Dec, 5,303 by air.", "OFFICIAL", "Al Jazeera"),
    (7, ZB, "gaza", "ISRAELI STRIKES KILL SEVEN IN GAZA",
     "Three died near a Khan Younis outpost, medics said; a Gaza City strike killed Hamas security chief Abu Nahel.", "CONFIRMED", "Reuters"),
    (8, ZA, "radar", "RUSSIAN JETS ENTER KOREA'S ADIZ",
     "Seoul scrambled jets; Ulleung islanders sheltered at 7:52 a.m. and were stood down three minutes later.", "CONFIRMED", "Yonhap"),
]
for i, c in enumerate(row2):
    card2(MX + i * (CW5 + 8), R2Y, CW5, *c)
R3Y = 584
row3 = [
    (9, ZC, "candle", "47,000 WOMEN KILLED BY PARTNERS",
     "Five women an hour die at the hands of partners or kin, the UN's annual count found. Africa is worst hit.", "OFFICIAL", "UNODC \u00b7 UN Women"),
    (10, ZA, "factory", "BANTEN FACTORY-FIRE TOLL RISES TO 26",
     "The toll from Saturday's candy-factory blaze rose again on Tuesday; eight workers are still missing.", "CONFIRMED", "Xinhua \u00b7 AP"),
    (11, ZA, "rocket", "FIRST FOREIGNER TO FLY TO TIANGONG",
     "Shenzhou-24 crew: Tang Hongbo, Wu Yi and Pakistan's M. Zeeshan Ali. Launch is set for Wednesday.", "OFFICIAL", "Xinhua \u00b7 CMSA"),
    (12, ZC, "gavel", "MEXICO TO TRY 'EL CHAPO ISIDRO' AT HOME",
     "It turns down the US extradition request for the captured cartel boss, the attorney general says.", "OFFICIAL", "Mexico AG"),
    (13, ZC, "bomb", "CAR BOMB HITS GOVERNOR'S OFFICE",
     "23 hurt in the 02:30 UTC blast in Villavicencio, Colombia; gangs are blamed for the attack.", "CONFIRMED", "El Tiempo \u00b7 AFP"),
]
for i, c in enumerate(row3):
    card2(MX + i * (CW5 + 8), R3Y, CW5, *c)
print("cards end", R3Y + 158)

# ---------------- bottom block (top-4 style): map + ALSO ----------------
BY = 746
d.text((MX, BY), "WHERE IT HAPPENED", font=F(SANS_B, 12.5), fill=INK)
d.text((MX + 400, BY), "ALSO ON TUESDAY 24 NOVEMBER \u2014 25 MORE DATED STORIES", font=F(SANS_B, 12.5), fill=INK)
MAPX, MAPY, MAPW, MAPH = MX, BY + 20, 376, 176

LAND = (233, 223, 197)
SEA = (203, 220, 231)


def ll(lon, lat):
    return (MAPX + (lon + 180) / 360 * MAPW, MAPY + (80 - lat) / 140 * MAPH)


def poly(pts):
    d.polygon([ll(lon, lat) for lon, lat in pts], fill=LAND)


d.rectangle([MAPX, MAPY, MAPX + MAPW, MAPY + MAPH], fill=SEA)
poly([(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70), (-80, 73), (-76, 68), (-85, 66), (-90, 60), (-95, 58), (-92, 57), (-85, 55), (-80, 50), (-76, 45), (-70, 44), (-74, 40), (-76, 36), (-80, 32), (-81, 26), (-84, 30), (-89, 30), (-94, 29), (-97, 26), (-97, 22), (-94, 18), (-90, 15), (-86, 13), (-83, 9), (-79, 9), (-83, 15), (-87, 16), (-92, 15), (-97, 16), (-102, 18), (-105, 22), (-110, 24), (-114, 29), (-117, 33), (-122, 37), (-124, 42), (-124, 48), (-130, 55), (-140, 60), (-152, 60), (-162, 62)])
poly([(-45, 60), (-30, 68), (-22, 70), (-20, 76), (-30, 80), (-45, 80), (-55, 76), (-58, 68), (-53, 62)])
poly([(-79, 9), (-75, 11), (-72, 12), (-64, 11), (-60, 9), (-52, 5), (-50, 0), (-44, -3), (-35, -8), (-38, -13), (-40, -20), (-48, -26), (-52, -32), (-57, -38), (-62, -41), (-65, -45), (-67, -50), (-68, -54), (-71, -54), (-73, -50), (-73, -44), (-73, -37), (-71, -30), (-70, -20), (-75, -15), (-79, -8), (-80, -4), (-80, 1), (-77, 4)])
poly([(-9, 43), (-9, 48), (-5, 48), (-1, 50), (0, 52), (3, 53), (5, 58), (5, 60), (10, 59), (18, 56), (21, 60), (24, 66), (30, 70), (40, 66), (44, 60), (40, 55), (38, 50), (35, 45), (30, 46), (28, 41), (23, 40), (19, 40), (15, 38), (12, 44), (8, 44), (3, 43), (-2, 37), (-6, 36), (-9, 37)])
poly([(-5, 50), (-3, 53), (-5, 55), (-3, 58), (-6, 58), (-8, 55), (-6, 52)])
poly([(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (34, 28), (35, 24), (38, 22), (40, 15), (43, 12), (48, 11), (51, 12), (44, 5), (42, -2), (40, -8), (40, -15), (37, -20), (35, -24), (32, -29), (28, -33), (20, -35), (17, -32), (15, -27), (13, -20), (12, -15), (13, -10), (9, -5), (9, 0), (6, 4), (-2, 5), (-8, 5), (-13, 8), (-17, 12), (-17, 15), (-16, 20), (-15, 25), (-13, 28), (-10, 31)])
poly([(44, -16), (47, -15), (50, -18), (49, -22), (47, -25), (45, -25), (44, -20), (43, -17)])
poly([(32, 70), (50, 68), (68, 70), (85, 73), (100, 77), (115, 76), (130, 72), (145, 71), (158, 70), (170, 66), (178, 65), (170, 62), (160, 60), (158, 52), (150, 48), (142, 50), (138, 46), (132, 43), (128, 40), (122, 39), (120, 35), (121, 31), (118, 26), (110, 21), (108, 18), (105, 9), (103, 6), (100, 9), (98, 14), (95, 17), (92, 16), (89, 22), (86, 20), (81, 15), (77, 8), (74, 19), (70, 22), (65, 25), (60, 25), (56, 27), (52, 26), (50, 29), (48, 30), (44, 29), (43, 33), (42, 38), (40, 42), (38, 47), (36, 51), (33, 47), (30, 46), (28, 42), (30, 50), (32, 55), (30, 62)])
poly([(130, 31), (133, 34), (137, 35), (139, 37), (140, 39), (141, 41), (142, 44), (143, 44), (141, 40), (139, 36), (136, 34), (132, 33), (130, 32)])
poly([(95, 5), (100, 0), (104, -3), (106, -6), (102, -4), (98, 2)])
poly([(109, 1), (113, 4), (117, 6), (119, 2), (117, -2), (113, -3), (110, -1)])
poly([(106, -6), (110, -7), (114, -8), (114, -9), (106, -8)])
poly([(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (147, -9), (142, -8), (137, -4), (132, -3)])
poly([(120, 18), (122, 16), (121, 14), (123, 11), (124, 9), (122, 10), (120, 13)])
poly([(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (129, -32), (132, -32), (135, -35), (138, -36), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (151, -24), (146, -19), (142, -15), (142, -11), (137, -12), (136, -15), (135, -12), (132, -11), (130, -13), (126, -14), (122, -17), (118, -20)])
poly([(167, -45), (171, -42), (173, -39), (175, -37), (176, -38), (174, -41), (171, -44), (168, -46)])
d.rectangle([MAPX, MAPY, MAPX + MAPW, MAPY + MAPH], outline=(150, 142, 126), width=1)

pins = [(1, 139, 36, ZA), (2, 2, 49, ZB), (3, 56, 27, ZB), (4, 30, 50, ZB), (5, 44, 33, ZB),
        (6, 102, 3, ZA), (7, 34, 31, ZB), (8, 130, 37, ZA), (9, -74, 41, ZC), (10, 106, -6, ZA),
        (11, 98, 40, ZA), (12, -99, 19, ZC), (13, -73, 4, ZC)]
for num, lon, lat, col in pins:
    px, py = ll(lon, lat)
    d.ellipse([px - 6.5, py - 6.5, px + 6.5, py + 6.5], fill=col, outline=(250, 248, 240), width=1)
    nt = str(num)
    fnt = F(SANS_B, 7 if num < 10 else 6)
    d.text((px - d.textlength(nt, font=fnt) / 2, py - 3.5), nt, font=fnt, fill=(255, 255, 255))
d.text((MAPX, MAPY + MAPH + 4), "Pins 1\u201313 = the illustrated stories; pin colours match the three zones above.", font=F(SANS, 8.5), fill=GREY)

liners = [
    (14, ZA, "DHAKA \u2014 Hasina sets Dec 16 return; arrest vowed (BBC)."),
    (15, ZB, "DAKAR \u2014 CAS restores Senegal as AFCON champions (wires)."),
    (16, ZA, "HIMALAYA \u2014 M5.6 quake hits Nepal\u2013Sikkim border (USGS)."),
    (17, ZA, "PORT MORESBY \u2014 Bougainville vote on nationhood (Conv.)."),
    (18, ZB, "GENEVA \u2014 Chess title match G1: Gukesh v Sindarov (FIDE)."),
    (19, ZB, "BRUSSELS \u2014 EU caps tariff-free Chinese hybrids (GDN)."),
    (20, ZA, "HANOI \u2014 Hot-pot eatery blast kills 6, hurts 10 (Reuters)."),
    (21, ZA, "SINGAPORE \u2014 Q3 GDP +6.1%; 2026 outlook raised (CNA)."),
    (22, ZA, "SINGAPORE \u2014 StarHub\u2013M1 S$5bn merger agreed (CNA)."),
    (23, ZA, "TOKYO \u2014 Factory PMI climbs to 53.7 (S&P Global)."),
    (24, ZA, "CANBERRA \u2014 Tech giants face 5% revenue fines (Guardian)."),
    (25, ZA, "HONIARA \u2014 Solomons ends China security pact (ABC)."),
    (26, ZB, "KYIV \u2014 Zelensky ready for four-way talks (Ukrinform)."),
    (27, ZB, "PARIS \u2014 Macron weighs constitutional spending cap (wires)."),
    (28, ZB, "ROME \u2014 WFP: wars block food aid for 7.3m people (WFP)."),
    (29, ZA, "JAKARTA \u2014 Ex-police chief charged with treason (CNA)."),
    (30, ZC, "WASHINGTON \u2014 Trump urges faster executions (wires)."),
    (31, ZC, "PHILADELPHIA \u2014 Avdija's 31 sinks 76ers, 128\u2013111 (AP)."),
    (32, ZC, "WASHINGTON \u2014 Megaspeed blacklisted in Nvidia case (BIS)."),
    (33, ZC, "GAL\u00c1PAGOS \u2014 El Ni\u00f1o floods force boat rescues (AFN)."),
    (34, ZC, "PENNSYLVANIA \u2014 Ninth death in measles outbreak (wires)."),
    (35, ZC, "IOWA \u2014 Army lead-explosives detonation goes ahead (wires)."),
    (36, ZB, "CAPE TOWN \u2014 Cities tighten water curbs amid drought (wires)."),
    (37, ZC, "NEW YORK \u2014 Gaza war cut 77 years of development (UNDP)."),
    (38, ZA, "GOLD COAST \u2014 England beat Australia, level T20 (wires)."),
]
LW2 = (CW - 400 - 16) // 2  # right block width 576, two columns
for col in range(2):
    yy = BY + 21
    for r in range(13):
        idx = col * 13 + r
        if idx >= len(liners):
            break
        n, zc, txt = liners[idx]
        lx = MX + 400 + col * (LW2 + 16)
        d.rounded_rectangle([lx, yy, lx + 16, yy + 11], radius=2, fill=zc)
        nt = str(n)
        d.text((lx + 8 - d.textlength(nt, font=F(SANS_B, 7.5)) / 2, yy + 1), nt, font=F(SANS_B, 7.5), fill=(255, 255, 255))
        lab, rest = txt.split(" \u2014 ", 1)
        d.text((lx + 20, yy), lab, font=F(SANS_B, 8.5), fill=INK)
        lw_ = d.textlength(lab, font=F(SANS_B, 8.5))
        d.text((lx + 20 + lw_ + 3, yy), "\u2014 " + rest, font=F(SANS, 8.5), fill=(52, 48, 42))
        yy += 15.5
    print("also col", col, "ends", yy)

# ---------------- date check ----------------
DY = 974
d.rectangle([MX, DY, W - MX, DY + 42], outline=RED, width=2)
d.rectangle([MX, DY, MX + 104, DY + 42], fill=RED)
d.text((MX + 9, DY + 6), "DATE", font=F(SANS_B, 13), fill=(255, 255, 255))
d.text((MX + 9, DY + 23), "CHECK", font=F(SANS_B, 13), fill=(255, 255, 255))
audit = ("Left out \u2014 earlier days: Nvidia rehires Huang, Wall Street's rally (Mon 23) \u00b7 NATO space pledge, Sputnik-S reports (Mon 23) \u00b7 "
         "Iran shadow-banking sanctions (Mon 23) \u00b7 COP31 collapses (Sun 22) \u00b7 Las Vegas GP (Sun 22) \u00b7 the Banten fire itself (Sat 22) \u2014 "
         "only Tuesday's toll rise counts \u00b7 ICJ Rohingya ruling (19 Nov).   TAGS: CONFIRMED = 2+ wires \u00b7 OFFICIAL = on the record \u00b7 "
         "REPORTED = one outlet \u00b7 CLAIM = one side says \u00b7 ONGOING = still unfolding.")
block(d, MX + 116, DY + 5, audit, F(SANS, 8.5), CW - 128, 11, fill=(52, 48, 42))
print("footer at", DY + 42)

img.save("entry.png", optimize=True)
print("saved")
