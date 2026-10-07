#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unify the poster background: recolor the flat/grey cover-boxes to a warm cream
that matches the card paper, with feathered edges, while preserving all text
(dark strokes) and coloured elements (green banner, yellow name, candles)."""
from PIL import Image
import numpy as np

U = np.asarray(Image.open("work/user-1.png").convert("RGB")).astype(np.float32)
H, Wd = U.shape[:2]
rng = np.random.default_rng(11)

def feather(h, w, F):
    yy = np.clip(np.minimum(np.arange(h), h - 1 - np.arange(h)) / F, 0, 1)
    xx = np.clip(np.minimum(np.arange(w), w - 1 - np.arange(w)) / F, 0, 1)
    return np.outer(yy, xx)

def unify(box, cream, tlo, thi, sat_lo, sat_hi, F, noise=1.3):
    x0, y0, x1, y1 = box
    sub = U[y0:y1, x0:x1]
    h, w = sub.shape[:2]
    lum = sub.mean(2)
    sat = sub.max(2) - sub.min(2)
    lightw = np.clip((lum - tlo) / (thi - tlo), 0, 1)          # light bg -> 1
    neutw = np.clip((sat_hi - sat) / (sat_hi - sat_lo), 0, 1)  # neutral -> 1
    rw = feather(h, w, F)
    m = (lightw * neutw * rw)[..., None]
    plate = np.array(cream, np.float32) + rng.normal(0, noise, (h, w, 3))
    U[y0:y1, x0:x1] = sub * (1 - m) + np.clip(plate, 0, 255) * m

CREAM = (240, 235, 231)

# Main right-side content field (poem, اوست باقی, body). Green banner + yellow
# name are protected by the low-lightness / high-saturation gates.
unify((1150, 165, 2190, 1360), CREAM, tlo=182, thi=223, sat_lo=14, sat_hi=26, F=46)

# Bottom family banner: grey box + faded ornamental border -> warm cream.
unify((1178, 1460, 2188, 1620), CREAM, tlo=150, thi=208, sat_lo=14, sat_hi=26, F=26)

Image.fromarray(np.clip(U, 0, 255).astype(np.uint8)).save("work/user_fixed.png")
print("saved work/user_fixed.png")
