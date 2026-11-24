# render.py — news-image-20261124
# Draws "THE WORLD IN ONE DAY — Tuesday 24 November 2026" as a 1024x1024 PNG.
# Every illustration is drawn in code with PIL primitives (flat drawings, no photos).
# Fully deterministic: no randomness, no timestamps, no network.
# Run: python3 render.py  -> writes entry.png next to this file.

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

CREAM = (247, 242, 231)
PAPER = (252, 249, 240)
INK = (26, 26, 26)
RED = (176, 30, 30)
DARKRED = (140, 20, 20)
BLUE = (30, 74, 122)
GREEN = (34, 120, 60)
GREY = (110, 105, 95)
LIGHTGREY = (200, 194, 182)
GOLD = (198, 148, 32)
TEAL = (18, 110, 105)
ORANGE = (214, 110, 30)

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


def font_lib(name, size):
    return ImageFont.truetype(os.path.join(FL, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font_lib("LiberationSerif-Italic.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS_O = lambda s: font_lib("LiberationSans-Italic.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width. Returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None, align="left", width=None):
    """Draw lines of text; returns y after the last line."""
    if leading is None:
        leading = fnt.size + 3
    for ln in lines:
        if align == "center":
            draw.text((x + (width or 0) // 2, y), ln, font=fnt, fill=fill, anchor="ma")
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
# (num, headline, body, source, region) — featured stories carry a body.
LEADS = [
    (1, "ASIA RALLIES ON HUANG'S RETURN",
     "Kospi jumps 6.3% intraday, Nikkei up 3% and MSCI Asia +1.8% as Jensen "
     "Huang's return revives the AI trade. Nvidia had soared 31% on Monday; "
     "Nasdaq +6.51%, S&P +4.73%.",
     "Bloomberg / Yonhap", "AP"),
    (2, "US BLACKLISTS MEGASPEED",
     "Washington adds Singapore-based Megaspeed, the AI firm at the centre of "
     "the Nvidia scandal, to its trade blacklist, plus six affiliates. US firms "
     "will now need a licence to sell it chips.",
     "Reuters", "AP"),
    (3, "ZELENSKY: RUSSIA PLANNING NEW STRIKES",
     "Ukraine's president says intelligence shows Russia preparing new strikes "
     "and urges allies to send more air-defence missiles, as Kyiv and other "
     "cities face near-continuous attacks.",
     "Reuters", "EU"),
]

CARDS = [
    (4, "CANADA & QATAR TO SIGN PACT",
     "The two countries will sign an investment protection deal on Tuesday in "
     "Ottawa, unlocking Qatari investment pledged in January.",
     "Reuters", "NA"),
    (5, "MOSCOW WARNS ESTONIA",
     "Russia accuses Estonia of letting Ukrainian drones use its airspace and "
     "of acts 'on the verge of triggering open war'. Tallinn denies it. [CLAIM]",
     "Reuters", "EU"),
    (6, "IRAN VOWS TO FIGHT BLOCKADE",
     "Tehran says it will use 'all available means' to confront the US naval "
     "blockade of its ports.",
     "Reuters", "ME"),
    (7, "GAZA A 'TOXIC WASTELAND'",
     "Oxfam: Israeli attacks left signs of contamination across 99% of Gaza; "
     "air, soil and water dangerous for decades.",
     "BBC", "ME"),
    (8, "SINGER FLOGGED 74 TIMES",
     "Iran lashed Parastoo Ahmadi and four bandmates, 74 lashes each, for a "
     "2024 concert performed without a hijab.",
     "BBC", "ME"),
    (9, "TRUMP'S MEME-COIN GALA",
     "Trump will welcome investors at a gala for his plunging meme coin.",
     "Reuters", "NA"),
    (10, "ARMENIA'S NEW CONSTITUTION",
     "Pashinyan unveils a draft charter dropping the Karabakh claim, a key "
     "step to a peace treaty with Azerbaijan.",
     "Reuters", "EU"),
    (11, "DENMARK: PHONES OUT OF SCHOOL",
     "Copenhagen will propose banning phones in primary and lower secondary "
     "schools from the 2027 school year.",
     "Reuters", "EU"),
    (12, "OETTINGER'S 5TH SHUTOUT",
     "Jake Oettinger blanks the Penguins as the Dallas Stars win in the NHL.",
     "Reuters", "NA"),
    (13, "UK PMI SLOWS SLIGHTLY",
     "Britain's November PMI shows a slight slowdown, but the fourth quarter "
     "still looks robust.",
     "Reuters", "EU"),
]

# (num, one-line headline, source, region)
INDEX = [
    (14, "Trump saw Nvidia's Huang as protector of open-weight AI models", "Reuters", "NA"),
    (15, "Trump tells CNBC he was represented at Nvidia board, spoke to Huang", "Reuters", "NA"),
    (16, "Nvidia bears face a $12.2bn hit on Huang's surprise return", "Reuters", "NA"),
    (17, "US lawmakers slam Huang return: Cotton wants Chip Security Act; Warren calls it 'reckless'", "Reuters", "NA"),
    (18, "Mexico and China agree a working group to boost trade", "Reuters", "LATAM"),
    (19, "US states back Epic Games as Apple asks Supreme Court to overturn contempt order", "Reuters", "NA"),
    (20, "US requests extradition of arrested Mexican drug lord 'El Chapo Isidro'", "Reuters", "LATAM"),
    (21, "US discussing military training for Syrian forces", "Reuters", "ME"),
    (22, "China, EU officials discuss exchange rates; PBOC chief Pan urges cooperation", "Reuters", "AP"),
    (23, "Belgian PM sets 31 Dec budget talks deadline amid national strike", "Reuters", "EU"),
    (24, "Russian Urals oil discounts widen at Indian ports", "Reuters", "AP"),
    (25, "WHO chief: fighting near Congo Ebola outbreak area disrupts response", "Reuters", "AF"),
    (26, "14 countries 'acknowledge' ICJ ruling on Rohingya 'genocide'", "Reuters", "AP"),
    (27, "Amazon to buy Decart's AI chip optimisation tech in latest AI talent grab", "Reuters", "NA"),
    (28, "Aviation groups urge at least a $30bn boost for FAA modernisation", "Reuters", "NA"),
    (29, "Turkish pro-Kurdish party confirms better conditions for militant who launched peace push", "Reuters", "EU"),
    (30, "Trump thinks China will buy another 250 Boeing airplanes", "Reuters", "NA"),
    (31, "EU urges multilateral talks to continue after COP31 collapse", "Reuters", "EU"),
    (32, "UN Security Council holds briefing on Ukraine", "Reuters LIVE", "GLOBAL"),
    (33, "Zelenskiy addresses the German parliament", "Reuters LIVE", "EU"),
    (34, "Israeli airstrike kills at least 3 in Khan Younis near a police outpost, 5 wounded", "Reuters", "ME"),
    (35, "North Korea weighs shutting Swiss office in Pyongyang over camp sanctions", "Reuters", "AP"),
    (36, "Severe drought pushes millions in Afghanistan deeper into crisis", "PBS", "AP"),
    (37, "Indonesia factory fire: 24 dead, 34 missing after sweet factory blaze", "24 Nov feed", "AP"),
    (38, "UN criticises airstrikes on Khartoum thought launched from Ethiopian soil", "24 Nov feed", "AF"),
    (39, "Zambia opposition leader charged with seeking to overthrow the government", "24 Nov feed", "AF"),
    (40, "Bangladesh vows to capture Sheikh Hasina after her return from India", "24 Nov feed", "AP"),
    (41, "Landmine blast kills five minors in northwest Syria", "24 Nov feed", "ME"),
    (42, "Chinese state official sentenced to death over disclosing state secrets", "24 Nov feed", "AP"),
    (43, "Estonian PM denies Trump encouraged Europe to stop Ukraine aid", "24 Nov feed", "EU"),
    (44, "Top Chinese and Swiss envoys discuss Korean Peninsula at Nanjing meeting", "24 Nov feed", "AP"),
    (45, "Iraqi PM arrives in Egypt on first official visit after taking office", "24 Nov feed", "AF"),
    (46, "Kremlin delays questions on the Libya incident to the armed forces", "24 Nov feed", "EU"),
    (47, "Moscow and St Petersburg residents report internet and mobile outages", "24 Nov feed", "EU"),
    (48, "Mossad operatives helped thwart the 2024 Taylor Swift Vienna attack, ex-chief says", "24 Nov feed", "EU"),
    (49, "Disputed West Bank 'military zones' become practically Israeli settler property", "24 Nov feed", "ME"),
    (50, "Soldiers in Mexico attacked after the arrest of a drug lord", "24 Nov feed", "LATAM"),
    (51, "US enacts new sanctions on dozens linked to Iran shadow banking networks", "24 Nov feed", "NA"),
    (52, "China's Korean Wave ban seems nearing a lift after a trade deal", "24 Nov feed", "AP"),
    (53, "Returning to the EU without a referendum is 'impossible', says Andy Burnham", "24 Nov feed", "EU"),
    (54, "Iranian courts direct the US to pay $290bn in damages [CLAIM]", "24 Nov feed", "ME"),
    (55, "The Gulf prepares for a tougher Democrat-controlled Congress (analysis)", "24 Nov feed", "ME"),
    (56, "Kitten 'Dym' survives a week under the ruins of the Dymer building", "24 Nov feed", "EU"),
    (57, "Bitcoin ~$63,400, gold ~$3,666/oz after Monday's rebound (Mon closes)", "BeInCrypto", "AP"),
    (58, "SK hynix +8.5%, Samsung +7%, TAIEX futures +8.65%, KOSPI 200 night futures +7.06%", "Bloomberg", "AP"),
    (59, "Moscow signals renewing negotiations with the US and Kyiv", "24 Nov feed", "EU"),
    (60, "South Korea says a suspected DPRK aircraft violated its airspace", "24 Nov feed", "AP"),
]

NUMBERS = [
    ("KOSPI +6.3%", "Nikkei +3%  (Tue Asia)"),
    ("NVIDIA +31%", "Nasdaq +6.51%  (Mon)"),
    ("153 / 134", "drones, night 22-23 Nov"),
    ("$12.2bn", "hit for Nvidia bears on Huang's return"),
    ("99%", "of Gaza shows contamination signs (Oxfam)"),
    ("24 dead", "Indonesia factory fire; 34 missing"),
]

# Drones fired per night (Ukrainian Air Force, via Ukrinform). Last bar = pending.
CHART = [("19-20", 404), ("20-21", 148), ("21-22", 186), ("22-23", 153)]

DATE_CHECK = ("NOT 24 NOV - LEFT OUT: COP31 collapse (22 Nov) - Huang reinstated "
    "(23 Nov) - Kilauea ep. 57 (23 Nov) - Benghazi warship strike (22 Nov) - "
    "EU sanctions package (23 Nov) - Trump Iran-strike threat (22 Nov) - "
    "Zaporizhzhia clinic, 3 dead (23 Nov) - UK concert evacuation (22-23 Nov) - "
    "S. Korea reshuffle (23 Nov) - Tajikistan leaves ICC (23 Nov) - Georgia "
    "surrogacy ban (22 Nov) - Kenya-DR Congo deal (22 Nov) - Pew ICE poll "
    "(23 Nov) - Gaza vehicle strike (23 Nov).")

NOT_YET = ("NOT YET HAPPENED: Ukraine's 23-24 Nov overnight drone tally (due "
    "~06:00 UTC) - October PCE inflation - EU €45bn Ukraine loan - EU leaders' "
    "summit - Nvidia earnings - Kilauea ep. 58 window - US Thanksgiving.")

WATCH = ("WHAT TO WATCH ON WEDNESDAY (25 NOV): October PCE inflation, the Fed's "
    "gauge - EU unveils its €45bn Ukraine loan - EU leaders' summit opens Thu - "
    "US markets shut Thu for Thanksgiving.")


# ---------------------------------------------------------------- illustrations
# Each draws a small flat scene into box (x, y, w, h). All coordinates are
# relative to the box; nothing is loaded from disk.

def ill_rally(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 244))
    # buildings
    for bx, bw, bh in [(0.06, 0.14, 0.45), (0.24, 0.12, 0.62), (0.40, 0.16, 0.38)]:
        d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h], fill=(90, 120, 150))
    # rising bars + arrow
    base = y + h * 0.86
    bars = [(0.58, 0.30), (0.68, 0.48), (0.78, 0.66), (0.88, 0.84)]
    for bx, bh in bars:
        d.rectangle([x + w * bx, base - h * bh, x + w * (bx + 0.06), base], fill=GREEN)
    pts = [(x + w * 0.56, base - h * 0.28), (x + w * 0.68, base - h * 0.46),
           (x + w * 0.78, base - h * 0.64), (x + w * 0.92, base - h * 0.82)]
    d.line(pts, fill=GREEN, width=3)
    d.polygon([(x + w * 0.92, base - h * 0.82), (x + w * 0.86, base - h * 0.80),
               (x + w * 0.90, base - h * 0.72)], fill=GREEN)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_megaspeed(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 44, 54))
    # server racks
    for i, rx in enumerate([0.08, 0.38, 0.68]):
        d.rectangle([x + w * rx, y + h * 0.14, x + w * (rx + 0.24), y + h * 0.86], fill=(70, 80, 95))
        for j in range(3):
            ly = y + h * (0.24 + j * 0.22)
            d.ellipse([x + w * (rx + 0.03), ly, x + w * (rx + 0.07), ly + 4], fill=(120, 220, 130) if i != 1 else (230, 80, 60))
            d.rectangle([x + w * (rx + 0.10), ly, x + w * (rx + 0.21), ly + 3], fill=(160, 170, 185))
    # red ban circle over a chip
    cx, cy, r = x + w * 0.52, y + h * 0.5, h * 0.30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=4)
    d.line([cx - r * 0.7, cy + r * 0.7, cx + r * 0.7, cy - r * 0.7], fill=RED, width=4)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_zelensky(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.55], fill=(30, 90, 160))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(240, 200, 40))
    # podium + speaker silhouette
    d.rectangle([x + w * 0.42, y + h * 0.62, x + w * 0.58, y + h * 0.95], fill=(60, 60, 70))
    d.ellipse([x + w * 0.46, y + h * 0.50, x + w * 0.54, y + h * 0.62], fill=(60, 60, 70))
    d.line([x + w * 0.30, y + h * 0.62, x + w * 0.44, y + h * 0.52], fill=INK, width=2)
    d.ellipse([x + w * 0.28, y + h * 0.48, x + w * 0.32, y + h * 0.54], fill=INK)
    # drone + warning triangle in the sky
    dx, dy = x + w * 0.78, y + h * 0.22
    d.ellipse([dx - 8, dy - 4, dx + 8, dy + 4], fill=(40, 40, 40))
    d.line([dx - 14, dy - 8, dx + 14, dy - 8], fill=(40, 40, 40), width=2)
    d.line([dx - 14, dy + 8, dx + 14, dy + 8], fill=(40, 40, 40), width=2)
    tx, ty = x + w * 0.16, y + h * 0.20
    d.polygon([(tx, ty - 10), (tx - 11, ty + 9), (tx + 11, ty + 9)], fill=(240, 180, 20), outline=INK)
    d.text((tx, ty - 2), "!", font=SANS_B(10), fill=INK, anchor="mm")
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_canada_qatar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 238, 228))
    # Canada flag (red-white-red + maple dot)
    d.rectangle([x + w * 0.06, y + h * 0.18, x + w * 0.44, y + h * 0.62], fill=(255, 255, 255), outline=INK)
    d.rectangle([x + w * 0.06, y + h * 0.18, x + w * 0.14, y + h * 0.62], fill=RED)
    d.rectangle([x + w * 0.36, y + h * 0.18, x + w * 0.44, y + h * 0.62], fill=RED)
    d.ellipse([x + w * 0.21, y + h * 0.32, x + w * 0.29, y + h * 0.48], fill=RED)
    # Qatar flag (maroon + white zigzag)
    d.rectangle([x + w * 0.56, y + h * 0.18, x + w * 0.94, y + h * 0.62], fill=(140, 30, 60), outline=INK)
    for i in range(4):
        yy = y + h * (0.22 + i * 0.10)
        d.polygon([(x + w * 0.56, yy), (x + w * 0.64, yy + h * 0.05), (x + w * 0.56, yy + h * 0.10)], fill=(255, 255, 255))
    # document below
    d.rectangle([x + w * 0.30, y + h * 0.70, x + w * 0.70, y + h * 0.94], fill=(255, 255, 255), outline=INK)
    d.line([x + w * 0.35, y + h * 0.78, x + w * 0.65, y + h * 0.78], fill=GREY, width=1)
    d.line([x + w * 0.35, y + h * 0.85, x + w * 0.60, y + h * 0.85], fill=GREY, width=1)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_estonia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 242))
    # map pin
    px, py = x + w * 0.5, y + h * 0.42
    d.ellipse([px - 14, py - 14, px + 14, py + 14], fill=RED, outline=INK)
    d.polygon([(px - 12, py + 6), (px + 12, py + 6), (px, py + 26)], fill=RED, outline=INK)
    d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(255, 255, 255))
    # small drone crossing
    dx, dy = x + w * 0.82, y + h * 0.20
    d.ellipse([dx - 7, dy - 3, dx + 7, dy + 3], fill=(40, 40, 40))
    d.line([dx - 12, dy - 6, dx + 12, dy - 6], fill=(40, 40, 40), width=2)
    # ground line + border posts
    d.line([x + w * 0.08, y + h * 0.86, x + w * 0.92, y + h * 0.86], fill=INK, width=2)
    for bx in (0.18, 0.82):
        d.rectangle([x + w * bx - 2, y + h * 0.78, x + w * bx + 2, y + h * 0.86], fill=INK)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_blockade(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.62], fill=(190, 215, 235))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(40, 90, 140))
    # ship
    sx, sy = x + w * 0.16, y + h * 0.44
    d.polygon([(sx, sy), (sx + w * 0.42, sy), (sx + w * 0.36, sy + h * 0.16), (sx + w * 0.06, sy + h * 0.16)], fill=(70, 70, 80))
    d.rectangle([sx + w * 0.10, sy - h * 0.16, sx + w * 0.20, sy], fill=(70, 70, 80))
    d.rectangle([sx + w * 0.24, sy - h * 0.10, sx + w * 0.32, sy], fill=(180, 60, 50))
    # red barrier line across the sea
    d.line([x + w * 0.62, y + h * 0.30, x + w * 0.62, y + h * 0.92], fill=RED, width=4)
    d.line([x + w * 0.62, y + h * 0.30, x + w * 0.70, y + h * 0.38], fill=RED, width=3)
    d.line([x + w * 0.62, y + h * 0.30, x + w * 0.54, y + h * 0.38], fill=RED, width=3)
    # waves
    for wx in (0.10, 0.35, 0.70, 0.88):
        d.arc([x + w * wx, y + h * 0.78, x + w * (wx + 0.12), y + h * 0.92], 180, 360, fill=(255, 255, 255), width=2)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_oxfam(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.45], fill=(200, 200, 195))
    d.rectangle([x, y + h * 0.45, x + w, y + h], fill=(150, 110, 70))
    # cracked earth
    d.line([x + w * 0.10, y + h * 0.55, x + w * 0.35, y + h * 0.72, x + w * 0.30, y + h * 0.92], fill=(90, 60, 30), width=2)
    d.line([x + w * 0.35, y + h * 0.72, x + w * 0.62, y + h * 0.66], fill=(90, 60, 30), width=2)
    d.line([x + w * 0.70, y + h * 0.55, x + w * 0.62, y + h * 0.72, x + w * 0.80, y + h * 0.94], fill=(90, 60, 30), width=2)
    # smoke plumes
    for sx, sy, sr in [(0.22, 0.30, 12), (0.30, 0.20, 9), (0.72, 0.28, 11), (0.80, 0.18, 8)]:
        d.ellipse([x + w * sx - sr, y + h * sy - sr, x + w * sx + sr, y + h * sy + sr], fill=(120, 120, 118))
    # small dry sprout
    d.line([x + w * 0.50, y + h * 0.90, x + w * 0.50, y + h * 0.70], fill=(110, 90, 40), width=2)
    d.line([x + w * 0.50, y + h * 0.78, x + w * 0.40, y + h * 0.70], fill=(110, 90, 40), width=2)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_ahmadi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 36, 48))
    # stage light
    d.polygon([(x + w * 0.42, y), (x + w * 0.58, y), (x + w * 0.72, y + h * 0.75), (x + w * 0.28, y + h * 0.75)], fill=(80, 76, 100))
    # microphone on stand
    mx, my = x + w * 0.5, y + h * 0.34
    d.ellipse([mx - 9, my - 11, mx + 9, my + 11], fill=(200, 200, 205), outline=INK)
    d.line([mx, my + 11, mx, y + h * 0.88], fill=(200, 200, 205), width=3)
    d.line([mx - 12, y + h * 0.88, mx + 12, y + h * 0.88], fill=(200, 200, 205), width=3)
    # musical note
    d.text((x + w * 0.80, y + h * 0.18), "\u266a", font=SANS_B(16), fill=(240, 200, 60))
    # red slash across the mic
    d.line([mx - 16, my + 14, mx + 16, my - 14], fill=RED, width=4)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_coin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 235, 210))
    # gold coin
    cx, cy, r = x + w * 0.42, y + h * 0.48, h * 0.30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD, outline=(140, 100, 20), width=2)
    d.ellipse([cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7], outline=(140, 100, 20), width=1)
    d.text((cx, cy), "$", font=SANS_B(int(h * 0.34)), fill=(120, 85, 10), anchor="mm")
    # plunging red arrow
    ax0, ay0 = x + w * 0.72, y + h * 0.16
    d.line([(ax0, ay0), (x + w * 0.86, y + h * 0.42), (x + w * 0.94, y + h * 0.66)], fill=RED, width=3)
    d.polygon([(x + w * 0.94, y + h * 0.66), (x + w * 0.86, y + h * 0.62), (x + w * 0.94, y + h * 0.54)], fill=RED)
    # party flags
    d.line([x + w * 0.06, y + h * 0.14, x + w * 0.94, y + h * 0.14], fill=GREY, width=1)
    for fx, fc in [(0.12, RED), (0.30, BLUE), (0.48, GREEN), (0.66, GOLD), (0.84, RED)]:
        d.polygon([(x + w * fx, y + h * 0.14), (x + w * (fx + 0.08), y + h * 0.14), (x + w * (fx + 0.04), y + h * 0.26)], fill=fc)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_armenia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(225, 235, 245))
    # mountain (Ararat)
    d.polygon([(x + w * 0.05, y + h * 0.85), (x + w * 0.30, y + h * 0.30), (x + w * 0.55, y + h * 0.85)], fill=(120, 140, 170))
    d.polygon([(x + w * 0.24, y + h * 0.42), (x + w * 0.30, y + h * 0.30), (x + w * 0.36, y + h * 0.42)], fill=(255, 255, 255))
    # document with seal
    d.rectangle([x + w * 0.58, y + h * 0.30, x + w * 0.94, y + h * 0.86], fill=(255, 255, 255), outline=INK)
    for i in range(3):
        d.line([x + w * 0.63, y + h * (0.40 + i * 0.10), x + w * 0.89, y + h * (0.40 + i * 0.10)], fill=GREY, width=1)
    d.ellipse([x + w * 0.70, y + h * 0.68, x + w * 0.82, y + h * 0.80], fill=RED)
    # dove
    dx, dy = x + w * 0.72, y + h * 0.16
    d.ellipse([dx - 8, dy - 4, dx + 8, dy + 4], fill=(255, 255, 255), outline=INK)
    d.polygon([(dx - 8, dy), (dx - 20, dy - 8), (dx - 16, dy + 2)], fill=(255, 255, 255), outline=INK)
    d.polygon([(dx + 2, dy - 4), (dx + 8, dy - 16), (dx + 12, dy - 4)], fill=(255, 255, 255), outline=INK)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_denmark(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 228, 210))
    # desk
    d.rectangle([x + w * 0.10, y + h * 0.62, x + w * 0.90, y + h * 0.70], fill=(150, 105, 60))
    d.rectangle([x + w * 0.14, y + h * 0.70, x + w * 0.18, y + h * 0.92], fill=(120, 85, 45))
    d.rectangle([x + w * 0.82, y + h * 0.70, x + w * 0.86, y + h * 0.92], fill=(120, 85, 45))
    # book
    d.rectangle([x + w * 0.60, y + h * 0.48, x + w * 0.88, y + h * 0.62], fill=(255, 255, 255), outline=INK)
    d.line([x + w * 0.74, y + h * 0.48, x + w * 0.74, y + h * 0.62], fill=INK, width=1)
    # phone with red slash
    px, py = x + w * 0.30, y + h * 0.38
    d.rectangle([px - 11, py - 18, px + 11, py + 18], fill=(40, 40, 48), outline=INK)
    d.rectangle([px - 7, py - 13, px + 7, py + 10], fill=(120, 180, 220))
    d.ellipse([px - 16, py - 22, px + 16, py + 22], outline=RED, width=3)
    d.line([px - 13, py + 17, px + 13, py - 17], fill=RED, width=3)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_nhl(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 228, 242))
    # rink lines
    d.line([x, y + h * 0.30, x + w, y + h * 0.30], fill=RED, width=2)
    d.line([x, y + h * 0.70, x + w, y + h * 0.70], fill=BLUE, width=2)
    # goal net
    gx, gy = x + w * 0.68, y + h * 0.42
    d.rectangle([gx, gy, gx + w * 0.24, gy + h * 0.34], outline=RED, width=2)
    for i in range(1, 4):
        d.line([gx + w * 0.06 * i, gy, gx + w * 0.06 * i, gy + h * 0.34], fill=(200, 200, 200), width=1)
    # goalie silhouette
    px, py = x + w * 0.30, y + h * 0.55
    d.ellipse([px - 8, py - 22, px + 8, py - 6], fill=(30, 60, 110))
    d.rectangle([px - 10, py - 6, px + 10, py + 14], fill=(30, 60, 110))
    d.line([px + 8, py - 2, px + 22, py + 8], fill=(120, 80, 40), width=3)
    # puck
    d.ellipse([x + w * 0.55, y + h * 0.80, x + w * 0.55 + 10, y + h * 0.80 + 6], fill=INK)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_pmi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 232, 238))
    # factory
    d.rectangle([x + w * 0.08, y + h * 0.45, x + w * 0.55, y + h * 0.88], fill=(90, 100, 115))
    d.polygon([(x + w * 0.08, y + h * 0.45), (x + w * 0.30, y + h * 0.28), (x + w * 0.55, y + h * 0.45)], fill=(70, 80, 95))
    d.rectangle([x + w * 0.58, y + h * 0.30, x + w * 0.64, y + h * 0.88], fill=(90, 100, 115))
    d.rectangle([x + w * 0.68, y + h * 0.42, x + w * 0.73, y + h * 0.88], fill=(90, 100, 115))
    # smoke
    d.ellipse([x + w * 0.58, y + h * 0.16, x + w * 0.66, y + h * 0.28], fill=(170, 170, 170))
    d.ellipse([x + w * 0.64, y + h * 0.10, x + w * 0.70, y + h * 0.20], fill=(190, 190, 190))
    # small chart bars, slightly down
    base = y + h * 0.88
    for i, bh in enumerate([0.42, 0.34, 0.26]):
        bx = 0.76 + i * 0.08
        d.rectangle([x + w * bx, base - h * bh, x + w * (bx + 0.05), base], fill=TEAL)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


