# Digitizing GHP 1977: pass C (Claude)

Second of the two independent digitizing passes required by SPEC section 9. Pass A is Asad's WebPlotDigitizer pass. Outputs are in `prior/digitized/pass_claude/`. Done 17 Nov 2026 from inputs only: no target values were used.

Source: Grange, Hribal and Porter, "Hardness of tempered martensite in carbon and low alloy steels", Metall. Trans. A 8 (1977) 1775 to 1785. The PDF is not in the repo. Overlay images of the traces drawn on the charts are not committed, because they reproduce the figures.

## Reproduce

```
mkdir work && pdfimages -png <GHP 1977 PDF> work/p
export GHP_WORK=work
python -I prior/digitize/crops.py      # crops Figs. 11 to 17 from work/p-008.png and work/p-009.png
python -I prior/digitize/fig7.py       # work/fig7_clean.csv
python -I prior/digitize/elements.py   # work/ghp_elements_digitized.csv, work/ghp_elements_summary.csv
```

`elements.py` takes a few minutes. A rerun from a clean folder reproduced the committed element values exactly.

## Source images

| Figure | Image in the PDF | Resolution on the chart |
| --- | --- | --- |
| Fig. 7 (Fe-C base hardness) | separate 400 × 516 px, 150 ppi grayscale image (`p-007.png`) | about 1.5 HV per pixel |
| Figs. 11 to 17 (element ΔHV) | 2550 × 3300 px, 300 ppi, 1-bit page scans (`p-008.png`, `p-009.png`) | about 6.6 px per HV (5.6 for Fig. 16, whose axis runs to 120) |

SPEC section 9 describes all the charts as 300 dpi 1-bit scans. That holds for Figs. 11 to 17 but not for Fig. 7, which is the lowest-resolution chart in the chain.

## Method

**Calibration.** Gridline positions were found from dark-pixel column and row sums. The mapping from pixel to value is piecewise linear between gridlines: the content axis in log10, the hardness axis linear. A single linear fit over the Fig. 7 gridlines leaves residuals up to ±1.1 HV (scan distortion), which the piecewise mapping avoids.

**Fig. 7, misplaced "100" label.** The label "100" is printed beside the bottom frame (pixel row 482), but the 100 HV gridline is the heavy line at row 469, 13 px higher. The gridlines from 200 to 800 HV are 66.4 px apart, so 100 HV falls at row 468 to 469 and the frame is at about 80 HV. `fig7.py` uses row 469 as 100 HV. Taking the frame as 100 would bias the lowest curves by about 15 HV. Pass A found the same independently.

**Fig. 7.** The ten curves (400 to 1300 °F) are tracked automatically, column by column:
- the trackers start from two seed columns where all ten curves separate (pixel columns 160 and 360);
- candidates are assigned to curves with an order-preserving rule, since the curves do not cross;
- pixels shared with gridlines are handled separately;
- points from the two seeds are kept where they agree within 1.2 px;
- a local quadratic outlier filter removes points pulled onto label text.

Output: HV at C = 0.05 to 0.98 wt% in 0.01 steps. `gap_C` marks stretches bridged by interpolation. The largest is 0.02% C at 1200 °F and C 0.69 to 0.71%, under the "1200 °F" label, above the data's C range (0.28 to 0.63%).

**Figs. 11 to 17.** Done by hand with computer snapping, as in WebPlotDigitizer:
1. Each curve was identified by eye on zoomed views with gridline labels.
2. Anchor points (content, ΔHV) were read by hand along it, to within about 1 HV (`anchors.py`).
3. The tracer follows the anchor path column by column and snaps to the nearest dark-pixel run within ±W px (W = 6 to 8 px, about 0.9 to 1.2 HV), skipping gridline columns.
4. Columns with no ink within the window (gaps between dashes, labels) are dropped, then bridged by interpolation.
5. The same outlier filter is applied.
6. Output is resampled on a 0.01-decade content grid, from the first to the last traced point.

