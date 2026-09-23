import os
import sys
from make_tutorial import render

SRC = sys.argv[1]  # folder with the raw screenshots 1.jpg, 2.webp, 3.png, 4.png
OUT = os.path.join(os.path.dirname(__file__), "..", "Tutorials", "ConeqTX Desktop")
P = "CONEQTX"

step1 = dict(title="Click the profile icon", hint="It's at the top right of the dashboard.",
             shot=f"{SRC}/1.jpg", crop=(540, 0, 1600, 560), target=(1529, 6, 1557, 34),
             badge_side="below")
step2 = dict(title="Click Account Settings", hint="It's the first option in the menu.",
             shot=f"{SRC}/2.webp", crop=(540, 0, 1600, 560), target=(1402, 97, 1506, 120),
             badge_side="left")

paths = {
    "A": [
        dict(step1, footer="Next: Click Account Settings →"),
        dict(step2, footer="Next: Find your Referral Link →"),
        dict(title="Find your Referral Link", hint="It's on the My Account page.",
             shot=f"{SRC}/3.png", crop=(420, 0, 1600, 320), target=(1133, 168, 1585, 228),
             badge_side="below", footer="You're done - your link is ready to share"),
    ],
    "B": [
        dict(step1, footer="Next: Click Account Settings →"),
        dict(step2, footer="Next: Click the Conectiv logo →"),
        dict(title="Click the Conectiv logo", hint="It's at the top left of the page.",
             shot=f"{SRC}/3.png", crop=(0, 0, 1040, 320), target=(6, 10, 165, 40),
             footer="Next: Click Copy ConeqtX Link →"),
        dict(title="Click Copy ConeqtX Link", hint="Scroll down to Referral Links.",
             shot=f"{SRC}/4.png", crop=(0, 60, 1040, 330), target=(211, 199, 857, 228),
             footer="You're done - your link is ready to share"),
    ],
}

for path, steps in paths.items():
    d = os.path.join(OUT, f"Path {path}")
    os.makedirs(d, exist_ok=True)
    for i, s in enumerate(steps, 1):
        out = os.path.join(d, f"coneqtx_web_{path}_step{i}.png")
        render(out, P, i, len(steps), **s)
        print(out)
