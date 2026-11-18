#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news poster for make.fun.

Build-time generator only: run it locally to produce entry.png, which the
grader entrypoint (main.py, standard library only) then copies to /output.
Every shape and letter below is drawn from code with Pillow; no photo, no
downloaded artwork and no network are used. The poster is a flat newspaper
front page: one masthead naming the day, one lead story, four picture
panels and two short briefs, all in large type so it still reads small.

Facts shown (all from reporting published on 18 November 2026):
  Gulf: Iran struck at Kuwait and Bahrain early on 18 Nov after the US
    struck Qeshm Island; the bases named host US forces.
  Crimea: the Kerch bridge road arch (227 m) fell into the strait after
    Ukrainian strikes; road traffic stayed shut, rail resumed.
  Shenzhen: Xi greeted Trump on arrival in Shenzhen; a three-way summit
    with Putin follows on Thursday; Xi spoke against protectionism.
  Alaska: Mary Peltola beat Dan Sullivan; Democrats hold the Senate 56-44.
  Cyclone: Xavier reached the Northern Cook Islands as a Category 5
    storm, gusts to 315 km/h, shelters activated.
  Ebola: the UN/WHO put the DRC outbreak at 11,000+ cases and about
    5,400 deaths, more than double in three months.
  Nvidia: quarterly revenue of $115.8bn, up 103% year on year, with
    about $130bn guided for the next quarter.
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


def draw_gulf_map(draw, x0, y0, x1, y1):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=SEA_DARK)
    # Land mass across the top, sea below; three labelled points.
    draw.polygon([(x0, y0), (x1, y0), (x1, y0 + 62), (x0 + 190, y0 + 88),
                  (x0 + 120, y0 + 66), (x0, y0 + 84)], fill=SAND)
    draw.polygon([(x0, y1), (x0 + 90, y1 - 52), (x0 + 170, y1 - 30), (x0 + 150, y1)],
                 fill=(198, 176, 132))
    small = font(SANS_BOLD, 21)
    # Qeshm island in the strait, Kuwait and Bahrain on the gulf shore.
    pts = [("QESHM", x0 + 222, y0 + 128), ("KUWAIT", x0 + 52, y0 + 96),
           ("BAHRAIN", x0 + 118, y0 + 150)]
    for name, px, py in pts:
        burst(draw, px, py, 15, RED)
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=GOLD)
        draw.text((px + 18, py - 11), name, font=small, fill=WHITE)
    drone(draw, x0 + 262, y0 + 62, 0.9, WHITE)
    drone(draw, x0 + 296, y0 + 176, 0.8, LIGHT)


