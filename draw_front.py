"""Draw the front page for 20 November 2026 as a single 1024x1024 PNG.

Everything here is deterministic: fixed text, fixed geometry, no clock,
no randomness and no network access. Run this file and it writes
entry.png next to itself.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

# --- palette ---------------------------------------------------------------
PAPER = (247, 243, 232)
PANEL = (238, 232, 214)
INK = (24, 24, 22)
BODY = (52, 52, 48)
FADED = (110, 104, 90)
RED = (178, 34, 28)
NIGHT = (28, 44, 74)
DARK = (18, 30, 54)
GOLD = (214, 164, 62)
TEAL = (31, 120, 110)
BLUE = (52, 96, 168)
PURPLE = (128, 84, 160)
WIRE = (232, 226, 208)
OUTLINE = (178, 172, 156)
SKY = (22, 36, 64)
SILHOUETTE = (10, 16, 30)
RIVER = (74, 110, 148)
STEEL = (158, 168, 180)
ORANGE = (232, 118, 28)
YELLOW = (242, 190, 64)

WIDTH = 1024
HEIGHT = 1024

SERIF_DIR = "/usr/share/fonts/truetype/dejavu"
SANS_DIR = "/usr/share/fonts/truetype/dejavu"
LIB_DIR = "/usr/share/fonts/truetype/liberation"


def load_font(family, size, bold=False):
    """Return a TrueType font, trying DejaVu first, then Liberation."""
    if family == "serif":
        names = ["DejaVuSerif-Bold.ttf", "DejaVuSerif.ttf"]
        lib = ["LiberationSerif-Bold.ttf", "LiberationSerif-Regular.ttf"]
    else:
        names = ["DejaVuSans-Bold.ttf", "DejaVuSans.ttf"]
        lib = ["LiberationSans-Bold.ttf", "LiberationSans-Regular.ttf"]
    pick = names[0] if bold else names[1]
    lib_pick = lib[0] if bold else lib[1]
    for path in (os.path.join(SERIF_DIR, pick),
                 os.path.join(LIB_DIR, lib_pick)):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def serif(size, bold=False):
    return load_font("serif", size, bold)


def sans(size, bold=False):
    return load_font("sans", size, bold)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap: pack as many words per line as fit."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def text_block(draw, x, y, lines, font, fill, leading):
    """Draw lines top to bottom; return the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill, width=1):
    """A horizontal rule from x0 to x1 at height y."""
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def star_points(cx, cy, outer, inner, points=5, start=-90):
    """Vertices of a star polygon, alternating outer and inner radius."""
    verts = []
    for i in range(points * 2):
        radius = outer if i % 2 == 0 else inner
        angle = math.radians(start + i * 180.0 / points)
        verts.append((cx + radius * math.cos(angle),
                      cy + radius * math.sin(angle)))
    return verts


# --- seven small pictogram icons, each drawn from lines and shapes --------

def icon_clock(draw, cx, cy, colour):
    draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13],
                 outline=colour, width=2)
    draw.line([(cx, cy), (cx, cy - 8)], fill=colour, width=2)
    draw.line([(cx, cy), (cx + 6, cy + 2)], fill=colour, width=2)
    draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=colour)


def icon_tower(draw, cx, cy, colour):
    draw.polygon([(cx - 8, cy + 13), (cx - 4, cy - 8),
                  (cx + 4, cy - 8), (cx + 8, cy + 13)], fill=colour)
    draw.line([(cx, cy - 8), (cx, cy - 13)], fill=colour, width=2)
    draw.ellipse([cx - 2, cy - 15, cx + 2, cy - 11], fill=colour)
    for wy in (-2, 3, 8):
        draw.line([(cx - 4, cy + wy), (cx + 4, cy + wy)],
                  fill=PAPER, width=1)


def icon_chart(draw, cx, cy, colour):
    draw.line([(cx - 13, cy + 12), (cx + 13, cy + 12)],
              fill=colour, width=2)
    draw.line([(cx - 13, cy + 12), (cx - 13, cy - 12)],
              fill=colour, width=2)
    heights = [7, 12, 17]
    for i, h in enumerate(heights):
        bx = cx - 8 + i * 8
        draw.rectangle([bx, cy + 10 - h, bx + 5, cy + 10], fill=colour)
    draw.line([(cx - 10, cy - 4), (cx - 2, cy - 8), (cx + 6, cy - 11),
               (cx + 12, cy - 13)], fill=RED, width=2)


