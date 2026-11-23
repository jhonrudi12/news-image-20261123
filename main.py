#!/usr/bin/env python3
"""The World Today -- 23 November 2026.

Draws a newspaper-style front page summing up the world's news of
Monday 23 November 2026 in a single 1024x1024 PNG.

Pure Python 3 standard library only: no network, no fonts, no image
libraries. The picture is drawn pixel by pixel with an embedded 5x7
bitmap font and simple vector shapes, so two runs write byte-identical
output. Writes to $MAKEFUN_OUTPUT_DIR (default /output).
"""

import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (245, 239, 224)
INK = (26, 23, 18)
NAVY = (22, 35, 63)
GOLD = (201, 162, 39)
RED = (166, 38, 29)
BLUE = (31, 78, 121)
TEAL = (15, 107, 92)
OCHRE = (154, 106, 0)
PLUM = (91, 58, 142)
GREEN = (46, 107, 46)
CELLBG = (255, 253, 246)
LEADBG = (239, 231, 210)
BORDER = (216, 207, 184)
WHITE = (255, 255, 255)
CREAM = (245, 239, 224)
SKY = (174, 205, 226)
SEA = (46, 90, 140)
FLAME = (224, 110, 30)
FLAME2 = (240, 180, 40)
GREY = (120, 116, 108)
DARKGREY = (74, 70, 64)

# ---------------------------------------------------------------- font
# 5x7 bitmap glyphs, '#' = ink. Written for this page only.
FONT = {}
def _g(ch, rows):
    FONT[ch] = rows

