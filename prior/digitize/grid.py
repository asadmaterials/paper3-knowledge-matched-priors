import numpy as np
XT=[0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.5,2.0]
def clusters(idx, gap=3):
    out=[]; cur=[idx[0]]
    for i in idx[1:]:
        if i-cur[-1]<=gap: cur.append(i)
        else: out.append(cur); cur=[i]
    out.append(cur); return [float(np.mean(c)) for c in out]
def detect(b, ymax, ystep, colfrac=0.5, rowfrac=0.5):
    """b: boolean dark array of chart crop (frame inclusive)."""
    h,w=b.shape
    cs=b.sum(0); rs=b.sum(1)
    cols=clusters([i for i,c in enumerate(cs) if c>colfrac*h])
    rows=clusters([i for i,c in enumerate(rs) if c>rowfrac*w])
    return cols, rows
class Axis:
    def __init__(self, cols, rows, ymax, ystep):
        assert len(cols)==len(XT), (len(cols), cols)
        nr=int(round(ymax/ystep))+1
        assert len(rows)==nr, (len(rows), rows)
        self.cols=np.array(cols); self.lx=np.log10(XT)
        self.rows=np.array(rows); self.yv=np.linspace(ymax,0,nr)
    def x(self,px): return float(10**np.interp(px,self.cols,self.lx))
    def y(self,py): return float(np.interp(py,self.rows,self.yv))
    def px(self,x): return float(np.interp(np.log10(x),self.lx,self.cols))
    def py(self,y): return float(np.interp(-y,-self.yv,self.rows))

def frame(b):
    """Locate the plot frame: longest horizontal/vertical dark lines."""
    rs=b.sum(1); cs=b.sum(0)
    hr=[i for i,c in enumerate(rs) if c>0.8*rs.max()]
    vc=[i for i,c in enumerate(cs) if c>0.8*cs.max()]
    return min(vc),max(vc),min(hr),max(hr)
def detect2(b, frac=0.6):
    x0,x1,y0,y1=frame(b)
    sub=b[y0:y1+1,x0:x1+1]; h,w=sub.shape
    cs=sub.sum(0); rs=sub.sum(1)
    cols=[c+x0 for c in clusters([i for i,c in enumerate(cs) if c>frac*h])]
    rows=[r+y0 for r in clusters([i for i,c in enumerate(rs) if c>frac*w])]
    return cols,rows,(x0,x1,y0,y1)
