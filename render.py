#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news poster, version 2, for make.fun.

Build-time generator only: run it locally to produce entry.png, which the
grader entrypoint (main.py, standard library only) then copies to /output.
Every shape and letter below is drawn from code with Pillow; no photo, no
downloaded artwork and no network are used. The poster is a dense
newspaper front page: one masthead naming the day, one lead story, four
picture panels, six small picture cards, a schematic world map and a
numbered index of thirty more stories, 41 stories in all across six
continents. Display type stays large so the page still reads small.

Facts shown (all from reporting published on 18 November 2026; several
items are 16-17 November events dominating 18 November coverage):
  1 Gulf: Iran struck at Kuwait and Bahrain early on 18 Nov after the
    US struck Qeshm Island; the bases named host US forces.
  2 Crimea: the Kerch bridge road arch (227 m) fell into the strait
    after Ukrainian strikes; road traffic stayed shut, rail resumed.
  3 Shenzhen: Xi greeted Trump on arrival; a three-way summit with
    Putin follows on Thursday; Xi spoke against protectionism.
  4 Alaska: Mary Peltola beat Dan Sullivan; Democrats hold the Senate
    56-44.
  5 Cyclone: Xavier reached the Northern Cook Islands as a Category 5
    storm, gusts to 315 km/h.
  6 Voyager 1: reached one light-day from Earth at 10:16 UTC, 25.9
    billion km out; radio signals now take 24 hours (NASA).
  7 COP31: Antalya climate talks deadlocked; the draft leaves
    fossil-fuel and finance gaps; the summit closes on Friday.
  8 EU loan: the European Commission proposed 45bn euros for Ukraine
    in 2027, 25bn military and 20bn budget support.
  9 Venezuela: US Defense Secretary Hegseth signed a military
    cooperation deal in Caracas with interim president Rodriguez.
  10 Dhoni: MS Dhoni retired as an IPL player and takes a CSK mentor
    role.
  11 Nvidia: quarterly revenue of $115.8bn, up 103% year on year,
    with about $130bn guided for the next quarter.
  12-41 (brief index): Ebola in Congo (UN: 11,000+ cases, 5,400
    deaths); Iraq's Kirkuk-Ceyhan oil pipeline flowing again after 12
    years; Quad leaders backing ASEAN centrality; Houthi drones at
    Saudi pipeline pumps; Kahana elected Knesset speaker and Eisenkot
    tapped to form a government; the Board of Peace faulting Israel
    and Hamas; Putin not ready for serious Ukraine talks; APEC trade
    lines and the US-China truce to 10 January; Myanmar reviewing
    ASEAN ties; Cyclone Akvan nearing Andhra Pradesh; a tanker hit in
    the Strait of Hormuz; the US losing measles-free status; cold
    killing in Gaza tents with four nations urging aid access; a
    Russian military plane crash in Siberia killing 19; Cambridge
    picking "human" as Word of the Year; US curbs on remote AI-chip
    access; Mozambique's Mondlane on trial; Ethiopia and Eritrea
    massing forces on their border; 64 children killed in Yemen
    (UNICEF); Italy's anti-antisemitism bill passing 147-93; UK and
    Australian sanctions over West Bank settlements; storms Bruna and
    Charles over Portugal and Madeira; Haiti's security pact with El
    Salvador; a C-130 for Colombia; Mexico-US trade talks "very far
    along"; India's 10th SAFF title; Nations League results; Zverev
    reaching the ATP Finals knockouts; Revolution Wind at full power;
    Australia's first new steel mill in 40 years, fossil-free.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

CREAM = (248, 244, 233)
INK = (22, 26, 40)
NAVY = (24, 52, 88)
NAVY_DARK = (16, 36, 62)
RED = (185, 28, 28)
GOLD = (217, 119, 6)
TEAL = (14, 116, 120)
SEA = (38, 102, 150)
SEA_DARK = (18, 66, 108)
SAND = (226, 205, 160)
SKY = (196, 222, 240)
WHITE = (255, 255, 255)
PAPER = (255, 253, 247)
GREY = (88, 94, 108)
LIGHT = (220, 228, 238)
LAND = (150, 178, 132)
MAPSEA = (178, 212, 232)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def centred(draw, cx, y, text, fnt, fill):
    draw.text((cx - text_w(draw, text, fnt) / 2, y), text, font=fnt, fill=fill)


