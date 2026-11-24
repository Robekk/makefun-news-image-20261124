#!/usr/bin/env python3
"""Builds entry.png — 'The World Today', a one-page broadsheet summing up
Tuesday 24 November 2026. Pure PIL, fully deterministic, no network."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (243, 238, 226)
INK = (26, 24, 20)
RED = (158, 27, 27)
GREY = (92, 86, 76)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
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


def block(d, x, y, text, font, width, leading):
    for ln in wrap(d, text, font, width):
        d.text((x, y), ln, font=font, fill=INK)
        y += leading
    return y


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
MX = 36            # side margin
CW = W - 2 * MX    # 952

# ---------- masthead ----------
d.text((MX, 12), "WORLD NEWS  \u2022  ONE DAY  \u2022  ONE PAGE", font=F(SANS_B, 15), fill=GREY)
r = "LATE EDITION"
d.text((W - MX - d.textlength(r, font=F(SANS_B, 15)), 12), r, font=F(SANS_B, 15), fill=GREY)
d.line([(MX, 40), (W - MX, 40)], fill=INK, width=2)
t = "The World Today"
d.text(((W - d.textlength(t, font=F(SERIF_B, 74))) / 2, 48), t, font=F(SERIF_B, 74), fill=INK)
d.line([(MX, 138), (W - MX, 138)], fill=INK, width=5)
d.line([(MX, 148), (W - MX, 148)], fill=INK, width=1)
d.rectangle([MX, 158, W - MX, 192], fill=INK)
t = "TUESDAY, 24 NOVEMBER 2026"
d.text(((W - d.textlength(t, font=F(SANS_B, 21))) / 2, 164), t, font=F(SANS_B, 21), fill=BG)

# ---------- lead + rail zone ----------
LY = 206
LW = 600           # lead width
RX = 676           # rail x
RW = W - MX - RX   # 312

d.text((MX, LY), "UKRAINE STRIKES RUSSIAN WARSHIP IN LIBYA", font=F(SANS_B, 17), fill=RED)
y = LY + 26
y = block(d, MX, y, "WAR COMES TO THE MEDITERRANEAN", F(SERIF_B, 41), LW, 48)
y += 4
y = block(d, MX, y,
          "Libya's east asked the UN to investigate after Ukrainian sea drones sank the "
          "Russian corvette Merkury in Benghazi harbour and set the weapons freighter "
          "Angara ablaze — a strike 2,400 km from the front line that President Zelensky "
          "hailed as \u201cexemplary\u201d.",
          F(SANS, 16.5), LW, 22)
print("lead deck ends", y)
IY = y + 8
IH = 84
d.rectangle([MX, IY, MX + LW, IY + IH], outline=INK, width=2)
d.rectangle([MX + 2, IY + 2, MX + LW - 2, IY + 48], fill=(196, 209, 219))
d.ellipse([MX + 52, IY + 10, MX + 92, IY + 44], fill=(232, 197, 92))
d.polygon([(MX + 8, IY + 48), (MX + 190, IY + 30), (MX + 330, IY + 48)], fill=(122, 128, 112))
d.rectangle([MX + 2, IY + 48, MX + LW - 2, IY + IH - 2], fill=(38, 62, 94))
d.rectangle([MX + 428, IY + 26, MX + 566, IY + 50], fill=(30, 30, 30))
d.rectangle([MX + 492, IY + 15, MX + 504, IY + 26], fill=(30, 30, 30))
d.ellipse([MX + 392, IY + 35, MX + 438, IY + 59], fill=(224, 122, 44))
d.ellipse([MX + 400, IY + 24, MX + 430, IY + 46], fill=(240, 170, 60))
d.ellipse([MX + 402, IY + 10, MX + 424, IY + 26], fill=(150, 146, 138))
d.ellipse([MX + 420, IY + 5, MX + 446, IY + 23], fill=(168, 164, 156))
d.rectangle([MX + 88, IY + 59, MX + 142, IY + 66], fill=(24, 24, 24))
d.line([(MX + 30, IY + 70), (MX + 44, IY + 70)], fill=(230, 230, 225), width=2)
d.line([(MX + 52, IY + 72), (MX + 66, IY + 72)], fill=(230, 230, 225), width=2)
cap = "Sea drones reached Benghazi: the Merkury, one of Russia's newest warships, burns in port."
d.text((MX, IY + IH + 6), cap, font=F(SERIF_I, 12.5), fill=GREY)
lead_end = IY + IH + 24

# rail story 1 — markets
ry = LY
ry = block(d, RX, ry, "HUANG'S RETURN SETS ASIA ALIGHT", F(SERIF_B, 21), RW, 25)
ry += 5
ry = block(d, RX, ry,
           "Nvidia reinstated Jensen Huang as CEO and Wall Street leapt; Asia followed — "
           "Taiwan's Taiex jumped 9.1% in a record point gain, Seoul's Kospi 7.5%, "
           "Tokyo's Nikkei 4.5%.",
           F(SANS, 14.5), RW, 19.5)
ry += 10
d.line([(RX, ry), (W - MX, ry)], fill=INK, width=1)
ry += 12
ry = block(d, RX, ry, "SEOUL SCRAMBLES JETS AT RUSSIAN PLANES", F(SERIF_B, 21), RW, 25)
ry += 5
ry = block(d, RX, ry,
           "South Korea scrambled jets on Tuesday as Russian warplanes entered its air "
           "defence zone. Ulleung Islanders sheltered for three minutes; Seoul will "
           "summon Russia's defence attach\u00e9.",
           F(SANS, 14.5), RW, 19.5)
print("rail ends", ry, "lead ends", lead_end)
ZONE_END = max(ry, lead_end)

# ---------- middle band: three columns ----------
MY = ZONE_END + 14
d.line([(MX, MY - 12), (W - MX, MY - 12)], fill=INK, width=2)
COLW, GAP = 304, 20
cols = [
    ("ZELENSKY: READY FOR FOUR-WAY TALKS",
     "Zelensky told NATO lawmakers Ukraine is ready to meet Russia, the US and "
     "Europe at once — \u201cliterally tomorrow\u201d. Partners aim for a meeting before "
     "Christmas; Putin has agreed Europeans can join."),
    ("ISRAELI STRIKE KILLS THREE IN GAZA",
     "An Israeli airstrike killed at least three Palestinians near a police "
     "outpost in Khan Younis in southern Gaza, local medics said, wounding five "
     "others on Tuesday."),
    ("FIRST FOREIGNER TO FLY TO CHINA'S STATION",
     "China unveiled the Shenzhou-24 crew: Tang Hongbo, Wu Yi and Pakistan's "
     "Muhammad Zeeshan Ali, the first foreign astronaut to visit Tiangong. "
     "Launch is set for Wednesday from Jiuquan."),
]
col_end = 0
for i, (h, b) in enumerate(cols):
    cx = MX + i * (COLW + GAP)
    cy = block(d, cx, MY, h, F(SERIF_B, 18), COLW, 23)
    cy += 5
    cy = block(d, cx, cy, b, F(SANS, 14), COLW, 19)
    col_end = max(col_end, cy)
    if i < 2:
        d.line([(cx + COLW + GAP / 2, MY), (cx + COLW + GAP / 2, cy)], fill=(178, 170, 156), width=1)
print("cols end", col_end)

# ---------- briefs: three rows of four ----------
BY = col_end + 12
d.rectangle([MX, BY, W - MX, BY + 26], fill=INK)
d.text((MX + 12, BY + 5), "IN BRIEF — ALSO TODAY", font=F(SANS_B, 14), fill=BG)
briefs = [
    ("JAPAN", "Factory PMI climbs to 53.7 on chip demand; services cool to 50.5."),
    ("SINGAPORE", "Q3 GDP beats forecasts at 6.1%; 2026 outlook raised to about 6%."),
    ("SEOUL", "Consumer sentiment slips to 103.1, a seven-month low (BOK)."),
    ("STARHUB\u2013M1", "S$5bn all-share merger cuts mobile operators from four to three."),
    ("HASINA", "Ousted PM seeks Dec 16 return from exile, on the state carrier."),
    ("AUSTRALIA", "Tech firms face fines up to 5% of global revenue in safety bill."),
    ("NEPAL", "M5.3 quake in Koshi province; no casualties reported so far."),
    ("SENEGAL", "Migrant boat capsizes off the coast; dozens of people missing."),
    ("NBA", "Avdija scores 31; Blazers' 19 threes beat the 76ers 128-111."),
    ("NHL", "Leafs snap nine-game skid, rallying from 2-0 down on Long Island."),
    ("CLIMATE", "COP31 ends with no deal after fossil-fuel wording is dropped."),
    ("AI TALKS", "UN and Barbados call for global AI safety rules within a year."),
]
BW2, GAP2 = 226, 16
by = BY + 36
for r in range(3):
    row_end = by
    for i in range(4):
        h, b = briefs[r * 4 + i]
        bx = MX + i * (BW2 + GAP2)
        d.text((bx, by), h, font=F(SANS_B, 13), fill=RED)
        row_end = max(row_end, block(d, bx, by + 17, b, F(SANS, 13), BW2, 17.5))
    by = row_end + 10
print("briefs end", by)

# ---------- footer ----------
d.line([(MX, 984), (W - MX, 984)], fill=INK, width=2)
t = "ALL STORIES REPORTED ON TUESDAY 24 NOVEMBER 2026  \u2022  DRAWN FROM THE DAY'S WIRE REPORTS"
d.text(((W - d.textlength(t, font=F(SANS_B, 11.5))) / 2, 992), t, font=F(SANS_B, 11.5), fill=GREY)

img.save("entry.png", optimize=True)
print("saved")