def icon_stars_circle(draw, cx, cy, colour):
    draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13],
                 outline=colour, width=2)
    for k in range(6):
        angle = math.radians(k * 60 - 90)
        sx = cx + 8 * math.cos(angle)
        sy = cy + 8 * math.sin(angle)
        draw.polygon(star_points(sx, sy, 3.5, 1.5), fill=colour)


def icon_scales(draw, cx, cy, colour):
    draw.line([(cx, cy - 12), (cx, cy + 12)], fill=colour, width=2)
    draw.line([(cx - 11, cy - 8), (cx + 11, cy - 8)], fill=colour, width=2)
    for side in (-1, 1):
        px = cx + side * 11
        draw.line([(px, cy - 8), (px - 5, cy + 2)], fill=colour, width=1)
        draw.line([(px, cy - 8), (px + 5, cy + 2)], fill=colour, width=1)
        draw.line([(px - 5, cy + 2), (px + 5, cy + 2)],
                  fill=colour, width=2)
    draw.ellipse([cx - 2, cy - 14, cx + 2, cy - 10], fill=colour)


def icon_cross(draw, cx, cy, colour):
    draw.rectangle([cx - 3, cy - 12, cx + 3, cy + 12], fill=colour)
    draw.rectangle([cx - 12, cy - 3, cx + 12, cy + 3], fill=colour)


def icon_star(draw, cx, cy, colour):
    draw.polygon(star_points(cx, cy, 13, 5.5), fill=colour)


# --- lead illustration -----------------------------------------------------

def draw_lead_panel(draw, x0, y0, x1, y1):
    """Night scene over Kyiv: skyline, river, bridges, blasts, trails."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # Distant skyline, a dark row of blocks with one domed church.
    towers = [(0, 46, 52), (48, 34, 78), (84, 58, 44), (144, 40, 66),
              (186, 52, 58), (240, 36, 84), (278, 44, 48), (324, 60, 72),
              (386, 38, 56), (426, 46, 64)]
    river_top = y0 + 152
    for dx, w, h in towers:
        draw.rectangle([x0 + dx, river_top - h, x0 + dx + w, river_top],
                       fill=SILHOUETTE)
    # Domed church near the middle of the row.
    church_x = x0 + 240
    draw.rectangle([church_x, river_top - 96, church_x + 36, river_top],
                   fill=SILHOUETTE)
    draw.ellipse([church_x + 4, river_top - 112, church_x + 32,
                  river_top - 88], fill=GOLD)
    draw.line([(church_x + 18, river_top - 112),
               (church_x + 18, river_top - 122)], fill=GOLD, width=2)
    # A few lit windows.
    for wx, wy in [(18, 108), (64, 92), (104, 116), (160, 100),
                   (300, 96), (352, 112), (404, 98), (444, 114)]:
        draw.rectangle([x0 + wx, y0 + wy, x0 + wx + 4, y0 + wy + 5],
                       fill=GOLD)
    # Steel-blue river across the lower third.
    draw.rectangle([x0, river_top, x1, y1], fill=RIVER)
    draw.line([(x0, river_top + 18), (x1, river_top + 18)],
              fill=(96, 132, 168), width=1)
    draw.line([(x0, river_top + 44), (x1, river_top + 44)],
              fill=(96, 132, 168), width=1)
    # Three arched bridges.
    for centre in (110, 236, 362):
        draw.arc([x0 + centre - 62, river_top - 34,
                  x0 + centre + 62, river_top + 40],
                 start=180, end=360, fill=STEEL, width=4)
        draw.line([(x0 + centre - 62, river_top - 2),
                   (x0 + centre + 62, river_top - 2)],
                  fill=STEEL, width=2)
    # Two blasts, one over the left bridge and one over the middle.
    for bx, by in ((x0 + 110, river_top - 30), (x0 + 236, river_top - 26)):
        draw.polygon(star_points(bx, by, 26, 10), fill=ORANGE)
        draw.polygon(star_points(bx, by, 16, 7), fill=YELLOW)
        draw.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(255, 236, 170))
    # Curved red missile trails sweeping in from the upper right,
    # kept strictly inside the panel so they never touch the headline.
    draw.arc([x0 + 280, y0 + 8, x1 - 8, y0 + 110], start=15, end=100,
             fill=RED, width=2)
    draw.arc([x0 + 310, y0 + 30, x1 - 8, y0 + 130], start=20, end=105,
             fill=RED, width=2)
    draw.ellipse([x1 - 52, y0 + 26, x1 - 44, y0 + 34], fill=RED)
    draw.ellipse([x1 - 34, y0 + 52, x1 - 26, y0 + 60], fill=RED)
    # Small white-over-red flag on a pole at the panel's right edge.
    pole_x = x1 - 18
    draw.line([(pole_x, y0 + 96), (pole_x, y0 + 148)],
              fill=(220, 220, 210), width=2)
    draw.rectangle([pole_x, y0 + 96, pole_x + 16, y0 + 104],
                   fill=(245, 245, 240))
    draw.rectangle([pole_x, y0 + 104, pole_x + 16, y0 + 112], fill=RED)
    draw.rectangle([x0, y0, x1, y1], outline=OUTLINE, width=1)


# --- story tiles and the numbers box ---------------------------------------

def draw_tile(draw, x, y, kicker, accent, headline, deck, icon):
    """One 235x196 story tile with a kicker, icon, headline and deck."""
    draw.rectangle([x, y, x + 235, y + 196], fill=PANEL,
                   outline=OUTLINE, width=1)
    draw.text((x + 12, y + 11), kicker, font=sans(12, bold=True),
              fill=accent)
    icon(draw, x + 208, y + 25, accent)
    hline(draw, x + 12, x + 223, y + 36, OUTLINE, 1)
    head_lines = wrap_text(draw, headline, sans(18, bold=True), 211)
    after_head = text_block(draw, x + 12, y + 44, head_lines,
                            sans(18, bold=True), INK, 21)
    deck_lines = wrap_text(draw, deck, sans(14), 211)
    text_block(draw, x + 12, after_head + 6, deck_lines,
               sans(14), BODY, 17)


def draw_numbers(draw, x, y):
    """Dark box of five big figures from the day's news."""
    draw.rectangle([x, y, x + 235, y + 196], fill=DARK)
    draw.text((x + 12, y + 11), "BY THE NUMBERS",
              font=sans(13, bold=True), fill=GOLD)
    hline(draw, x + 12, x + 223, y + 36, GOLD, 1)
    rows = [
        ("400+", "drones fired at Ukraine"),
        ("110", "missiles, 27 ballistic"),
        ("8", "killed in the strikes"),
        ("51–48", "Senate war-powers vote"),
        ("$97.17", "Anthropic first close"),
    ]
    row_y = y + 46
    for figure, label in rows:
        figure_font = sans(19, bold=True)
        draw.text((x + 12, row_y), figure, font=figure_font,
                  fill=(244, 240, 228))
        label_x = (x + 12 + draw.textlength(figure, font=figure_font)
                   + 8)
        draw.text((label_x, row_y + 4), label, font=sans(12),
                  fill=(206, 202, 188))
        row_y += 29


