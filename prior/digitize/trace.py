import os, sys
WORK = os.environ.get('GHP_WORK', 'work')
import sys, numpy as np, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from calib import Ax
from runs import runs
from clean import clean
COL={'Mn':(220,20,60),'P':(0,140,0),'Si':(0,90,255),'Cr':(255,140,0),'Mo':(160,0,200),'V':(0,170,170),'Ni':(120,120,0)}
def trace(f, anchors, W=6, thr=128):
    a=Ax(f); b=np.array(Image.open(f'{WORK}/el/f{f}.png').convert('L')).astype(int)
    gr=[int(round(r)) for r in a.rows]; gc=set()
    for c in a.cols: gc|={int(round(c))+k for k in (-2,-1,0,1,2)}
    skip=[slice(r-1,r+2) for r in gr]
    ax=np.array([a.px(x) for x,_ in anchors]); ay=np.array([a.py(y) for _,y in anchors])
    pts=[]
    for px in range(int(np.ceil(ax[0])), int(np.floor(ax[-1]))+1):
        if px in gc: continue
        g=float(np.interp(px,ax,ay))
        cand=[c for c,w in runs(b[:,px].copy(),thr,skip) if abs(c-g)<=W]
        if cand:
            c=min(cand,key=lambda c:abs(c-g)); pts.append((px,c,g))
    pts=np.array(pts)
    keep=clean(pts[:,0],pts[:,1],win=15,thr=1.0,iters=60)
    out=[(a.x(p[0]),a.y(p[1]),a.y(p[2])) for p,k in zip(pts,keep) if k]
    return out, pts, keep
def overlay(f, curves, out, s=2):
    a=Ax(f); im=Image.open(f'{WORK}/el/f{f}.png').convert('RGB'); im=im.resize((im.width*s,im.height*s),Image.NEAREST)
    d=ImageDraw.Draw(im)
    for name,pts in curves.items():
        c=COL.get(name,(255,0,0))
        xy=[(a.px(x)*s,a.py(y)*s) for x,y,*_ in pts]
        for p in xy: d.ellipse((p[0]-1.5,p[1]-1.5,p[0]+1.5,p[1]+1.5),fill=c)
    im.save(out)
