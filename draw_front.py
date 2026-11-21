"""Draw the front page for news-image-20261120.

One 1024x1024 newspaper page summing up world news from Friday,
20 November 2026. Deterministic: no randomness, no clock, no network.
Python + Pillow only.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 232)
PAPER2 = (238, 232, 214)
INK = (24, 24, 22)
BODY = (52, 52, 48)
FAINT = (110, 104, 90)
RULE = (24, 24, 22)
RED = (178, 34, 28)
NAVY = (28, 44, 74)
NAVY2 = (18, 30, 54)
GOLD = (214, 164, 62)
TEAL = (31, 120, 110)
BLUE = (52, 96, 168)
STEEL = (74, 112, 148)
DARK_SKYLINE = (12, 22, 44)
PANEL_LINE = (190, 182, 164)
NUM_FG = (240, 238, 230)
NUM_LABEL = (185, 200, 220)
STRIP = (232, 226, 208)
PURPLE = (128, 84, 160)
ORANGE = (255, 140, 0)
YELLOW = (255, 200, 40)

DEJAVU = "/usr/share/fonts/truetype/dejavu/"
LIBERATION = "/usr/share/fonts/truetype/liberation/"

FONTS = {
    "serif_bold": ("DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf"),
    "serif": ("DejaVuSerif.ttf", "LiberationSerif-Regular.ttf"),
    "sans_bold": ("DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"),
    "sans": ("DejaVuSans.ttf", "LiberationSans-Regular.ttf"),
}


def font(name, size):
    """Load a font by short name, falling back to Liberation."""
    primary, fallback = FONTS[name]
    for base, fname in ((DEJAVU, primary), (LIBERATION, fallback)):
        path = os.path.join(base, fname)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit width."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    """Draw lines top-down; returns y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def star_points(cx, cy, r_outer, r_inner, points=5):
    import math

    pts = []
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        angle = -math.pi / 2 + i * math.pi / points
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return pts


# ---------------------------------------------------------------- icons
def icon_clock(draw, x, y, s, color):
    cx, cy, r = x + s / 2, y + s / 2, s / 2 - 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=2)
    draw.line([(cx, cy), (cx, cy - r + 6)], fill=color, width=2)
    draw.line([(cx, cy), (cx + r - 7, cy + 3)], fill=color, width=2)
    draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=color)


def icon_tower(draw, x, y, s, color):
    draw.rectangle([x + 8, y + 6, x + s - 8, y + s - 2], outline=color, width=2)
    draw.polygon([(x + 8, y + 6), (x + s / 2, y + 1), (x + s - 8, y + 6)],
                 outline=color)
    for wy in (y + 11, y + 17):
        for wx in (x + 11, x + s / 2 - 1):
            draw.rectangle([wx, wy, wx + 3, wy + 3], fill=color)
    draw.line([(x + 4, y + s - 2), (x + s - 4, y + s - 2)], fill=color, width=2)


def icon_chart(draw, x, y, s, color):
    draw.line([(x + 3, y + 3), (x + 3, y + s - 4)], fill=color, width=2)
    draw.line([(x + 3, y + s - 4), (x + s - 3, y + s - 4)], fill=color, width=2)
    pts = [(x + 4, y + s - 9), (x + 10, y + 14), (x + 16, y + 18),
           (x + 21, y + 8), (x + s - 4, y + 11)]
    draw.line(pts, fill=color, width=2)
    for px, py in pts:
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=color)


def icon_stars(draw, x, y, s, color):
    import math

    cx, cy, r = x + s / 2, y + s / 2, s / 2 - 4
    for i in range(8):
        angle = i * math.pi / 4
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=color)
    draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=color)


def icon_scales(draw, x, y, s, color):
    cx = x + s / 2
    draw.line([(cx, y + 3), (cx, y + s - 5)], fill=color, width=2)
    draw.line([(x + 4, y + 7), (x + s - 4, y + 7)], fill=color, width=2)
    draw.line([(x + 2, y + s - 3), (x + s - 2, y + s - 3)], fill=color, width=2)
    for px in (x + 6, x + s - 6):
        draw.line([(px, y + 7), (px - 4, y + 15)], fill=color, width=1)
        draw.line([(px, y + 7), (px + 4, y + 15)], fill=color, width=1)
        draw.arc([px - 5, y + 13, px + 5, y + 21], 0, 180, fill=color, width=2)


