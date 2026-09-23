"""Render "My Trading Stack" tutorial step images (desktop, 1920x1080).

Everything is drawn at 2x and downscaled for smooth edges.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import os

FONT = os.path.join(os.path.dirname(__file__), "fonts", "OpenSans-Variable.ttf")
ARROW_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Open Sans has no →
GREEN = (12, 107, 0)
RED = (229, 57, 53)
WHITE = (255, 255, 255)
BLACK = (17, 17, 17)
S = 2  # supersample factor
W, H = 1920, 1080
BOX_W, BOX_TOP, BOX_BOTTOM = 1400, 372, 955  # area for the browser window
TITLEBAR = 33


def font(size, weight):
    f = ImageFont.truetype(FONT, size * S)
    f.set_variation_by_axes([weight, 100])
    return f


def center_text(d, y, text, f, fill):
    l, t, r, b = d.textbbox((0, 0), text, font=f, anchor="ls")
    d.text(((W * S - (r - l)) // 2 - l, y * S), text, font=f, fill=fill, anchor="lm")


def pill(d, cy, text, f, pad_x, h, radius):
    arrow = text.endswith(" →")
    if arrow:
        text = text[:-2]
        af = ImageFont.truetype(ARROW_FONT, int(f.size * 0.85))
        aw = d.textlength(" →", font=af)
    else:
        aw = 0
    tw = d.textlength(text, font=f)
    w = (tw + aw) / S + 2 * pad_x
    x0 = (W - w) / 2
    d.rounded_rectangle([x0 * S, (cy - h / 2) * S, (x0 + w) * S, (cy + h / 2) * S],
                        radius=radius * S, fill=WHITE)
    tx = (x0 + pad_x) * S
    d.text((tx, cy * S), text, font=f, fill=BLACK, anchor="lm")
    if arrow:
        d.text((tx + tw, cy * S), " →", font=af, fill=BLACK, anchor="lm")


def render(out, platform, step, total, title, hint, footer, shot, crop, target,
           badge_side="right", blur=()):
    src = Image.open(shot).convert("RGB")
    for box in blur:  # hide personal info
        region = src.crop(box).filter(ImageFilter.GaussianBlur(8))
        src.paste(region, box[:2])
    src = src.crop(crop)

    canvas = Image.new("RGB", (W * S, H * S), GREEN)
    d = ImageDraw.Draw(canvas)
    center_text(d, 50, "MY TRADING STACK™", font(34, 700), WHITE)
    center_text(d, 111, platform, font(62, 700), WHITE)
    pill(d, 183, f"STEP {step} OF {total}", font(26, 700), 39, 50, 25)
    center_text(d, 257, title, font(66, 700), WHITE)
    center_text(d, 327, hint, font(26, 400), WHITE)

    # fit screenshot + title bar into the box
    max_h = BOX_BOTTOM - BOX_TOP - TITLEBAR
    scale = min(BOX_W / src.width, max_h / src.height)
    sw, sh = round(src.width * scale), round(src.height * scale)
    fx = (W - sw) // 2
    fy = BOX_TOP + (max_h - sh) // 2
    fh = sh + TITLEBAR

    shadow = Image.new("L", canvas.size, 0)
    ImageDraw.Draw(shadow).rounded_rectangle(
        [fx * S, (fy + 8) * S, (fx + sw) * S, (fy + fh + 8) * S], radius=8 * S, fill=110)
    shadow = shadow.filter(ImageFilter.GaussianBlur(14 * S))
    canvas.paste(Image.new("RGB", canvas.size, (0, 40, 0)), (0, 0), shadow)
    d = ImageDraw.Draw(canvas)

    d.rounded_rectangle([fx * S, fy * S, (fx + sw) * S, (fy + fh) * S],
                        radius=6 * S, fill=(236, 238, 239))
    for i in range(3):
        cx, cy = fx + 25 + 22 * i, fy + TITLEBAR / 2
        d.ellipse([(cx - 5) * S, (cy - 5) * S, (cx + 5) * S, (cy + 5) * S], fill=(196, 200, 202))
    d.rounded_rectangle([(fx + 120) * S, (fy + 8) * S, (fx + sw - 120) * S, (fy + 26) * S],
                        radius=4 * S, fill=WHITE)
    canvas.paste(src.resize((sw * S, sh * S), Image.LANCZOS), (fx * S, (fy + TITLEBAR) * S))

    # callout box around the target (target in original screenshot coords)
    tx0, ty0, tx1, ty1 = target
    X = lambda x: fx + (x - crop[0]) * scale
    Y = lambda y: fy + TITLEBAR + (y - crop[1]) * scale
    bx0, by0, bx1, by1 = X(tx0) - 6, Y(ty0) - 6, X(tx1) + 6, Y(ty1) + 6
    d.rounded_rectangle([bx0 * S, by0 * S, bx1 * S, by1 * S], radius=8 * S,
                        outline=RED, width=5 * S)

    # numbered badge
    r = 23
    cy = (by0 + by1) / 2
    if badge_side == "right":
        cx = bx1 + r + 4
    elif badge_side == "left":
        cx = bx0 - r - 4
    else:  # below
        cx, cy = (bx0 + bx1) / 2, by1 + r + 4
    bshadow = Image.new("L", canvas.size, 0)
    ImageDraw.Draw(bshadow).ellipse([(cx - r) * S, (cy - r + 3) * S, (cx + r) * S, (cy + r + 3) * S], fill=120)
    bshadow = bshadow.filter(ImageFilter.GaussianBlur(4 * S))
    canvas.paste(Image.new("RGB", canvas.size, (0, 0, 0)), (0, 0), bshadow)
    d = ImageDraw.Draw(canvas)
    d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=WHITE,
              outline=RED, width=4 * S)
    d.text((cx * S, (cy + 1) * S), str(step), font=font(30, 600), fill=RED, anchor="mm")

    pill(d, 1014, footer, font(32, 700), 42, 58, 4)

    canvas.resize((W, H), Image.LANCZOS).save(out, optimize=True)
