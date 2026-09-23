# My Trading Stack™ tutorial images

Referral-link help-center tutorials, built from real screenshots.
Source of truth for the process: "Yvonne — My Trading Stack Canva Tutorial Assignment".

## Privacy — ALWAYS
- ALWAYS cover the **username** and the **referral link / code** in every image.
- Also cover: names/profile photos, email/phone, account & routing numbers, IDs,
  balances/buying power/portfolio values/P&L, holdings/positions/transactions,
  personal QR codes, private notifications/messages.
- Use SOLID, fully opaque boxes (`tools/redact.py`). Never a transparent box,
  scribble, or weak blur. Zoom in to confirm nothing is readable.
- Do not cover the button/menu text being taught.
- RAW screenshots never go into git (`*_RAW.png` is ignored).

## Template (don't change between platforms)
MY TRADING STACK™ / PLATFORM NAME / STEP X OF Y pill / one-action title
(e.g. Tap “Rewards”) / short hint / screenshot in device frame /
ONE numbered marker on the target / white footer "Next: … →" or
"You're done - your link is ready to share". Dark green (#0C6B00) + white.

## One action per image, three versions per step
`<platform>_<ios|android|web>[_<path>]_<NN>_<slug>_{RAW,CLEAN,FINAL}.png`
under `Tutorials/<Platform> <Device>/[Path X/]`, plus a
`<platform>_<device>_REVIEW_BOARD.png` for Michelle and a `HANDOFF.md` for Mahfuzar.

## Tooling
`tools/make_tutorial.py` (FINAL renderer), `tools/redact.py` (CLEAN),
`tools/review_board.py`; per-platform scripts like `tools/coneqtx_web.py`.