def star_points(cx, cy, outer, inner, points=5, rotation=-90):
    pts = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        a = math.radians(rotation + i * 180 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def burst(draw, cx, cy, r, fill):
    pts = []
    for i in range(16):
        rr = r if i % 2 == 0 else r * 0.45
        a = math.radians(i * 22.5)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    draw.polygon(pts, fill=fill)


def drone(draw, cx, cy, scale, fill):
    arm = 16 * scale
    draw.line([(cx - arm, cy - arm), (cx + arm, cy + arm)], fill=fill, width=3)
    draw.line([(cx - arm, cy + arm), (cx + arm, cy - arm)], fill=fill, width=3)
    for dx, dy in ((-arm, -arm), (arm, -arm), (-arm, arm), (arm, arm)):
        draw.ellipse([cx + dx - 7 * scale, cy + dy - 3, cx + dx + 7 * scale, cy + dy + 3], fill=fill)
    draw.ellipse([cx - 8 * scale, cy - 6 * scale, cx + 8 * scale, cy + 6 * scale], fill=fill)


def badge(draw, x, y, n, size=20):
    draw.rectangle([x, y, x + size, y + size], fill=RED)
    fnt = font(SANS_BOLD, 13 if size >= 20 else 11)
    t = str(n)
    draw.text((x + size / 2 - text_w(draw, t, fnt) / 2, y + (3 if size >= 20 else 2)),
              t, font=fnt, fill=WHITE)


def draw_gulf_map(draw, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    draw.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=SEA_DARK)
    draw.polygon([(x0, y0), (x1, y0), (x1, y0 + 0.30 * h), (x0 + 0.55 * w, y0 + 0.42 * h),
                  (x0 + 0.35 * w, y0 + 0.32 * h), (x0, y0 + 0.40 * h)], fill=SAND)
    draw.polygon([(x0, y1), (x0 + 0.26 * w, y1 - 0.34 * h), (x0 + 0.49 * w, y1 - 0.20 * h),
                  (x0 + 0.43 * w, y1)], fill=(198, 176, 132))
    small = font(SANS_BOLD, 16)
    for name, fx, fy in (("QESHM", 0.64, 0.62), ("KUWAIT", 0.15, 0.48), ("BAHRAIN", 0.34, 0.74)):
        px, py = x0 + fx * w, y0 + fy * h
        burst(draw, px, py, 12, RED)
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=GOLD)
        draw.text((px + 14, py - 9), name, font=small, fill=WHITE)
    drone(draw, x0 + 0.76 * w, y0 + 0.28 * h, 0.7, WHITE)
    drone(draw, x0 + 0.86 * w, y0 + 0.86 * h, 0.6, LIGHT)


