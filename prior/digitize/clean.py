import numpy as np
def clean(x, y, win=12, thr=1.0, iters=4):
    """Drop points deviating > thr (pixel units) from a local quadratic fit of their neighbours."""
    x=np.asarray(x,float); y=np.asarray(y,float); keep=np.ones(len(x),bool)
    for _ in range(iters):
        dev=np.zeros(len(x))
        for i in range(len(x)):
            m=keep&(np.abs(x-x[i])<=win); m[i]=False
            if m.sum()<6: continue
            p=np.polyfit(x[m],y[m],2); dev[i]=abs(np.polyval(p,x[i])-y[i])
        bad=keep&(dev>thr)
        if not bad.any(): break
        # remove worst first
        keep[np.argmax(np.where(keep,dev,-1))]=False
        keep &= ~(dev>3*thr)
    return keep
