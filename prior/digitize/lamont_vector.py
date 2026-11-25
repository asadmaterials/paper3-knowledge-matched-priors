"""Extract Lamont's charts (r/R = 0 and r/R = 0.5) from the vector paths in Totten (ed.), Steel Heat Treatment:
Metallurgy and Technologies, 2nd ed. (CRC, 2006), section 5.5.1, Figs. 5.49 and 5.50 (after Lamont, Iron Age 152 (1943) 64-70).
Pass C (Claude). The charts on page 2 of the 4-page excerpt are vector drawings: each H curve is one or more cubic Bezier
segments, evaluated here exactly, so the only reading error is the axis calibration.

Calibration (PDF points to inches), from the inch gridlines and their labels:
  Fig. 5.49 (r/R = 0):   J = (x - 223.52) / 94.0,   D = (287.37 - y) / 23.0   (1/4 in. J gridlines 23.5 pt apart; 0.5 in. D gridlines 11.5 pt)
  Fig. 5.50 (r/R = 0.5): J = (x - 238.41) / 80.40,  D = (640.31 - y) / 19.583
The mm scales printed beside the inch scales are not used: on Fig. 5.49 they disagree with the inch scales by up to about 3%
(the 160 mm tick sits at 6.5 in., i.e. 165 mm).

Usage: python -I prior/digitize/lamont_vector.py <excerpt.pdf> OUT
Writes OUT/lamont_rR0_rR05.csv: for each chart and H, D (in. and mm) and the equivalent Jominy distance J (in. and mm),
on a D grid every 0.025 in. within each curve's drawn range.
"""
import os, sys, csv
import numpy as np
import pdfplumber

PDF, OUT = sys.argv[1], sys.argv[2]
CAL = {0.0: dict(x0=223.52, sx=94.0, y0=287.37, sy=23.0, box=(220.4, 410.43, 127.11, 288.39)),
       0.5: dict(x0=238.41, sx=80.40, y0=640.31, sy=19.583, box=(239.61, 399.28, 445.07, 641.07))}
H_ORDER = [0.2, 0.35, 0.5, 0.7, 1.0, 1.5, 2.0, 5.0, float('inf')]  # curves sorted by D at the right-hand end

def sample(path, n=400):
    pts = []; cur = None
    for op in path:
        k = op[0]
        if k == 'm': cur = np.array(op[1], float); pts.append(cur)
        elif k == 'l':
            p = np.array(op[1], float); pts += [cur + (p - cur) * t for t in np.linspace(0, 1, 50)[1:]]; cur = p
        elif k in 'cvy':
            if k == 'c': p1, p2, p3 = (np.array(q, float) for q in op[1:4])
            elif k == 'v': p1 = cur; p2, p3 = (np.array(q, float) for q in op[1:3])
            else: p1, p3 = (np.array(q, float) for q in op[1:3]); p2 = p3
            for t in np.linspace(0, 1, n)[1:]:
                pts.append((1 - t) ** 3 * cur + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3)
            cur = p3
    return np.array(pts)

def curves():
    out = {}
    with pdfplumber.open(PDF) as pdf:
        page = pdf.pages[1]
        for rR, cal in CAL.items():
            X0, X1, T, B = cal['box']; sel = []
            for c in page.curves:
                if c['x0'] >= X0 + 1 and c['x1'] <= X1 + 1 and c['top'] >= T - 1 and c['bottom'] <= B + 1 and (c['linewidth'] or 0) > 0.7:
                    s = sample(c['path'])
                    sel.append(dict(J=(s[:, 0] - cal['x0']) / cal['sx'], D=(cal['y0'] - s[:, 1]) / cal['sy'], dash=bool(c['dash'] and c['dash'][0])))
            solid = [c for c in sel if not c['dash']]
            for d in [c for c in sel if c['dash']]:  # a dashed piece continues the solid curve that ends where it starts
                k = min(solid, key=lambda c: np.hypot(c['J'].max() - d['J'].min(), c['D'][c['J'].argmax()] - d['D'][d['J'].argmin()]))
                k['J'] = np.r_[k['J'], d['J']]; k['D'] = np.r_[k['D'], d['D']]; k['dashed_from'] = float(d['J'].min())
            solid.sort(key=lambda c: c['D'][c['J'].argmax()])
            assert len(solid) == len(H_ORDER), (rR, len(solid))
            for H, c in zip(H_ORDER, solid):
                o = np.argsort(c['D']); out[(rR, H)] = (c['J'][o], c['D'][o], c.get('dashed_from'))
    return out

def main():
    os.makedirs(OUT, exist_ok=True)
    cs = curves()
    with open(f'{OUT}/lamont_rR0_rR05.csv', 'w', newline='') as fh:
        fh.write('# Equivalent Jominy distance J against round-bar diameter D for quench severity H: Lamont, Iron Age 152 (1943) 64-70,\n'
                 '# as redrawn in Totten (ed.), Steel Heat Treatment: Metallurgy and Technologies, 2nd ed. (CRC, 2006), Figs. 5.49 (r/R = 0) and 5.50 (r/R = 0.5).\n'
                 '# Exact evaluation of the figures\' vector paths (pass C, Claude, 25 Nov 2026); inch axes. Not the author\'s data.\n'
                 '# dashed = 1 where the curve is drawn dashed in the figure (only H = 5.0 at r/R = 0.5, at large J).\n')
        w = csv.writer(fh); w.writerow(['r_over_R', 'H', 'D_in', 'D_mm', 'J_in', 'J_mm', 'dashed'])
        for (rR, H), (J, D, dfrom) in sorted(cs.items()):
            for d in np.arange(np.ceil(D.min() / 0.025) * 0.025, D.max() + 1e-9, 0.025):
                j = float(np.interp(d, D, J))
                w.writerow([rR, 'inf' if np.isinf(H) else H, round(d, 3), round(d * 25.4, 2), round(j, 4), round(j * 25.4, 2),
                            int(dfrom is not None and j >= dfrom)])

if __name__ == '__main__':
    main()