ILL = {1: ill_rally, 2: ill_megaspeed, 3: ill_zelensky, 4: ill_canada_qatar,
       5: ill_estonia, 6: ill_blockade, 7: ill_oxfam, 8: ill_ahmadi, 9: ill_coin,
       10: ill_armenia, 11: ill_denmark, 12: ill_nhl, 13: ill_pmi}


# ---------------------------------------------------------------- world map
# Continents as ellipses in lon/lat; dots are drawn where inside any ellipse.
LAND = [
    (-100, 50, 34, 17), (-90, 34, 20, 11), (-125, 44, 11, 9), (-86, 18, 9, 7),
    (-60, -10, 14, 19), (-70, -32, 8, 10),
    (10, 52, 17, 7), (26, 60, 12, 7),
    (15, 6, 19, 21), (30, -20, 11, 11),
    (70, 50, 44, 17), (100, 30, 24, 14), (45, 30, 14, 9), (78, 20, 9, 11),
    (105, 14, 11, 9), (135, -25, 14, 7),
]


def _inside(lon, lat):
    for clt, clat, rx, ry in LAND:
        if ((lon - clt) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1.0:
            return True
    return False


def lonlat_to_xy(lon, lat, x, y, w, h):
    px = x + (lon + 180.0) / 360.0 * w
    py = y + (90.0 - lat) / 180.0 * h
    return px, py


# (story num, city label, lon, lat, label dx, dy) — on-map labels only where
# they do not collide; the legend under the map names every pin.
PINS = [
    (1, "Seoul", 127, 37, 6, -10), (2, "Singapore", 104, 1, 6, -8),
    (3, "", 30, 50, 0, 0), (4, "Ottawa", -75, 45, -38, -10),
    (5, "", 25, 59, 0, 0), (6, "Tehran", 51, 35, 6, -8),
    (7, "", 34, 31, 0, 0), (9, "", 44, 40, 0, 0),
    (10, "", 12, 55, 0, 0), (11, "London", 0, 51, -34, 8),
    (12, "Pittsburgh", -80, 40, -44, 10), (35, "Pyongyang", 127, 39, -58, 8),
    (37, "Jakarta", 107, -6, 6, -8), (38, "Khartoum", 32, 15, 6, -8),
    (40, "Dhaka", 90, 23, 6, -8), (41, "", 36, 33, 0, 0),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 246))
    step = 6
    lon0, lon1, lat0, lat1 = -180, 180, 84, -58
    ix = 0
    xx = x + 3
    while xx < x + w - 3:
        lon = lon0 + (xx - x) / w * (lon1 - lon0)
        yy = y + 3
        while yy < y + h - 3:
            lat = lat0 - (yy - y) / h * (lat0 - lat1)
            if _inside(lon, lat):
                d.ellipse([xx - 1, yy - 1, xx + 1, yy + 1], fill=(120, 140, 160))
            yy += step
        xx += step
        ix += 1
    # pins
    fnum = SANS_B(8)
    flab = SANS(8)
    for num, city, lon, lat, dx, dy in PINS:
        px, py = lonlat_to_xy(lon, lat, x, y, w, h)
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=(255, 255, 255), width=1)
        tw = d.textlength(str(num), font=fnum)
        d.text((px - tw / 2, py - 4), str(num), font=fnum, fill=(255, 255, 255))
        if city:
            d.text((px + dx, py + dy), city, font=flab, fill=INK)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def draw_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    fT = SANS_B(10)
    fS = SANS(8)
    d.text((x + 8, y + 6), "DRONES FIRED PER NIGHT (UKRAINE)", font=fT, fill=INK)
    d.text((x + 8, y + 20), "Ukrainian Air Force, via Ukrinform", font=fS, fill=GREY)
    bx0, by0 = x + 14, y + h - 32
    bw, gap = 46, 12
    maxv = 404
    for i, (lab, val) in enumerate(CHART):
        bx = bx0 + i * (bw + gap)
        bh = (h - 74) * val / maxv
        d.rectangle([bx, by0 - bh, bx + bw, by0], fill=BLUE)
        d.text((bx + bw / 2, by0 - bh - 12), str(val), font=SANS_B(9), fill=INK, anchor="ma")
        d.text((bx + bw / 2, by0 + 4), lab, font=fS, fill=INK, anchor="ma")
    # pending bar
    bx = bx0 + 4 * (bw + gap)
    d.rectangle([bx, by0 - 8, bx + bw, by0], outline=RED, width=1)
    d.line([bx, by0 - 8, bx + bw, by0], fill=RED, width=1)
    d.line([bx, by0, bx + bw, by0 - 8], fill=RED, width=1)
    d.text((bx + bw / 2, by0 - 22), "?", font=SANS_B(11), fill=RED, anchor="ma")
    d.text((bx + bw / 2, by0 + 4), "23-24", font=fS, fill=RED, anchor="ma")
    d.text((x + 8, y + h - 13), "23-24 night: not yet published at press time (posts ~06:00 UTC).",
           font=fS, fill=RED)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 16  # margin

    # top rule
    d.rectangle([0, 0, W, 7], fill=RED)

    # masthead
    f_mast = SERIF_B(25)
    d.text((W // 2, 30), "THE WORLD IN ONE DAY", font=f_mast, fill=INK, anchor="mm")
    d.text((M, 30), "No. 328", font=SANS(10), fill=GREY, anchor="lm")
    d.text((W - M, 30), "60 STORIES", font=SANS_B(10), fill=RED, anchor="rm")
    hrule(d, M, W - M, 44, fill=INK, width=2)

    # date
    f_date = SERIF_B(30)
    d.text((W // 2, 68), "Tuesday 24 November 2026", font=f_date, fill=INK, anchor="mm")
    hrule(d, M, W - M, 88, fill=INK, width=1)

    # red deck
    f_deck = SERIF_I(13)
    deck = ("Asia rallies as Huang returns  \u2022  US blacklists Megaspeed  "
            "\u2022  Zelensky warns of new Russian strikes")
    d.text((W // 2, 102), deck, font=f_deck, fill=RED, anchor="mm")

    # numbers band
    y0, bh = 114, 34
    bw = (W - 2 * M - 5 * 4) // 6
    f_nb = SANS_B(13)
    f_ns = SANS(8)
    for i, (big, small) in enumerate(NUMBERS):
        bx = M + i * (bw + 4)
        d.rectangle([bx, y0, bx + bw, y0 + bh], fill=PAPER, outline=INK, width=1)
        d.text((bx + bw / 2, y0 + 4), big, font=f_nb, fill=RED, anchor="ma")
        lines = wrap(d, small, f_ns, bw - 8)
        text_block(d, bx + 4, y0 + 20, lines[:1], f_ns, fill=GREY)
    hrule(d, M, W - M, y0 + bh + 6, fill=INK, width=1)

    # region band
    regions = {}
    for _, _, _, _, reg in LEADS + CARDS:
        regions[reg] = regions.get(reg, 0) + 1
    for _, _, _, reg in INDEX:
        regions[reg] = regions.get(reg, 0) + 1
    order = ["AP", "EU", "ME", "NA", "AF", "LATAM", "GLOBAL"]
    names = {"AP": "ASIA-PACIFIC", "EU": "EUROPE", "ME": "MIDDLE EAST",
             "NA": "N. AMERICA", "AF": "AFRICA", "LATAM": "LATIN AMERICA",
             "GLOBAL": "GLOBAL"}
    parts = [f"{names[r]} {regions.get(r, 0)}" for r in order]
    f_rb = SANS_B(10)
    d.text((W // 2, 164), "60 STORIES  \u2022  " + "  \u2022  ".join(parts), font=f_rb, fill=BLUE, anchor="mm")

    # timeline strip
    ty = 176
    d.rectangle([M, ty, W - M, ty + 34], fill=(255, 255, 255), outline=INK, width=1)
    d.text((M + 6, ty + 4), "DAY BY THE CLOCK \u2014 ALL TIMES UTC", font=SANS_B(9), fill=RED)
    tl = [("00:03", "TAIEX futures +8.65%"),
          ("00:06", "Kospi +5% triggers buy sidecar"),
          ("00:19", "Nikkei +2.7% in early trade"),
          ("02:01", "Kyiv Shahed air alert begins"),
          ("06:00", "Ukraine overnight tally due \u2014 PENDING"),
          ("12:00", "make.fun round 2 judging")]
    f_tt = SANS_B(8)
    f_tl = SANS(8)
    tx = M + 6
    for t, lab in tl:
        d.text((tx, ty + 17), t, font=f_tt, fill=RED)
        tw = d.textlength(t, font=f_tt)
        d.text((tx + tw + 3, ty + 17), lab, font=f_tl, fill=INK)
        tx += tw + 3 + d.textlength(lab, font=f_tl) + 14
        if tx > W - M - 60:
            break
    d.text((M + 6, ty + 17), "", font=f_tl, fill=INK)

    # leads
    ly = 216
    lh = 152
    lw = (W - 2 * M - 2 * 8) // 3
    for i, (num, head, body, src, reg) in enumerate(LEADS):
        bx = M + i * (lw + 8)
        d.rectangle([bx, ly, bx + lw, ly + lh], fill=PAPER, outline=INK, width=1)
        ILL[num](d, bx + 6, ly + 6, lw - 12, 52)
        yy = ly + 64
        d.text((bx + 6, yy), f"{num}.", font=SANS_B(12), fill=RED)
        hl = wrap(d, head, SERIF_B(13), lw - 26)
        text_block(d, bx + 24, yy, hl[:2], SERIF_B(13), fill=INK, leading=15)
        yy += 15 * len(hl[:2]) + 2
        bl = wrap(d, body, SANS(10), lw - 12)
        max_bl = max(2, (ly + lh - 18 - yy) // 12)
        text_block(d, bx + 6, yy, bl[:max_bl], SANS(10), fill=INK, leading=12)
        d.text((bx + 6, ly + lh - 16), f"Source: {src}", font=SANS_O(8), fill=GREY)

    # cards: 5 cols x 2 rows
    cy = ly + lh + 6
    ch = 78
    cw = (W - 2 * M - 4 * 6) // 5
    for i, (num, head, body, src, reg) in enumerate(CARDS):
        r, c = divmod(i, 5)
        bx = M + c * (cw + 6)
        by = cy + r * (ch + 5)
        d.rectangle([bx, by, bx + cw, by + ch], fill=PAPER, outline=INK, width=1)
        ILL[num](d, bx + 5, by + 5, 52, 52)
        tx0 = bx + 62
        hl = wrap(d, f"{num}. {head}", SANS_B(9), cw - 67)
        yy = text_block(d, tx0, by + 5, hl[:2], SANS_B(9), fill=INK, leading=10)
        bl = wrap(d, body, SANS(8), cw - 67)
        max_bl = max(1, (by + ch - 13 - yy - 1) // 9)
        text_block(d, tx0, yy + 1, bl[:max_bl], SANS(8), fill=GREY, leading=9)
        d.text((tx0, by + ch - 12), src, font=SANS_O(7), fill=GREY)

    # map + chart
    my = cy + 2 * ch + 5 + 8
    mh = 142
    mw = 636
    d.text((M, my), "WHERE IT HAPPENED", font=SANS_B(11), fill=RED)
    draw_map(d, M, my + 16, mw, mh - 16)
    cx0 = M + mw + 8
    cw2 = W - M - cx0
    d.text((cx0, my), "THE DRONE WAR, NIGHT BY NIGHT", font=SANS_B(11), fill=RED)
    draw_chart(d, cx0, my + 16, cw2, mh - 16)
    # legend under map
    leg = ("Pins = story numbers: 1 Seoul \u00b7 2 Singapore \u00b7 3 Kyiv \u00b7 4 Ottawa "
           "\u00b7 5 Tallinn \u00b7 6 Tehran \u00b7 7 Gaza \u00b7 9 Yerevan \u00b7 10 Copenhagen "
           "\u00b7 11 London \u00b7 12 Pittsburgh \u00b7 35 Pyongyang \u00b7 37 Jakarta "
           "\u00b7 38 Khartoum \u00b7 40 Dhaka \u00b7 41 Damascus")
    d.text((M, my + mh + 3), leg, font=SANS(8), fill=GREY)

    # index: 47 more stories, 3 columns
    iy = my + mh + 18
    d.text((M, iy), "THE REST OF THE DAY \u2014 47 MORE STORIES", font=SANS_B(11), fill=RED)
    hrule(d, M, W - M, iy + 15, fill=INK, width=1)
    colw = (W - 2 * M - 2 * 10) // 3
    f_ix = SANS(9)
    line_h = 12
    per_col = 16
    for ci in range(3):
        cx = M + ci * (colw + 10)
        chunk = INDEX[ci * per_col:(ci + 1) * per_col]
        yy = iy + 20
        for num, head, src, reg in chunk:
            line = f"{num}. {head} \u2014 {src}"
            # shrink to fit one line: drop source if too long
            if d.textlength(line, font=f_ix) > colw:
                line = f"{num}. {head}"
            if d.textlength(line, font=f_ix) > colw:
                words = line.split()
                while words and d.textlength(" ".join(words) + "\u2026", font=f_ix) > colw:
                    words.pop()
                line = " ".join(words) + "\u2026"
            d.text((cx, yy), line, font=f_ix, fill=INK)
            yy += line_h
    iy2 = iy + 20 + per_col * line_h

    # bottom boxes
    by = iy2 + 4
    bh2 = H - 18 - by
    bw2 = (W - 2 * M - 8) // 2
    max_box_lines = max(3, (bh2 - 22) // 10)
    # DATE CHECK
    d.rectangle([M, by, M + bw2, by + bh2], fill=(255, 245, 240), outline=RED, width=2)
    d.text((M + 6, by + 4), "DATE CHECK", font=SANS_B(10), fill=RED)
    dl = wrap(d, DATE_CHECK, SANS(8), bw2 - 12)
    text_block(d, M + 6, by + 18, dl[:max_box_lines], SANS(8), fill=INK, leading=10)
    # NOT YET + WATCH
    bx2 = M + bw2 + 8
    d.rectangle([bx2, by, bx2 + bw2, by + bh2], fill=(240, 246, 252), outline=BLUE, width=2)
    d.text((bx2 + 6, by + 4), "NOT YET HAPPENED  +  WHAT TO WATCH WEDNESDAY", font=SANS_B(9), fill=BLUE)
    nl = wrap(d, NOT_YET + " " + WATCH, SANS(8), bw2 - 12)
    text_block(d, bx2 + 6, by + 18, nl[:max_box_lines], SANS(8), fill=INK, leading=10)

    # footer
    d.text((W // 2, H - 11),
           "Sources: Reuters \u00b7 BBC \u00b7 Bloomberg \u00b7 Yonhap \u00b7 AP \u00b7 USGS \u00b7 Pew \u00b7 TradingView  |  "
           "Every story first reported Tue 24 Nov 2026 in some timezone, unless dated.  [CLAIM] = unverified claim.",
           font=SANS(8), fill=GREY, anchor="mm")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    path = build()
    size = os.path.getsize(path)
    print(f"wrote {path} ({size} bytes, limit 1048576)")
    im = Image.open(path)
    print(f"size: {im.size}, mode: {im.mode}")
