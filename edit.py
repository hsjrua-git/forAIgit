#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Memorial poster editor: composite RTL renderer (Noto shaping + punctuation fallback)."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import re

SRC = "/tmp/claude-1000/-data-projects-for-AI/7cae4492-ff5b-4dce-9026-ff59ccc562d9/images/1.jpg"
OUT = "work/out.png"

TITR   = "/usr/share/fonts/truetype/farsiweb/titr.ttf"
NASKH  = "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf"
NASKHB = "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf"
NAST   = "/usr/share/fonts/truetype/noto/NotoNastaliqUrdu-Regular.ttf"
DV     = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DVB    = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

im = Image.open(SRC).convert("RGBA")
W, H = im.size
rng = np.random.default_rng(7)

NUMPIECE = re.compile(r"[0-9۰-۹.,:]+|/")

def tokenize(s):
    toks, i, n = [], 0, len(s)
    isnum = lambda c: c.isdigit() or "۰" <= c <= "۹"
    while i < n:
        c = s[i]
        if c in "()":
            toks.append(("paren", c)); i += 1; continue
        if isnum(c):
            j = i
            while j < n and (isnum(s[j]) or s[j] in "/.,:"):
                j += 1
            toks.append(("num", s[i:j])); i = j; continue
        j = i
        while j < n and s[j] not in "()" and not isnum(s[j]):
            j += 1
        toks.append(("ar", s[i:j])); i = j
    return toks

_scratch = ImageDraw.Draw(Image.new("RGBA", (4, 4)))

def _adv(tt, tx, pf, ff):
    if tt == "ar":
        return _scratch.textlength(tx, font=pf, direction="rtl")
    if tt == "paren":
        return _scratch.textlength(")" if tx == "(" else "(", font=ff)
    a = 0
    for p in NUMPIECE.findall(tx):
        a += _scratch.textlength(p, font=(ff if p == "/" else pf))
    return a

def line_width(text, primary, size, fallback=DV):
    pf = ImageFont.truetype(primary, size); ff = ImageFont.truetype(fallback, size)
    return sum(_adv(tt, tx, pf, ff) for tt, tx in tokenize(text))

def render_line(text, primary, size, fill, fallback=DV, sw=0, sf=None):
    pf = ImageFont.truetype(primary, size); ff = ImageFont.truetype(fallback, size)
    toks = tokenize(text)
    advs = [_adv(tt, tx, pf, ff) for tt, tx in toks]
    total = sum(advs)
    Wc, Hc = int(total) + 2 * size + 24, int(size * 2.8)
    canvas = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    baseline = int(size * 1.85)
    penx = size + 12 + total
    for (tt, tx), a in zip(toks, advs):
        penx -= a
        if tt == "ar":
            d.text((penx, baseline), tx, font=pf, fill=fill, direction="rtl",
                   anchor="ls", stroke_width=sw, stroke_fill=sf)
        elif tt == "paren":
            g = ")" if tx == "(" else "("
            d.text((penx, baseline), g, font=ff, fill=fill, anchor="ls",
                   stroke_width=sw, stroke_fill=sf)
        else:
            sx = penx
            for p in NUMPIECE.findall(tx):
                f = ff if p == "/" else pf
                d.text((sx, baseline), p, font=f, fill=fill, anchor="ls",
                       stroke_width=sw, stroke_fill=sf)
                sx += _scratch.textlength(p, font=f)
    bb = canvas.getbbox()
    return canvas.crop(bb) if bb else canvas

def fit_size(text, primary, start, maxw, fallback=DV, minsz=8):
    s = start
    while s > minsz and line_width(text, primary, s, fallback) > maxw:
        s -= 1
    return s

def wrap(text, primary, size, maxw, fallback=DV):
    words, lines, cur = text.split(" "), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if line_width(t, primary, size, fallback) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = wd
    if cur:
        lines.append(cur)
    return lines

def paste_center(tile, cx, cy):
    im.alpha_composite(tile, (int(cx - tile.width / 2), int(cy - tile.height / 2)))

