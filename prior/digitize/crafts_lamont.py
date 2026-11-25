"""Digitize the Crafts and Lamont (1947) tempering decrement D and disproportionate-softening factor f,
from their reproductions in Athavale's PhD dissertation (Missouri S&T, 2019), pass C (Claude).

Inputs (extract with pdfimages from the dissertation PDF into WORK):
  pdfimages -j -f 48 -l 48 <dissertation.pdf> WORK/d48   -> d48-000.jpg (Paper I Fig. 4, D), d48-001.jpg (Paper I Fig. 5, f)
  pdfimages -j -f 56 -l 56 <dissertation.pdf> WORK/d56   -> d56-000.jpg (Paper I Fig. 9, original and corrected D)
  pdfimages -j -f 66 -l 66 <dissertation.pdf> WORK/d66   -> d66-000.jpg (Paper II Fig. 3, f with every line labelled)
Outputs in OUT: crafts_lamont_D.csv, crafts_lamont_f.csv.
Usage: python -I prior/digitize/crafts_lamont.py WORK OUT
"""
import os, sys, csv
import numpy as np
from PIL import Image

WORK, OUT = sys.argv[1], sys.argv[2]
# Axis calibration: (x pixels, x values, y pixels, y values) from the frame and tick marks.
CAL = {
 'd48-000': ([73, 109.0, 145.5, 183.0, 218.5, 257.0, 292.0, 330.0, 366.5, 405.0, 442.0, 478.5, 515.0, 551.0, 589], list(range(0, 1401, 100)),
             [540, 498.0, 460.5, 423.0, 387.0, 346.5, 309.5, 272.0, 233.0, 196.5, 158.0, 121.0, 85.5, 48.0, 10], list(range(0, 15))),
 'd56-000': ([68, 102.5, 137.0, 172.0, 205.5, 241.0, 274.5, 310.0, 344.5, 381.0, 415.5, 450.0, 484.0, 518.0, 554], list(range(0, 1401, 100)),
             [507, 468.0, 433.0, 397.5, 364.0, 325.5, 291.0, 256.0, 219.0, 184.5, 149.0, 113.5, 80.0, 45.0, 9], list(range(0, 15))),
 'd48-001': ([110, 178.5, 245.5, 312.5, 378.5, 444.5, 510.5, 578.0], [0, .1, .2, .3, .4, .5, .6, .7],
             [693, 624.5, 556.0, 489.0, 422.5, 356.0, 286.5, 218.5, 152.0, 83.0, 12], [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]),
 'd66-000': ([103, 167.0, 229.5, 292.0, 354.0, 415.0, 477.0, 540.5], [0, .1, .2, .3, .4, .5, .6, .7],
             [648, 584.0, 519.5, 457.5, 395.5, 332.5, 268.0, 204.5, 142.5, 77.5, 12], [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]),
}
FRAME = {'d48-000': (73, 589, 10, 540), 'd56-000': (68, 554, 9, 507), 'd48-001': (110, 613, 12, 693), 'd66-000': (103, 573, 12, 648)}

class Cal:
    def __init__(s, n):
        xp, xv, yp, yv = CAL[n]; s.ax = np.polyfit(xp, xv, 1); s.ay = np.polyfit(yp, yv, 1)
    def x(s, p): return float(np.polyval(s.ax, p))
    def y(s, p): return float(np.polyval(s.ay, p))

def load(n): return np.array(Image.open(f'{WORK}/{n}.jpg').convert('RGB')).astype(int)

def mask(a, color):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    if color == 'blue': return (b > 140) & (r < 110) & (g < 110)
    if color == 'red': return (r > 140) & (r - g > 90) & (r - b > 90)
    if color == 'black': return (r < 90) & (g < 90) & (b < 90)

def d_curve(n, color):
    """Two-segment continuous line through the coloured curve; returns three vertices (degF, HRC)."""
    c = Cal(n); a = load(n); L, R, T, B = FRAME[n]; m = mask(a, color)
    pts = []
    for x in range(L + 4, R - 3):
        ys = np.where(m[T + 3:B - 3, x])[0]
        if len(ys) == 0: continue
        for run in np.split(ys, np.where(np.diff(ys) > 2)[0] + 1):
            pts.append((x, T + 3 + run.mean()))
    p = np.array(pts); keep = np.ones(len(p), bool)
    def fit(px, py):
        best = None
        for k in np.linspace(px.min() + 10, px.max() - 10, 400):
            A = np.c_[np.ones_like(px), px, np.maximum(px - k, 0)]
            co = np.linalg.lstsq(A, py, rcond=None)[0]; rss = ((A @ co - py) ** 2).sum()
            if best is None or rss < best[0]: best = (rss, k, co)
        return best
    for _ in range(8):  # drop label text and other ink more than 3 px from the fit
        _, k, co = fit(p[keep, 0], p[keep, 1])
        new = np.abs(co[0] + co[1] * p[:, 0] + co[2] * np.maximum(p[:, 0] - k, 0) - p[:, 1]) <= 3.0
        if (new == keep).all(): break
        keep = new
    q = p[keep]; f = lambda x: co[0] + co[1] * x + co[2] * max(x - k, 0)
    v = [(q[:, 0].min(), f(q[:, 0].min())), (k, f(k)), (q[:, 0].max(), f(q[:, 0].max()))]
    return [(round(c.x(u), 1), round(c.y(w), 3)) for u, w in v]