Because of the snapping window, pass C is not independent of the hand-read anchors to better than about 1 HV. Pass A is the independent check.

V and Ni are not traced. SPEC uses GHP's linear Ni rule, and V is not in the data.

## Checks done

- **Overlays:** every traced curve was drawn back on the chart at 2× and inspected. The overlay PDF was sent separately.
- **Tracer sensitivity:** the traces were rerun with ink thresholds 100 and 160 (of 255) and windows ±2 px. The largest change on any curve is 1.7 HV (Mo at 800 °F); 30 of the 35 curves change by 1.3 HV or less.
- **Internal consistency with GHP's text:**

| Check | GHP's text | Pass C |
| --- | --- | --- |
| P | the effect is "the same" at all tempering temperatures from 500 to 1200 °F | at 0.05, 0.1 and 0.2% P, the 700 and 1000 to 1300 °F charts agree within 1 HV; exceptions below |
| Mo at 0.2% | rises with tempering temperature to 1000 °F, the same at 1000 and 1100 °F, lower at 1200 °F | 28.6, 30.2, 30.0, 44.2, 42.4, 39.1, 20.5 HV at 700 to 1300 °F |
| Cr at 0.5% | maximum at 800 °F | 22.3, 52.9, 35.7, 35.8, 39.9, 37.8, 29.0 HV at 700 to 1300 °F |

- **Cross-check against ASM Handbook Vol. 4 "Tempering of Steel" Fig. 10** (a redrawing of the GHP element charts at 1000 to 1300 °F): not done. In the PDF it is a 469 × 349 px, 75 ppi JPEG, too coarse to check readings to better than 3 to 5 HV.

## Reading notes (also in `ghp1977_figs11-17_ranges.csv`)

- **800 °F (Fig. 12), Mo and Cr:** two dashed curves meet near the Mo label at about 0.37%. Mo is taken as the upper curve ending at the label. Cr is taken as the lower curve: steep between 0.22 and 0.37%, then the dashed tail to 0.95%. The opposite assignment would make the Mo effect at 0.2% fall from 28.6 HV at 700 °F to 7.3 at 800 °F and rise again to 30.0 at 900 °F, against GHP's text. Pass A should check this.
- **1000 °F (Fig. 14), Si and Cr:** drawn as one dashed line below about 0.2%. That line merges with the Mn line between about 0.15 and 0.32%, so in that range Si, Cr and Mn have the same value.
- **1200 °F (Fig. 16), Mn and Si:** coincide below about 0.25%.
- **1100 °F (Fig. 15), below about 0.06%:** Mn, Si and Cr overlap within about 1.5 HV.
- **Scan defects:** solid black areas cover the lower left of Fig. 13 (900 °F; 0.025 to 0.16%, 0 to 5 HV) and Fig. 17 (1300 °F; 0.025 to 0.17%, 0 to 5 HV). Curves are traced only from where they leave the defect: at 1300 °F, Mn from 0.11%, Si 0.13%, Cr 0.15%, Mo 0.18%.
- **Last dash near a label:** for Cr at 1000 °F, the last dash (about 0.88 to 0.95%) runs into the label "Cr". It is kept, giving x_last 0.95%; without it, x_last is 0.82%. The difference in ΔHV is about 1.5 HV.
- **Dashed curves:** in Fig. 13 the Cr curve is solid to about 0.6% and dashed from there to 0.95%, close to GHP's tested limit of 0.63%. In other charts whole curves are dashed. So "dashed" cannot be read as "extrapolated" throughout.
- **P at 900 °F:** about 5 HV below the P curve of every other chart (17.8 against about 23 HV at 0.1% P), and it ends at 0.2% rather than 0.25%. The 5× zoom confirms the traced line is the one ending at the P label. This affects only the secondary pool.
- **P at 800 °F below 0.05%:** starts at about 2.3 HV at 0.02%, against about 5.7 on the other charts. Confirmed at 5× zoom.

