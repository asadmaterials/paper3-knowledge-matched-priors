"""Compare digitizing pass A (WebPlotDigitizer) with pass C (this folder).

Usage: python -I prior/digitize/compare.py prior/digitized/pass_asad prior/digitized/pass_claude prior/digitized/comparison
Pass C is interpolated at each pass A point (linear in C for Fig. 7, linear in log10 content for
Figs. 14 to 17), within pass C's traced range only. Differences are pass A minus pass C, in HV.
"""
import csv, glob, re, sys, collections, numpy as np
A_DIR, C_DIR, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
def rd(p):
    return [r for r in csv.reader(open(p)) if r and not r[0].startswith('#')]
# pass C
C7=collections.defaultdict(list)
for r in rd(f'{C_DIR}/ghp1977_fig7.csv')[1:]: C7[int(r[0])].append((float(r[1]),float(r[2])))
CE=collections.defaultdict(list)
for r in rd(f'{C_DIR}/ghp1977_figs11-17.csv')[1:]: CE[(int(r[1]),r[2])].append((float(r[3]),float(r[4])))
out=[]; pts=[]
for f in sorted(glob.glob(f'{A_DIR}/passA_fig*.csv')):
    m=re.search(r'passA_fig(\d+)_(\d+)F(?:_(\w+))?\.csv',f); fig,T,el=int(m[1]),int(m[2]),m[3] or 'base'
    a=np.array(sorted((float(x),float(y)) for x,y in rd(f)))
    c=np.array(C7[T] if fig==7 else CE[(T,el)])
    tr=(lambda v: v) if fig==7 else np.log10
    lo,hi=c[0,0],c[-1,0]
    inside=(a[:,0]>=lo)&(a[:,0]<=hi)
    cv=np.interp(tr(a[inside,0]),tr(c[:,0]),c[:,1]); d=a[inside,1]-cv
    for (x,y),cc,dd in zip(a[inside],cv,d): pts.append((fig,T,el,round(x,4),round(y,2),round(cc,2),round(dd,2)))
    out.append(dict(fig=fig,T=T,el=el,nA=len(a),n=int(inside.sum()),
        maxabs=round(float(np.abs(d).max()),2),mean=round(float(d.mean()),2),meanabs=round(float(np.abs(d).mean()),2),
        xA=(round(a[0,0],3),round(a[-1,0],3)),xC=(round(lo,3),round(hi,3)),
        worst=(round(float(a[inside][np.argmax(np.abs(d)),0]),3),round(float(d[np.argmax(np.abs(d))]),2))))
for o in out: print(o['fig'], o['T'], o['el'], 'n', o['n'], 'max', o['maxabs'], 'mean', o['mean'], 'mean abs', o['meanabs'])
with open(f'{OUT}/passA_vs_passC_points.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['fig','T_F','element','x','passA','passC_interp','A_minus_C']); w.writerows(pts)
with open(f'{OUT}/passA_vs_passC_summary.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['fig','T_F','element','n_A','n_compared','max_abs_diff','mean_diff_A_minus_C','mean_abs_diff','x_first_A','x_last_A','x_first_C','x_last_C','worst_x','worst_diff'])
    for o in out: w.writerow([o['fig'],o['T'],o['el'],o['nA'],o['n'],o['maxabs'],o['mean'],o['meanabs'],*o['xA'],*o['xC'],*o['worst']])
