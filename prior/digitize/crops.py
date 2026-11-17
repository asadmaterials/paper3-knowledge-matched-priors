"""Crop the element charts (Figs. 11 to 17) from the page images.

Run `pdfimages -png <GHP 1977 PDF> WORK/p` first: pages 6 and 7 of the paper
are WORK/p-008.png and WORK/p-009.png (2550 x 3300 px, 300 ppi, 1-bit).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from charts import CHARTS
WORK = os.environ.get("GHP_WORK", "work")
os.makedirs(f"{WORK}/el", exist_ok=True)
for f, (pg, box, T, ymax) in CHARTS.items():
    Image.open(f"{WORK}/{pg}.png").convert("L").crop(box).save(f"{WORK}/el/f{f}.png")
