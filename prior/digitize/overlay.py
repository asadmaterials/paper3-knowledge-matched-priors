from PIL import Image, ImageDraw; import csv, sys, collections
COL=[(230,25,75),(60,180,75),(0,130,200),(245,130,48),(145,30,180),(70,240,240),(240,50,230),(210,180,0),(0,128,128),(170,110,40),(128,0,0),(0,0,128)]
def draw(img, curves, toimg, scale=3, crop=None, out='o.png'):
    """curves: dict label -> list of (u,v) data coords; toimg: (u,v)->(x,y) pixels"""
    im=Image.open(img).convert('RGB'); im=im.resize((im.width*scale,im.height*scale),Image.NEAREST)
    d=ImageDraw.Draw(im)
    for i,(lab,pts) in enumerate(curves.items()):
        c=COL[i%len(COL)]
        xy=[tuple(v*scale for v in toimg(u,w)) for u,w in pts]
        if len(xy)>1: d.line(xy,fill=c,width=1)
        for p in xy[::6]: d.ellipse((p[0]-2,p[1]-2,p[0]+2,p[1]+2),outline=c)
    if crop: im=im.crop(crop)
    im.save(out)
