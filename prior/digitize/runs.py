import numpy as np
def runs(col, thr, skip=()):
    d = col < thr
    for s in skip: d[s] = False
    out=[]; i=0; n=len(d)
    while i<n:
        if d[i]:
            j=i
            while j+1<n and d[j+1]: j+=1
            w=col[i:j+1]; wt=(thr-w).astype(float)
            out.append((float((np.arange(i,j+1)*wt).sum()/wt.sum()), j-i+1))
            i=j+1
        else: i+=1
    return out
