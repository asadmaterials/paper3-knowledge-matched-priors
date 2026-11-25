"""Combine digitizing passes A and C into the values the prior uses (DECISION_LOG entry 17).

Rule (Asad, 23 Nov 2026): where both passes cover a content, the value is their mean; where only
one pass covers it, that pass alone, flagged in column `source` (both, A or C). Each pass is
interpolated on a common grid: linear in C for Fig. 7, linear in log10 content for the element
charts. Each curve runs from the earlier first point to the later last point of the two passes,
so the drawn end x_max used by rule H is the later of the two ends.
Pass A element readings <= 0 (axis ink, per the pass A note) are dropped.

Usage: python -I prior/digitize/combine.py prior/digitized/pass_asad prior/digitized/pass_claude prior/digitized/combined
"""
import csv, glob, os, re, sys, collections
import numpy as np

A_DIR, C_DIR, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)

def rows(p):
    return [r for r in csv.reader(open(p)) if r and not r[0].startswith('#')]

# pass C
C7 = collections.defaultdict(list)
for r in rows(f'{C_DIR}/ghp1977_fig7.csv')[1:]:
    C7[int(r[0])].append((float(r[1]), float(r[2])))
CE = collections.defaultdict(list)
FIG = {}
for r in rows(f'{C_DIR}/ghp1977_figs11-17.csv')[1:]:
    CE[(int(r[1]), r[2])].append((float(r[3]), float(r[4])))
    FIG[int(r[1])] = int(r[0])
# pass A
A7, AE = {}, {}
for f in sorted(glob.glob(f'{A_DIR}/passA_fig*.csv')):
    m = re.search(r'passA_fig(\d+)_(\d+)F(?:_(\w+))?\.csv', f)
    pts = sorted((float(x), float(y)) for x, y in rows(f))
    if m[3] is not None:
        # Pass A note: on Fig. 14 the Cr/Si line merges with the x axis at the far left, and
        # readings <= 0 there are axis ink. Such points are dropped from every element curve.
        pts = [p for p in pts if p[1] > 0]
    pts = np.array(pts)
    if m[3] is None:
        A7[int(m[2])] = pts
    else:
        AE[(int(m[2]), m[3])] = pts

def combine(a, c, grid, tr):
    """a, c: arrays of (x, y) sorted by x, or None. Returns list of (x, value, source, vA, vC)."""
    out = []
    for g in grid:
        vals = {}
        for name, p in (('A', a), ('C', c)):
            if p is not None and p[0, 0] - 1e-9 <= g <= p[-1, 0] + 1e-9:
                vals[name] = float(np.interp(tr(g), tr(p[:, 0]), p[:, 1]))
        if not vals:
            continue
        src = 'both' if len(vals) == 2 else next(iter(vals))
        out.append((g, round(float(np.mean(list(vals.values()))), 2), src,
                    round(vals['A'], 2) if 'A' in vals else '', round(vals['C'], 2) if 'C' in vals else ''))
    return out

def ends(a, c):
    ps = [p for p in (a, c) if p is not None]
    return min(p[0, 0] for p in ps), max(p[-1, 0] for p in ps)

HEAD = ('# Combined digitized values from Grange, Hribal and Porter, Metall. Trans. A 8 (1977) 1775-1785, {what}.\n'
        '# Digitized readings, not the authors\' data. Mean of pass A (Asad, WebPlotDigitizer) and pass C (Claude) where both\n'
        '# cover a content; single pass where only one does (column source). DECISION_LOG entry 17; built by prior/digitize/combine.py.\n')

# Fig. 7: C from 0.04 to 1.00 in 0.01 steps
out7 = []
for T in sorted(set(C7) | set(A7)):
    c = np.array(C7[T]) if T in C7 else None
    a = A7.get(T)
    lo, hi = ends(a, c)
    grid = [round(g, 2) for g in np.arange(0.04, 1.0001, 0.01) if lo - 1e-9 <= g <= hi + 1e-9]
    out7 += [(T,) + r for r in combine(a, c, grid, lambda v: v)]
with open(f'{OUT}/ghp1977_fig7_combined.csv', 'w', newline='') as f:
    f.write(HEAD.format(what='Fig. 7 (Fe-C base hardness, HV)'))
    w = csv.writer(f); w.writerow(['T_F', 'C_wt', 'HV', 'source', 'HV_passA', 'HV_passC']); w.writerows(out7)

# Element charts: 0.01-decade grid, plus each curve's two end points
outE, ends_rows = [], []
for key in sorted(set(CE) | set(AE)):
    T, el = key
    c = np.array(CE[key]) if key in CE else None
    a = AE.get(key)
    lo, hi = ends(a, c)
    lg = np.arange(np.ceil(np.log10(lo) * 100) / 100, np.log10(hi) + 1e-9, 0.01)
    grid = np.unique(np.r_[round(lo, 4), np.round(10 ** lg, 4), round(hi, 4)])
    res = combine(a, c, grid, np.log10)
    outE += [(FIG[T], T, el) + r for r in res]
    ends_rows.append((FIG[T], T, el, round(lo, 4), res[0][1], round(hi, 4), res[-1][1],
                      'A' if a is not None and a[-1, 0] >= (c[-1, 0] if c is not None else 0) else 'C'))
with open(f'{OUT}/ghp1977_figs11-17_combined.csv', 'w', newline='') as f:
    f.write(HEAD.format(what='Figs. 11 to 17 (dHV against element content, wt%)'))
    w = csv.writer(f); w.writerow(['fig', 'T_F', 'element', 'content_wt', 'dHV', 'source', 'dHV_passA', 'dHV_passC'])
    w.writerows(outE)
with open(f'{OUT}/ghp1977_figs11-17_combined_ends.csv', 'w', newline='') as f:
    f.write('# First readable point (start of the low-content line) and drawn end x_max (rule H) of each combined curve.\n')
    w = csv.writer(f); w.writerow(['fig', 'T_F', 'element', 'x_first', 'dHV_first', 'x_max', 'dHV_at_x_max', 'x_max_from_pass'])
    w.writerows(ends_rows)
print('fig7 rows', len(out7), 'element rows', len(outE))
print('fig7', collections.Counter(r[3] for r in out7), 'elements', collections.Counter(r[5] for r in outE))