_g('A', [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"])
_g('B', ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."])
_g('C', [".####", "#....", "#....", "#....", "#....", "#....", ".####"])
_g('D', ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."])
_g('E', ["#####", "#....", "#....", "####.", "#....", "#....", "#####"])
_g('F', ["#####", "#....", "#....", "####.", "#....", "#....", "#...."])
_g('G', [".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."])
_g('H', ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"])
_g('I', ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"])
_g('J', ["..###", "....#", "....#", "....#", "....#", "#...#", ".###."])
_g('K', ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"])
_g('L', ["#....", "#....", "#....", "#....", "#....", "#....", "#####"])
_g('M', ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"])
_g('N', ["#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"])
_g('O', [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."])
_g('P', ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."])
_g('Q', [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"])
_g('R', ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"])
_g('S', [".####", "#....", "#....", ".###.", "....#", "....#", "####."])
_g('T', ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."])
_g('U', ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."])
_g('V', ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."])
_g('W', ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"])
_g('X', ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"])
_g('Y', ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."])
_g('Z', ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"])
_g('0', [".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."])
_g('1', ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."])
_g('2', [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"])
_g('3', ["####.", "....#", "....#", ".###.", "....#", "....#", "####."])
_g('4', ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."])
_g('5', ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."])
_g('6', [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."])
_g('7', ["#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."])
_g('8', [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."])
_g('9', [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."])
_g('a', [".....", ".....", ".###.", "....#", ".####", "#...#", ".####"])
_g('b', ["#....", "#....", "####.", "#...#", "#...#", "#...#", "####."])
_g('c', [".....", ".....", ".####", "#....", "#....", "#....", ".####"])
_g('d', ["....#", "....#", ".####", "#...#", "#...#", "#...#", ".####"])
_g('e', [".....", ".....", ".###.", "#...#", "#####", "#....", ".###."])
_g('f', ["..##.", ".#..#", ".#...", "###..", ".#...", ".#...", ".#..."])
_g('g', [".....", ".####", "#...#", "#...#", ".####", "....#", ".###."])
_g('h', ["#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"])
_g('i', ["..#..", ".....", ".##..", "..#..", "..#..", "..#..", ".###."])
_g('j', ["....#", ".....", "...##", "....#", "....#", "#...#", ".###."])
_g('k', ["#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."])
_g('l', [".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."])
_g('m', [".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"])
_g('n', [".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"])
_g('o', [".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."])
_g('p', [".....", ".....", "####.", "#...#", "#...#", "####.", "#...."])
_g('q', [".....", ".....", ".####", "#...#", "#...#", ".####", "....#"])
_g('r', [".....", ".....", "#.##.", "##..#", "#....", "#....", "#...."])
_g('s', [".....", ".....", ".####", "#....", ".###.", "....#", "####."])
_g('t', [".#...", ".#...", "###..", ".#...", ".#...", ".#..#", "..##."])
_g('u', [".....", ".....", "#...#", "#...#", "#...#", "#..##", ".##.#"])
_g('v', [".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."])
_g('w', [".....", ".....", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"])
_g('x', [".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"])
_g('y', [".....", ".....", "#...#", "#...#", ".####", "....#", ".###."])
_g('z', [".....", ".....", "#####", "...#.", "..#..", ".#...", "#####"])
_g(' ', [".....", ".....", ".....", ".....", ".....", ".....", "....."])
_g('.', [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."])
_g(',', [".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."])
_g(':', [".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."])
_g(';', [".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."])
_g('!', ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."])
_g('?', [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."])
_g("'", ["..#..", "..#..", ".#...", ".....", ".....", ".....", "....."])
_g('"', [".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."])
_g('-', [".....", ".....", ".....", ".###.", ".....", ".....", "....."])
_g('(', ["...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"])
_g(')', ["##...", "..#..", "...#.", "...#.", "...#.", "..#..", "##..."])
_g('/', ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."])
_g('&', [".###.", "#...#", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"])
_g('%', ["##..#", "##.#.", "...#.", "..#..", ".#...", "#.##", "#..##"])
_g('+', [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."])
_g('=', [".....", ".....", "#####", ".....", "#####", ".....", "....."])
_g('$', ["..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."])
_g('#', [".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."])
_g('*', [".....", ".#.#.", ".###.", "#####", ".###.", ".#.#.", "....."])
_g('_', [".....", ".....", ".....", ".....", ".....", ".....", "#####"])
_g('~', [".....", ".....", ".##.#", "#.##.", ".....", ".....", "....."])

BLANK = ["....."] * 7


def text_w(s, scale):
    """Pixel width of s at the given scale (6 px per glyph incl. spacing)."""
    return len(s) * 6 * scale - scale


def wrap(text, max_w, scale):
    """Word-wrap text to lines fitting max_w pixels at scale."""
    lines = []
    for raw in text.split("\n"):
        words = raw.split(" ")
        cur = ""
        for wd in words:
            trial = wd if not cur else cur + " " + wd
            if text_w(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w=W, h=H):
        self.w = w
        self.h = h
        self.px = bytearray(PAPER * w * h)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            self.px[base:base + (x1 - x0) * 3] = bytes(c) * (x1 - x0)

    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.rect(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.rect(x0 - t // 2, y0 - t // 2, t, t, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=True):
        for yy in range(cy - r, cy + r + 1):
            dx = int((r * r - (yy - cy) * (yy - cy)) ** 0.5) if abs(yy - cy) <= r else 0
            if fill:
                self.rect(cx - dx, yy, 2 * dx + 1, 1, c)
            else:
                self.set(cx - dx, yy, c)
                self.set(cx + dx, yy, c)

    def tri(self, x0, y0, x1, y1, x2, y2, c):
        ymin = min(y0, y1, y2)
        ymax = max(y0, y1, y2)
        for yy in range(ymin, ymax + 1):
            xs = []
            for (ax, ay, bx, by) in ((x0, y0, x1, y1), (x1, y1, x2, y2), (x2, y2, x0, y0)):
                if ay == by:
                    continue
                if (ay <= yy < by) or (by <= yy < ay):
                    xs.append(ax + (yy - ay) * (bx - ax) / (by - ay))
            if len(xs) >= 2:
                self.rect(int(min(xs)), yy, int(max(xs)) - int(min(xs)) + 1, 1, c)

    def glyph(self, ch, x, y, scale, c):
        rows = FONT.get(ch, BLANK)
        for r, row in enumerate(rows):
            for col, bit in enumerate(row):
                if bit == '#':
                    self.rect(x + col * scale, y + r * scale, scale, scale, c)

    def text(self, s, x, y, scale, c, align="left"):
        if align == "center":
            x -= text_w(s, scale) // 2
        elif align == "right":
            x -= text_w(s, scale)
        cx = x
        for ch in s:
            self.glyph(ch, cx, y, scale, c)
            cx += 6 * scale
        return cx

    def para(self, text, x, y, max_w, scale, c, leading=None):
        """Draw wrapped text; returns y just below the last line."""
        lh = leading if leading is not None else 7 * scale + 3
        for ln in wrap(text, max_w, scale):
            self.text(ln, x, y, scale, c)
            y += lh
        return y


def write_png(cv, path):
    raw = bytearray()
    stride = cv.w * 3
    for yy in range(cv.h):
        raw.append(0)
        raw += cv.px[yy * stride:(yy + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(typ, data):
        out = struct.pack(">I", len(data)) + typ + data
        out += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)

# ---------------------------------------------------------------- pictograms
def pic_climate(cv, x, y, w, h):
    """Globe with a crack: the climate talks break down."""
    cx, cy, r = x + w // 2, y + h // 2 + 4, 52
    cv.circle(cx, cy, r, SKY)
    cv.circle(cx, cy, r, NAVY, fill=False)
    cv.circle(cx - 18, cy - 12, 12, GREEN)
    cv.circle(cx + 16, cy + 14, 14, GREEN)
    cv.rect(cx - 8, cy - 26, 22, 10, GREEN)
    cv.rect(cx - 30, cy + 18, 16, 8, GREEN)
    cv.line(cx - r + 6, cy - 20, cx - 8, cy - 2, RED, 3)
    cv.line(cx - 8, cy - 2, cx + 6, cy + 12, RED, 3)
    cv.line(cx + 6, cy + 12, cx + r - 8, cy + 26, RED, 3)
    sx, sy = x + w - 26, y + 8
    cv.circle(sx, sy, 9, GOLD)
    for dx, dy in ((-14, 0), (14, 0), (0, -14), (0, 14), (-10, -10), (10, 10)):
        cv.line(sx, sy, sx + dx, sy + dy, GOLD, 2)


def pic_ballot(cv, x, y, w, h):
    """Ballot box, a paper going in, and the number 258."""
    cv.rect(x + 28, y + 8, 64, 46, NAVY)
    cv.rect(x + 30, y + 10, 60, 42, WHITE)
    cv.line(x + 38, y + 34, x + 50, y + 46, GREEN, 4)
    cv.line(x + 50, y + 46, x + 80, y + 16, GREEN, 4)
    cv.rect(x + 14, y + 58, 92, 46, NAVY)
    cv.rect(x + 44, y + 54, 32, 6, INK)
    cv.text("258", x + 60, y + 70, 3, WHITE, align="center")


def pic_ship(cv, x, y, w, h):
    """Warship on the sea, hit at Benghazi, with drones above."""
    cv.rect(x, y + h - 26, w, 26, SEA)
    cv.line(x + 6, y + h - 18, x + 30, y + h - 18, WHITE, 2)
    cv.line(x + 44, y + h - 12, x + 78, y + h - 12, WHITE, 2)
    cv.line(x + 84, y + h - 20, x + 112, y + h - 20, WHITE, 2)
    cv.rect(x + 12, y + 62, 96, 16, DARKGREY)
    cv.tri(x + 108, y + 62, x + 118, y + 78, x + 108, y + 78, DARKGREY)
    cv.rect(x + 40, y + 44, 34, 18, GREY)
    cv.vline(x + 56, y + 26, 20, DARKGREY, 3)
    cv.circle(x + 92, y + 40, 12, FLAME)
    cv.circle(x + 92, y + 40, 7, FLAME2)
    cv.line(x + 92, y + 24, x + 92, y + 56, FLAME, 2)
    cv.line(x + 78, y + 28, x + 106, y + 52, FLAME, 2)
    cv.circle(x + 20, y + 16, 3, INK)
    cv.circle(x + 104, y + 12, 3, INK)
    cv.line(x + 20, y + 19, x + 44, y + 42, GREY, 1)
    cv.line(x + 104, y + 15, x + 96, y + 30, GREY, 1)


def pic_fire(cv, x, y, w, h):
    """Factory burning: flames over a sawtooth roof."""
    cv.rect(x + 14, y + 56, 92, 48, DARKGREY)
    cv.tri(x + 14, y + 56, x + 37, y + 38, x + 60, y + 56, GREY)
    cv.tri(x + 60, y + 56, x + 83, y + 38, x + 106, y + 56, GREY)
    for wx in (26, 52, 78):
        cv.rect(x + wx, y + 70, 14, 14, GOLD)
    cv.tri(x + 34, y + 56, x + 48, y + 18, x + 62, y + 56, FLAME)
    cv.tri(x + 58, y + 56, x + 74, y + 26, x + 90, y + 56, FLAME2)
    cv.tri(x + 44, y + 56, x + 54, y + 36, x + 64, y + 56, (250, 220, 90))
    cv.circle(x + 30, y + 14, 8, GREY)
    cv.circle(x + 92, y + 10, 7, GREY)
    cv.circle(x + 60, y + 6, 6, GREY)


def pic_exam(cv, x, y, w, h):
    """Graduation cap over a paper marked AI, crossed out."""
    cv.tri(x + 14, y + 34, x + 60, y + 12, x + 106, y + 34, INK)
    cv.tri(x + 14, y + 34, x + 60, y + 56, x + 106, y + 34, DARKGREY)
    cv.rect(x + 40, y + 40, 40, 14, INK)
    cv.line(x + 106, y + 34, x + 106, y + 58, GOLD, 3)
    cv.circle(x + 106, y + 62, 4, GOLD)
    cv.rect(x + 22, y + 66, 76, 38, WHITE)
    cv.rect(x + 22, y + 66, 76, 38, NAVY)
    cv.text("AI", x + 44, y + 74, 3, RED)
    cv.line(x + 78, y + 72, x + 94, y + 96, RED, 3)
    cv.line(x + 94, y + 72, x + 78, y + 96, RED, 3)


def pic_flags(cv, x, y, w, h):
    """Nepal's double pennant beside India's tricolour."""
    cv.vline(x + 22, y + 8, 92, INK, 3)
    cv.tri(x + 25, y + 12, x + 25, y + 34, x + 62, y + 28, WHITE)
    cv.tri(x + 27, y + 14, x + 27, y + 32, x + 58, y + 27, RED)
    cv.tri(x + 25, y + 36, x + 25, y + 58, x + 62, y + 52, WHITE)
    cv.tri(x + 27, y + 38, x + 27, y + 56, x + 58, y + 51, RED)
    cv.vline(x + 96, y + 8, 92, INK, 3)
    cv.rect(x + 99, y + 12, 52, 14, (255, 153, 51))
    cv.rect(x + 99, y + 26, 52, 14, WHITE)
    cv.rect(x + 99, y + 40, 52, 14, (19, 136, 8))
    cv.circle(x + 125, y + 33, 7, NAVY, fill=False)
    cv.circle(x + 125, y + 33, 2, NAVY)
    cv.hline(x + 8, y + 100, w - 16, INK, 2)


# ---------------------------------------------------------------- stories
LEAD = {
    "kicker": "CLIMATE - ANTALYA, TURKEY",
    "color": RED,
    "headline": "COP31 COLLAPSES WITHOUT A DEAL",
    "summary": "After two weeks of talks and two days of overtime, the longest climate summit ever ends with no deal - the first collapse since Copenhagen in 2009. The draft never named fossil fuels, and the EU and others refused to back it.",
    "pic": pic_climate,
}

CELLS = [
    {
        "kicker": "USA - POLITICS",
        "color": BLUE,
        "headline": "DEMOCRATS WIN RECORD HOUSE MAJORITY",
        "summary": "Democrats reach 258 House seats, their biggest majority since 1992. Chuck Hubbard beats Rep. Virginia Foxx in N. Carolina.",
        "pic": pic_ballot,
    },
    {
        "kicker": "WAR AT SEA - LIBYA",
        "color": TEAL,
        "headline": "RUSSIAN WARSHIP HIT OFF LIBYA",
        "summary": "Suspected Ukrainian sea drones badly damage the Russian corvette Merkury at Benghazi, Libya, days after a Baltic strike.",
        "pic": pic_ship,
    },
    {
        "kicker": "ASIA - DISASTER",
        "color": OCHRE,
        "headline": "FACTORY FIRE: 50 MISSING IN JAVA",
        "summary": "Seven body bags are recovered and about 50 workers are missing after fire guts a candy factory in Serang, west Java.",
        "pic": pic_fire,
    },
    {
        "kicker": "ASIA - EDUCATION",
        "color": PLUM,
        "headline": "MINISTER QUITS OVER AI EXAM CHEATING",
        "summary": "Education Minister Choi Kyo-jin quits over last-minute anti-cheating rules that sowed chaos before the college entrance exam.",
        "pic": pic_exam,
    },
]

WIDE = {
    "kicker": "ASIA - DIPLOMACY, TODAY",
    "color": GREEN,
    "headline": "NEPAL PM MEETS MODI IN DELHI TODAY",
    "summary": "Nepal's PM Balendra Shah holds delegation talks with PM Modi in Delhi - his first bilateral trip abroad since taking office in March. Trade, energy and connectivity top the agenda.",
    "pic": pic_flags,
}

ALSO = ("ALSO TODAY: Drone strike on a flat near Kyiv leaves 14 missing in Dymer. "
        "Trump vows to work with Democrats to cap credit-card interest at 10%.")


# ---------------------------------------------------------------- layout
def draw_masthead(cv):
    cv.rect(0, 0, W, 150, NAVY)
    cv.text("THE WORLD TODAY", W // 2, 16, 8, CREAM, align="center")
    cv.hline(28, 128, W - 56, GOLD, 3)
    cv.text("MONDAY 23 NOVEMBER 2026", W // 2, 86, 4, GOLD, align="center")
    cv.text("EARLY EDITION", 28, 92, 2, CREAM)
    cv.text("SIX STORIES", W - 28, 92, 2, CREAM, align="right")


def draw_lead(cv):
    x0, y0, x1, y1 = 28, 162, 996, 356
    cv.rect(x0, y0, x1 - x0, y1 - y0, LEADBG)
    cv.rect(x0, y0, x1 - x0, y1 - y0, BORDER)
    cv.text(LEAD["kicker"], x0 + 16, y0 + 12, 2, LEAD["color"])
    y = cv.para(LEAD["headline"], x0 + 16, y0 + 34, 740, 4, INK, leading=31)
    cv.para(LEAD["summary"], x0 + 16, y + 8, 740, 2, INK, leading=17)
    LEAD["pic"](cv, 812, y0 + 22, 168, 150)


def draw_cell(cv, x0, y0, x1, y1, st):
    cv.rect(x0, y0, x1 - x0, y1 - y0, CELLBG)
    cv.rect(x0, y0, x1 - x0, y1 - y0, BORDER)
    cv.text(st["kicker"], x0 + 12, y0 + 10, 2, st["color"])
    y = cv.para(st["headline"], x0 + 12, y0 + 30, x1 - x0 - 24, 3, INK, leading=24)
    cv.para(st["summary"], x0 + 12, y + 6, 306, 2, INK, leading=17)
    st["pic"](cv, x1 - 128, y0 + 66, 120, 110)


def draw_wide(cv):
    x0, y0, x1, y1 = 28, 772, 996, 896
    cv.rect(x0, y0, x1 - x0, y1 - y0, CELLBG)
    cv.rect(x0, y0, x1 - x0, y1 - y0, BORDER)
    cv.text(WIDE["kicker"], x0 + 16, y0 + 10, 2, WIDE["color"])
    y = cv.para(WIDE["headline"], x0 + 16, y0 + 30, 780, 3, INK, leading=24)
    cv.para(WIDE["summary"], x0 + 16, y + 6, 780, 2, INK, leading=17)
    WIDE["pic"](cv, 830, y0 + 10, 150, 108)


def draw_footer(cv):
    y = cv.para(ALSO, 28, 908, 968, 2, INK, leading=17)
    cv.hline(28, 966, 968, INK, 2)
    cv.text("SOURCES: AP, REUTERS, CNN, YONHAP, MEA - EARLY EDITION 07:30 WIB",
            28, 978, 2, DARKGREY)
    cv.text("THE WORLD TODAY", 996, 978, 2, DARKGREY, align="right")


def build():
    cv = Canvas()
    draw_masthead(cv)
    draw_lead(cv)
    cells = [(28, 372, 500, 560), (524, 372, 996, 560),
             (28, 572, 500, 760), (524, 572, 996, 760)]
    for box, st in zip(cells, CELLS):
        draw_cell(cv, *box, st)
    draw_wide(cv)
    draw_footer(cv)
    return cv


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    size = write_png(build(), path)
    print("wrote %s (%d bytes)" % (path, size))


if __name__ == "__main__":
    main()
