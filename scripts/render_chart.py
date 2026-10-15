#!/usr/bin/env python3
"""Rendert ein Balken- oder Liniendiagramm im Instagram-Format (1080x1350).

Aufruf:
    .venv/bin/python scripts/render_chart.py spec.json media/<slug>/02.png

Spezifikation (JSON):
{
  "kind": "bar",                       # bar | line
  "title": "Nestlé Umsatz 9M",
  "subtitle": "in CHF Mrd., organisches Wachstum in %",
  "labels": ["2024", "2025", "2026"],
  "series": [
    {"name": "Umsatz", "values": [67.1, 66.9, 65.9]}
  ],
  "unit": "CHF Mrd.",                  # Anzeige an den Werten, optional
  "decimals": 1,                       # Nachkommastellen bei Wertelabels
  "source": "Nestlé Medienmitteilung 16.10.2026",
  "note": "9 Monate, jeweils per 30.9.",   # optional
  "square": false                      # true = 1080x1080 statt 1080x1350
}

Mehrere Serien ergeben gruppierte Balken bzw. mehrere Linien.
"""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

# Farbwelt: dunkles Blau als Hauptfarbe, Rot als Akzent (Schweizer Anklang ohne Flagge).
BG = "#FFFFFF"
INK = "#1A1A1A"
MUTED = "#6B6B6B"
GRID = "#E6E6E6"
PALETTE = ["#1F3A5F", "#D7263D", "#4F7CAC", "#A3A3A3", "#F4A261"]
HANDLE = "@schweizer_aktien"


def fmt_ch(value, decimals):
    """Schweizer Zahlenformat: Apostroph als Tausendertrennung, Punkt als Dezimal."""
    s = f"{value:,.{decimals}f}"
    return s.replace(",", "'")


def render(spec, out):
    square = spec.get("square", False)
    w_in, h_in = (10.8, 10.8) if square else (10.8, 13.5)
    fig = plt.figure(figsize=(w_in, h_in), dpi=100, facecolor=BG)

    # Layout: Titelblock oben, Chart in der Mitte, Fussnote unten.
    ax = fig.add_axes([0.10, 0.22, 0.84, 0.52])
    ax.set_facecolor(BG)

    kind = spec.get("kind", "bar")
    labels = spec["labels"]
    series = spec["series"]
    decimals = spec.get("decimals", 1)
    unit = spec.get("unit", "")

    if kind == "bar":
        n = len(series)
        width = 0.8 / n
        for i, s in enumerate(series):
            xs = [x + (i - (n - 1) / 2) * width for x in range(len(labels))]
            bars = ax.bar(xs, s["values"], width=width * 0.92,
                          color=PALETTE[i % len(PALETTE)], label=s.get("name"), zorder=3)
            for b, v in zip(bars, s["values"]):
                ax.annotate(fmt_ch(v, decimals), (b.get_x() + b.get_width() / 2, b.get_height()),
                            xytext=(0, 6), textcoords="offset points", ha="center",
                            fontsize=16, color=INK, fontweight="bold")
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels)
        ax.margins(y=0.18)
    elif kind == "line":
        for i, s in enumerate(series):
            ax.plot(labels, s["values"], color=PALETTE[i % len(PALETTE)], linewidth=4,
                    marker="o", markersize=9, label=s.get("name"), zorder=3)
            last = s["values"][-1]
            ax.annotate(fmt_ch(last, decimals), (len(labels) - 1, last), xytext=(10, 0),
                        textcoords="offset points", va="center", fontsize=16,
                        color=PALETTE[i % len(PALETTE)], fontweight="bold")
        ax.margins(x=0.08, y=0.15)
    else:
        raise SystemExit(f"unbekannter kind: {kind}")

    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: fmt_ch(v, 0 if v == int(v) else decimals)))
    ax.grid(axis="y", color=GRID, zorder=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="both", colors=MUTED, labelsize=16, length=0)
    if unit:
        ax.set_ylabel(unit, color=MUTED, fontsize=15)
    if len(series) > 1:
        ax.legend(frameon=False, fontsize=15, loc="upper left", bbox_to_anchor=(0, 1.12), ncol=len(series))

    # Titelblock
    fig.text(0.10, 0.90, spec["title"], fontsize=36, fontweight="bold", color=INK, va="top", wrap=True)
    if spec.get("subtitle"):
        fig.text(0.10, 0.83, spec["subtitle"], fontsize=20, color=MUTED, va="top", wrap=True)

    # Fussnote: Hinweis, Quelle, Handle
    y = 0.12
    if spec.get("note"):
        fig.text(0.10, y, spec["note"], fontsize=15, color=MUTED, va="top", wrap=True)
        y -= 0.035
    fig.text(0.10, y, f"Quelle: {spec['source']}", fontsize=15, color=MUTED, va="top", wrap=True)
    fig.text(0.10, 0.04, "Keine Anlageberatung. Eigene Recherche.", fontsize=14, color=MUTED, va="top")
    fig.text(0.94, 0.04, HANDLE, fontsize=14, color=INK, va="top", ha="right", fontweight="bold")

    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=100, facecolor=BG)
    plt.close(fig)

    from PIL import Image
    with Image.open(out) as im:
        print(f"{out}: {im.size[0]}x{im.size[1]} px, {out.stat().st_size / 1e6:.2f} MB")


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    spec = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
    render(spec, Path(argv[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
