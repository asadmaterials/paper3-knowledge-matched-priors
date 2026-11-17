"""Trace the element curves of GHP 1977 Figs. 11 to 17 from hand-read anchors (anchors.py),
resample them on a log-content grid (0.01 decade), and report tracing sensitivity.
Run crops.py first."""
import os, sys, csv, numpy as np; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
WORK = os.environ.get('GHP_WORK', 'work')
from trace import trace; from anchors import A; from charts import CHARTS
W={11:7,12:7,13:7,14:6,15:6,16:6,17:8}
def curve(f,el,thr=128,w=None):
    out,_,_=trace(f,A[f][el],W=w or W[f],thr=thr)
    x=np.array([o[0] for o in out]); y=np.array([o[1] for o in out])
    o=np.argsort(x); return x[o],y[o]
def resample(x,y,grid):
    lx=np.log10(x); return np.interp(np.log10(grid),lx,y)
rows=[]; summ=[]; sens=[]
for f in sorted(A):
    T=CHARTS[f][2]
    for el in A[f]:
        x,y=curve(f,el)
        lg=np.arange(np.ceil(np.log10(x[0])*100)/100, np.log10(x[-1])+1e-9, 0.01)
        grid=np.round(10**lg,4)
        # include endpoints
        grid=np.unique(np.r_[round(x[0],4),grid,round(x[-1],4)])
        v=resample(x,y,grid)
        for g,val in zip(grid,v): rows.append((f,T,el,g,round(float(val),2)))
        summ.append((f,T,el,round(x[0],3),round(float(y[0]),1),round(x[-1],3),round(float(y[-1]),1),len(x)))
        # sensitivity: thresholds and window
        alts=[]
        for thr,w in ((100,None),(160,None),(128,W[f]+2),(128,max(W[f]-2,3))):
            try:
                xa,ya=curve(f,el,thr,w)
                g2=grid[(grid>=max(x[0],xa[0]))&(grid<=min(x[-1],xa[-1]))]
                alts.append(np.max(np.abs(resample(x,y,g2)-resample(xa,ya,g2))))
            except Exception as e: alts.append(np.nan)
        sens.append((f,T,el,round(float(np.nanmax(alts)),2)))
with open(f'{WORK}/ghp_elements_digitized.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['fig','T_F','element','content_wt','dHV']); w.writerows(rows)
with open(f'{WORK}/ghp_elements_summary.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['fig','T_F','element','x_first','dHV_first','x_last','dHV_last','n_points']); w.writerows(summ)
for s in summ: print(s)
print('sensitivity max |diff| HV:'); 
for s in sens: print(s)