def icon_cross(draw, x, y, s, color):
    w = 7
    cx, cy = x + s / 2, y + s / 2
    draw.rectangle([cx - w / 2, y + 2, cx + w / 2, y + s - 2], fill=color)
    draw.rectangle([x + 2, cy - w / 2, x + s - 2, cy + w / 2], fill=color)


def icon_star(draw, x, y, s, color):
    pts = star_points(x + s / 2, y + s / 2, s / 2 - 1, (s / 2 - 1) * 0.45)
    draw.polygon(pts, fill=color)


# ---------------------------------------------------------------- lead art
def draw_lead_art(draw, x0, y0, x1, y1):
    """Night sky over Kyiv: skyline, river, three bridges, explosions."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    # Fixed stars (deterministic positions).
    stars = [(52, 204), (120, 218), (200, 200), (300, 214), (380, 202),
             (450, 222), (90, 240), (250, 232), (330, 244), (420, 238),
             (160, 250), (470, 252)]
    for sx, sy in stars:
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(220, 220, 200))
    # Moon.
    draw.ellipse([430, 198, 458, 226], fill=(232, 228, 200))
    draw.ellipse([438, 204, 450, 216], fill=(NAVY[0] + 20, NAVY[1] + 20,
                                              NAVY[2] + 20))
    # Skyline silhouette.
    base = y0 + 150
    buildings = [(28, 60), (70, 92), (118, 48), (150, 78), (196, 58),
                 (232, 100), (280, 66), (330, 88), (378, 54), (420, 80),
                 (458, 62)]
    for bx, bh in buildings:
        draw.rectangle([bx, base - bh, bx + 42, base], fill=DARK_SKYLINE)
    # Church dome + spire.
    draw.ellipse([196, base - 108, 232, base - 72], fill=DARK_SKYLINE)
    draw.polygon([(210, base - 108), (214, base - 128), (218, base - 108)],
                 fill=DARK_SKYLINE)
    # Tall tower with pointed top.
    draw.rectangle([330, base - 118, 348, base], fill=DARK_SKYLINE)
    draw.polygon([(330, base - 118), (339, base - 140), (348, base - 118)],
                 fill=DARK_SKYLINE)
    # Lit windows.
    for wx, wy in [(80, 300), (130, 292), (244, 306), (292, 296), (390, 302),
                   (432, 296), (164, 312), (344, 312)]:
        draw.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 190, 80))
    # River band across the lower third.
    river_y = y0 + 153
    draw.rectangle([x0, river_y, x1, y1], fill=STEEL)
    draw.line([(x0, river_y + 18), (x1, river_y + 18)],
              fill=(120, 160, 190), width=1)
    draw.line([(x0, river_y + 44), (x1, river_y + 44)],
              fill=(120, 160, 190), width=1)
    # Three arched bridges.
    for bx0, bx1 in [(40, 160), (190, 310), (340, 470)]:
        draw.arc([bx0, river_y - 6, bx1, river_y + 44], 180, 360,
                 fill=(16, 16, 14), width=4)
        draw.line([(bx0, river_y + 20), (bx1, river_y + 20)],
                  fill=(16, 16, 14), width=3)
    # Explosions on the left and middle bridges.
    for ex, ey in [(100, 356), (250, 350)]:
        for r, col in [(22, ORANGE), (15, YELLOW), (8, (255, 240, 160))]:
            draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col)
        for dx, dy in [(-30, -18), (28, -22), (-26, 16), (30, 14),
                       (0, -30), (-32, 0), (32, -2)]:
            draw.line([(ex, ey), (ex + dx, ey + dy)], fill=YELLOW, width=2)
    # Red missile trails curving in from the top right.
    draw.arc([330, 190, 540, 330], 200, 290, fill=RED, width=3)
    draw.arc([360, 190, 560, 320], 205, 285, fill=(220, 60, 50), width=2)
    draw.arc([300, 190, 520, 350], 195, 280, fill=RED, width=2)
    # Small white-red flag on a pole at the right edge.
    draw.line([(492, 300), (492, 348)], fill=(230, 230, 220), width=2)
    draw.rectangle([470, 300, 492, 307], fill=(240, 240, 235))
    draw.rectangle([470, 307, 492, 314], fill=RED)


# ---------------------------------------------------------------- tiles
def draw_tile(draw, x, y, w, h, kicker, headline, deck, accent, icon_fn):
    draw.rectangle([x, y, x + w, y + h], fill=PAPER2,
                   outline=PANEL_LINE, width=1)
    draw.text((x + 12, y + 10), kicker, font=font("sans_bold", 12), fill=accent)
    icon_fn(draw, x + w - 40, y + 10, 28, accent)
    rule(draw, x + 12, y + 30, x + w - 12, width=1, fill=PANEL_LINE)
    head_lines = wrap(draw, headline, font("sans_bold", 18), w - 24)
    y_cur = text_block(draw, x + 12, y + 40, head_lines,
                       font("sans_bold", 18), INK, 22)
    deck_lines = wrap(draw, deck, font("sans", 14), w - 24)
    text_block(draw, x + 12, y_cur + 6, deck_lines,
               font("sans", 14), BODY, 18)


def draw_numbers_box(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=NAVY2)
    draw.text((x + 12, y + 10), "BY THE NUMBERS",
              font=font("sans_bold", 12), fill=GOLD)
    rule(draw, x + 12, y + 30, x + w - 12, width=1, fill=(70, 90, 120))
    rows = [
        ("400+", "drones fired at Ukraine"),
        ("110", "missiles, 27 ballistic"),
        ("8", "killed in the strikes"),
        ("51–48", "Senate war-powers vote"),
        ("$97.17", "Anthropic's first close"),
    ]
    ry = y + 44
    for num, label in rows:
        draw.text((x + 12, ry), num, font=font("sans_bold", 16), fill=NUM_FG)
        draw.text((x + 100, ry + 2), label, font=font("sans", 11),
                  fill=NUM_LABEL)
        ry += 30


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Frame.
    draw.rectangle([6, 6, 1017, 1017], outline=RULE, width=2)

    # Masthead.
    draw.text((28, 22), "THE WORLD IN ONE PICTURE",
              font=font("sans_bold", 13), fill=RED)
    right = "No. 20 — 2026"
    draw.text((996 - draw.textlength(right, font=font("sans_bold", 13)), 22),
              right, font=font("sans_bold", 13), fill=FAINT)
    title = "THE DAY IN THE WORLD"
    tw = draw.textlength(title, font=font("serif_bold", 58))
    draw.text(((W - tw) / 2, 40), title, font=font("serif_bold", 58), fill=INK)
    rule(draw, 28, 112, 996, width=3)
    date = "FRIDAY, 20 NOVEMBER 2026"
    dw = draw.textlength(date, font=font("sans_bold", 20))
    draw.text(((W - dw) / 2, 122), date, font=font("sans_bold", 20), fill=INK)
    rule(draw, 28, 152, 996, width=1)

    # Lead.
    draw.text((28, 166), "KYIV — WAR SPILLS INTO POLAND",
              font=font("sans_bold", 13), fill=RED)
    draw_lead_art(draw, 28, 190, 500, 420)
    caption = ("Russian missiles hit Kyiv's bridges overnight; two missiles "
               "and a drone crossed into Poland.")
    cap_lines = wrap(draw, caption, font("serif", 13), 472)
    text_block(draw, 28, 424, cap_lines, font("serif", 13), FAINT, 16)

    # Lead right column.
    head_lines = wrap(draw, "MISSILES OVER KYIV, INTO POLAND",
                      font("serif_bold", 40), 472)
    y_cur = text_block(draw, 524, 186, head_lines,
                       font("serif_bold", 40), INK, 48)
    deck = ("Russia fires 400 drones and 110 missiles in one of its biggest "
            "barrages of the war — hitting three bridges across the Dnipro, "
            "killing eight, and sending two missiles and a jet drone into "
            "NATO Poland.")
    deck_lines = wrap(draw, deck, font("sans", 17), 472)
    y_cur = text_block(draw, 524, y_cur + 10, deck_lines,
                       font("sans", 17), BODY, 23)
    rule(draw, 524, y_cur + 12, 996, width=1, fill=PANEL_LINE)
    draw.text((524, y_cur + 22),
              "Hours after Putin's Shenzhen talks with Trump —",
              font=font("sans_bold", 14), fill=INK)
    draw.text((524, y_cur + 42),
              "and his vow of a 'much more painful' reply.",
              font=font("sans_bold", 14), fill=INK)
    rule(draw, 28, 458, 996, width=2)

    # Story grid.
    gx, gy = 28, 474
    tw_, th_, gap = 235, 196, 12
    tiles = [
        ("WASHINGTON", "TRUMP: NO IRAN CALL UNTIL 2027",
         "Trump tells Axios he will not decide the next step in the Iran war "
         "until the new year. Senate Republicans block a war-powers vote, "
         "51–48.", RED, icon_clock),
        ("RIYADH", "HOUTHI MISSILE HITS RIYADH TOWER",
         "A missile damages the PIF tower in Riyadh's financial district, "
         "as the Iran war enters its ninth month and tanker attacks mount "
         "in Hormuz.", RED, icon_tower),
        ("NEW YORK", "ANTHROPIC UP 17% — STOCKS SLIDE",
         "The record $81.3bn IPO closes at $97.17, but the S&P 500 falls 2% "
         "and Japan's Nikkei drops 4.8% as the AI sell-off spreads.",
         RED, icon_chart),
        ("BRUSSELS", "EU AND UK MEET IN BRUSSELS",
         "Costa and von der Leyen meet PM Burnham at the second EU–UK "
         "summit. Germany's Merz rejects a new Yalta over Europe.",
         BLUE, icon_stars),
        ("THE HAGUE", "MYANMAR GUILTY OF GENOCIDE",
         "The World Court rules 9–6: the 2017 campaign against the Rohingya "
         "was genocide — the first state ever held responsible.",
         RED, icon_scales),
        ("NAIROBI", "KENYA BEATS EBOLA",
         "Kenya discharges its last Ebola patient, 37 days after the first "
         "case — the outbreak is over.", TEAL, icon_cross),
        ("WORLD", "GTA VI TOPS $2.3BN",
         "The game's worldwide launch tops $2.3 billion in sales.",
         PURPLE, icon_star),
    ]
    positions = [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)]
    for (col, row), (kicker, headline, deck_t, accent, icon_fn) in zip(
            positions, tiles):
        x = gx + col * (tw_ + gap)
        y = gy + row * (th_ + gap)
        draw_tile(draw, x, y, tw_, th_, kicker, headline, deck_t, accent,
                  icon_fn)
    # Numbers box: grid column 4, row 2.
    draw_numbers_box(draw, gx + 3 * (tw_ + gap), gy + (th_ + gap), tw_, th_)

    # Wire strip.
    sy = 892
    draw.rectangle([28, sy, 996, sy + 62], fill=STRIP)
    draw.text((40, sy + 8), "ALSO TODAY", font=font("sans_bold", 13), fill=RED)
    wire = ("COP31 draft drops all fossil-fuel language  •  IMF: world "
            "public debt nears 100% of GDP  •  Italy fines Meta €805m over "
            "photo access  •  FAA ground stop strands 1.5m travellers  •  "
            "Bukele registers for a third term in El Salvador")
    wire_lines = wrap(draw, wire, font("sans_bold", 14), 916)
    text_block(draw, 40, sy + 26, wire_lines, font("sans_bold", 14), INK, 18)

    # Footer.
    draw.text((28, 972),
              "Every story was reported on 20 November 2026. Sources: "
              "Reuters, AP, AFP, BBC, CNN, WSJ, Just Security, Euronews.",
              font=font("sans", 12), fill=FAINT)
    draw.text((28, 992), "Drawn by an AI agent for make.fun — one day, one picture.",
              font=font("sans", 12), fill=FAINT)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    main()
