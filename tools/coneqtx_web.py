"""ConeqTX desktop referral-link tutorial: RAW -> CLEAN -> FINAL + review board.

Usage: python3 coneqtx_web.py <folder with raw screenshots 1.jpg 2.webp 3.png 4.png>
"""
import os
import sys

from PIL import Image

from make_tutorial import render
from redact import redact
from review_board import review_board

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Tutorials", "ConeqTX Desktop")
PLATFORM = "CONEQTX"
DONE = "You're done - your link is ready to share"

# Private info to cover in each RAW screenshot (x0, y0, x1, y1).
# Username and referral link are ALWAYS covered.
RAW = {
    "dashboard": ("1.jpg", [
        (812, 105, 922, 135),                     # name in welcome banner
        (1476, 10, 1516, 30),                     # TL account number
        (74, 349, 118, 363), (74, 366, 150, 380),  # profile name + ID
        (658, 429, 694, 444),                     # account balance
        (905, 417, 1570, 434), (905, 488, 1570, 505),  # P&L figures
        (30, 612, 115, 628), (30, 640, 160, 658),  # active trades
    ]),
    "profile_menu": ("2.webp", [
        (812, 105, 922, 135),
        (1478, 11, 1518, 28),
        (1408, 54, 1508, 69), (1408, 71, 1494, 86),  # menu name + ID
        (72, 350, 116, 364), (72, 367, 148, 381),
        (658, 430, 694, 445),
        (905, 418, 1570, 435), (905, 489, 1570, 506),
        (28, 614, 113, 630), (28, 642, 160, 660),
    ]),
    "my_account": ("3.png", [
        (1473, 8, 1572, 26),     # name in header
        (199, 197, 253, 214),    # username
        (669, 196, 716, 213),    # membership id
        (1138, 197, 1266, 214),  # referral link
        (199, 278, 314, 295),    # full name
        (199, 352, 268, 372),    # password
        (669, 358, 832, 390),    # birth date
        (1138, 359, 1262, 376),  # email
        (669, 452, 830, 470),    # enroller
        (1138, 452, 1204, 470),  # enroller phone
        (199, 533, 393, 551),    # enroller email
        (669, 533, 758, 551),    # day phone
        (1138, 533, 1228, 551),  # mobile
    ]),
    "referral_links": ("4.png", [
        (1522, 222, 1566, 238),  # member id
        (1515, 250, 1566, 266),  # username
        (1445, 278, 1566, 294),  # email
        (225, 0, 560, 12),       # commission figures
        (1538, 6, 1556, 21),     # bonus volume
    ]),
}

profile = dict(slug="profile", screen="dashboard", label="Profile icon",
               title="Click the profile icon", hint="It's at the top right of the dashboard.",
               crop=(540, 0, 1600, 560), target=(1529, 6, 1557, 34), badge_side="below")
settings = dict(slug="account-settings", screen="profile_menu", label="Account Settings",
                title="Click “Account Settings”", hint="It's the first option in the profile menu.",
                crop=(540, 0, 1600, 560), target=(1402, 97, 1506, 120), badge_side="left")

PATHS = {
    "A": [
        dict(profile, footer="Next: Click “Account Settings” →"),
        dict(settings, footer="Next: Find your “Referral Link” →"),
        dict(slug="referral-link", screen="my_account", label="Referral Link",
             title="Find your “Referral Link”", hint="It's on the My Account page.",
             crop=(420, 0, 1600, 320), target=(1133, 168, 1585, 228), badge_side="below",
             footer=DONE),
    ],
    "B": [
        dict(profile, footer="Next: Click “Account Settings” →"),
        dict(settings, footer="Next: Click the “CONECTIV” logo →"),
        dict(slug="conectiv-logo", screen="my_account", label="CONECTIV logo",
             title="Click the “CONECTIV” logo", hint="It's at the top left of the My Account page.",
             crop=(0, 0, 1040, 320), target=(6, 10, 165, 40),
             footer="Next: Click “Copy ConeqtX Link” →"),
        dict(slug="copy-link", screen="referral_links", label="Copy ConeqtX Link",
             title="Click “Copy ConeqtX Link”", hint="Scroll down to Referral Links.",
             crop=(0, 60, 1040, 330), target=(211, 199, 857, 228), footer=DONE),
    ],
}

rows = []
for path, steps in PATHS.items():
    d = os.path.join(OUT, f"Path {path}")
    os.makedirs(d, exist_ok=True)
    finals = []
    for i, s in enumerate(steps, 1):
        s = dict(s)
        base = os.path.join(d, f"coneqtx_web_{path}_{i:02d}_{s.pop('slug')}")
        raw_file, boxes = RAW[s.pop("screen")]
        Image.open(os.path.join(SRC, raw_file)).convert("RGB").save(base + "_RAW.png")
        clean = redact(base + "_RAW.png", base + "_CLEAN.png", boxes)
        label = s.pop("label")
        render(base + "_FINAL.png", PLATFORM, i, len(steps), shot=clean, **s)
        finals.append((label, base + "_FINAL.png"))
        print(base)
    rows.append((f"PATH {path}", finals))

review_board(os.path.join(OUT, "coneqtx_web_REVIEW_BOARD.png"), "CONEQTX — DESKTOP", rows)
