#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Export 'مهدی مرادیان' exactly as rendered in the poster banner (Titr, yellow +
dark stroke), on a transparent background."""
from PIL import Image, ImageDraw, ImageFont

TITR   = "/usr/share/fonts/truetype/farsiweb/titr.ttf"
YELLOW = (247, 224, 22)
STROKE = (38, 48, 20)
TXT    = "مهدی مرادیان"

scratch = ImageDraw.Draw(Image.new("RGBA", (4, 4)))

def width(size):
    return scratch.textlength(TXT, font=ImageFont.truetype(TITR, size), direction="rtl")

# same as edit.py: fit_size(TXT, TITR, start=92, maxw=505)
size = 92
while size > 8 and width(size) > 505:
    size -= 1

pf = ImageFont.truetype(TITR, size)
total = scratch.textlength(TXT, font=pf, direction="rtl")
Wc, Hc = int(total) + 2 * size + 24, int(size * 2.8)
canvas = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
d = ImageDraw.Draw(canvas)
baseline = int(size * 1.85)
d.text((size + 12, baseline), TXT, font=pf, fill=YELLOW, direction="rtl",
       anchor="ls", stroke_width=2, stroke_fill=STROKE)
bb = canvas.getbbox()
tile = canvas.crop(bb) if bb else canvas
out = "work/exports/mahdi-moradian-yellow.png"
tile.save(out)
print(out, tile.size, "size=", size)