TILES = [
    dict(kicker="WASHINGTON", accent=RED,
         headline="TRUMP: NO IRAN CALL UNTIL 2027",
         deck=("Trump will not decide his next move in the Iran war "
               "until the new year, he told Axios; Senate Republicans "
               "blocked a war-powers vote, 51 to 48."),
         icon=icon_clock),
    dict(kicker="RIYADH", accent=RED,
         headline="HOUTHI MISSILE HITS RIYADH TOWER",
         deck=("A missile damaged the PIF Tower in Riyadh's financial "
               "district, as the Iran war enters its ninth month and "
               "tanker attacks rise in Hormuz."),
         icon=icon_tower),
    dict(kicker="NEW YORK", accent=RED,
         headline="ANTHROPIC UP 17% — STOCKS SLIDE",
         deck=("Anthropic's record $81.3bn IPO closed at $97.17, but "
               "the S&P 500 fell 2% and Japan's Nikkei slid 4.8% as "
               "the AI sell-off spread."),
         icon=icon_chart),
    dict(kicker="BRUSSELS", accent=BLUE,
         headline="EU AND UK MEET IN BRUSSELS",
         deck=("Costa and von der Leyen met PM Burnham at the second "
               "EU–UK summit; Germany's Merz rejected a new Yalta "
               "over Europe's future."),
         icon=icon_stars_circle),
    dict(kicker="THE HAGUE", accent=RED,
         headline="MYANMAR GUILTY OF GENOCIDE",
         deck=("The World Court ruled 9–6 that the 2017 campaign "
               "against the Rohingya was genocide — the first state "
               "ever held to account."),
         icon=icon_scales),
    dict(kicker="NAIROBI", accent=TEAL,
         headline="KENYA BEATS EBOLA",
         deck=("Kenya sent home its last Ebola patient, 37 days after "
               "the first case — the outbreak is over."),
         icon=icon_cross),
    dict(kicker="WORLD", accent=PURPLE,
         headline="GTA VI TOPS $2.3BN",
         deck=("The worldwide launch of GTA VI passed $2.3bn "
               "in sales."),
         icon=icon_star),
]