def mini_bridge(draw, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    horizon = y0 + int(0.55 * h)
    draw.rectangle([x0, horizon, x1, y1], fill=SEA)
    mid = (x0 + x1) // 2
    gap = int(0.24 * w)
    draw.rectangle([x0, horizon - 7, mid - gap, horizon - 1], fill=INK)
    draw.rectangle([mid + gap, horizon - 7, x1, horizon - 1], fill=INK)
    draw.arc([x0 + 8, horizon - 30, mid - gap + 6, horizon + 4], 180, 360, fill=INK, width=4)
    draw.arc([mid + gap - 6, horizon - 30, x1 - 8, horizon + 4], 180, 360, fill=INK, width=4)
    draw.polygon([(mid - gap + 2, horizon + 2), (mid + gap - 8, horizon + 10),
                  (mid + gap - 14, horizon + 15), (mid - gap - 4, horizon + 7)], fill=(52, 58, 72))
    for px in (x0 + 18, x1 - 28):
        draw.rectangle([px, horizon, px + 7, y1 - 2], fill=(52, 58, 72))
    for sx, sy, sr in ((mid - 10, horizon - 26, 7), (mid + 6, horizon - 30, 9),
                       (mid + 20, horizon - 24, 6)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(140, 146, 158))


def mini_flags(draw, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(214, 230, 244))
    base = y1 - 4
    heights = [26, 40, 22, 34, 44, 30, 20, 36]
    bw = w // len(heights)
    for i, hgt in enumerate(heights):
        bx = x0 + i * bw + 2
        draw.rectangle([bx, base - hgt, bx + bw - 4, base], fill=(70, 88, 112))
    fw, fh = 44, 27
    tops = y0 + 4
    poles = [x0 + 30, x0 + 96, x0 + 162]
    for px in poles:
        draw.rectangle([px, tops, px + 3, base], fill=INK)
    cx = poles[0] + 4
    draw.rectangle([cx, tops, cx + fw, tops + fh], fill=(222, 41, 16))
    draw.polygon(star_points(cx + 11, tops + 10, 7, 3), fill=GOLD)
    for sx, sy in ((cx + 26, tops + 5), (cx + 32, tops + 10), (cx + 32, tops + 17), (cx + 26, tops + 21)):
        draw.polygon(star_points(sx, sy, 3, 1.2), fill=GOLD)
    rx = poles[1] + 4
    for j, col in enumerate((WHITE, (0, 82, 180), RED)):
        draw.rectangle([rx, tops + j * fh // 3, rx + fw, tops + (j + 1) * fh // 3], fill=col)
    draw.rectangle([rx, tops, rx + fw, tops + fh], outline=GREY, width=1)
    ux = poles[2] + 4
    for j in range(5):
        draw.rectangle([ux, tops + j * fh // 5, ux + fw, tops + (j + 1) * fh // 5],
                       fill=RED if j % 2 == 0 else WHITE)
    draw.rectangle([ux, tops, ux + 18, tops + 14], fill=NAVY)


def mini_capitol(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(232, 236, 242))
    cx = x0 + 62
    base = y1 - 4
    draw.pieslice([cx - 30, y0 + 8, cx + 30, y0 + 52], 180, 360, fill=(120, 130, 148))
    draw.rectangle([cx - 34, y0 + 28, cx + 34, y0 + 33], fill=(120, 130, 148))
    for i in range(5):
        colx = cx - 28 + i * 13
        draw.rectangle([colx, y0 + 33, colx + 6, base], fill=(160, 168, 180))
    draw.rectangle([cx - 38, base, cx + 38, base + 2], fill=(120, 130, 148))
    bx = x0 + 118
    big = font(SANS_BOLD, 20)
    inside = font(SANS_BOLD, 11)
    draw.rectangle([bx, y0 + 8, bx + 72, y0 + 24], fill=(37, 99, 235))
    draw.text((bx + 5, y0 + 10), "DEM", font=inside, fill=WHITE)
    draw.text((bx + 78, y0 + 6), "56", font=big, fill=(37, 99, 235))
    draw.rectangle([bx, y0 + 30, bx + 57, y0 + 46], fill=RED)
    draw.text((bx + 5, y0 + 32), "REP", font=inside, fill=WHITE)
    draw.text((bx + 63, y0 + 28), "44", font=big, fill=RED)


def mini_cyclone(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=SEA_DARK)
    cx, cy = (x0 + x1) // 2 - 14, (y0 + y1) // 2
    for i, r in enumerate(range(7, 28, 6)):
        start = i * 70
        draw.arc([cx - r, cy - r, cx + r, cy + r], start, start + 300, fill=WHITE, width=4)
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=GOLD)
    for ix, iy in ((x0 + 14, y1 - 10), (x1 - 16, y0 + 10)):
        draw.ellipse([ix - 6, iy - 4, ix + 6, iy + 4], fill=(86, 168, 92))


def mini_voyager(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=NAVY_DARK)
    for sx, sy in ((8, 6), (26, 14), (44, 5), (60, 18), (84, 8), (104, 16),
                   (124, 6), (136, 20), (18, 24), (96, 26)):
        draw.ellipse([x0 + sx - 1, y0 + sy - 1, x0 + sx + 1, y0 + sy + 1], fill=WHITE)
    for t in range(11):
        px, py = x0 + 10 + t * 9, y0 + 26 - t * 2
        draw.ellipse([px - 1, py - 1, px + 1, py + 1], fill=LIGHT)
    px, py = x0 + 118, y0 + 10
    draw.rectangle([px - 6, py - 3, px + 6, py + 3], fill=GOLD)
    draw.line([(px + 6, py), (px + 14, py - 5)], fill=GOLD, width=2)
    draw.arc([px + 10, py - 9, px + 18, py - 1], 270, 90, fill=WHITE, width=2)
    draw.line([(px - 6, py), (px - 16, py + 6)], fill=LIGHT, width=2)


def mini_cop(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(16, 90, 86))
    cx, cy = x0 + 30, y0 + 16
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(120, 190, 220), outline=WHITE, width=1)
    draw.arc([cx - 12, cy - 5, cx + 12, cy + 5], 0, 180, fill=WHITE, width=1)
    draw.line([(cx, cy - 12), (cx, cy + 12)], fill=WHITE, width=1)
    draw.ellipse([x0 + 70, y0 + 6, x0 + 96, y0 + 24], fill=(86, 168, 92))
    draw.line([(x0 + 70, y0 + 24), (x0 + 96, y0 + 6)], fill=(30, 90, 40), width=2)
    burst(draw, x0 + 124, y0 + 12, 8, GOLD)


def mini_eu(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx, sy = cx + 22 * math.cos(a), cy + 11 * math.sin(a)
        draw.polygon(star_points(sx, sy, 4, 1.6), fill=GOLD)
    draw.text((cx - 6, cy - 10), "\u20ac", font=font(SANS_BOLD, 18), fill=GOLD)


def mini_venezuela(draw, x0, y0, x1, y1):
    hw = (x1 - x0) // 2
    for j in range(5):
        draw.rectangle([x0, y0 + j * (y1 - y0) // 5, x0 + hw - 3, y0 + (j + 1) * (y1 - y0) // 5],
                       fill=RED if j % 2 == 0 else WHITE)
    draw.rectangle([x0, y0, x0 + 26, y0 + 14], fill=NAVY)
    vx = x0 + hw + 3
    for j, col in enumerate(((250, 200, 0), (0, 60, 160), (200, 20, 30))):
        draw.rectangle([vx, y0 + j * (y1 - y0) // 3, x1, y0 + (j + 1) * (y1 - y0) // 3], fill=col)
    for k in range(4):
        sx = vx + 14 + k * 12
        draw.ellipse([sx - 2, y0 + 13, sx + 2, y0 + 17], fill=WHITE)


def mini_dhoni(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(52, 130, 70))
    draw.rectangle([x0 + 18, y0 + 4, x0 + 128, y0 + 28], fill=(200, 180, 140))
    for sx in (x0 + 30, x0 + 36, x0 + 42):
        draw.rectangle([sx, y0 + 8, sx + 3, y0 + 22], fill=GOLD)
    draw.polygon([(x0 + 96, y0 + 26), (x0 + 104, y0 + 26), (x0 + 112, y0 + 8), (x0 + 104, y0 + 6)],
                 fill=(220, 190, 130))
    draw.ellipse([x0 + 118, y0 + 6, x0 + 126, y0 + 14], fill=RED)


def mini_chip(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(28, 32, 44))
    cx, cy = x0 + 34, y0 + 16
    for dx in (-14, -5, 5, 14):
        draw.line([(cx + dx, y0 + 2), (cx + dx, y0 + 8)], fill=GOLD, width=2)
        draw.line([(cx + dx, y1 - 8), (cx + dx, y1 - 2)], fill=GOLD, width=2)
    draw.rectangle([cx - 13, cy - 9, cx + 13, cy + 9], fill=(60, 70, 92), outline=GOLD, width=2)
    draw.rectangle([cx - 6, cy - 4, cx + 6, cy + 4], fill=GOLD)
    draw.line([(x0 + 66, y0 + 24), (x0 + 86, y0 + 12), (x0 + 104, y0 + 16), (x0 + 128, y0 + 4)],
              fill=(74, 222, 128), width=3)
    draw.polygon([(x0 + 128, y0 + 4), (x0 + 118, y0 + 4), (x0 + 126, y0 + 12)], fill=(74, 222, 128))


def world_map(draw, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=MAPSEA)

    def poly(fracs):
        draw.polygon([(x0 + fx * w, y0 + fy * h) for fx, fy in fracs], fill=LAND)

    poly([(0.03, 0.08), (0.16, 0.05), (0.26, 0.12), (0.24, 0.30), (0.18, 0.45),
          (0.12, 0.52), (0.06, 0.40), (0.02, 0.22)])
    poly([(0.24, 0.52), (0.32, 0.50), (0.35, 0.62), (0.31, 0.85), (0.27, 0.95), (0.24, 0.75)])
    poly([(0.46, 0.10), (0.55, 0.08), (0.58, 0.20), (0.54, 0.32), (0.47, 0.30), (0.45, 0.18)])
    poly([(0.46, 0.35), (0.56, 0.33), (0.60, 0.45), (0.57, 0.68), (0.52, 0.85),
          (0.48, 0.65), (0.45, 0.48)])
    poly([(0.58, 0.08), (0.75, 0.05), (0.92, 0.12), (0.96, 0.28), (0.88, 0.45),
          (0.78, 0.55), (0.66, 0.50), (0.58, 0.35)])
    poly([(0.86, 0.68), (0.94, 0.66), (0.96, 0.78), (0.90, 0.88), (0.85, 0.80)])
    lab = font(SANS_BOLD, 10)
    for text, fx, fy in (("N. AMERICA", 0.04, 0.33), ("S. AMERICA", 0.225, 0.82),
                         ("EUROPE", 0.455, 0.13), ("AFRICA", 0.485, 0.56),
                         ("ASIA", 0.75, 0.28), ("OCEANIA", 0.85, 0.78)):
        draw.text((x0 + fx * w, y0 + fy * h), text, font=lab, fill=(60, 80, 60))
    numf = font(SANS_BOLD, 10)
    for n, fx, fy in ((1, 0.625, 0.47), (2, 0.55, 0.30), (3, 0.80, 0.55), (4, 0.08, 0.18),
                      (5, 0.95, 0.85), (7, 0.57, 0.42), (8, 0.52, 0.34), (9, 0.285, 0.65),
                      (10, 0.705, 0.50), (11, 0.155, 0.44)):
        px, py = x0 + fx * w, y0 + fy * h
        draw.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=WHITE, width=1)
        t = str(n)
        draw.text((px - text_w(draw, t, numf) / 2, py - 6), t, font=numf, fill=WHITE)
    sx, sy = x0 + 0.93 * w, y0 + 0.16 * h
    draw.polygon(star_points(sx, sy, 10, 4), fill=GOLD)
    draw.text((sx + 12, sy - 6), "6", font=numf, fill=INK)
    draw.text((x0 + 8, y1 - 14), "DOTS = STORY NUMBERS", font=lab, fill=(60, 80, 100))


def card(draw, x0, y0, x1, y1, num, tag, head_lines, deck_lines, art):
    draw.rectangle([x0, y0, x1, y1], fill=PAPER, outline=INK, width=2)
    art(draw, x0 + 6, y0 + 6, x1 - 6, y0 + 68)
    badge(draw, x0 + 10, y0 + 10, num)
    draw.text((x0 + 12, y0 + 72), tag, font=font(SANS_BOLD, 15), fill=RED)
    hf = font(SANS_BOLD, 24)
    for i, line in enumerate(head_lines):
        draw.text((x0 + 12, y0 + 90 + i * 26), line, font=hf, fill=INK)
    df = font(SANS, 17)
    for i, line in enumerate(deck_lines):
        draw.text((x0 + 12, y0 + 142 + i * 19), line, font=df, fill=(44, 50, 64))


def mini(draw, x0, y0, x1, y1, num, head_lines, deck, art):
    draw.rectangle([x0, y0, x1, y1], fill=PAPER, outline=INK, width=2)
    art(draw, x0 + 5, y0 + 5, x1 - 5, y0 + 37)
    badge(draw, x0 + 8, y0 + 8, num, size=16)
    hf = font(SANS_BOLD, 15)
    for i, line in enumerate(head_lines):
        draw.text((x0 + 8, y0 + 41 + i * 17), line, font=hf, fill=INK)
    draw.text((x0 + 8, y0 + 73), deck, font=font(SANS, 11), fill=(44, 50, 64))


BRIEFS = [
    ("EBOLA IN CONGO", "UN: 11,000+ cases, 5,400 deaths"),
    ("IRAQ OIL FLOWS AGAIN", "Kirkuk-Ceyhan line back after 12 years"),
    ("QUAD BACKS ASEAN", "Pact on AI, minerals, maritime security"),
    ("HOUTHI DRONES", "5 drones sent at Saudi pipeline pumps"),
    ("ISRAEL'S NEW SPEAKER", "Kahana elected; Eisenkot to form government"),
    ("BOARD OF PEACE", "Faults Israel and Hamas on truce terms"),
    ("PUTIN ON UKRAINE TALKS", "Not ready for serious negotiations"),
    ("APEC TRADE LINES", "Xi hits protectionism; truce to Jan 10"),
    ("MYANMAR REVIEWS ASEAN", 'Junta chief cites "unfair treatment"'),
    ("CYCLONE AKVAN", "Landfall due Friday on Andhra coast"),
    ("TANKER HIT IN HORMUZ", "Crew member missing after strike"),
    ("MEASLES STATUS LOST", "US: 5,400+ cases, 10 deaths"),
    ("GAZA'S COLD", "Deaths in tents; 4 nations urge aid access"),
    ("SIBERIA PLANE CRASH", "Russian military plane down; 19 dead"),
    ("WORD OF THE YEAR", 'Cambridge picks "human" amid AI debate'),
    ("AI CHIP CURBS", "US limits remote access; China objects"),
    ("MOZAMBIQUE TRIAL", "Mondlane tried over 2024 protests"),
    ("ETHIOPIA-ERITREA", "Forces mass along shared border"),
    ("YEMEN'S CHILDREN", "UNICEF: 64 killed since September"),
    ("ITALY VOTES BILL", "Anti-antisemitism law passes 147-93"),
    ("SETTLEMENT SANCTIONS", "UK and Australia act over West Bank"),
    ("STORMS HIT IBERIA", "Bruna and Charles bring record rain"),
    ("HAITI SECURITY PACT", "Deal with El Salvador; 4,595 killed"),
    ("COLOMBIA AID", "Hegseth delivers C-130 Hercules"),
    ("MEXICO TRADE TALKS", 'Sheinbaum: "very far along" with US'),
    ("INDIA'S 10TH SAFF TITLE", "India beat Pakistan 2-1 in final"),
    ("NATIONS LEAGUE", "Portugal, Norway advance; Germany 5-0"),
    ("ZVEREV ADVANCES", "Into ATP Finals knockouts in Turin"),
    ("WIND AT FULL POWER", "Revolution Wind: 704 MW, 65 turbines"),
    ("FOSSIL-FREE STEEL", "Australia's first new mill in 40 years"),
]


def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 1014, 1014], outline=INK, width=5)

    # Masthead: the date is the largest thing on the page.
    centred(draw, 512, 24, "THE WORLD IN ONE IMAGE", font(SANS_BOLD, 21), NAVY)
    centred(draw, 512, 46, "18 NOVEMBER 2026", font(SERIF_BOLD, 72), INK)
    centred(draw, 512, 124, "WEDNESDAY  \u2022  41 STORIES  \u2022  SIX CONTINENTS",
            font(SANS_BOLD, 20), GREY)
    draw.line([(24, 152), (1000, 152)], fill=INK, width=4)
    draw.line([(24, 158), (1000, 158)], fill=INK, width=1)

    # Lead story: the Gulf.
    draw.rectangle([24, 164, 1000, 332], fill=NAVY)
    draw.text((42, 174), "1  \u2022  THE GULF  \u2022  LEAD STORY", font=font(SANS_BOLD, 19), fill=GOLD)
    head = font(SANS_BOLD, 40)
    draw.text((42, 198), "IRAN STRIKES", font=head, fill=WHITE)
    draw.text((42, 240), "US BASES IN GULF", font=head, fill=WHITE)
    deck = font(SANS, 22)
    draw.text((42, 284), "Drones hit Kuwait and Bahrain", font=deck, fill=LIGHT)
    draw.text((42, 306), "after US strike on Qeshm Island", font=deck, fill=LIGHT)
    draw_gulf_map(draw, 640, 172, 992, 324)

    # Four picture panels in one row.
    cards = [
        (24, 2, "UKRAINE  \u2022  EUROPE", ["CRIMEA BRIDGE", "DOWN"],
         ["227m arch fell into", "the strait; road shut"], mini_bridge),
        (270, 3, "CHINA  \u2022  DIPLOMACY", ["TRUMP IN", "SHENZHEN"],
         ["Xi greets him; summit", "with Putin Thursday"], mini_flags),
        (516, 4, "USA  \u2022  POLITICS", ["PELTOLA WINS", "ALASKA"],
         ["Democrats take Senate,", "56 seats to 44"], mini_capitol),
        (762, 5, "PACIFIC  \u2022  WEATHER", ["CYCLONE", "XAVIER HITS"],
         ["Cat 5 over the Cook", "Islands; gusts 315 km/h"], mini_cyclone),
    ]
    for x0, num, tag, head_lines, deck_lines, art in cards:
        card(draw, x0, 340, x0 + 238, 520, num, tag, head_lines, deck_lines, art)

    # Six small picture cards in one row.
    minis = [
        (24, 6, ["VOYAGER 1, ONE", "LIGHT-DAY OUT"], "Signals take 24 hours", mini_voyager),
        (188, 7, ["COP31 TALKS", "DEADLOCKED"], "Draft gaps; ends Friday", mini_cop),
        (352, 8, ["EU OFFERS", "UKRAINE \u20ac45BN"], "\u20ac25bn arms + \u20ac20bn aid", mini_eu),
        (516, 9, ["HEGSETH SIGNS", "CARACAS PACT"], "US military deal signed", mini_venezuela),
        (680, 10, ["DHONI RETIRES", "FROM IPL"], "Takes CSK mentor role", mini_dhoni),
        (844, 11, ["NVIDIA SALES", "DOUBLE"], "$115.8bn; $130bn guided", mini_chip),
    ]
    for x0, num, head_lines, deck_line, art in minis:
        mini(draw, x0, 528, x0 + 156, 614, num, head_lines, deck_line, art)

    # Schematic world map with numbered story dots.
    world_map(draw, 24, 622, 1000, 698)

    # Numbered brief index: thirty more stories in three columns.
    draw.text((24, 704), "THE REST OF THE DAY \u2014 30 MORE STORIES",
              font=font(SANS_BOLD, 16), fill=INK)
    src = "SOURCES: AP, REUTERS, AFP, UN NEWS, NASA, IMD, UKMTO, METSERVICE, CAMBRIDGE, CSK, EC, CPJ, UNICEF, BIS"
    srcf = font(SANS, 10)
    draw.text((1000 - text_w(draw, src, srcf), 708), src, font=srcf, fill=GREY)
    draw.line([(24, 726), (1000, 726)], fill=INK, width=2)
    cols = [24, 353, 682]
    headf = font(SANS_BOLD, 13)
    detf = font(SANS, 12)
    for i, (head_line, detail) in enumerate(BRIEFS):
        x = cols[i // 10]
        y = 732 + (i % 10) * 28
        draw.text((x, y), str(12 + i), font=headf, fill=RED)
        draw.text((x + 24, y), head_line, font=headf, fill=INK)
        draw.text((x + 24, y + 14), detail, font=detf, fill=(44, 50, 64))
    for gx in (343, 672):
        draw.line([(gx, 730), (gx, 1010)], fill=(200, 205, 215), width=1)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