## Drawn ends (last traced point, wt%)

| Element | 700 | 800 | 900 | 1000 | 1100 | 1200 | 1300 °F | GHP tested to |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Cr | 0.89 | 0.94 | 0.95 | 0.95 (0.82) | 0.85 | 0.88 | 0.93 | 0.63 |
| Si | 0.92 | 0.98 | 0.98 | 0.95 | 0.98 | 0.97 | 0.92 | 0.85 |
| Mn | 1.79 | 1.97 | 1.97 | 1.96 | 1.97 | 1.95 | **1.10** | 1.95 |
| Mo | 0.49 | 0.37 | 0.49 | 0.47 | 0.47 | 0.48 | 0.49 | 0.41 |
| P | 0.25 | 0.25 | 0.20 | 0.25 | 0.25 | 0.25 | 0.25 | 0.28 |

## Findings that need a SPEC decision (inputs only)

Counted on the cleaned data, from composition and TT only. A row counts if either chart that brackets its tempering temperature, with nonzero weight, is affected.

1. **Contents below the first readable point.** SPEC section 3 says "each ΔHV curve runs to zero". The charts do not show this:
   - every curve starts at the chart's lower limit of 0.02%, mostly at nonzero ΔHV (P about 5.7 HV, Mo about 3, Mn about 2);
   - at 1300 °F the scan defect hides everything below 0.11 to 0.18%.

   Affected confirmatory rows:
   - P below 0.02% (P in the data is 0.004 to 0.031%): 300 of 360 rows, 100 steels;
   - Cr below the first readable point: 68 rows, 46 steels (S35C, S45C, S55C and SMn, Cr 0.01 to 0.15%). Below 0.02% on the 1000 and 1100 °F charts; below 0.046% at 1200 °F; below 0.15% at 1300 °F, which carries a weight of 0.02 at 650 °C;
   - Mo below 0.18% on the 1300 °F chart: 22 rows (19 SCM at 650 °C, where that chart carries a weight of 0.02; 3 SNCM439 at 680 °C, weight 0.56), Mo 0.15 to 0.17%.

   A rule is needed. One candidate is linear in content from zero at zero content to the first readable point. For P this matches the shape of the curve: ΔHV/x is about 290, 260 and 230 HV per wt% at 0.02, 0.05 and 0.1% P on the 1000 to 1300 °F charts.
2. **Above the drawn end applies to more elements than Cr.** SPEC applies rules H and E "to Si and Cr". In the confirmatory pool:
   - Cr is above the drawn end in 124 rows (42 steels: SCr440, SCM, SNC631 and SNCM439; Cr 0.86 to 1.12%);
   - Mn is above the 1300 °F drawn end (1.10%) in 19 rows: the SMn steels at 650 °C, where the 1300 °F chart carries a weight of only 0.02.

   The rule should name every element.
3. **Cu.** GHP give no ΔHV for Cu (0.01 to 0.26% in the data). SPEC should state that Cu adds nothing to the GHP sum.
4. **Fig. 7 resolution**, as above: about 1.5 HV per pixel, so the base hardness carries about ±1 HV of reading error before any comparison with pass A.

## Comparison with pass A

Pass A (Asad, WebPlotDigitizer) arrived 23 Nov 2026 and is in `prior/digitized/pass_asad/`. It covers the charts the confirmatory pool needs (TT 550 to 680 °C, i.e. 1022 to 1256 °F):
- Fig. 7 at 1000 to 1300 °F;
- Figs. 14 to 17, Mn, Si, Cr, Mo and P.

Figs. 11 to 13 and Fig. 7 at 400 to 900 °F have pass C only. They are needed only for the secondary pool (spring steels at 420 to 500 °C).

`compare.py` interpolates pass C at every pass A point, within pass C's traced range. The results are in `prior/digitized/comparison/`: a summary per curve and every point. Differences are pass A minus pass C.