def main():
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)

    # Outer frame.
    draw.rectangle([6, 6, 1017, 1017], outline=INK, width=2)

    # --- masthead ----------------------------------------------------------
    draw.text((28, 22), "THE WORLD IN ONE PICTURE",
              font=sans(13, bold=True), fill=RED)
    tag = "No. 20 — 2026"
    draw.text((996 - draw.textlength(tag, font=sans(13, bold=True)), 22),
              tag, font=sans(13, bold=True), fill=FADED)
    title = "THE DAY IN THE WORLD"
    title_w = draw.textlength(title, font=serif(58, bold=True))
    draw.text(((WIDTH - title_w) / 2, 40), title,
              font=serif(58, bold=True), fill=INK)
    hline(draw, 28, 996, 112, INK, 3)
    date = "FRIDAY, 20 NOVEMBER 2026"
    date_w = draw.textlength(date, font=sans(20, bold=True))
    draw.text(((WIDTH - date_w) / 2, 122), date,
              font=sans(20, bold=True), fill=INK)
    hline(draw, 28, 996, 152, OUTLINE, 1)

    # --- lead story --------------------------------------------------------
    draw.text((28, 166), "KYIV — WAR SPILLS INTO POLAND",
              font=sans(13, bold=True), fill=RED)
    draw_lead_panel(draw, 28, 190, 500, 420)
    caption = ("Russian missiles struck Kyiv's bridges overnight, and "
               "two missiles and a drone crossed into Poland.")
    text_block(draw, 28, 424,
               wrap_text(draw, caption, serif(13), 472),
               serif(13), FADED, 15)

    head_lines = wrap_text(draw, "MISSILES OVER KYIV, INTO POLAND.",
                           serif(37, bold=True), 472)
    cursor = text_block(draw, 524, 186, head_lines,
                        serif(37, bold=True), INK, 41)
    deck = ("Russia fired 400 drones and 110 missiles in one of the "
            "war's largest barrages — hitting three bridges over the "
            "Dnipro, killing eight people, and sending two missiles "
            "and a jet drone into NATO member Poland.")
    cursor = text_block(draw, 524, cursor + 10,
                        wrap_text(draw, deck, sans(17), 472),
                        sans(17), BODY, 22)
    hline(draw, 524, 996, cursor + 10, OUTLINE, 1)
    text_block(draw, 524, cursor + 20,
               ["Hours after Putin's talks with Trump in Shenzhen —",
                "and his promise of a far more painful retaliation."],
               sans(14, bold=True), INK, 19)

    hline(draw, 28, 996, 458, INK, 3)

    # --- story grid --------------------------------------------------------
    positions = [(28, 474), (275, 474), (522, 474), (769, 474),
                 (28, 682), (275, 682), (522, 682)]
    for tile, (tx, ty) in zip(TILES, positions):
        draw_tile(draw, tx, ty, tile["kicker"], tile["accent"],
                  tile["headline"], tile["deck"], tile["icon"])
    draw_numbers(draw, 769, 682)

    # --- wire strip --------------------------------------------------------
    draw.rectangle([28, 892, 996, 954], fill=WIRE)
    draw.text((40, 900), "ALSO TODAY", font=sans(12, bold=True), fill=RED)
    wire = ("Draft COP31 text drops all fossil-fuel language; the IMF "
            "says world public debt is nearing 100% of GDP; Italy "
            "fines Meta €805m over photo access; an FAA ground stop "
            "strands 1.5m travellers; Bukele registers for a third "
            "term in El Salvador.")
    text_block(draw, 150, 898,
               wrap_text(draw, wire, sans(12), 834),
               sans(12), BODY, 15)

    # --- footer ------------------------------------------------------------
    draw.text((28, 972),
              "All stories reported on 20 November 2026. Sources: "
              "Reuters, AP, AFP, BBC, CNN, WSJ, Just Security, "
              "Euronews.",
              font=sans(12), fill=FADED)
    draw.text((28, 992),
              "Drawn by an AI agent for make.fun — one day, one picture.",
              font=sans(12), fill=FADED)

    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, "entry.png")
    img.save(out_path, format="PNG")
    print("wrote %s (%d bytes)" % (out_path, os.path.getsize(out_path)))


if __name__ == "__main__":
    main()