def draw_bridge(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    horizon = y0 + 58
    draw.rectangle([x0, horizon, x1, y1], fill=SEA)
    for wx in range(x0 + 8, x1 - 20, 42):
        draw.arc([wx, horizon + 14, wx + 28, horizon + 30], 200, 340, fill=WHITE, width=2)
    # Deck in two halves with a gap where the arch fell.
    mid = (x0 + x1) // 2
    draw.rectangle([x0, horizon - 10, mid - 52, horizon - 2], fill=INK)
    draw.rectangle([mid + 52, horizon - 10, x1, horizon - 2], fill=INK)
    # Standing arch stubs on both sides of the gap.
    draw.arc([x0 + 20, horizon - 46, mid - 30, horizon + 6], 180, 360, fill=INK, width=5)
    draw.arc([mid + 30, horizon - 46, x1 - 20, horizon + 6], 180, 360, fill=INK, width=5)
    # Fallen span, tilted into the water, kept inside the art box.
    draw.polygon([(mid - 48, horizon + 2), (mid + 40, horizon + 18),
                  (mid + 30, horizon + 26), (mid - 56, horizon + 10)], fill=(52, 58, 72))
    draw.polygon([(mid - 30, horizon + 20), (mid + 44, horizon + 28),
                  (mid + 36, horizon + 32), (mid - 36, horizon + 24)], fill=(52, 58, 72))
    # Pillars and smoke over the gap.
    for px in (x0 + 44, x0 + 150, x1 - 160, x1 - 54):
        draw.rectangle([px, horizon, px + 10, y1 - 4], fill=(52, 58, 72))
    for sx, sy, sr in ((mid - 18, horizon - 42, 11), (mid + 8, horizon - 50, 13),
                       (mid + 30, horizon - 38, 9)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(140, 146, 158))


def draw_flags(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(214, 230, 244))
    # Skyline silhouettes.
    base = y1 - 8
    heights = [52, 78, 44, 66, 88, 58, 40, 70]
    bw = (x1 - x0) // len(heights)
    for i, hgt in enumerate(heights):
        bx = x0 + i * bw + 3
        draw.rectangle([bx, base - hgt, bx + bw - 6, base], fill=(70, 88, 112))
        for wy in range(base - hgt + 8, base - 6, 14):
            for wx in range(bx + 5, bx + bw - 10, 12):
                draw.rectangle([wx, wy, wx + 4, wy + 4], fill=GOLD)
    # Three flags on poles: China, Russia, United States.
    fw, fh = 74, 46
    tops = y0 + 8
    poles = [x0 + 52, x0 + 198, x0 + 344]
    for px in poles:
        draw.rectangle([px, tops, px + 4, base], fill=INK)
    # China: red field, one large star and four small ones.
    cx = poles[0] + 6
    draw.rectangle([cx, tops, cx + fw, tops + fh], fill=(222, 41, 16))
    draw.polygon(star_points(cx + 18, tops + 15, 11, 4.5), fill=GOLD)
    for sx, sy in ((cx + 40, tops + 7), (cx + 50, tops + 14), (cx + 50, tops + 24), (cx + 40, tops + 31)):
        draw.polygon(star_points(sx, sy, 5, 2), fill=GOLD)
    # Russia: white, blue, red stripes.
    rx = poles[1] + 6
    for j, col in enumerate((WHITE, (0, 82, 180), RED)):
        draw.rectangle([rx, tops + j * fh // 3, rx + fw, tops + (j + 1) * fh // 3], fill=col)
    draw.rectangle([rx, tops, rx + fw, tops + fh], outline=GREY, width=1)
    # United States: stripes and a starred canton.
    ux = poles[2] + 6
    for j in range(7):
        draw.rectangle([ux, tops + j * fh // 7, ux + fw, tops + (j + 1) * fh // 7],
                       fill=RED if j % 2 == 0 else WHITE)
    draw.rectangle([ux, tops, ux + 30, tops + 25], fill=NAVY)
    for r in range(3):
        for c in range(4):
            draw.ellipse([ux + 4 + c * 7, tops + 4 + r * 7, ux + 7 + c * 7, tops + 7 + r * 7], fill=WHITE)


def draw_capitol(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(232, 236, 242))
    # Capitol dome and columns on the left, kept inside the art box.
    cx = x0 + 108
    base = y1 - 6
    draw.rectangle([cx - 8, y0 + 4, cx + 8, y0 + 18], fill=INK)
    draw.polygon([(cx - 8, y0 + 4), (cx + 22, y0 + 9), (cx - 8, y0 + 14)], fill=RED)
    draw.pieslice([cx - 52, y0 + 14, cx + 52, y0 + 92], 180, 360, fill=(120, 130, 148))
    draw.rectangle([cx - 58, y0 + 50, cx + 58, y0 + 57], fill=(120, 130, 148))
    for i in range(6):
        colx = cx - 50 + i * 20
        draw.rectangle([colx, y0 + 57, colx + 10, base], fill=(160, 168, 180))
    draw.rectangle([cx - 64, base, cx + 64, base + 3], fill=(120, 130, 148))
    # Senate bars on the right: party names inside the bars, totals beside.
    bx = x0 + 218
    big = font(SANS_BOLD, 34)
    inside = font(SANS_BOLD, 17)
    draw.rectangle([bx, y0 + 12, bx + 168, y0 + 34], fill=(37, 99, 235))
    draw.text((bx + 8, y0 + 14), "DEM", font=inside, fill=WHITE)
    draw.text((bx + 176, y0 + 8), "56", font=big, fill=(37, 99, 235))
    draw.rectangle([bx, y0 + 48, bx + 132, y0 + 70], fill=RED)
    draw.text((bx + 8, y0 + 50), "REP", font=inside, fill=WHITE)
    draw.text((bx + 140, y0 + 44), "44", font=big, fill=RED)


def draw_cyclone(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=SEA_DARK)
    cx, cy = (x0 + x1) // 2 - 20, (y0 + y1) // 2
    # Spiral bands: arcs of growing radius, sized to fill the art box.
    for i, r in enumerate(range(12, 48, 9)):
        start = i * 70
        draw.arc([cx - r, cy - r, cx + r, cy + r], start, start + 300, fill=WHITE, width=6)
    draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=GOLD)
    # Island dots and wind arrows.
    for ix, iy in ((x0 + 24, y1 - 22), (x1 - 30, y0 + 20), (x1 - 66, y1 - 18)):
        draw.ellipse([ix - 8, iy - 5, ix + 8, iy + 5], fill=(86, 168, 92))
    draw.line([(x0 + 18, y0 + 18), (x0 + 58, y0 + 30)], fill=LIGHT, width=3)
    draw.polygon([(x0 + 58, y0 + 30), (x0 + 44, y0 + 24), (x0 + 48, y0 + 36)], fill=LIGHT)


def panel(draw, x0, y0, x1, y1, tag, headline, deck_lines, art):
    draw.rectangle([x0, y0, x1, y1], fill=PAPER, outline=INK, width=3)
    art(draw, x0 + 8, y0 + 8, x1 - 8, y0 + 96)
    tag_f = font(SANS_BOLD, 20)
    draw.text((x0 + 14, y0 + 104), tag, font=tag_f, fill=RED)
    head_f = font(SANS_BOLD, 33)
    draw.text((x0 + 14, y0 + 128), headline, font=head_f, fill=INK)
    deck_f = font(SANS, 24)
    for i, line in enumerate(deck_lines):
        draw.text((x0 + 14, y0 + 168 + i * 28), line, font=deck_f, fill=(44, 50, 64))


def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 1014, 1014], outline=INK, width=5)

    # Masthead: the date is the largest thing on the page.
    centred(draw, 512, 28, "THE WORLD IN ONE IMAGE", font(SANS_BOLD, 23), NAVY)
    centred(draw, 512, 52, "18 NOVEMBER 2026", font(SERIF_BOLD, 82), INK)
    centred(draw, 512, 142, "WEDNESDAY  \u2022  SEVEN STORIES, FIVE CONTINENTS",
            font(SANS_BOLD, 22), GREY)
    draw.line([(24, 172), (1000, 172)], fill=INK, width=4)
    draw.line([(24, 178), (1000, 178)], fill=INK, width=1)

    # Lead story: the Gulf.
    draw.rectangle([24, 188, 1000, 420], fill=NAVY)
    draw.text((44, 202), "THE GULF  \u2022  LEAD STORY", font=font(SANS_BOLD, 21), fill=GOLD)
    head = font(SANS_BOLD, 47)
    draw.text((44, 228), "IRAN STRIKES", font=head, fill=WHITE)
    draw.text((44, 280), "US BASES IN GULF", font=head, fill=WHITE)
    deck = font(SANS, 28)
    draw.text((44, 342), "Drones hit Kuwait and Bahrain", font=deck, fill=LIGHT)
    draw.text((44, 374), "after US strike on Qeshm Island", font=deck, fill=LIGHT)
    draw_gulf_map(draw, 636, 200, 984, 408)

    # Two picture panels: Crimea and Shenzhen.
    panel(draw, 24, 432, 500, 662, "UKRAINE  \u2022  EUROPE", "CRIMEA BRIDGE DOWN",
          ["227m road arch fell into", "the Kerch Strait; road shut"], draw_bridge)
    panel(draw, 524, 432, 1000, 662, "CHINA  \u2022  DIPLOMACY", "TRUMP IN SHENZHEN",
          ["Xi greets him on arrival;", "summit with Putin Thursday"], draw_flags)

    # Two picture panels: Alaska and the cyclone.
    panel(draw, 24, 674, 500, 904, "UNITED STATES  \u2022  POLITICS", "PELTOLA WINS ALASKA",
          ["Democrats take the Senate,", "56 seats to 44"], draw_capitol)
    panel(draw, 524, 674, 1000, 904, "PACIFIC  \u2022  WEATHER", "CYCLONE XAVIER HITS",
          ["Category 5 over the Cook", "Islands; gusts 315 km/h"], draw_cyclone)

    # Bottom briefs: health and technology.
    draw.line([(24, 916), (1000, 916)], fill=INK, width=3)
    draw.line([(512, 922), (512, 994)], fill=GREY, width=2)
    brief_head = font(SANS_BOLD, 26)
    brief_body = font(SANS, 23)
    draw.text((30, 924), "EBOLA DOUBLES IN CONGO", font=brief_head, fill=INK)
    draw.text((30, 954), "UN: 11,000+ cases, 5,400 deaths", font=brief_body, fill=(44, 50, 64))
    draw.text((530, 924), "NVIDIA SALES DOUBLE", font=brief_head, fill=INK)
    draw.text((530, 954), "$115.8bn quarter; $130bn guided", font=brief_body, fill=(44, 50, 64))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
