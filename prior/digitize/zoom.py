import os, sys
WORK = os.environ.get('GHP_WORK', 'work')
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
from calib import Ax
from grid import XT
try: FONT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
except Exception: FONT=ImageFont.load_default()
def zoom(f, x0, x1, y0, y1, s=2, out=None, extra=None):
    a=Ax(f); im=Image.open(f'{WORK}/el/f{f}.png').convert('RGB')
    if extra: extra(im,a)
    L,R=int(a.px(x0))-5,int(a.px(x1))+5; T,B=int(a.py(y1))-5,int(a.py(y0))+5
    c=im.crop((L,T,R,B)); c=c.resize((c.width*s,c.height*s),Image.LANCZOS)
    M=40; canvas=Image.new('RGB',(c.width+M,c.height+M),'white'); canvas.paste(c,(M,0))
    d=ImageDraw.Draw(canvas)
    for x in XT:
        if x0<=x<=x1:
            X=M+(a.px(x)-L)*s; d.text((X-12,c.height+4),f'{x:g}',fill='blue',font=FONT)
    for y in a.yv:
        if y0<=y<=y1:
            Y=(a.py(y)-T)*s; d.text((2,Y-8),f'{y:g}',fill='blue',font=FONT)
    out=out or f'{WORK}/el/z{f}.png'; canvas.save(out); return out
if __name__=='__main__':
    f=int(sys.argv[1]); v=list(map(float,sys.argv[2:6])); s=int(sys.argv[6]) if len(sys.argv)>6 else 2
    print(zoom(f,*v,s=s))