def fill_region(box, color, feather=10, noise=2):
    l, t, r, b = box; w, h = r - l, b - t
    patch = np.clip(np.array(color, np.float32) + rng.normal(0, noise, (h, w, 3)), 0, 255).astype(np.uint8)
    ov = Image.fromarray(patch, "RGB").convert("RGBA")
    a = Image.new("L", (w, h), 255)
    ad = ImageDraw.Draw(a)
    for i in range(feather):
        ad.rectangle([i, i, w - 1 - i, h - 1 - i], outline=int(255 * (i + 1) / (feather + 1)))
    ov.putalpha(a)
    im.alpha_composite(ov, (l, t))

CREAM = (239, 234, 233); GREEN = (32, 61, 30); YELLOW = (247, 224, 22)
INK = (52, 50, 48); NAVY = (44, 47, 82); BOLDINK = (32, 31, 30)

# ---- Region 7: bold phrase "اوست باقی" (make sharp) ----
fill_region((760, 205, 950, 248), CREAM)
paste_center(render_line("اوست باقی", NASKHB, 30, BOLDINK, DVB), 854, 226)

# ---- Region 6: delete faint small line below "اوست باقی" ----
fill_region((690, 244, 1015, 282), CREAM)

# ---- Region 1: name "مهدی مرادیان" (yellow on green, sharp) ----
fill_region((618, 299, 1152, 381), GREEN, feather=14)
nsz = fit_size("مهدی مرادیان", TITR, 92, 505)
paste_center(render_line("مهدی مرادیان", TITR, nsz, YELLOW, DV, sw=2, sf=(38, 48, 20)), 885, 341)

# ---- Region 5: "(فرزند غلامعلی)" (make sharp) ----
fill_region((715, 396, 1040, 435), CREAM)
paste_center(render_line("(فرزند غلامعلی)", NASKHB, 24, BOLDINK, DVB), 876, 415)

# ---- Region 4: top calligraphy -> rubaʿi (4 hemistichs, 2 lines) ----
fill_region((610, 84, 1176, 200), CREAM, feather=14)
poem = [
    "جوان نازنین در خاک رفتی    از این دنیای غم غمناک رفتی",
    "زدی آتش به جان دوست داران    چو گل پاک آمدی و پاک رفتی",
]
psz = min(fit_size(l, NAST, 42, 566) for l in poem)
plh = int(psz * 1.42)
py = 142 - plh // 2
for l in poem:
    paste_center(render_line(l, NAST, psz, INK), 893, py)
    py += plh

# ---- Region 3: bottom banner families ----
fill_region((660, 752, 1158, 806), CREAM)
fam = "خانواده‌های مرادیان، دهقانی و سایر فامیل‌های وابسته"
fsz = fit_size(fam, NASKHB, 34, 486)
paste_center(render_line(fam, NASKHB, fsz, NAVY, DVB), 908, 779)

# ---- Region 2: body condolence text ----
fill_region((600, 430, 1190, 720), CREAM, feather=12)
fill_region((544, 480, 616, 510), CREAM, feather=6)  # erase faint ۱۴۰۶ remnant in left margin
MAXW = 540
head = "به اطلاع کلیه سروران گرامی می‌رسانیم"
p1 = ("مراسم یادبودی روز پنجشنبه ۱۴۰۵/۰۶/۰۹ از ساعت ۴ تا ۵ عصر در امامزاده "
      "حسین (ع) روستای خافتر بر سر تربت خاک آن عزیز برگزار می‌گردد.")
p2 = ("حضور شما سروران گرامی موجب شادی روح آن عزیز از دست رفته و تسلی خاطر "
      "بازماندگان خواهد شد.")
blocks = [(head, NASKHB, DVB, 29, BOLDINK), (p1, NASKH, DV, 24, INK),
          (p2, NASKH, DV, 24, INK)]
tiles, gaps = [], []
for txt, pf, ffb, sz, col in blocks:
    lh = int(sz * 1.55)
    for ln in wrap(txt, pf, sz, MAXW, ffb):
        tiles.append((render_line(ln, pf, sz, col, ffb), lh))
    gaps.append(True)
totalh = sum(lh for _, lh in tiles) + 2 * 16  # two paragraph gaps
cy = 432 + (715 - 432 - totalh) // 2
i = 0
for txt, pf, ffb, sz, col in blocks:
    lh = int(sz * 1.55)
    for ln in wrap(txt, pf, sz, MAXW, ffb):
        tile, _ = tiles[i]; i += 1
        paste_center(tile, 872, cy + lh // 2); cy += lh
    cy += 16

im.convert("RGB").save(OUT, quality=95)
print("saved", OUT, "size", im.size)