def f_lines(n, color, nlines=5):
    """Five straight lines of one colour: slope and intercept in data units (f against wt% C)."""
    c = Cal(n); a = load(n); L, R, T, B = FRAME[n]; m = mask(a, color)
    m[:, :L + 4] = False; m[:, R - 3:] = False; m[:T + 3] = False; m[B - 3:] = False
    ys, xs = np.where(m); xs = xs.astype(float); ys = ys.astype(float)
    best = None
    for s in np.linspace(0.8, 1.6, 161):
        h, _ = np.histogram(ys - s * xs, bins=np.arange((ys - s * xs).min(), (ys - s * xs).max() + 2, 2))
        sc = np.sort(h)[-nlines:].sum()
        if best is None or sc > best[0]: best = (sc, s)
    s = best[1]; b = ys - s * xs
    h, e = np.histogram(b, bins=np.arange(b.min(), b.max() + 2, 2)); peaks = []
    for i in np.argsort(h)[::-1]:
        cen = (e[i] + e[i + 1]) / 2
        if all(abs(cen - q) > 15 for q in peaks): peaks.append(cen)
        if len(peaks) == nlines: break
    out = []
    for pk in sorted(peaks):  # top line first
        X, Y = xs[np.abs(b - pk) <= 4], ys[np.abs(b - pk) <= 4]
        for _ in range(6):
            co = np.polyfit(X, Y, 1); k = np.abs(np.polyval(co, X) - Y) <= 2.5
            if k.all(): break
            X, Y = X[k], Y[k]
        p0 = (c.x(X.min()), c.y(np.polyval(co, X.min()))); p1 = (c.x(X.max()), c.y(np.polyval(co, X.max())))
        slope = (p1[1] - p0[1]) / (p1[0] - p0[0]); out.append((slope, p0[1] - slope * p0[0]))
    return out

def main():
    os.makedirs(OUT, exist_ok=True)
    D = {'original (Paper I Fig. 4)': d_curve('d48-000', 'blue'),
         'original (Paper I Fig. 9)': d_curve('d56-000', 'blue'),
         'corrected (Paper I Fig. 9)': d_curve('d56-000', 'red')}
    with open(f'{OUT}/crafts_lamont_D.csv', 'w', newline='') as fh:
        fh.write('# Tempering decrement D (HRC) against tempering temperature (deg F): Crafts and Lamont, Trans. AIME 172 (1947) 222-243, Fig. 2,\n'
                 '# as reproduced in Athavale, PhD dissertation, Missouri S&T (2019), Paper I Figs. 4 and 9; "corrected" is the dissertation\'s own curve.\n'
                 '# Digitized readings, not the authors\' data. Pass C (Claude), 25 Nov 2026. Each curve is two straight segments through three vertices.\n'
                 '# The corrected curve meets D = 0 at its first vertex extrapolated to the axis (column D0_T_F).\n')
        w = csv.writer(fh); w.writerow(['curve', 'vertex', 'T_F', 'D_HRC', 'D0_T_F'])
        for name, v in D.items():
            d0 = ''
            if name.startswith('corrected'):
                (t0, d_0), (t1, d_1) = v[0], v[1]; d0 = round(t0 - d_0 * (t1 - t0) / (d_1 - d_0), 1)
            for i, (t, d) in enumerate(v): w.writerow([name, i + 1, t, d, d0 if i == 0 else ''])
    temps = {'black': [400, 600, 800, 1000, 1200], 'red': [500, 700, 900, 1100, 1300]}
    with open(f'{OUT}/crafts_lamont_f.csv', 'w', newline='') as fh:
        fh.write('# Factor for disproportionate softening f against carbon (wt%): Crafts and Lamont (1947) Fig. 4, as reproduced in Athavale (2019),\n'
                 '# Paper I Fig. 5 and Paper II Fig. 3 (the latter labels every line: solid 400-1200 deg F, dashed 500-1300 deg F).\n'
                 '# Digitized readings, not the authors\' data. Pass C (Claude), 25 Nov 2026. Each line: f = slope * C + intercept.\n'
                 '# Drawn range: C from 0.05% (or where f = 1.0) to 0.65% (or where f = 0).\n')
        w = csv.writer(fh); w.writerow(['source', 'T_F', 'slope_per_wt', 'intercept', 'C_start_wt', 'C_end_wt'])
        for n, src in (('d66-000', 'Paper II Fig. 3'), ('d48-001', 'Paper I Fig. 5')):
            for col in ('black', 'red'):
                for T, (s, b) in zip(temps[col], f_lines(n, col)):
                    c0 = max(0.05, (1.0 - b) / s); c1 = min(0.65, -b / s)
                    w.writerow([src, T, round(s, 4), round(b, 4), round(c0, 3), round(c1, 3)])

if __name__ == '__main__':
    main()
