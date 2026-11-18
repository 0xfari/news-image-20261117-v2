#!/usr/bin/env python3
"""Draw Tuesday 17 November 2026 as one newspaper front page, 1024x1024.

Everything is drawn with Pillow shapes and text: no photos, no network,
no randomness. 48 stories: 3 illustrated leads, 10 illustrated grid
stories, 35 numbered briefs, plus a world map with pins for stories 1-13.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 222)
INK = (26, 26, 26)
RED = (178, 34, 34)
DARKRED = (139, 0, 0)
NAVY = (31, 42, 92)
TEAL = (0, 110, 110)
GOLD = (184, 134, 11)
GREY = (90, 90, 90)
LIGHT = (232, 224, 200)

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    for base in (FD, FL):
        path = os.path.join(base, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_I = lambda s: font("DejaVuSans-Oblique.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, color=INK, leading=None, max_lines=None):
    """Draw wrapped text; returns y just below the last line."""
    lh = leading or int(fnt.size * 1.25)
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += lh
    return y


def chip(draw, x, y, text, fnt, bg, fg=(255, 255, 255)):
    """Small rounded label; returns width used."""
    tw = draw.textlength(text, font=fnt)
    draw.rounded_rectangle([x, y, x + tw + 12, y + fnt.size + 7],
                           radius=4, fill=bg)
    draw.text((x + 6, y + 3), text, font=fnt, fill=fg)
    return tw + 12


# ---------------------------------------------------------------- stories
LEADS = [
    dict(n=1, tag="EUROPE · UKRAINE WAR", art="kerch",
         head="Ukraine says a Crimean Bridge span fell into the sea",
         body="Second strike in two days; Zelenskyy hails an "
              "\u201cunprecedented operation\u201d."),
    dict(n=2, tag="MIDDLE EAST · IRAN WAR", art="gulf",
         head="Iran sends drones at a US radar in Bahrain; US hits back",
         body="Bahrain and the US say all were downed; US jets then strike "
              "Qeshm."),
    dict(n=3, tag="ASIA · DIPLOMACY", art="quad",
         head="Trump holds his first Quad summit, in Manila",
         body="The four unveil critical-minerals deals; Putin reaches "
              "Shenzhen for Thursday\u2019s talks with Trump and Xi."),
]

GRID = [
    dict(n=4, tag="AFRICA · HEALTH", art="ebola",
         head="Ebola cases in DR Congo top 11,000, WHO says",
         body="Cases doubled in three months; 5,400 have died."),
    dict(n=5, tag="GLOBAL · CLIMATE", art="cop31",
         head="COP31 split over a fossil-fuel phase-out",
         body="Nations weigh the first draft; talks end Friday."),
    dict(n=6, tag="AMERICAS · HEALTH", art="measles",
         head="US, Mexico and Bolivia lose measles-free status",
         body="PAHO cites a year of spread; US has 5,700+ cases."),
    dict(n=7, tag="US · BUSINESS", art="nvidia",
         head="Nvidia\u2019s sales double to $115.8bn",
         body="Reported after the close; Dow fell 849 points."),
    dict(n=8, tag="MIDDLE EAST · GAZA", art="gaza",
         head="Gaza truce at risk of collapse, UN is told",
         body="Board of Peace report; 1.4m face acute hunger."),
    dict(n=9, tag="ASIA · POLITICS", art="mongolia",
         head="Mongolia\u2019s president says he will resign",
         body="Denies a $25m bribe claim; parliament must accept."),
    dict(n=10, tag="EUROPE · POLITICS", art="serbia",
         head="Serbia\u2019s student-led majority takes its seats",
         body="Student List holds 140 of 250; Vu\u010di\u0107\u2019s party out."),
    dict(n=11, tag="ASIA · LABOUR", art="bangladesh",
         head="Bangladesh police tear-gas workers",
         body="They want Tk 30,000 a month, up from 12,500."),
    dict(n=12, tag="RUSSIA · AIR CRASH", art="an12",
         head="Russian An-12 crash kills all 19 aboard",
         body="Plane came down near Kemerovo; fault suspected."),
    dict(n=13, tag="AFRICA · JUSTICE", art="mozambique",
         head="Mozambique puts opposition on trial",
         body="Mondlane faces 5 charges over 2024 protests."),
]

BRIEFS = [
    (14, "Kyiv: Russia hits the North and South Dnipro bridges"),
    (15, "Russia says it downed a record 1,441 drones overnight"),
    (16, "UN: Ukraine\u2019s civilian deaths this year top all of 2025"),
    (17, "France: public-sector strike; 146,000 march (unions: 500,000)"),
    (18, "Poland: Tusk survives no-confidence vote, 242 to 200"),
    (19, "Germany: Deutsche Bank leak \u2014 15m files, 230 journalists"),
    (20, "Moldova shuts airspace as a drone nears Chisinau"),
    (21, "Turkey: police seize opposition broadcaster S\u00f6zc\u00fc TV"),
    (22, "UK sanctions 8 firms building West Bank settlements"),
    (23, "EU: five nations plan a Rwanda return hub"),
    (24, "Estonia to shut Russia border crossings on 1 Dec"),
    (25, "Prague: two trains collide; 46 people injured"),
    (26, "Knesset elects Eisenkot ally Kahana speaker, 66\u201352"),
    (27, "West Bank: settlers kill a woman, 72, near Jericho"),
    (28, "Oman: Iran\u2019s Araghchi holds shipping-safety talks"),
    (29, "Houthis push toward Aden as Yemeni forces pull back"),
    (30, "Bahrain jails 64 for life over alleged Iran links"),
    (31, "US intel: reported Iran \u201cdirty bomb\u201d plot; no credible threat"),
    (32, "China and Canada agree C$400m tariff relief in Shenzhen"),
    (33, "Japan offers ASEAN its crude oil reserves"),
    (34, "Thailand pledges to scrap tariffs on US goods"),
    (35, "South Korea: IMF lifts 2026 growth forecast to 3.9%"),
    (36, "India: Cyclone Akvan strengthens; Odisha evacuates"),
    (37, "India: bus falls into Uttarakhand gorge; 8 dead"),
    (38, "Japan scrambles jets as Russian planes breach airspace"),
    (39, "JPMorgan outage cuts off Zelle users for hours"),
    (40, "Apple: Pay, iCloud and App Store outage; not a hack"),
    (41, "Microsoft explains last week\u2019s global outage"),
    (42, "Kenya: WFP aids 30,000 who fled Ethiopia clashes"),
    (43, "Pope Leo XIV returns from his South America tour"),
    (44, "Awa people make first sustained contact"),
    (45, "Depardieu pleads guilty to sexual assault in Paris"),
    (46, "Football: Norway win 3\u20132 in Denmark; Haaland twice"),
    (47, "Football: India beat Pakistan 2\u20131 in SAFF final"),
    (48, "Football: Brazil beat Singapore 7\u20130; Vinicius hat-trick"),
]

# lon, lat for map pins 1-13
PINS = {
    1: (37, 45), 2: (50, 26), 3: (121, 14), 4: (23, 0), 5: (24, 41),
    6: (-100, 39), 7: (-122, 37), 8: (34, 31), 9: (107, 48),
    10: (20, 45), 11: (90, 24), 12: (86, 55), 13: (32, -26),
}
PIN_COL = {1: NAVY, 2: (180, 120, 0), 3: (120, 60, 160), 4: (0, 130, 60),
           5: (90, 90, 90), 6: RED, 7: RED, 8: (180, 120, 0), 9: (120, 60, 160),
           10: NAVY, 11: (120, 60, 160), 12: NAVY, 13: (0, 130, 60)}


# ---------------------------------------------------------------- art panels
def panel_frame(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def art_kerch(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.55], fill=(190, 220, 235))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(38, 110, 145))
    for i in range(7):  # waves
        wx = x + 12 + i * 44
        d.arc([wx, y + h * 0.62, wx + 34, y + h * 0.78], 0, 180, fill=(140, 200, 220), width=2)
        d.arc([wx, y + h * 0.80, wx + 34, y + h * 0.95], 0, 180, fill=(140, 200, 220), width=2)
    d.rectangle([x, y + h * 0.42, x + w * 0.42, y + h * 0.50], fill=(70, 70, 70))
    d.rectangle([x + w * 0.60, y + h * 0.42, x + w, y + h * 0.50], fill=(70, 70, 70))
    d.polygon([(x + w * 0.42, y + h * 0.50), (x + w * 0.52, y + h * 0.86),
               (x + w * 0.58, y + h * 0.86), (x + w * 0.60, y + h * 0.50)],
              fill=(50, 50, 50))
    for px, py in [(x + w * 0.14, y + h * 0.50), (x + w * 0.30, y + h * 0.50),
                   (x + w * 0.72, y + h * 0.50), (x + w * 0.88, y + h * 0.50)]:
        d.rectangle([px, py, px + 7, y + h * 0.62], fill=(60, 60, 60))
    d.ellipse([x + w * 0.47, y + h * 0.06, x + w * 0.56, y + h * 0.22], fill=(150, 150, 150))
    d.ellipse([x + w * 0.52, y + h * 0.14, x + w * 0.62, y + h * 0.32], fill=(120, 120, 120))
    d.ellipse([x + w * 0.44, y + h * 0.18, x + w * 0.51, y + h * 0.32], fill=(170, 170, 170))
    d.text((x + 8, y + 6), "CRIMEA", font=SANS_B(11), fill=INK)
    d.text((x + w - 52, y + 6), "RUSSIA", font=SANS_B(11), fill=INK)
    d.polygon([(x + 18, y + 22), (x + 34, y + 18), (x + 34, y + 26)], fill=INK)
    d.polygon([(x + w - 34, y + 22), (x + w - 18, y + 18), (x + w - 18, y + 26)], fill=INK)
    d.rectangle([x, y + h - 15, x + w, y + h], fill=NAVY)
    d.text((x + 8, y + h - 13), "KERCH STRAIT · STRUCK FOR A SECOND DAY",
           font=SANS_B(10), fill=(255, 255, 255))


def art_gulf(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 222, 180))
    d.polygon([(x + w * 0.10, y), (x + w * 0.85, y), (x + w * 0.72, y + h * 0.55),
               (x + w * 0.30, y + h * 0.62), (x + w * 0.05, y + h * 0.40)],
              fill=(150, 205, 225))
    d.polygon([(x + w * 0.55, y + h * 0.62), (x + w * 0.95, y + h * 0.55),
               (x + w, y + h), (x + w * 0.60, y + h)], fill=(150, 205, 225))
    d.text((x + w * 0.42, y + 4), "IRAN", font=SANS_B(11), fill=INK)
    d.text((x + 8, y + h * 0.62), "BAHRAIN", font=SANS_B(10), fill=INK)
    d.text((x + w - 58, y + h - 18), "HORMUZ", font=SANS_B(10), fill=INK)
    d.text((x + w * 0.62, y + h * 0.42), "QESHM", font=SANS_B(10), fill=INK)
    d.ellipse([x + w * 0.30, y + h * 0.55, x + w * 0.34, y + h * 0.62], fill=RED)
    d.ellipse([x + w * 0.68, y + h * 0.70, x + w * 0.72, y + h * 0.77], fill=RED)
    for i in range(6):
        px = x + w * (0.38 + i * 0.05)
        py = y + h * (0.48 - i * 0.02)
        d.ellipse([px, py, px + 3, py + 3], fill=NAVY)
    chip(d, x + w * 0.30, y + h * 0.28, "DRONES DOWNED", SANS_B(9), RED)
    chip(d, x + w * 0.58, y + h * 0.52, "US STRIKES", SANS_B(9), NAVY)


def flag_us(d, x, y, w, h):
    for i in range(7):
        d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                    fill=RED if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + w * 0.4, y + h * 0.55], fill=NAVY)


def flag_india(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(255, 153, 51))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(255, 255, 255))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(19, 136, 8))
    d.ellipse([x + w / 2 - 4, y + h / 2 - 4, x + w / 2 + 4, y + h / 2 + 4],
              outline=NAVY, width=1)


def flag_japan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.ellipse([x + w / 2 - 6, y + h / 2 - 6, x + w / 2 + 6, y + h / 2 + 6],
              fill=(188, 0, 45))


def flag_aus(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 0, 139))
    for sx, sy in [(0.7, 0.25), (0.8, 0.45), (0.65, 0.6), (0.85, 0.7)]:
        d.ellipse([x + w * sx - 2, y + h * sy - 2, x + w * sx + 2, y + h * sy + 2],
                  fill=(255, 255, 255))


def art_quad(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 225, 245))
    d.rectangle([x, y, x + w, y + 22], fill=(90, 50, 140))
    d.text((x + 8, y + 4), "QUAD LEADERS\u2019 SUMMIT · MANILA",
           font=SANS_B(11), fill=(255, 255, 255))
    flags = [("US", flag_us), ("INDIA", flag_india), ("JAPAN", flag_japan),
             ("AUSTRALIA", flag_aus)]
    fw, fh = 58, 34
    gap = (w - 4 * fw) / 5
    for i, (name, fn) in enumerate(flags):
        fx = x + gap + i * (fw + gap)
        fn(d, fx, y + 32, fw, fh)
        d.rectangle([fx, y + 32, fx + fw, y + 32 + fh], outline=INK, width=1)
        d.text((fx, y + 70), name, font=SANS_B(9), fill=INK)
    d.rectangle([x + 10, y + h - 26, x + w - 10, y + h - 10], fill=(90, 50, 140))
    d.text((x + 16, y + h - 24), "NEW CRITICAL-MINERALS DEALS",
           font=SANS_B(10), fill=(255, 255, 255))


def art_ebola(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.rectangle([x + 8, y + 14, x + w * 0.52, y + h - 8], fill=(245, 240, 225),
                outline=INK)
    d.polygon([(x + 8, y + 24), (x + w * 0.30, y + 10), (x + w * 0.52, y + 24)],
              fill=(178, 34, 34))
    d.rectangle([x + w * 0.28, y + 24, x + w * 0.32, y + 36], fill=RED)
    d.rectangle([x + w * 0.24, y + 28, x + w * 0.36, y + 32], fill=RED)
    d.text((x + w * 0.58, y + 6), "11,000+", font=SANS_B(13), fill=RED)
    d.text((x + w * 0.58, y + 22), "CASES", font=SANS_B(9), fill=INK)
    for i, bh in enumerate([8, 14, 20, 28]):
        d.rectangle([x + w * 0.58 + i * 14, y + h - 6 - bh,
                     x + w * 0.58 + i * 14 + 9, y + h - 6], fill=RED)


def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 235, 245))
    d.ellipse([x + 10, y + 8, x + 52, y + h - 8], fill=(90, 160, 200))
    d.ellipse([x + 20, y + 16, x + 42, y + 30], fill=(120, 190, 120))
    d.rectangle([x + 58, y + h / 2 - 2, x + w - 60, y + h / 2 + 2], fill=INK)
    d.polygon([(x + w - 60, y + h / 2 - 8), (x + w - 48, y + h / 2),
               (x + w - 60, y + h / 2 + 8)], fill=INK)
    d.text((x + 58, y + 6), "DRAFT", font=SANS_B(10), fill=INK)
    chip(d, x + w - 92, y + 4, "COP31", SANS_B(9), (0, 110, 110))
    d.rectangle([x + w - 22, y + 12, x + w - 12, y + h - 12], fill=(255, 255, 255),
                outline=RED)
    d.rectangle([x + w - 19, y + h - 22, x + w - 15, y + h - 14], fill=RED)
    d.text((x + 58, y + h - 18), "PHASE-OUT?", font=SANS_B(10), fill=RED)


def art_measles(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    flag_us(d, x + 8, y + 8, 34, 20)
    d.rectangle([x + 48, y + 8, x + 82, y + 28], fill=(0, 104, 71))
    d.text((x + 52, y + 12), "MX", font=SANS_B(10), fill=(255, 255, 255))
    d.rectangle([x + 88, y + 8, x + 122, y + 28], fill=(213, 0, 50))
    d.text((x + 92, y + 12), "BO", font=SANS_B(10), fill=(255, 255, 255))
    d.ellipse([x + w - 52, y + 8, x + w - 12, y + 44], fill=RED)
    for dx, dy in [(-14, 4), (14, 4), (0, -12), (0, 14)]:
        d.ellipse([x + w - 32 + dx - 3, y + 26 + dy - 3,
                   x + w - 32 + dx + 3, y + 26 + dy + 3], fill=RED)
    chip(d, x + 8, y + h - 20, "5,700+ CASES", SANS_B(9), RED)


def art_nvidia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 60, 30))
    for i, bh in enumerate([12, 20, 16, 28, 36]):
        d.rectangle([x + 10 + i * 16, y + h - 8 - bh, x + 10 + i * 16 + 11,
                     y + h - 8], fill=(118, 185, 0))
    d.text((x + w - 78, y + 6), "$115.8BN", font=SANS_B(13), fill=(118, 185, 0))
    d.text((x + w - 78, y + 24), "DOW -849", font=SANS_B(9), fill=(255, 255, 255))


def art_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 225, 200))
    for i in range(3):
        tx = x + 10 + i * 46
        d.polygon([(tx, y + h - 14), (tx + 18, y + 14), (tx + 36, y + h - 14)],
                  fill=(255, 255, 255), outline=INK)
    d.rectangle([x + w - 52, y + h - 26, x + w - 8, y + h - 10], fill=(200, 60, 60))
    d.text((x + w - 50, y + h - 24), "AID", font=SANS_B(10), fill=(255, 255, 255))
    d.text((x + 8, y + 4), "1.4M FACE HUNGER", font=SANS_B(10), fill=RED)


def art_mongolia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 235, 220))
    d.rectangle([x + 10, y + 18, x + w - 10, y + h - 8], fill=(200, 190, 170),
                outline=INK)
    d.polygon([(x + 10, y + 18), (x + w / 2, y + 4), (x + w - 10, y + 18)],
              fill=(150, 130, 110))
    for i in range(4):
        d.rectangle([x + 22 + i * 26, y + 28, x + 30 + i * 26, y + h - 14],
                    fill=(120, 100, 80))
    chip(d, x + w - 78, y + 2, "RESIGN", SANS_B(9), RED)


def art_serbia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.rectangle([x + 8, y + 16, x + w * 0.45, y + h - 8], fill=(230, 225, 210),
                outline=INK)
    d.polygon([(x + 8, y + 26), (x + w * 0.26, y + 12), (x + w * 0.45, y + 26)],
              fill=(160, 150, 130))
    import math
    cx, cy = x + w * 0.72, y + h - 6
    for i in range(11):
        a = math.pi * (1 - i / 10)
        px, py = cx + 34 * math.cos(a), cy - 30 * math.sin(a)
        d.ellipse([px - 4, py - 4, px + 4, py + 4],
                  fill=RED if i < 6 else NAVY)
    d.text((x + w * 0.55, y + 4), "140 – 103", font=SANS_B(11), fill=INK)


def art_bangladesh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 230, 220))
    d.rectangle([x + 8, y + 16, x + w * 0.55, y + h - 8], fill=(120, 130, 120),
                outline=INK)
    d.rectangle([x + 14, y + 8, x + 20, y + 16], fill=(120, 130, 120))
    d.rectangle([x + 26, y + 4, x + 32, y + 16], fill=(120, 130, 120))
    for i in range(3):
        d.ellipse([x + w * 0.62 + i * 22, y + h - 26, x + w * 0.62 + i * 22 + 12,
                   y + h - 14], fill=(255, 200, 120))
        d.rectangle([x + w * 0.62 + i * 22 + 2, y + h - 40,
                     x + w * 0.62 + i * 22 + 10, y + h - 26], fill=NAVY)
    chip(d, x + w - 82, y + 2, "TK 30,000", SANS_B(9), (0, 110, 110))


def art_an12(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 215, 230))
    d.polygon([(x + 8, y + h - 8), (x + w * 0.4, y + 12), (x + w * 0.7, y + h - 8)],
              fill=(140, 150, 160))
    d.polygon([(x + w * 0.5, y + h - 8), (x + w * 0.8, y + 20), (x + w - 8, y + h - 8)],
              fill=(160, 170, 180))
    d.ellipse([x + w * 0.30, y + 12, x + w * 0.62, y + 30], fill=(90, 90, 90))
    d.polygon([(x + w * 0.30, y + 20), (x + w * 0.14, y + 34), (x + w * 0.34, y + 26)],
              fill=(90, 90, 90))
    d.text((x + 8, y + h - 16), "ALL 19 ABOARD KILLED", font=SANS_B(10), fill=RED)


def art_mozambique(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 230, 215))
    d.rectangle([x + 10, y + 22, x + 70, y + 32], fill=(120, 80, 40))
    d.rectangle([x + 38, y + 32, x + 44, y + h - 10], fill=(120, 80, 40))
    d.rectangle([x + 20, y + h - 12, x + 62, y + h - 6], fill=(120, 80, 40))
    d.text((x + 78, y + 8), "5", font=SERIF_B(28), fill=INK)
    d.text((x + 96, y + 14), "CHARGES", font=SANS_B(10), fill=INK)
    d.text((x + 78, y + 36), "MAPUTO", font=SANS_B(9), fill=GREY)


ART = {"kerch": art_kerch, "gulf": art_gulf, "quad": art_quad,
       "ebola": art_ebola, "cop31": art_cop31, "measles": art_measles,
       "nvidia": art_nvidia, "gaza": art_gaza, "mongolia": art_mongolia,
       "serbia": art_serbia, "bangladesh": art_bangladesh,
       "an12": art_an12, "mozambique": art_mozambique}


# ---------------------------------------------------------------- map
def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 228, 238), outline=INK, width=1)
    # rough continents as flat blobs
    blobs = [
        [(0.03, 0.30), (0.20, 0.22), (0.28, 0.32), (0.24, 0.52), (0.12, 0.55), (0.04, 0.42)],
        [(0.30, 0.28), (0.48, 0.20), (0.62, 0.24), (0.60, 0.42), (0.44, 0.50), (0.32, 0.44)],
        [(0.44, 0.55), (0.52, 0.52), (0.55, 0.72), (0.48, 0.82), (0.42, 0.68)],
        [(0.62, 0.30), (0.78, 0.22), (0.92, 0.30), (0.88, 0.50), (0.74, 0.52), (0.64, 0.42)],
        [(0.80, 0.62), (0.90, 0.60), (0.93, 0.72), (0.84, 0.76), (0.78, 0.68)],
    ]
    for blob in blobs:
        pts = [(x + fx * w, y + fy * h) for fx, fy in blob]
        d.polygon(pts, fill=(238, 222, 180), outline=(200, 185, 150))
    for n, (lon, lat) in PINS.items():
        px = x + (lon + 180) / 360 * w
        py = y + (90 - lat) / 180 * h
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=PIN_COL[n],
                  outline=(255, 255, 255), width=1)
        d.text((px - 3, py - 6), str(n), font=SANS_B(9), fill=(255, 255, 255))


# ---------------------------------------------------------------- page
def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)

    # kicker
    d.text((16, 12), "THE WORLD\u2019S NEWS IN ONE PICTURE",
           font=SANS_B(13), fill=RED)
    right = "48 STORIES \u00b7 6 CONTINENTS \u00b7 ALL FROM TUESDAY"
    d.text((W - 16 - d.textlength(right, font=SANS_B(13)), 12), right,
           font=SANS_B(13), fill=INK)
    # masthead
    d.text((16, 30), "Tuesday 17 November 2026", font=SERIF_B(56), fill=INK)
    d.text((16, 96), "Every story here happened or was first reported on "
           "Tuesday 17 November 2026.",
           font=SERIF(13), fill=GREY)
    # region strip
    strip = [("EUROPE 17", NAVY), ("MIDDLE EAST 8", (180, 120, 0)),
             ("ASIA 11", (120, 60, 160)), ("AFRICA 3", (0, 130, 60)),
             ("AMERICAS 8", RED), ("WORLD 1", GREY)]
    sx = 16
    for label, col in strip:
        tw = d.textlength(label, font=SANS_B(11)) + 16
        d.rectangle([sx, 116, sx + tw, 134], fill=col)
        d.text((sx + 8, 119), label, font=SANS_B(11), fill=(255, 255, 255))
        sx += tw + 6

    # ---- leads
    lx = [16, 350, 684]
    for i, st in enumerate(LEADS):
        x = lx[i]
        w = 324
        ART[st["art"]](d, x, 142, w, 96)
        panel_frame(d, x, 142, w, 96)
        d.text((x, 244), f"{st['n']}  ·  {st['tag']}", font=SANS_B(11), fill=RED)
        y = para(d, x, 260, st["head"], SANS_B(18), w, leading=21, max_lines=2)
        para(d, x, y + 2, st["body"], SANS(12), w, leading=15, max_lines=2)

    d.line([16, 338, W - 16, 338], fill=INK, width=1)

    # ---- grid, 5 x 2
    gx = [16, 214, 412, 610, 808]
    gy = [344, 480]
    for i, st in enumerate(GRID):
        x, y = gx[i % 5], gy[i // 5]
        w = 196
        ART[st["art"]](d, x, y, w, 52)
        panel_frame(d, x, y, w, 52)
        d.text((x, y + 58), f"{st['n']}  ·  {st['tag']}", font=SANS_B(9), fill=RED)
        yy = para(d, x, y + 72, st["head"], SANS_B(14), w, leading=16, max_lines=2)
        para(d, x, yy + 1, st["body"], SANS(11), w, leading=13, max_lines=2)

    # ---- by the numbers
    d.line([16, 614, W - 16, 614], fill=INK, width=1)
    d.text((16, 620), "BY THE NUMBERS", font=SANS_B(11), fill=RED)
    nums = [("1,441", "record drones downed overnight"),
            ("$115.8bn", "Nvidia revenue, up 103%"),
            ("11,000", "Ebola cases in DR Congo"),
            ("849", "points the Dow fell on Tuesday")]
    nx = 150
    for val, lab in nums:
        d.text((nx, 618), val, font=SERIF_B(20), fill=INK)
        d.text((nx, 640), lab, font=SANS(10), fill=GREY)
        nx += 215
    d.line([16, 660, W - 16, 660], fill=INK, width=1)

    # ---- map + briefs
    d.text((16, 668), "WHERE IT HAPPENED", font=SANS_B(12), fill=RED)
    draw_map(d, 16, 688, 292, 268)
    d.text((16, 960), "Pins: stories 1\u201313 \u00b7 dots: briefs 14\u201348",
           font=SANS(10), fill=GREY)
    bx = 322
    d.text((bx, 668), "ALSO ON TUESDAY 17 NOVEMBER \u2014 35 MORE STORIES",
           font=SANS_B(12), fill=RED)
    cols = [BRIEFS[i:i + 12] for i in (0, 12, 24)]
    for ci, col in enumerate(cols):
        cx = bx + ci * 232
        cy = 688
        for n, txt in col:
            d.text((cx, cy), str(n), font=SANS_B(11), fill=RED)
            cy = para(d, cx + 22, cy, txt, SANS(10), 208, leading=11,
                      max_lines=2)
            cy += 2

    # ---- footer
    d.line([16, 984, W - 16, 984], fill=INK, width=1)
    d.text((16, 990),
           "DATE CHECK \u2014 Left out on purpose: Ebola passed 11,000 on 10 Nov; "
           "Vulcan lost 40 satellites on 15 Nov. Disputed claims are attributed.",
           font=SANS(10), fill=INK)
    d.text((16, 1004), "Sources: Reuters, AP, BBC, Al Jazeera, WHO, UN. Original drawings.",
           font=SANS(10), fill=GREY)

    img.save(out_path, "PNG", optimize=True)
    return img


if __name__ == "__main__":
    build("entry.png")
    print("wrote entry.png")
