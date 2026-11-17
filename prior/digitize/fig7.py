"""Digitize GHP 1977 Fig. 7 (Fe-C tempered martensite hardness), pass C (Claude).

Input: WORK/p-007.png, the 400 x 516 px, 150 ppi grayscale image of Fig. 7
extracted from the paper PDF with `pdfimages -png <pdf> WORK/p`.
Output: WORK/fig7_raw.csv (tracked pixels) and WORK/fig7_clean.csv
(HV at C = 0.05 to 0.98 wt% in 0.01 steps, per tempering temperature;
gap_C is the distance in wt% C to the nearest traced point, so a large value marks
a stretch bridged by linear interpolation, e.g. under a curve label).
"""
import os, sys, csv, collections
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from runs import runs
from track2 import track
from clean import clean

WORK = os.environ.get("GHP_WORK", "work")
im = np.array(Image.open(f"{WORK}/p-007.png")).astype(int)
# Calibration from the gridlines (pixel -> value), piecewise linear between gridlines.
ROWS = [4, 69, 136, 203, 269, 336, 401.5, 469]; HVS = [800, 700, 600, 500, 400, 300, 200, 100]
COLS = [48, 113.5, 178.5, 244.5, 310.5, 376.5]; CS = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
fy = lambda y: float(np.interp(y, ROWS, HVS)); fx = lambda x: float(np.interp(x, COLS, CS))
py = lambda h: float(np.interp(-h, [-v for v in HVS], ROWS)); px = lambda c: float(np.interp(c, CS, COLS))
SKIP_ROWS = [4, 69, 136, 203, 269, 336, 401, 402, 469, 482]
SKIP_COLS = set()
for g in [47, 48, 49, 113, 114, 178, 179, 244, 245, 278, 310, 311, 376, 377, 389, 390, 391]:
    SKIP_COLS |= {g - 1, g, g + 1}
TEMPS = [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300]

def multi(seed_cols, agree=1.2):
    passes = []
    for x0 in seed_cols:
        seeds = sorted(c for c, w in runs(im[:, x0].copy(), 130, [slice(g - 1, g + 2) for g in SKIP_ROWS]) if 6 < c < 478)
        assert len(seeds) == 10, (x0, len(seeds))
        passes.append(track(im, seeds, x0, 52, 377, skip_rows=SKIP_ROWS, skip_cols=SKIP_COLS, ylim=(6, 478), tol=1.8, grow=0.05))
    out = []
    for k in range(10):
        d = {}
        for x in sorted(set().union(*[p[k].keys() for p in passes])):
            ys = [p[k][x][0] for p in passes if x in p[k]]
            if len(ys) == 1 or max(ys) - min(ys) <= agree:
                d[x] = float(np.mean(ys))
        out.append(d)
    return out

def main():
    res = multi([160, 360])
    raw, clean_rows = [], []
    grid = np.round(np.arange(0.05, 0.981, 0.01), 2)
    for T, r in zip(TEMPS, res):
        xs = np.array(sorted(r)); ys = np.array([r[x] for x in xs])
        keep = clean(xs, ys, thr=0.8, iters=40)
        c = np.array([fx(x) for x in xs[keep]]); h = np.array([fy(y) for y in ys[keep]])
        raw += [(T, round(a, 4), round(b, 1)) for a, b in zip(c, h)]
        for g in grid:
            if c.min() - 0.003 <= g <= c.max() + 0.003:
                gap = float(np.min(np.abs(c - g)))  # distance to nearest traced point
                clean_rows.append((T, g, round(float(np.interp(g, c, h)), 1), round(gap, 3)))
    with open(f"{WORK}/fig7_raw.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["T_F", "C_wt", "HV"]); w.writerows(raw)
    with open(f"{WORK}/fig7_clean.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["T_F", "C_wt", "HV", "gap_C"]); w.writerows(clean_rows)

if __name__ == "__main__":
    main()
