"""Make a privacy-safe CLEAN copy of a RAW screenshot.

Private info is covered with SOLID, fully opaque boxes (never blur/transparent),
per the My Trading Stack production rules.
"""
from PIL import Image, ImageDraw

COVER = (58, 62, 68)
PAD = 3


def redact(raw_path, clean_path, boxes):
    im = Image.open(raw_path).convert("RGB")
    d = ImageDraw.Draw(im)
    for x0, y0, x1, y1 in boxes:
        d.rounded_rectangle([x0 - PAD, y0 - PAD, x1 + PAD, y1 + PAD], radius=3, fill=COVER)
    im.save(clean_path, optimize=True)
    return clean_path