| Curve | Points compared | Largest difference (HV) | Mean difference (HV) | Mean absolute difference (HV) |
| --- | --- | --- | --- | --- |
| Fig. 7, 1000 °F | 27 | 1.42 | +0.35 | 0.56 |
| Fig. 7, 1100 °F | 35 | 1.96 | +0.46 | 0.66 |
| Fig. 7, 1200 °F | 42 | 1.71 | +0.57 | 0.74 |
| Fig. 7, 1300 °F | 43 | 1.53 | +0.08 | 0.52 |
| Cr, 1000 °F | 25 | 0.91 | −0.28 | 0.41 |
| Cr, 1100 °F | 27 | 1.22 | −0.22 | 0.32 |
| Cr, 1200 °F | 23 | 0.85 | +0.04 | 0.18 |
| Cr, 1300 °F | 20 | 0.68 | +0.10 | 0.16 |
| All 20 element curves | 845 | 1.80 (Mo, 1200 °F, at 0.16%) | −0.43 to +0.10 | 0.11 to 0.58 |

- **No curve where the passes followed different lines.** Every difference is within 2 HV. The largest are on steep stretches of Mo, at the left ends of curves, and for Fig. 7, where one pixel is about 1.5 HV.
- **Fig. 7 bias:** pass A reads 0.1 to 0.6 HV higher on average, under half a pixel.
- **Drawn ends:** the passes agree within 4% of content, except Mn at 1300 °F. There pass A ends where the curve runs into its label (1.20%) and pass C before it (1.10%).
- **Ends that include a final dash near a label:** for Cr, pass A ends later at 1000 and 1100 °F, pass C later at 1300 °F.
- **Value at the drawn end, the value rule H holds:** the passes differ by at most 0.9 HV on every curve.

### The Fig. 17 dark patch

Pass A found that the black area at the lower left of Fig. 17 is inverted, not lost ink. Before opening any pass A file, pass C examined the patch and recorded a reading (scratch note, 23 Nov 2026; summarized here):
- The major vertical gridlines appear white inside the black, which confirms the inversion.
- Four white marks were read: three short shallow ones near 0.054, 0.064 and 0.077% (read by eye at 2.6 to 3.6 HV), and one steep one, W4, at 0.124 to 0.135% (2.2 to 3.8 HV, centre 0.129%, 3.0 HV), placed on the extension of the Cr dashes.
- No reading of the solid Mn/Si line inside the patch was claimed.

Against pass A:
- **W4** matches pass A's Cr (0.123%, 2.28 HV; 0.129%, 3.11 HV) within 0.1 HV, assigned to the same curve. This check was blind.
- **The three shallow marks** were read by eye about 0.7 to 0.9 HV above pass A's Mo points. A column-by-column pixel measurement after opening pass A places them at 1.9 to 2.1 HV (0.054%), 2.5 HV (0.064%) and 3.3 HV (0.078%), within 0.3 HV of pass A's Mo. That measurement was not blind.
- **Mn and Si inside the patch:** pass A interpolated between gridline gaps. Pass C has no independent reading.

Outside the patch, pass A reads Mo dashes at 0.113% (5.76 HV) and 0.137 to 0.161% (9.1 to 13.0 HV), above the patch. Pass C had seen candidate dashes at (0.113%, 5.9 HV) and (0.144%, 10.8 HV) but left them out as ambiguous. Pass A supports them as Mo.

What the data need below pass C's first points at 1300 °F:
- Mo 0.15 to 0.17% (22 rows): covered by the Mo dashes above the patch.
- Cr 0.01 to 0.15% at 650 °C: the 1300 °F chart has a weight of only 0.02 there.
- Si (minimum 0.16%) and Mn (minimum 0.37%): never below pass C's first points (0.13% and 0.11%).

The decision is recorded in DECISION_LOG entry 17.
