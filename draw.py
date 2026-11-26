#!/usr/bin/env python3
"""Draw the news-image-20261125 entry: Wednesday 25 November 2026 in one page.

Everything is drawn in code with PIL: masthead, timeline strip, illustrated
lead and tier-2 cards, a numbered world map with a Europe zoom inset, the
numbered story list, and a DATE CHECK footer naming the stale stories left
out. No AI-generated imagery; every story below was verified as happening
or first reported on Wednesday 25 November 2026 (any time zone) against two
named outlets before it was placed on the page.

Run: python3 draw.py  ->  entry.png beside this file (1024x1024).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette -------------------------------------------------------------
INK = (26, 24, 22)
PAPER = (247, 243, 234)
NAVY = (27, 42, 74)
NAVY_D = (18, 30, 54)
RED = (176, 32, 40)
GOLD = (176, 138, 44)
TEAL = (23, 96, 104)
GREEN = (46, 110, 58)
GREY = (92, 88, 80)
LIGHT = (236, 230, 216)
CARD = (255, 253, 248)
SKY = (196, 222, 238)
SEA = (140, 186, 214)
LAND = (232, 222, 196)
LAND_E = (205, 190, 150)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

_fonts = {}


def font(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def tw(d, text, f):
    return d.textlength(text, font=f)


def wrap(d, text, f, max_w):
    """Greedy word wrap to max_w pixels; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(d, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, f, fill, max_w, leading, max_lines=None):
    """Draw wrapped text; returns the y just below the last line."""
    lines = wrap(d, text, f, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def chip(d, x, y, text, fill, fg=(255, 255, 255), size=11):
    """Small rounded label; returns its width."""
    f = font(SANS_B, size)
    w = int(tw(d, text, f)) + 12
    rrect(d, [x, y, x + w, y + size + 8], 4, fill=fill)
    d.text((x + 6, y + 3), text, font=f, fill=fg)
    return w


def pin(d, cx, cy, n, r=11, fill=RED):
    """Numbered map pin."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=(255, 255, 255), width=2)
    f = font(SANS_B, 12 if n < 10 else 10)
    t = str(n)
    d.text((cx - tw(d, t, f) / 2, cy - 7), t, font=f, fill=(255, 255, 255))


def diamond(d, cx, cy, s, fill):
    d.polygon([(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)], fill=fill)


def rule(d, x0, x1, y, fill=GOLD, width=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        import math

        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill)


# --- scene illustrations (all vector shapes, no images) -------------------

def scene_ship(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(168, 205, 228))
    sea_y = y1 - 26
    d.rectangle([x0, sea_y, x1, y1], fill=SEA)
    for wx in range(x0 + 8, x1 - 10, 26):
        d.arc([wx, sea_y + 4, wx + 18, sea_y + 14], 0, 180, fill=(220, 240, 250), width=2)
    hull = [(x0 + 18, sea_y), (x1 - 14, sea_y), (x1 - 30, sea_y + 16), (x0 + 34, sea_y + 16)]
    d.polygon(hull, fill=(34, 52, 84))
    cols = [(196, 64, 52), (46, 110, 58), (222, 160, 44), (70, 110, 170), (150, 84, 150)]
    cx = x0 + 26
    for i, c in enumerate(cols):
        d.rectangle([cx, sea_y - 22, cx + 44, sea_y - 2], fill=c, outline=(255, 255, 255), width=1)
        cx += 46
    d.rectangle([x1 - 58, sea_y - 34, x1 - 26, sea_y - 2], fill=(240, 240, 240), outline=(120, 120, 120))
    d.rectangle([x1 - 52, sea_y - 28, x1 - 32, sea_y - 22], fill=(90, 140, 190))
    d.rectangle([x0 + 8, y0 + 8, x0 + 44, y0 + 26], fill=(27, 42, 116))
    star(d, x0 + 26, y0 + 17, 6, (255, 210, 60))
    d.rectangle([x0 + 52, y0 + 8, x0 + 88, y0 + 26], fill=(196, 40, 40))
    star(d, x0 + 62, y0 + 17, 5, (255, 220, 80))
    d.ellipse([x1 - 66, y0 + 6, x1 - 8, y0 + 48], fill=(255, 255, 255), outline=RED, width=3)
    d.text((x1 - 60, y0 + 14), "UP TO", font=font(SANS_B, 10), fill=RED)
    d.text((x1 - 58, y0 + 26), "20%", font=font(SANS_B, 15), fill=RED)


def scene_chart(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(20, 26, 40))
    for gy in range(y0 + 14, y1 - 8, 16):
        d.line([(x0 + 8, gy), (x1 - 8, gy)], fill=(52, 64, 88), width=1)
    pts = []
    n = 16
    for i in range(n):
        px = x0 + 14 + i * (x1 - x0 - 90) / (n - 1)
        drop = (i / (n - 1)) ** 1.6
        py = y0 + 18 + drop * (y1 - y0 - 44) + (6 if i % 3 == 1 else -4 if i % 3 == 2 else 0)
        pts.append((px, py))
    d.line(pts, fill=(255, 92, 92), width=4)
    for px, py in pts[::3]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 170, 170))
    chip_x, chip_y = x0 + 16, y1 - 52
    d.rectangle([chip_x, chip_y, chip_x + 40, chip_y + 40], fill=(240, 180, 60), outline=(255, 255, 255), width=2)
    for p in range(4):
        d.line([(chip_x + 6 + p * 9, chip_y - 6), (chip_x + 6 + p * 9, chip_y)], fill=(240, 180, 60), width=3)
        d.line([(chip_x + 6 + p * 9, chip_y + 40), (chip_x + 6 + p * 9, chip_y + 46)], fill=(240, 180, 60), width=3)
    d.text((chip_x + 9, chip_y + 11), "AI", font=font(SANS_B, 16), fill=(20, 26, 40))
    d.text((x1 - 108, y0 + 6), "KOSPI -6.2%", font=font(SANS_B, 12), fill=(255, 150, 150))
    d.text((x1 - 108, y0 + 20), "SK HYNIX -11.1%", font=font(SANS_B, 10.5), fill=(255, 150, 150))
    d.text((x1 - 108, y0 + 33), "SAMSUNG -9.9%", font=font(SANS_B, 10.5), fill=(255, 150, 150))
    d.text((x1 - 108, y0 + 46), "TAIEX -4.8%", font=font(SANS_B, 10.5), fill=(255, 150, 150))


def scene_rocket(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(14, 22, 48))
    import random

    rnd = random.Random(25)
    for _ in range(40):
        sx, sy = rnd.randint(x0 + 4, x1 - 4), rnd.randint(y0 + 4, y1 - 12)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(200, 215, 255))
    h = y1 - y0
    rx = x0 + 62
    nose_y = y0 + max(4, h // 10)
    shoulder_y = y0 + h // 2
    base_y = y1 - max(10, h // 5)
    d.polygon([(rx, nose_y), (rx - 12, shoulder_y), (rx + 12, shoulder_y)], fill=(240, 240, 240))
    d.rectangle([rx - 12, shoulder_y, rx + 12, base_y], fill=(235, 235, 235))
    d.rectangle([rx - 12, shoulder_y + 4, rx + 12, shoulder_y + 9], fill=RED)
    wy = shoulder_y + (base_y - shoulder_y) // 2
    d.ellipse([rx - 4, wy - 4, rx + 4, wy + 4], fill=(70, 130, 200), outline=(120, 120, 120))
    d.polygon([(rx - 12, base_y), (rx - 24, base_y + 8), (rx - 12, base_y + 8)], fill=(200, 60, 60))
    d.polygon([(rx + 12, base_y), (rx + 24, base_y + 8), (rx + 12, base_y + 8)], fill=(200, 60, 60))
    d.polygon([(rx - 7, base_y + 8), (rx + 7, base_y + 8), (rx, y1 - 2)], fill=(255, 160, 40))
    d.polygon([(rx - 3, base_y + 8), (rx + 3, base_y + 8), (rx, y1 - 5)], fill=(255, 220, 90))
    sx0 = x1 - 130
    sy = y0 + h // 3
    d.rectangle([sx0, sy, sx0 + 90, sy + 14], fill=(210, 215, 225))
    d.rectangle([sx0 + 34, sy - 8, sx0 + 56, sy + 22], fill=(180, 188, 205))
    d.rectangle([sx0 - 26, sy + 3, sx0, sy + 11], fill=(70, 110, 190))
    d.rectangle([sx0 + 90, sy + 3, sx0 + 116, sy + 11], fill=(70, 110, 190))
    d.rectangle([sx0 + 6, y0 + 5, sx0 + 30, y0 + 16], fill=(196, 40, 40))
    star(d, sx0 + 12, y0 + 10, 4, (255, 220, 80))
    d.rectangle([sx0 + 36, y0 + 5, sx0 + 60, y0 + 16], fill=(30, 110, 60))
    d.ellipse([sx0 + 46, y0 + 7, sx0 + 55, y0 + 14], fill=(255, 255, 255))
    d.text((x0 + 8, y1 - 14), "SHENZHOU-24", font=font(SANS_B, 10), fill=(180, 200, 240))
    d.text((sx0 + 18, y1 - 14), "TIANGONG", font=font(SANS_B, 10), fill=(180, 200, 240))


def scene_port_night(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(30, 26, 54))
    h = y1 - y0
    d.ellipse([x1 - 40, y0 + 5, x1 - 20, y0 + 22], fill=(240, 235, 210))
    horizon = y1 - max(8, h // 5)
    d.rectangle([x0, horizon, x1, y1], fill=(20, 40, 70))
    crane_top = y0 + max(10, h // 3)
    for cx in (x0 + 30, x0 + 84, x0 + 138):
        d.rectangle([cx, crane_top, cx + 6, horizon], fill=(70, 66, 90))
        d.rectangle([cx, crane_top, cx + 38, crane_top + 4], fill=(70, 66, 90))
        d.line([(cx + 36, crane_top + 4), (cx + 36, crane_top + 14)], fill=(70, 66, 90), width=2)
    d.rectangle([x0 + 12, horizon - 10, x0 + 92, horizon], fill=(120, 60, 50))
    d.rectangle([x0 + 96, horizon - 10, x0 + 176, horizon], fill=(60, 90, 120))
    ex, ey = x0 + 146, horizon - 12
    for r, c in ((14, (255, 120, 30)), (9, (255, 180, 50)), (5, (255, 230, 130))):
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=c)
    for dx, dy in ((-20, -13), (18, -16), (0, -20), (-10, -6), (12, -5)):
        d.line([(ex, ey), (ex + dx, ey + dy)], fill=(255, 200, 90), width=2)
    d.text((x0 + 30, y0 + 5), "HODEIDAH PORT", font=font(SANS_B, 10), fill=(200, 205, 240))


def scene_courthouse(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(222, 232, 240))
    h = y1 - y0
    base = y1 - max(6, h // 8)
    roof_y = y0 + max(8, h // 6)
    d.polygon([(x0 + 14, roof_y + 10), (x1 - 14, roof_y + 10), ((x0 + x1) // 2, roof_y)], fill=(120, 110, 95))
    d.rectangle([x0 + 14, roof_y + 10, x1 - 14, roof_y + 15], fill=(140, 130, 112))
    for i in range(5):
        cx = x0 + 30 + i * ((x1 - x0 - 60) // 4)
        d.rectangle([cx - 5, roof_y + 17, cx + 5, base - 6], fill=(240, 238, 230), outline=(150, 142, 125))
    d.rectangle([x0 + 10, base - 6, x1 - 10, base], fill=(140, 130, 112))
    d.rectangle([x1 - 52, y0 + 6, x1 - 16, y0 + 20], fill=(30, 110, 60))
    d.polygon([(x1 - 52, y0 + 6), (x1 - 16, y0 + 13), (x1 - 52, y0 + 20)], fill=(240, 200, 40))
    d.rectangle([x0 + 16, y0 + 6, x0 + 58, y0 + 26], fill=(255, 255, 255), outline=(150, 150, 150))
    d.line([(x0 + 20, y0 + 12), (x0 + 54, y0 + 12)], fill=(170, 170, 170), width=2)
    d.line([(x0 + 20, y0 + 18), (x0 + 54, y0 + 18)], fill=(170, 170, 170), width=2)
    d.line([(x0 + 20, y0 + 6), (x0 + 54, y0 + 26)], fill=RED, width=3)
    d.line([(x0 + 54, y0 + 6), (x0 + 20, y0 + 26)], fill=RED, width=3)


def scene_tanker(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(250, 226, 190))
    h = y1 - y0
    road = y1 - max(10, h // 4)
    d.rectangle([x0, road, x1, y1], fill=(90, 88, 84))
    tank_h = max(12, h // 3)
    d.rectangle([x0 + 18, road - tank_h, x0 + 118, road - 3], fill=(210, 214, 220), outline=(110, 110, 110))
    d.ellipse([x0 + 28, road - tank_h + 2, x0 + 48, road - 5], fill=(170, 180, 195))
    d.rectangle([x0 + 122, road - tank_h + 4, x0 + 150, road - 3], fill=(60, 90, 150))
    d.rectangle([x0 + 138, road - tank_h + 8, x0 + 148, road - tank_h + 14], fill=(170, 210, 240))
    for wx in (x0 + 34, x0 + 96, x0 + 134):
        d.ellipse([wx - 8, road - 9, wx + 8, road + 5], fill=(30, 30, 30))
        d.ellipse([wx - 3, road - 4, wx + 3, road], fill=(160, 160, 160))
    flame_top = y0 + 3
    for fx, frac in ((x0 + 40, 0.75), (x0 + 66, 1.0), (x0 + 92, 0.85), (x0 + 116, 0.6)):
        fh = (road - tank_h - flame_top) * frac
        d.polygon([(fx - 9, road - tank_h), (fx + 9, road - tank_h), (fx, road - tank_h - fh)], fill=(240, 110, 30))
        d.polygon([(fx - 5, road - tank_h), (fx + 5, road - tank_h), (fx, road - tank_h - fh * 0.6)], fill=(255, 200, 70))
    d.ellipse([x0 + 52, y0 + 2, x0 + 96, y0 + 14], fill=(120, 118, 115))
    d.ellipse([x0 + 84, y0 + 1, x0 + 120, y0 + 11], fill=(150, 148, 145))


def scene_bill(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(230, 240, 248))
    h = y1 - y0
    hx = x0 + 14
    roof_y = y0 + max(8, h // 5)
    wall_y = roof_y + 12
    d.polygon([(hx, wall_y), (hx + 28, roof_y), (hx + 56, wall_y)], fill=(150, 70, 60))
    d.rectangle([hx + 6, wall_y, hx + 50, y1 - 6], fill=(245, 240, 225), outline=(150, 140, 120))
    d.rectangle([hx + 22, y1 - 22, hx + 35, y1 - 6], fill=(110, 80, 60))
    d.rectangle([hx + 11, wall_y + 6, hx + 20, wall_y + 15], fill=(255, 220, 120))
    d.rectangle([hx + 37, wall_y + 6, hx + 46, wall_y + 15], fill=(255, 220, 120))
    bx = x0 + 84
    d.rectangle([bx, y0 + 5, x1 - 8, y1 - 5], fill=(255, 255, 255), outline=(150, 150, 150))
    d.rectangle([bx, y0 + 5, x1 - 8, y0 + 18], fill=NAVY)
    d.text((bx + 5, y0 + 7), "ENERGY BILL", font=font(SANS_B, 9), fill=(255, 255, 255))
    d.text((bx + 6, y0 + 20), "£2,166", font=font(SANS_B, 18), fill=RED)
    d.text((bx + 6, y1 - 13), "was £1,723", font=font(SANS, 9), fill=GREY)


def scene_treaty(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(190, 222, 240))
    h = y1 - y0
    sea_y = y1 - max(10, h // 4)
    d.rectangle([x0, sea_y, x1, y1], fill=SEA)
    isl_top = sea_y - max(8, h // 5)
    d.polygon([(x0 + 10, sea_y), (x0 + 56, isl_top), (x0 + 102, sea_y)], fill=(90, 160, 90))
    trunk_top = isl_top - max(8, h // 4)
    d.line([(x0 + 56, isl_top), (x0 + 56, trunk_top)], fill=(110, 80, 50), width=3)
    for a in range(-2, 3):
        d.line([(x0 + 56, trunk_top), (x0 + 56 + a * 11, trunk_top - 7 + abs(a) * 3)], fill=(60, 140, 60), width=3)
    d.rectangle([x1 - 96, y0 + 6, x1 - 56, y0 + 22], fill=(27, 42, 116))
    star(d, x1 - 88, y0 + 11, 4, (255, 255, 255))
    star(d, x1 - 68, y0 + 18, 3, (255, 255, 255))
    d.rectangle([x1 - 48, y0 + 6, x1 - 8, y0 + 22], fill=(40, 130, 80))
    star(d, x1 - 40, y0 + 11, 4, (255, 255, 255))
    star(d, x1 - 18, y0 + 18, 3, (255, 255, 255))
    doc_y = sea_y - max(16, h // 3)
    d.rectangle([x0 + 122, doc_y, x0 + 160, sea_y], fill=(255, 255, 255), outline=(140, 140, 140))
    d.line([(x0 + 128, doc_y + 6), (x0 + 154, doc_y + 6)], fill=(170, 170, 170), width=2)
    d.line([(x0 + 128, doc_y + 12), (x0 + 148, doc_y + 12)], fill=(170, 170, 170), width=2)
    d.ellipse([x0 + 142, sea_y - 10, x0 + 156, sea_y - 2], fill=(240, 200, 60), outline=RED)


# --- world map (schematic continents, lon/lat polygons) --------------------

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66), (-80, 62),
     (-78, 58), (-65, 50), (-55, 47), (-65, 44), (-70, 42), (-74, 39), (-76, 35),
     (-80, 31), (-81, 26), (-84, 30), (-89, 29), (-94, 29), (-97, 26), (-97, 22),
     (-94, 18), (-90, 21), (-87, 21), (-86, 16), (-83, 9), (-79, 9), (-81, 13),
     (-84, 16), (-88, 14), (-92, 15), (-97, 16), (-102, 18), (-105, 20), (-110, 23),
     (-114, 29), (-117, 33), (-122, 37), (-124, 42), (-124, 47), (-128, 51), (-133, 56),
     (-150, 60), (-158, 58), (-162, 61), (-168, 66)],
    # South America
    [(-79, 9), (-75, 10), (-72, 12), (-64, 10), (-60, 8), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-39, -13), (-39, -17), (-40, -21), (-48, -26), (-52, -33), (-58, -39),
     (-62, -41), (-65, -45), (-67, -50), (-68, -54), (-71, -54), (-74, -50), (-73, -44),
     (-73, -37), (-71, -30), (-70, -23), (-70, -18), (-75, -15), (-77, -12), (-79, -8),
     (-81, -4), (-80, 1), (-77, 4), (-79, 9)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (34, 28),
     (35, 24), (37, 22), (38, 20), (40, 15), (43, 12), (44, 11), (48, 11), (51, 12),
     (51, 10), (48, 5), (42, -1), (40, -6), (39, -10), (40, -15), (36, -20), (35, -24),
     (33, -26), (31, -29), (27, -33), (20, -35), (18, -32), (16, -28), (14, -22),
     (12, -18), (13, -12), (12, -6), (9, -1), (9, 4), (4, 6), (-2, 5), (-8, 5),
     (-13, 8), (-16, 12), (-17, 15), (-16, 20), (-15, 25), (-10, 29), (-6, 35)],
    # Eurasia
    [(-9, 37), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 49), (2, 51), (5, 53),
     (8, 55), (8, 57), (10, 59), (5, 60), (5, 62), (10, 64), (14, 67), (18, 69),
     (25, 71), (31, 70), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75),
     (100, 77), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 69),
     (170, 67), (178, 66), (178, 65), (170, 60), (162, 58), (158, 52), (156, 51),
     (150, 45), (142, 42), (140, 40), (135, 35), (129, 33), (126, 34), (122, 31),
     (120, 28), (118, 25), (113, 22), (110, 20), (108, 15), (107, 12), (105, 9),
     (103, 8), (101, 6), (100, 8), (98, 10), (97, 15), (94, 17), (92, 16), (91, 22),
     (88, 22), (86, 20), (82, 16), (80, 13), (77, 8), (76, 10), (73, 16), (72, 20),
     (70, 22), (66, 25), (61, 25), (57, 26), (56, 27), (52, 28), (50, 29), (48, 30),
     (50, 26), (54, 24), (56, 26), (58, 23), (59, 22), (55, 17), (52, 15), (48, 14),
     (44, 13), (43, 12), (42, 15), (40, 20), (38, 24), (36, 28), (34, 31), (36, 36),
     (30, 36), (27, 37), (27, 40), (23, 36), (23, 40), (19, 42), (14, 45), (12, 44),
     (10, 44), (8, 44), (7, 44), (3, 43), (3, 42), (0, 39), (-1, 38), (-2, 37),
     (-6, 36), (-9, 37)],
    # Australia
    [(114, -22), (113, -26), (115, -32), (118, -35), (124, -33), (130, -32), (135, -35),
     (138, -35), (140, -38), (145, -38), (147, -38), (150, -37), (153, -30), (153, -27),
     (151, -24), (149, -20), (146, -19), (145, -15), (142, -11), (142, -13), (141, -17),
     (140, -18), (136, -15), (135, -12), (132, -11), (130, -12), (126, -14), (122, -17),
     (118, -20), (114, -22)],
]

ISLANDS = [  # (lon, lat, rx_deg, ry_deg)
    (-3, 54, 3.5, 4.5),   # Britain
    (138, 37, 4, 5),      # Japan (rough)
    (47, -19, 3, 5),      # Madagascar
    (102, 0, 5, 2.5),     # Sumatra
    (108, -7, 5, 1.6),    # Java
    (114, 1, 5, 4),       # Borneo
    (120, -2, 3.5, 3),    # Sulawesi
    (136, -3, 6, 2.5),    # New Guinea
    (122, 13, 3, 4),      # Philippines
    (172, -42, 3, 4),     # New Zealand
    (-42, 72, 7, 5),      # Greenland
    (160, -9, 3, 1.2),    # Solomon Islands
    (121, 24, 1.2, 1.8),  # Taiwan
]


def draw_map(d, box, pins, zoom_box=None, zoom_pins=None):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(188, 216, 234), outline=(120, 140, 160), width=1)

    def proj(lon, lat):
        px = x0 + (lon + 180) / 360 * (x1 - x0)
        py = y0 + (82 - lat) / 140 * (y1 - y0)
        return px, py

    for glon in range(-150, 181, 30):
        gx, _ = proj(glon, 0)
        d.line([(gx, y0), (gx, y1)], fill=(205, 225, 240), width=1)
    for glat in range(-60, 81, 30):
        _, gy = proj(0, glat)
        d.line([(x0, gy), (x1, gy)], fill=(205, 225, 240), width=1)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND, outline=LAND_E)
    for lon, lat, rxd, ryd in ISLANDS:
        cx, cy = proj(lon, lat)
        rx = rxd / 360 * (x1 - x0)
        ry = ryd / 140 * (y1 - y0)
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=LAND, outline=LAND_E)

    # compass rose
    cx, cy = x1 - 26, y1 - 24
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=(90, 110, 130), width=1)
    d.polygon([(cx, cy - 12), (cx - 3, cy), (cx + 3, cy)], fill=RED)
    d.polygon([(cx, cy + 12), (cx - 3, cy), (cx + 3, cy)], fill=(90, 110, 130))
    d.text((cx - 3, cy - 24), "N", font=font(SANS_B, 10), fill=INK)

    for n, lon, lat in pins:
        px, py = proj(lon, lat)
        pin(d, px, py, n)

    if zoom_box and zoom_pins:
        zx0, zy0, zx1, zy1 = zoom_box
        d.rectangle(zoom_box, fill=(196, 222, 238), outline=(90, 110, 130), width=2)
        d.rectangle([zx0, zy0, zx1, zy0 + 14], fill=NAVY)
        d.text((zx0 + 5, zy0 + 2), "EUROPE — ZOOM", font=font(SANS_B, 9), fill=(255, 255, 255))

        def zproj(lon, lat):
            px = zx0 + (lon + 12) / 66 * (zx1 - zx0)
            py = zy0 + 14 + (64 - lat) / 30 * (zy1 - zy0 - 14)
            return px, py

        eu = [p for p in CONTINENTS[3] if -12 <= p[0] <= 50 and 34 <= p[1] <= 64]
        if len(eu) > 2:
            d.polygon([zproj(lon, lat) for lon, lat in eu], fill=LAND, outline=LAND_E)
        for n, lon, lat in zoom_pins:
            px, py = zproj(lon, lat)
            pin(d, px, py, n, r=10)


# --- story data (all verified Wed 25 Nov 2026, two named outlets each) -----

LEADS = [
    dict(
        n=1, kicker="WASHINGTON · TRADE", tag="OFFICIAL", tagc=NAVY,
        head="US proposes tariffs on 14 economies",
        body="Section 301 plan: China up to 20%, EU 15%, India 25%, Vietnam 35%. Hearing 25 Jan 2027; not in force yet.",
        why="Washington's biggest tariff move of the year, aimed at 14 partners at once.",
        scene=scene_ship,
    ),
    dict(
        n=2, kicker="SEOUL · TOKYO · TAIPEI · MARKETS", tag="CONFIRMED", tagc=TEAL,
        head="AI doubts sink Asian chip stocks: Kospi −6.2%",
        body="Kospi ends at 4,697.51; SK hynix −11.1%, Samsung −9.9%. Taiex −4.8% after Tuesday's record, Nikkei −2.8%.",
        why="Investors doubt the AI spending boom will pay off — a day after a record rally.",
        scene=scene_chart,
    ),
    dict(
        n=3, kicker="JIUQUAN, CHINA · SPACE", tag="OFFICIAL", tagc=NAVY,
        head="Pakistan's first astronaut docks at Tiangong",
        body="Shenzhou-24 launched 00:18 UTC, docked 03:56 UTC. Muhammad Zeeshan Ali, first foreigner on China's station, stays about a week.",
        why="China's space station takes its first foreign astronaut.",
        scene=scene_rocket,
    ),
]

TIER2 = [
    dict(
        n=4, kicker="HODEIDAH, YEMEN · WAR", tag="OFFICIAL", tagc=NAVY,
        head="Saudi-led coalition strikes Hodeidah port",
        body="Raids early Wed after Houthis threatened Jeddah, Saudi ports.",
        scene=scene_port_night,
    ),
    dict(
        n=5, kicker="CAPE TOWN · COURTS", tag="CONFIRMED", tagc=TEAL,
        head="Court sets aside Phala Phala report",
        body="Bench voids the 2022 sofa-cash report; impeachment collapses.",
        scene=scene_courthouse,
    ),
    dict(
        n=6, kicker="GIZA, EGYPT · DISASTER", tag="REPORTED", tagc=(150, 100, 20),
        head="Fuel tanker fire kills 31+ near Cairo",
        body="Tanker overturned on the Ring Road Wed evening; 21 injured.",
        scene=scene_tanker,
    ),
    dict(
        n=7, kicker="LONDON · ENERGY", tag="OFFICIAL", tagc=NAVY,
        head="UK energy price cap to rise 26%",
        body="Ofgem: typical bill £1,723 → £2,166 a year from 1 Jan 2027.",
        scene=scene_bill,
    ),
    dict(
        n=8, kicker="CANBERRA · DIPLOMACY", tag="OFFICIAL", tagc=NAVY,
        head="Solomons sign security pact with Australia",
        body="Australia 'primary security partner'; no foreign bases.",
        scene=scene_treaty,
    ),
]

ALSO = [
    ("Kyiv", "Russian strikes kill 5, cut power in 5 regions — Zaporizhzhia plant on diesel, 17th grid loss (Reuters)."),
    ("Samara", "Ukrainian drones hit Syzran, Kuibyshev refineries — Kyiv says; 145 drones downed, 1 killed (Reuters)."),
    ("Washington", "US Q3 GDP revised up to 4.3% — from 3.4%; fastest in 3 years (BEA)."),
    ("New York", "Wall Street Wed — Dow +0.33% to 50,182.95, Nasdaq −0.62% (Reuters/AP)."),
    ("Iowa", "Army detonates ~9,500 lb lead azide — whole US stockpile; zero lead detected (AP)."),
    ("Cartagena", "Supermarket siege ends, all hostages freed — 1 captor killed, 4 detained (AFP/Reuters)."),
    ("Dhaka", "Garment minimum wage rises 36% — 12,500 → 17,500 taka a month (AFP)."),
    ("Pyongyang", "North Korea expels Swiss envoy — 48 hours to leave, office to close (KCNA/Reuters)."),
    ("Karachi", "Building collapse kills 3, injures 14 — 6-storey block under construction (Dawn/AFP)."),
    ("Kuala Lumpur", "Malaysia sues Google RM600m — over YouTube gambling, scam content (Reuters)."),
    ("Sydney", "Australia inflation jumps to 4.9% in October — trimmed mean 3.8% (ABS)."),
    ("Canberra", "Defence apology to LGBTQIA+ personnel — delivered Wed, 34 years after ban lifted (Defence/AAP)."),
    ("Flinders Island", "Bushfire evacuations — 9 people lifted out by police boat Wed (AAP/ABC)."),
    ("Brussels", "EU unveils Quantum Act, €50bn tech fund — quantum leadership by 2030 (Reuters)."),
    ("Athens", "24-hour strike halts ferries, grounds flights — 32 flights cancelled (Reuters/AFP)."),
    ("Paris", "Eurostar surprise strike cancels 8 trains — ~80% of London–Paris ran (Eurostar/Reuters)."),
    ("Europe", "Champions League Wed — Lille 2-1 Bayern, PSG 2-2 Roma, Liverpool 3-0 Brugge (UEFA)."),
    ("Ras Tanura", "4 Houthi drones downed; fire claim — satellite shows smoke; hit unconfirmed (Reuters). CLAIM"),
    ("Hormuz", "Iran says 2 more tankers hit mines — no names, unverified (Reuters/IRNA). CLAIM"),
    ("Gaza City", "Israeli strike kills Hamas security chief — Abu al-Ouf, wife, 2 daughters (Xinhua/IDF)."),
    ("Jerusalem", "Judges urge dropping Netanyahu bribery charge — Case 4000 'unlikely to convict' (Reuters)."),
    ("Enugu", "Nollywood legend Pete Edochie dies at 79 — announced Wed by family (Radio Nigeria)."),
    ("Addis Ababa", "Africa CDC/WHO $1.576bn Ebola plan — Bundibugyo plan to May 2027 (Africa CDC)."),
    ("World", "16 Days of Activism begins — UN day to end violence against women (UN Women)."),
    ("Bogor", "Rescuers recover 9 dead Wed, 17 trapped — mine flooded Mon; 325 rescuers (AP)."),
    ("Blue Nile", "19 dead in RSF drone strikes, toll reported Wed — struck Tue (Reuters)."),
]

PINS = [  # (n, lon, lat) for stories 1-13
    (1, -77, 39), (2, 127, 37), (3, 100, 41), (4, 43, 15), (5, 18, -34),
    (6, 31, 30), (7, 0, 51), (8, 160, -9), (9, 30, 50), (10, 48, 53),
    (11, -84, 32), (12, -70, 44), (13, -91, 41),
]
ZOOM_PINS = [(7, 0, 51), (9, 30, 50), (10, 48, 53)]

REGIONS = [
    ("EUROPE", 7, (27, 42, 74)), ("ASIA", 7, (176, 32, 40)),
    ("AMERICAS", 5, (46, 110, 58)), ("MIDDLE EAST", 5, (150, 100, 20)),
    ("AFRICA", 5, (120, 70, 140)), ("OCEANIA", 4, (23, 96, 104)),
    ("GLOBAL", 1, (92, 88, 80)),
]

TIMELINE = [
    ("00:18", "Shenzhou-24 lifts off"),
    ("03:56", "Docks at Tiangong"),
    ("07:00", "Ofgem cap +26%"),
    ("13:30", "US GDP revised to 4.3%"),
    ("21:00", "Wall Street closes"),
]

DATE_CHECK = (
    "Every story above happened or was first reported on Wednesday 25 November 2026. "
    "Left out as other days' news: UN femicide report (Tue 24) · Senegal AFCON title restored (Tue 24) · "
    "Nigeria rate hold (Tue 24) · Abu Nahel killing (Tue 24) · Zambia treason indictment (Mon 23) · "
    "Bogor mine flood itself (Mon 23) · RSF Blue Nile strikes (Tue 24) · Cameroon elephant death (19 Nov) · "
    "Nvidia +31.5% on Huang's return (Mon 23). NOT YET: US Thanksgiving (Thu 26) · USTR tariff hearing "
    "(25 Jan 2027) · UK cap rise (1 Jan 2027)."
)
SOURCES = (
    "Sources: Reuters · AP · AFP · Xinhua · Yonhap · ABS · BEA · Ofgem · UEFA · Al Jazeera · Dawn. "
    "Every drawing original, made in code. Entry by @herza-afril."
)


# --- card renderers ----------------------------------------------------------

def lead_card(d, x, y, w, h, s):
    rrect(d, [x, y, x + w, y + h], 6, fill=CARD, outline=(190, 182, 165), width=1)
    scene_h = 60
    s["scene"](d, [x + 4, y + 4, x + w - 4, y + 4 + scene_h])
    d.ellipse([x + 8, y + 8, x + 34, y + 34], fill=RED, outline=(255, 255, 255), width=2)
    d.text((x + 17, y + 13), str(s["n"]), font=font(SANS_B, 15), fill=(255, 255, 255))
    ty = y + 4 + scene_h + 5
    d.text((x + 10, ty), s["kicker"], font=font(SANS_B, 10), fill=GREY)
    twd = int(tw(d, s["tag"], font(SANS_B, 10))) + 12
    chip(d, x + w - twd - 8, ty - 2, s["tag"], s["tagc"], size=10)
    ty += 15
    ty = text_block(d, x + 10, ty, s["head"], font(SERIF_B, 17), INK, w - 20, 19, max_lines=2)
    ty = text_block(d, x + 10, ty + 2, s["body"], font(SANS, 11), (52, 48, 44), w - 20, 13, max_lines=3)
    d.text((x + 10, ty + 3), "WHY IT MATTERS", font=font(SANS_B, 9), fill=RED)
    text_block(d, x + 10, ty + 15, s["why"], font(SANS, 10), (52, 48, 44), w - 20, 12.5, max_lines=2)


def tier2_card(d, x, y, w, h, s):
    rrect(d, [x, y, x + w, y + h], 6, fill=CARD, outline=(190, 182, 165), width=1)
    scene_h = 52
    s["scene"](d, [x + 3, y + 3, x + w - 3, y + 3 + scene_h])
    d.ellipse([x + 6, y + 6, x + 26, y + 26], fill=RED, outline=(255, 255, 255), width=2)
    d.text((x + 12, y + 9), str(s["n"]), font=font(SANS_B, 12), fill=(255, 255, 255))
    ty = y + 3 + scene_h + 4
    d.text((x + 7, ty), s["kicker"], font=font(SANS_B, 8.5), fill=GREY)
    twd = int(tw(d, s["tag"], font(SANS_B, 9))) + 12
    chip(d, x + w - twd - 5, ty - 1, s["tag"], s["tagc"], size=9)
    ty += 13
    ty = text_block(d, x + 7, ty, s["head"], font(SERIF_B, 13), INK, w - 14, 15, max_lines=2)
    text_block(d, x + 7, ty + 1, s["body"], font(SANS, 9.5), (52, 48, 44), w - 14, 11, max_lines=2)


# --- page assembly -----------------------------------------------------------

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 18
    CW = W - 2 * M

    # masthead
    d.rectangle([M, 8, M + CW, 30], fill=NAVY)
    d.text((M + 10, 12), "THE WORLD IN ONE DAY", font=font(SANS_B, 12), fill=(255, 255, 255))
    right = "34 STORIES · 7 REGIONS · EVERY ONE DATED WEDNESDAY"
    d.text((M + CW - 10 - tw(d, right, font(SANS_B, 11)), 13), right, font=font(SANS_B, 11), fill=(255, 220, 130))
    title = "Wednesday 25 November 2026"
    tf = font(SERIF_B, 50)
    while tw(d, title, tf) > CW - 90:
        tf = font(SERIF_B, tf.size - 2)
    diamond(d, M + 22, 60, 8, RED)
    diamond(d, M + CW - 22, 60, 8, RED)
    d.text(((W - tw(d, title, tf)) / 2, 33), title, font=tf, fill=INK)
    sub = "US tariffs on 14 economies · Kospi −6.2% in chip rout · Pakistan's first astronaut docks at Tiangong"
    sf = font(SERIF, 15)
    d.text(((W - tw(d, sub, sf)) / 2, 87), sub, font=sf, fill=RED)
    rule(d, M, M + CW, 105, fill=NAVY, width=2)

    # timeline strip
    ty0, ty1 = 109, 143
    d.rectangle([M, ty0, M + CW, ty1], fill=NAVY_D)
    d.text((M + 10, ty0 + 3), "WEDNESDAY'S TIMELINE · UTC", font=font(SANS_B, 10), fill=(255, 220, 130))
    slot = (CW - 20) / len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        sx = M + 10 + i * slot
        d.text((sx, ty0 + 17), t, font=font(SANS_B, 12), fill=(255, 255, 255))
        d.text((sx + 42, ty0 + 19), label, font=font(SANS, 9.5), fill=(210, 220, 240))

    # leads
    ly = 149
    lw = (CW - 22) // 3
    for i, s in enumerate(LEADS):
        lead_card(d, M + i * (lw + 11), ly, lw, 208, s)

    # tier-2
    t2y = ly + 208 + 6
    t2w = (CW - 32) // 5
    for i, s in enumerate(TIER2):
        tier2_card(d, M + i * (t2w + 8), t2y, t2w, 128, s)

    # map band
    my = t2y + 128 + 6
    d.text((M, my), "WHERE IT HAPPENED — NUMBERED PINS MATCH THE STORIES", font=font(SANS_B, 11), fill=INK)
    map_box = [M, my + 16, M + 640, my + 112]
    zoom_box = [M + 6, my + 22, M + 156, my + 88]
    draw_map(d, map_box, PINS, zoom_box=zoom_box, zoom_pins=ZOOM_PINS)
    kx = M + 652
    d.text((kx, my + 16), "THE DAY BY REGION", font=font(SANS_B, 12), fill=INK)
    ry = my + 34
    for name, count, col in REGIONS:
        d.rectangle([kx, ry + 2, kx + 12, ry + 11], fill=col)
        d.text((kx + 18, ry), name, font=font(SANS_B, 11), fill=INK)
        d.text((M + CW - 16 - tw(d, str(count), font(SANS_B, 12)), ry), str(count), font=font(SANS_B, 12), fill=INK)
        ry += 14
    d.text((kx, ry + 2), "34 stories · 2 on the Ukraine war", font=font(SANS, 10), fill=GREY)

    # ALSO list
    ay = my + 112 + 6
    d.text((M, ay), "ALSO TODAY — 26 MORE VERIFIED STORIES", font=font(SANS_B, 12), fill=INK)
    rule(d, M, M + CW, ay + 17, fill=(190, 182, 165), width=1)
    col_w = (CW - 14) // 2
    row_h = 22.5
    ly2 = ay + 21
    for idx, (place, text) in enumerate(ALSO):
        n = 9 + idx
        col = 0 if idx < 13 else 1
        row = idx if idx < 13 else idx - 13
        x = M + col * (col_w + 14)
        y = ly2 + row * row_h
        if row % 2 == 0:
            d.rectangle([x - 3, y - 1, x + col_w + 3, y + row_h - 2], fill=(241, 236, 224))
        d.ellipse([x, y + 1, x + 17, y + 18], fill=NAVY)
        nf = font(SANS_B, 9)
        d.text((x + 8.5 - tw(d, str(n), nf) / 2, y + 4), str(n), font=nf, fill=(255, 255, 255))
        line = f"{place}: {text}"
        text_block(d, x + 22, y + 1, line, font(SANS, 9.5), INK, col_w - 24, 11, max_lines=2)

    # DATE CHECK footer
    fy = int(ly2 + 13 * row_h) + 7
    rrect(d, [M, fy, M + CW, fy + 48], 5, fill=(250, 247, 240), outline=RED, width=1)
    d.text((M + 10, fy + 6), "DATE CHECK", font=font(SANS_B, 11), fill=RED)
    text_block(d, M + 96, fy + 6, DATE_CHECK, font(SANS, 9.5), INK, CW - 106, 12, max_lines=3)
    d.text((M + 10, fy + 52), SOURCES, font=font(SANS, 9.5), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
