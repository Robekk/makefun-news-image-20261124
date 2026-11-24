#!/usr/bin/env python3
"""Build the front-page poster for make.fun bounty news-image-20261124.
Sums up the world news of Tuesday 24 November 2026 in one 1024x1024 image.
Deterministic: pure PIL drawing, no randomness, no network.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 244, 234)
INK = (18, 16, 12)
RED = (163, 22, 33)
NAVY = (29, 53, 87)
GREY = (90, 84, 72)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, text, font, maxw, leading, fill=INK):
    for ln in wrap(draw, text, font, maxw):
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 36            # side margin
RIGHT = W - MX     # 988

# ---------- top strip ----------
d.line([(MX, 20), (RIGHT, 20)], fill=INK, width=2)
d.text((MX, 27), "WORLD NEWS  •  ONE DAY  •  ONE PAGE", font=F(SANS_B, 15), fill=GREY)
t = "LATE EDITION"
d.text((RIGHT - d.textlength(t, font=F(SANS_B, 15)), 27), t, font=F(SANS_B, 15), fill=GREY)
d.line([(MX, 52), (RIGHT, 52)], fill=INK, width=1)

# ---------- masthead ----------
mast = F(SERIF_B, 66)
t = "The World Today"
d.text(((W - d.textlength(t, font=mast)) / 2, 60), t, font=mast, fill=INK)
d.line([(MX, 136), (RIGHT, 136)], fill=INK, width=5)
d.line([(MX, 144), (RIGHT, 144)], fill=INK, width=1)

# ---------- date band ----------
d.rectangle([MX, 154, RIGHT, 188], fill=INK)
t = "TUESDAY, 24 NOVEMBER 2026"
df = F(SANS_B, 24)
d.text(((W - d.textlength(t, font=df)) / 2, 160), t, font=df, fill=(255, 252, 240))

# ---------- LEAD (left) ----------
LX, LW = MX, 600
y = 204
d.text((LX, y), "UKRAINE STRIKES RUSSIAN WARSHIP IN LIBYA", font=F(SANS_B, 19), fill=RED)
y += 30
for ln in ["WAR COMES TO", "THE MEDITERRANEAN"]:
    d.text((LX, y), ln, font=F(SERIF_B, 42), fill=INK)
    y += 50
y += 8
y = block(d, LX, y,
          "Libya's east asked the UN to investigate after Ukrainian sea drones sank "
          "the Russian corvette Merkury in Benghazi harbour and set the weapons "
          "freighter Angara ablaze — a strike 2,400 km from the front line that "
          "President Zelensky hailed as \u201cexemplary\u201d.",
          F(SANS, 19), LW, 25)
print("lead deck ends", y)

# ---------- illustration ----------
IX, IY, IW, IH = LX, 478, LW, 142
d.rectangle([IX, IY, IX + IW, IY + IH], fill=(206, 219, 228))            # sky
d.rectangle([IX, IY + 84, IX + IW, IY + IH], fill=NAVY)                  # sea
d.ellipse([IX + 36, IY + 14, IX + 84, IY + 62], fill=(240, 200, 90))     # sun
d.polygon([(IX, IY + 84), (IX + 150, IY + 66), (IX + 330, IY + 84)], fill=(120, 130, 120))  # coast
sx, sy = IX + 356, IY + 62                                               # warship
d.polygon([(sx, sy + 22), (sx + 196, sy + 22), (sx + 178, sy + 40), (sx + 18, sy + 40)], fill=(30, 30, 34))
d.rectangle([sx + 52, sy + 6, sx + 118, sy + 22], fill=(30, 30, 34))
d.rectangle([sx + 78, sy - 16, sx + 84, sy + 6], fill=(30, 30, 34))
d.rectangle([sx + 128, sy + 12, sx + 158, sy + 22], fill=(30, 30, 34))
ex, ey = sx + 26, sy + 34                                                # fire at the bow waterline
for rx, ry, ox, oy, c in [(30, 15, 0, 0, (214, 90, 30)), (21, 20, 2, -12, (232, 130, 40)),
                          (11, 13, 3, -22, (246, 190, 80))]:
    d.ellipse([ex - rx + ox, ey - ry + oy, ex + rx + ox, ey + ry + oy], fill=c)
d.ellipse([ex - 13, ey - 62, ex + 17, ey - 38], fill=(150, 146, 138))    # smoke above the flames
d.ellipse([ex + 2, ey - 74, ex + 24, ey - 56], fill=(168, 164, 156))
dx, dy = IX + 66, IY + 104                                               # sea drone
d.polygon([(dx, dy), (dx + 54, dy), (dx + 44, dy + 10), (dx + 8, dy + 10)], fill=(24, 24, 28))
d.rectangle([dx + 20, dy - 7, dx + 34, dy], fill=(24, 24, 28))
for i in range(3):
    d.line([(dx - 12 - i * 16, dy + 8 + i * 3), (dx - 2 - i * 16, dy + 8 + i * 3)], fill=(240, 244, 246), width=2)
d.rectangle([IX, IY, IX + IW, IY + IH], outline=INK, width=2)
cap = "Sea drones reached Benghazi: the Merkury, one of Russia's newest warships, burns in port."
d.text((IX, IY + IH + 7), cap, font=F(SERIF_I, 15), fill=GREY)

# ---------- right rail ----------
RX, RW = 664, RIGHT - 664
y = 204
d.text((RX, y), "SEOUL SCRAMBLES JETS OVER", font=F(SERIF_B, 24), fill=INK); y += 29
d.text((RX, y), "RUSSIAN PLANES", font=F(SERIF_B, 24), fill=INK); y += 35
y = block(d, RX, y,
          "South Korea scrambled air force jets on Tuesday as Russian military planes "
          "entered its air defence zone off the east coast. Ulleung Islanders were told "
          "to take shelter, then given the all-clear three minutes later. Seoul will "
          "summon Russia's defence attach\u00e9 to lodge a protest.",
          F(SANS, 16), RW, 21)
y += 12
d.line([(RX, y), (RIGHT, y)], fill=GREY, width=1); y += 12
d.text((RX, y), "UN: AGREE AI RULES", font=F(SERIF_B, 24), fill=INK); y += 29
d.text((RX, y), "WITHIN ONE YEAR", font=F(SERIF_B, 24), fill=INK); y += 35
y = block(d, RX, y,
          "UN chief Ant\u00f3nio Guterres and Barbados PM Mia Mottley issued the Bridgetown "
          "Call: agree a global AI safety framework within one year, backed by a "
          "proposed $3bn fund so poorer nations get a voice.",
          F(SANS, 16), RW, 21)
print("rail ends", y)

# ---------- middle band: three columns ----------
MY = 678
d.line([(MX, MY - 14), (RIGHT, MY - 14)], fill=INK, width=2)
cols = [
    ("EU PROPOSES 22ND SANCTIONS PACKAGE",
     "Brussels proposed a 22nd package of sanctions on Russia, targeting banks, "
     "crypto platforms and ex-combatants, and barring Russian teams and athletes "
     "from EU events under their flag."),
    ("NATO VOWS SPACE DEFENCE",
     "NATO vowed to defend its interests in space after reports that Russia is "
     "preparing a nuclear-armed satellite, possibly launching as soon as "
     "December."),
    ("DOZENS MISSING OFF SENEGAL",
     "A migrant boat capsized off Senegal's coast, leaving dozens of people "
     "missing — the latest tragedy for the small boats that cross toward "
     "Europe."),
]
CW, GAP = 304, 20
for i, (h, b) in enumerate(cols):
    cx = MX + i * (CW + GAP)
    yy = block(d, cx, MY, h, F(SERIF_B, 20), CW, 24)
    yy += 5
    yy = block(d, cx, yy, b, F(SANS, 15), CW, 20.5)
    print("col", i, "ends", yy)
    if i:
        d.line([(cx - GAP // 2, MY), (cx - GAP // 2, MY + 150)], fill=GREY, width=1)

# ---------- briefs ----------
BY = 860
d.rectangle([MX, BY, RIGHT, BY + 28], fill=INK)
d.text((MX + 12, BY + 5), "IN BRIEF — ALSO TODAY", font=F(SANS_B, 16), fill=(255, 252, 240))
briefs = [
    ("INDONESIA  ", "Rescue teams searched a burning factory as workers stayed missing after a major fire."),
    ("SEATTLE  ", "ICE agents made arrests at Seattle's airport, in scenes a lawmaker called \u201cappalling\u201d."),
    ("CLIMATE  ", "COP31 talks in T\u00fcrkiye bogged down over fossil fuels and climate finance."),
]
for i, (h, b) in enumerate(briefs):
    bx = MX + i * (CW + GAP)
    by = BY + 42
    d.text((bx, by), h, font=F(SANS_B, 15), fill=RED)
    block(d, bx + d.textlength(h, font=F(SANS_B, 15)), by, b, F(SANS, 15),
          CW - d.textlength(h, font=F(SANS_B, 15)), 20)

# ---------- footer ----------
d.line([(MX, 980), (RIGHT, 980)], fill=INK, width=2)
t = "ALL STORIES REPORTED ON TUESDAY 24 NOVEMBER 2026  •  DRAWN FROM THE DAY'S WIRE REPORTS"
ff = F(SANS_B, 13.5)
d.text(((W - d.textlength(t, font=ff)) / 2, 990), t, font=ff, fill=GREY)

img.save("/home/hatch/workspace/makefun/news-image-20261124/entry-repo/entry.png")
print("saved")
