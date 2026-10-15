#!/usr/bin/env python3
"""Rendert eine Kennzahlen-Karte im Instagram-Format (1080x1350) mit Pillow.

Aufruf:
    .venv/bin/python scripts/render_card.py spec.json media/<slug>/01.png

Spezifikation (JSON):
{
  "kicker": "Übernahme",                      # kleine Zeile über dem Titel, optional
  "title": "Galderma kauft ZO Skin Health",
  "subtitle": "Medienmitteilung vom 14.10.2026",
  "items": [
    {"value": "USD 1.5 Mrd.", "label": "Kaufpreis (Unternehmenswert), in bar"},
    {"value": "USD 330 Mio.", "label": "Umsatz ZO, 12 Monate bis Juni 2026"}
  ],
  "note": "optionaler Hinweis",
  "source": "Galderma Medienmitteilung 14.10.2026",
  "square": false
}
Maximal 5 Einträge in items.
"""
import json
import sys
from pathlib import Path

import matplotlib
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
REG = FONT_DIR / "DejaVuSans.ttf"

BG = (255, 255, 255)
INK = (26, 26, 26)
MUTED = (107, 107, 107)
GRID = (230, 230, 230)
ACCENT = (31, 58, 95)
RED = (215, 38, 61)
HANDLE = "@schweizer_aktien"
W = 1080
MARGIN = 96


def font(path, size):
    return ImageFont.truetype(str(path), size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_block(draw, x, y, text, fnt, color, max_w, leading=1.2):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += int(fnt.size * leading)
    return y


def render(spec, out):
    H = 1080 if spec.get("square") else 1350
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    max_w = W - 2 * MARGIN

    # Akzentbalken oben
    d.rectangle([0, 0, W, 14], fill=RED)

    y = 110
    if spec.get("kicker"):
        d.text((MARGIN, y), spec["kicker"].upper(), font=font(BOLD, 26), fill=RED)
        y += 48
    y = draw_block(d, MARGIN, y, spec["title"], font(BOLD, 58), INK, max_w, 1.15)
    y += 10
    if spec.get("subtitle"):
        y = draw_block(d, MARGIN, y, spec["subtitle"], font(REG, 30), MUTED, max_w)
    y += 40

    items = spec.get("items", [])[:5]
    footer_top = H - 230
    avail = footer_top - y
    row_h = min(190, avail // max(len(items), 1)) if items else 0
    val_font = font(BOLD, 62 if row_h >= 170 else 52)
    lab_font = font(REG, 28)
    for it in items:
        d.line([MARGIN, y, W - MARGIN, y], fill=GRID, width=2)
        yy = y + 26
        d.text((MARGIN, yy), it["value"], font=val_font, fill=ACCENT)
        yy += val_font.size + 12
        draw_block(d, MARGIN, yy, it["label"], lab_font, MUTED, max_w)
        y += row_h
    if items:
        d.line([MARGIN, y, W - MARGIN, y], fill=GRID, width=2)

    # Fusszeile
    fy = H - 200
    small = font(REG, 24)
    if spec.get("note"):
        fy = draw_block(d, MARGIN, fy, spec["note"], small, MUTED, max_w) + 6
    fy = draw_block(d, MARGIN, fy, "Quelle: " + spec["source"], small, MUTED, max_w)
    d.text((MARGIN, H - 70), "Keine Anlageberatung. Eigene Recherche.", font=font(REG, 22), fill=MUTED)
    hf = font(BOLD, 22)
    d.text((W - MARGIN - d.textlength(HANDLE, font=hf), H - 70), HANDLE, font=hf, fill=INK)

    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, optimize=True)
    print(f"{out}: {W}x{H} px, {out.stat().st_size / 1e6:.2f} MB")


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    render(json.loads(Path(argv[0]).read_text(encoding="utf-8")), Path(argv[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
