import numpy as np
from runs import runs
def assign(preds, cand, tols):
    """order-preserving assignment of sorted candidates to sorted predictions (DP)."""
    n,m=len(preds),len(cand)
    INF=1e9
    # dp[i][j]: min cost using first i preds and first j cands
    dp=np.full((n+1,m+1),INF); dp[0,:]=0; ch={}
    for i in range(1,n+1):
        for j in range(0,m+1):
            # pred i-1 unmatched (cost = tol penalty)
            best=dp[i-1,j]+tols[i-1]; arg=('u',j)
            if j>0:
                if dp[i,j-1]<best: best=dp[i,j-1]; arg=('s',j-1)   # skip cand j-1
                c=abs(preds[i-1]-cand[j-1])
                if c<=tols[i-1] and dp[i-1,j-1]+c<best: best=dp[i-1,j-1]+c; arg=('m',j-1)
            dp[i,j]=best; ch[(i,j)]=arg
    i,j=n,m; out=[None]*n
    while i>0:
        t,k=ch[(i,j)]
        if t=='u': i-=1; j=k
        elif t=='s': j=k
        else: out[i-1]=cand[k]; i-=1; j=k
    return out
def track(im, seeds, x0, x1, x2, thr=130, skip_rows=(), skip_cols=(), tol=2.5, grow=0.3, ylim=(0,10**9)):
    res=[{} for _ in seeds]
    skip=[slice(max(g-1,0),g+2) for g in skip_rows]
    for direction,xend in ((-1,x1),(1,x2)):
        ys=list(map(float,seeds)); sl=[0.0]*len(seeds); miss=[0]*len(seeds)
        for x in range(x0,xend+direction,direction):
            preds=[y+s for y,s in zip(ys,sl)]
            if x in skip_cols:
                for k in range(len(ys)): ys[k]=preds[k]; miss[k]+=1
                continue
            cand=sorted(c for c,w in runs(im[:,x].copy(),thr,skip) if ylim[0]<c<ylim[1])
            got=assign(preds,cand,[tol+grow*m for m in miss])
            flags=['obs']*len(got)
            if any(g is None for g in got) and skip_rows:
                full=[(c,w) for c,w in runs(im[:,x].copy(),thr) if ylim[0]<c<ylim[1]]
                for k,g in enumerate(got):
                    if g is None:
                        for c,w in full:
                            if 3<=w<=4 and abs(c-preds[k])<=tol+1 and any(abs(c-r)<=2.5 for r in skip_rows):
                                got[k]=c; flags[k]='grid'; break
            for k,g in enumerate(got):
                if g is None: ys[k]=preds[k]; miss[k]+=1
                else:
                    if miss[k]==0: sl[k]=0.7*sl[k]+0.3*(g-ys[k])
                    else: sl[k]=0.7*sl[k]+0.3*(g-(ys[k]-sl[k]*miss[k]))/(miss[k]+1)
                    ys[k]=g; miss[k]=0; res[k][x]=(g,flags[k])
    return res
