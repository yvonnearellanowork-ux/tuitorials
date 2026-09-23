"""Build a review board: every FINAL image of one platform/device on one page."""
from PIL import Image, ImageDraw

from make_tutorial import GREEN, WHITE, BLACK, font

W = 1920
MARGIN, GAP = 60, 30


def review_board(out, heading, rows):
    """rows: [(row label, [(step label, final image path), ...]), ...]"""
    cols = max(len(steps) for _, steps in rows)
    tw = (W - 2 * MARGIN - (cols - 1) * GAP) // cols
    th = tw * 1080 // 1920
    row_h = 60 + th + 50
    H = 170 + len(rows) * row_h + 20
    board = Image.new("RGB", (W, H), GREEN)
    d = ImageDraw.Draw(board)
    d.text((W // 2, 45), "MY TRADING STACK™ — REVIEW BOARD", font=font(26, 700, 1), fill=WHITE, anchor="mm")
    d.text((W // 2, 105), heading, font=font(52, 700, 1), fill=WHITE, anchor="mm")
    y = 170
    for label, steps in rows:
        d.text((MARGIN, y + 25), label, font=font(30, 700, 1), fill=WHITE, anchor="lm")
        for i, (step_label, path) in enumerate(steps):
            x = MARGIN + i * (tw + GAP)
            board.paste(Image.open(path).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y + 60))
            d.rounded_rectangle([x, y + 60 + th + 10, x + tw, y + 60 + th + 45], radius=4, fill=WHITE)
            d.text((x + tw // 2, y + 60 + th + 28), f"STEP {i + 1}  ·  {step_label}",
                   font=font(20, 700, 1), fill=BLACK, anchor="mm")
        y += row_h
    board.save(out, optimize=True)
