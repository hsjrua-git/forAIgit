#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Export individual text elements as transparent PNGs (Nastaliq)."""
from PIL import Image, ImageDraw, ImageFont
import os

NAST = "/usr/share/fonts/truetype/noto/NotoNastaliqUrdu-Regular.ttf"
INK  = (40, 38, 37)
OUTD = "work/exports"
os.makedirs(OUTD, exist_ok=True)

def render_nast(text, size, fill=INK):
    """Render one RTL line in Nastaliq on a transparent, tightly-cropped canvas."""
    f = ImageFont.truetype(NAST, size)
    Wc, Hc = 60, int(size * 4.2)
    scratch = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    Wc += int(scratch.textlength(text, font=f, direction="rtl")) + size * 2
    canvas = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    d.text((Wc - size, int(size * 3.0)), text, font=f, fill=fill,
           direction="rtl", anchor="rs")
    bb = canvas.getbbox()
    return canvas.crop(bb) if bb else canvas

def save(tile, name):
    p = os.path.join(OUTD, name)
    tile.save(p)
    print(p, tile.size)

def stack(tiles, gap):
    w = max(t.width for t in tiles)
    h = sum(t.height for t in tiles) + gap * (len(tiles) - 1)
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    y = 0
    for t in tiles:
        canvas.alpha_composite(t, ((w - t.width) // 2, y))
        y += t.height + gap
    bb = canvas.getbbox()
    return canvas.crop(bb) if bb else canvas

# 1) Poem (top) — rubaʿi, two lines
poem = [
    "جوان نازنین در خاک رفتی    از این دنیای غم غمناک رفتی",
    "زدی آتش به جان دوست داران    چو گل پاک آمدی و پاک رفتی",
]
save(stack([render_nast(l, 58) for l in poem], gap=22), "sher.png")

# 2) Families line
fam = "خانواده‌های مرادیان، دهقانی و سایر فامیل‌های وابسته"
save(render_nast(fam, 62), "khanevadeha.png")

# 3) Name
save(render_nast("مهدی مرادیان", 130), "mahdi-moradian.png")

# 4) Son of
save(render_nast("فرزند غلامعلی", 78), "farzand-gholamali.png")
