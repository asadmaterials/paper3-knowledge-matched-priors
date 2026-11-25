# Codified metallurgical prior: specification v0.2 (draft)

Status: draft v0.2, 3 November 2026, updated 12, 13, 15 and 17 November 2026. To be frozen before Gate A (30 November 2026). No coefficient may be coded until its row in the source table below is marked "verified against original". Every change after 12 November is recorded in `prior/DECISION_LOG.md`, with what had been seen of the QT targets at the time.

## 1. Scope

- Confirmatory pool: the 360 QT rows tempered at 550 °C or above (120 steels; column `confirmatory`). Decided 16 November 2026 (DECISION_LOG entry 3), narrowing the 3 November choice of the 378 QT rows (entry 1).
- Secondary pool: all 378 QT rows (132 steels), adding the 12 spring steels tempered at 420 to 500 °C, whose hardenability is "not applicable (inputs not sourced)". The full 437-row pool is a further secondary analysis.
- Target: rotating-bending fatigue strength at 10^7 cycles, MPa.
- The C and N branches are needed only for the secondary full-pool analysis and are specified in section 7.

## 2. What the QT pool looks like

| Variable | Range in QT pool | Note |
| --- | --- | --- |
| C | 0.28 to 0.63 wt% | 51 rows above 0.5 |
| Si | 0.16 to 2.05 wt% | 12 rows at 1.31 or above (silicon spring steels) |
| Mn | 0.37 to 1.60 wt% | |
| Ni | 0.01 to 2.78 wt% | |
| Cr | 0.01 to 1.12 wt% | |
| Mo | 0.00 to 0.24 wt% | |
| P | 0.004 to 0.031 wt% | |
| Cu | 0.01 to 0.26 wt% | |
| Tempering temperature TT | 420 to 680 °C | 300 of 378 rows at 550, 600 or 650 °C |
| Tempering time Tt | 60 min for every row | |
| Through-hardening temperature THT | 825 to 865 °C | |
| Through-hardening quench code THQCr | 8 (276 rows) or 24 (102 rows) | 24 = water quench, 8 = oil quench (NRIM SR-93-02 Table 3; DECISION_LOG entry 8) |

Because Tt is constant, any time-temperature tempering parameter reduces to a function of TT alone in this pool.

## 3. The chain (QT branch)

The prior predicts fatigue strength in two steps. It does not compute as-quenched hardness: the tempered-hardness method below works directly from composition and tempering conditions, assuming a fully martensitic as-quenched structure.

### Step 1: tempered martensite hardness (Grange, Hribal and Porter 1977)

Verified against the original (Metall. Trans. A 8, 1775 to 1785, November 1977), 13 Nov 2026:

- **Method:** estimated HV at a tempering temperature = HV of the Fe-C alloy with the same carbon (Fig. 7) + the sum of ΔHV for Mn, P, Si, Ni, Cr, Mo and V (one read-off chart per temperature, Figs. 8 to 17). Effects are assumed additive and independent of carbon (p. 1782).
- **Form: charts, not tables.** Fig. 7 gives Fe-C hardness against carbon (0 to 1.0%) for 1 h tempers at 400 to 1300 °F in 100 °F steps. Figs. 8 to 17 give ΔHV against element content on a log scale (0.02 to 2%), one chart per temperature from 400 °F (Fig. 8) to 1300 °F (Fig. 17). The charts must be digitized (section 9).
- **Tempering:** 1 h at 100 °F (56 °C) intervals, 400 to 1300 °F (204 to 704 °C). The QT range 420 to 680 °C (788 to 1256 °F) needs Figs. 11 to 17 (700 to 1300 °F) and Fig. 7.
- **Hardness scale:** diamond pyramid (HV), 20 kg load (p. 1776). No conversion is needed before σw ≈ 1.6 HV.
- **Specimens and validity:** 1.3 to 2.5 mm thick, brine-quenched from 927 °C, austenite grain size ASTM 4 to 6. The method "is valid only for steel quenched to martensite" (p. 1784), which is what the hardenability rule below checks.
- **Composition levels tested (Table I):** C 0.12 to 0.98; Mn 0.35 to 1.95; P 0.002 to 0.28; Si 0.09 to 0.85; Ni 0.20 to 1.55; Cr 0.10 to 0.63; Mo 0.06 to 0.41; V 0.02 to 0.18 wt%. The authors give "no assurance that extrapolating the composition range ... beyond that given in Figs. 8 through 17, will be reliable" (p. 1784).
- **Nickel:** its effect is "essentially the same at all tempering temperatures" and can be expressed by "a single line drawn from zero for a nickel free steel to an increase in hardness (ΔHV) of 10 points ... for a steel containing 1.5 pct nickel" (p. 1781).

**Primary rule:** because every QT row is tempered for exactly 1 h, the prior reads the digitized GHP charts at the 100 °F steps either side of the row's tempering temperature and interpolates linearly in temperature. The tempering parameter is not needed for the QT pool.

**Cross-check only:** the GHP tempering parameter, confirmed from the axis label of Fig. 21 in the original:

```latex
P = (T_{F} + 460)\,(18 + \log_{10} t_{h}) \times 10^{-3}
```

with T_F the tempering temperature in °F and t_h the time in hours. For the QT pool, t_h = 1, so P = (T_F + 460) × 0.018.

```latex
HV_T = HV_{base}(C, P) + \sum_{i} \Delta HV_i(P)\, x_i
```

where ΔHV_i is read from the chart for element i at content x_i (wt%); it is not linear in x_i.

**QT steels outside the tested composition levels (inputs only, counted 13 Nov 2026):**

| Element | GHP upper level | QT steels above it | Who |
| --- | --- | --- | --- |
| Si | 0.85 | 9 | The silicon spring steels (SUP7, SUP12), all in the low-temper group |
| Ni | 1.55 | 30 | SNC631 (about 2.7% Ni) and SNCM439/447 (1.6 to 1.9%) |
| Cr | 0.63 | 75 | SCr440, SCM435/440, SNC631, SNCM, SUP9A and SUP12 (0.7 to 1.1%) |
| C, Mn, P, Mo | within range | 0 | |

79 of the 132 QT steels have at least one element above the tested level. **Contents below a curve's first readable point** (decided 23 Nov 2026, DECISION_LOG entry 17): the curves do not run to zero; most start at the charts' lower limit of 0.02% with a nonzero ΔHV (P about 5.7 HV), and at 1300 °F some start higher. Below the first readable point, ΔHV is linear in content from (0, 0) to that point. This covers P below 0.02% in most rows. **Cu** has no GHP curve and contributes 0 to the GHP sum (decided 23 Nov 2026; a limitation, section 6). **Drawn range against tested levels.** The charts draw several curves beyond the Table I tested levels: on Fig. 12 (800 °F) the Cr curve runs to about 0.95% and Si to about 1.0%; on Fig. 15 (1100 °F) Cr runs to about 0.8% (read by eye, 15 Nov 2026; exact ends come from digitizing). GHP's caveat is against extrapolating "beyond that given in Figs. 8 through 17", i.e. beyond the drawn curve. So the extension point x_max(i, T) is the end of the drawn curve for element i on the chart for temperature T, and the counts above use the stricter Table I levels. After digitizing, the counts are reported both ways.

**Rule above the drawn end** (exact coordinates; R8 in review round 6). For element i at temperature T, with x_max the end of the drawn curve:

- **Rule H (hold):** ΔHV_i(x) = ΔHV_i(x_max) for x > x_max.
- **Rule E (extend in log content, matching the chart axis):** ΔHV_i(x) = ΔHV_i(x_max) + s · (log₁₀ x − log₁₀ x_max) for x > x_max, where s is the least-squares slope of ΔHV against log₁₀ x over the last 0.3 decade of the drawn curve (x_max/10^0.3 to x_max; the whole drawn curve if it is shorter), in HV per decade of content, floored at 0. A 0.3-decade window is used because digitizing error of a few HV over a 0.1-decade window would give slope errors of tens of HV per decade.
- **Nickel:** GHP's own straight line, ΔHV = 10 × Ni/1.5 at every temperature, for all Ni contents. This is used at all contents under both rules; beyond 1.5% Ni it is an extrapolation and is reported as such.
- Scope and order (decided 23 Nov 2026, DECISION_LOG entry 17): the rule is applied to every digitized element (Mn, Si, Cr, Mo, P) and to every steel, on each chart at that chart's own drawn end, before interpolating between the two charts that bracket the tempering temperature. Mn needs it at 1300 °F, where its curve is drawn only to about 1.2%. Gate A is evaluated under both rules (section 8.5). The BO arms use rule H (decided 17 Nov 2026, DECISION_LOG entry 16); rule E, applied in the same scope and order, is reported as a sensitivity analysis.
- **Values used:** the combined digitized curves in `prior/digitized/combined/` (decided 23 Nov 2026, DECISION_LOG entry 17): the mean of pass A and pass C where both cover a content, the single pass where only one does (flagged per row). x_max is the later of the two passes' drawn ends, since ink beyond the earlier end was confirmed on the image. The first readable point for the low-content rule is the earlier of the two passes' first points.

### Step 2: fatigue limit from hardness (Murakami; Garwood et al.)

```latex
\sigma_w \approx 1.6\, HV
```

with σw in MPa and HV in kgf/mm². Verified in Murakami, *Metal Fatigue: Effects of Small Defects and Nonmetallic Inclusions*, 2nd ed. (Elsevier, 2019), Eq. (1.2): σw0 ≅ 1.6 HV ± 0.1 HV, "valid for HV ≤ 400 but unconservative (overestimation) for HV > 400"; above 400 HV "σw0 has no definite correlation with HV, and there is a large amount of scatter, which is material-dependent" (inclusions). Eq. (18.1) restates the same relation as the "ideal" upper bound, σw,ideal = 1.6 HV ± 0.1 HV. Murakami gives no plateau value.

No hardness-to-tensile-strength step is used, which removes one approximate conversion from the chain.

### Output and range handling

- Prior score: s(x) = σw from step 2, in MPa.
- High hardness (decided 17 Nov 2026, DECISION_LOG entry 15): σw = 1.6 HV at every hardness, with no plateau and no cap, described as Murakami's ideal upper bound, which overestimates σw above 400 HV. No source gives a plateau value, and a flat hold would tie the top rows, which decide the endpoint. Spearman ρ is unchanged by any strictly increasing σw(HV), so this choice cannot affect Gate A; it matters only through the BO arms' affine mean a + b·s(x). BO sensitivity analysis: σw held flat at 1.6 × 400 = 640 MPa above 400 HV. Gate A reports the number of QT rows whose predicted HV exceeds 400 (computed from inputs only).
- Composition outside the GHP validity ranges: inputs are clipped to the edge of the range and the row is flagged. Counts are reported per element.
- Through-hardening temperature and THQCr are not used for hardness in v0.2. Whether full martensite is reached is decided by the hardenability rule below.

### Hardenability rule (family fixed before any codified-prior correlation)

Written down on 12 Nov 2026, after the within-TT statistics in DECISION_LOG entry 2 had been seen (see entry 5). The family below is fixed; only its tabulated factors and inputs, taken from the cited sources, may be filled in. No variant is to be chosen by its correlation with NIMS fatigue.

1. **Ideal critical diameter** D_I, by the Grossmann multiplying-factor method as standardized in ASTM A255-10 (reapproved 2018), Standard Test Methods for Determining Hardenability of Steel: D_I = Π f_i(x_i) over C, Mn, Si, Ni, Cr, Mo and Cu, with the multiplying factors of Table 6 (in.), or the equations of Table 11 that generate it. The edition used is A255-10 (2018), the only full edition in hand (A255-20a: 4-page preview only; A255-02: superseded, with no Ni factor above 2.00% and no Cr factor above 1.75%). Above 1.50% Ni, A255-10 uses a separate cubic expression, which covers SNC631 (Ni 2.63 to 2.78%).
    - **Grain size (decided 17 Nov 2026, DECISION_LOG entry 15):** A255 has no grain-size input: "A No. 7 austenitic grain size is assumed" (section 10.3), and the carbon factor in Table 6 is for grain size 7. The prior uses grain size 7, so the calculation is reproducible from the standard. Direction of bias: NRIM SR-93-02 section 2.2 reports austenitic grain size numbers of about 8 to 10 for the structural steels, i.e. finer grain than 7, and finer grain lowers hardenability. Grain size 7 therefore overstates D_I, and the rule flags fewer steels as not fully hardened than it should. The metallography check (step 5) shows whether this bias matters. Grain size 8 to 10 is added as a sensitivity analysis only if sourced carbon factors by grain size are obtained (candidate: Grossmann 1942, Trans. AIME 150, the original of the method, to be checked for whether its carbon chart covers grain sizes 8 to 10). The report's number is taken as equivalent to the ASTM E112 number: both scales define grain size number G by a grain count that doubles with each unit of G (ISO 643, on which the JIS method is based, uses 8 × 2^G grains per mm²; E112 corresponds to about 7.75 × 2^G per mm²), so they differ by about 0.05 in G. For the spring steels, grain size awaits NIMS sheets 59, 60 and 63.
    - **Composition validity (A255-10 section 10.1.1):** "Calculated DI and Jominy hardenability curves are valid only within the chemical ranges stated above" (section 10.1: C 0.10 to 0.70, Mn 0.50 to 1.65, Si 0.15 to 0.60, Ni ≤ 1.50, Cr ≤ 1.35, Mo ≤ 0.55, Cu ≤ 0.35, V ≤ 0.20 wt%). The wider ranges in 10.1.1 (C 0.01 to 0.90, Mn 0.01 to 1.95, Si 0.01 to 2.00, Ni to 3.50, Cr to 2.50, Mo to 0.55, Cu to 0.55, V to 0.20) carry multiplying factors only "to facilitate melting process control". In the confirmatory pool, 31 of the 120 steels are outside the main range (counted from inputs, 17 Nov 2026): 30 with Ni above 1.50 (SNC631 and SNCM) and 3 with Mn below 0.50 (steel 37, S55C, Mn 0.37; two SNC631 steels, Mn 0.49), 2 of them in both groups. None is outside the 10.1.1 factor ranges. **Pre-stated rule:** these steels are computed with the 10.1.1 factors and flagged as outside A255's validity range; the count is reported; sensitivity analysis: the same steels treated as fully hardened (RT = Q).
2. **Section check at the test surface:** rotating-bending fatigue is controlled by the specimen surface, so the check is made at the depth of the fatigue specimen's test-section surface within the heat-treated blank, not at the bar centre. Inputs, sourced for the structural steels from NRIM SR-93-02 (Table 1, section 2.2 and Fig. 2a; checked against the report 15 Nov 2026): bars of 19 to 22 mm diameter (SMn 19 to 23 mm, SNCM447 19 to 20 mm) were cut into pieces of about 200 mm and heat-treated whole in salt baths; the rotating-bending specimen has an 8 mm test-section diameter. The test surface is therefore at r = 4 mm in a 19 to 22 mm bar, about 5.5 to 7 mm below the quenched surface (r/R about 0.36 to 0.42). Each steel's bar diameter is taken per grade from the report. Grossmann D_I is defined for 50% martensite at the centre of a round bar, so the rule needs a relation from D_I to hardness at that depth. Source: ASTM A255-10 itself, which converts D_I into a calculated Jominy curve: IH from Table 7 divided by the distance hardness dividing factor for the steel's D_I and the Jominy distance (Table 2 in inches, Table 3 in mm; generating equations in Tables 15 and 16), so steps 1 and 2 share one source. The remaining link, from a bar position under quench severity H to an equivalent Jominy distance, is taken from Lamont's charts (below).
    - **Quench severity H (decided 17 Nov 2026, DECISION_LOG entry 15):** from the quench medium, confirmed for the structural steels (NRIM SR-93-02 Table 3: THQCr 24 = water quench, 8 = oil quench; DECISION_LOG entry 8). The report gives only "WQ" or "OQ", not the agitation. Grossmann's H table as reproduced in ASM Handbook Vol. 4 (1991), "Quenching of Steel", Table 1, after Hollomon and Jaffe (1947), gives for water: none 0.9 to 1.0, mild 1.0 to 1.1, moderate 1.2 to 1.3, good 1.4 to 1.5; for "oil and salt": none 0.25 to 0.30, mild 0.30 to 0.35, moderate 0.35 to 0.40, good 0.4 to 0.5. Laboratory quenches are usually agitated by hand, so the range is pre-stated from none to good: **water 0.9 to 1.5 (central 1.1), oil 0.25 to 0.5 (central 0.35)**, the central values at mild to moderate agitation. Gate A is evaluated at both ends of each range (section 8.5). Grossmann's oils had no speed improvers, so his oil values are conservative for modern oils; a 1975 to 1980 laboratory practice is assumed to be close to them.
    - **Lamont charts and position (decided 17 Nov 2026, DECISION_LOG entry 15):** Lamont's charts give the Jominy distance equivalent to a position r/R in a round bar of diameter D quenched at severity H. Sources in hand: Totten (ed.), *Steel Heat Treatment: Metallurgy and Technologies*, 2nd ed. (CRC, 2006), section 5.5.1, Figs. 5.49 to 5.51 (r/R = 0, 0.5 and 0.8, after Lamont 1943); ASM Handbook Vol. 4, "Quenching of Steel", Fig. 41 (r/R = 0 and 0.5, lower resolution). No source in hand gives r/R = 0.4. The r/R = 0.5 chart alone would not do: that position cools faster than the test surface (r/R 0.36 to 0.42), so it predicts more hardening and fewer flags, the same direction as the grain size 7 bias, and the two would compound. **Primary:** for each steel, r/R = 4 mm / (bar diameter / 2), and the equivalent Jominy distance is interpolated linearly in r/R between the r/R = 0 and r/R = 0.5 charts (Totten Figs. 5.49 and 5.50), each read at the steel's bar diameter and H. **Sensitivity:** the r/R = 0 and r/R = 0.5 charts alone, as bounds. ASM Vol. 4 Table 12 (Jominy distance against equivalent bar diameter for 1141 steel, apparently for the bar centre) is used only as a cross-check of the centre chart. The 19 to 22 mm bars lie in the crowded lower corner of the charts (scales to about 240 mm), so reading error there is reported with the digitizing (section 9).
3. **Effect on hardness: the Athavale and Van Aken hybrid** (Crafts and Lamont 1947, with GHP for the tempered martensite). Source: Athavale and Van Aken, "On predicting quenched and tempered hardness of mixed microstructures", Proc. 29th ASM Heat Treating Society Conf. (2017) 19 to 26, reproduced as Paper I of V. A. Athavale, PhD dissertation, Missouri S&T (2019), open access (scholarsmine.mst.edu/doctoral_dissertations/2826). Equations checked against the dissertation text, 16 Nov 2026. All hardness in HRC:
    - IH: as-quenched hardness of 100% martensite, from carbon (ASTM A255-10 Table 7, "Initial Hardness").
    - Q: GHP tempered-martensite hardness from step 1, converted HV to HRC with ASTM E140-12b (2019) Eq. (A1.1), section A1.1.1; HRC to HV by inverting Eq. (A1.1) numerically and checking against E140 Table 1. (The dissertation cites E140-07, where the same conversion is Eq. X1.1.1; the edition used here numbers it A1.1.)
    - D: tempering decrement against temperature, Crafts and Lamont Fig. 2; f: disproportionate-softening factor against carbon and temperature, Crafts and Lamont Fig. 4 (reproduced as Figs. 4 and 5 of Paper I). Digitized from the 1947 original if obtained, otherwise from the reproductions.
    - RQ: as-quenched hardness at the test surface, from the A255 calculated Jominy curve at the Lamont-equivalent Jominy distance (step 2).
    - S = Q − f·IH; R = (Q − f·IH + D)/(1 − f); tempered hardness RT = RQ − D if RQ < R, otherwise RT = f·RQ + S.
    - Then HRC to HV (E140) for σw ≈ 1.6 HV.
    - **Consistency check:** for a fully martensitic steel, RQ = IH, so RT = f·IH + Q − f·IH = Q. The hybrid therefore changes only steels not fully hardened at the test surface, and reduces to GHP otherwise; the implementation is tested for this. "Fully hardened" means RQ = IH, i.e. a dividing factor of 1.00 at the equivalent Jominy distance. A255 Table 2 gives factors above 1.00 at most distances unless D_I is large, so most steels will count as not fully hardened, and for them the hybrid's reduction is small when RQ is close to IH.
    - **Hardness below HRC 20 (decided 17 Nov 2026, DECISION_LOG entry 15):** E140 Table 1 and Eq. (A1.1) cover HRC 20 to 68 (HV 238 and above), and E140 section A1.1 says the equations "should not be used for converting numbers outside of the defined hardness range". Rule: steels judged fully hardened are computed entirely in HV (RT = Q) and need no conversion. For a steel not fully hardened, the hybrid is applied only if Q, IH and RQ are all at or above HRC 20. If any is below, the hybrid is not applicable: RT = Q, the steel-temperature row is flagged, and the count is reported. Sensitivity analysis: the same rows with Eq. (A1.1) extrapolated below HRC 20, labelled as outside E140's range. Expected consequence, stated now: Q is most likely to fall below HRC 20 for the plain-carbon steels at 650 °C, which are also the steels the hybrid is meant to correct, so the primary rule leaves those rows uncorrected and the sensitivity analysis shows the effect.
    - **Pre-stated choices:** (a) D is the original Crafts and Lamont curve; the dissertation's corrected curve (Paper I Fig. 9: D = 0 at 454 °C and below, about 2 HRC more loss from 593 to 704 °C, fitted to their own Jominy data) is a sensitivity analysis. (b) Crafts and Lamont used a 2 h temper; GHP and NIMS use 1 h; no time correction is made, and this is stated as a limitation. (c) The hybrid was validated on 1 h tempers from 204 to 649 °C; the 680 °C rows are an extrapolation. (d) The dissertation's fitted workbook equations are not published, so D and f are digitized like the GHP charts, with two passes.
4. **Not applicable, decided before computing any correlation**, in either of two cases: (a) the blank size, test-section depth or quench medium cannot be sourced (grain size may be assumed, per step 1); or (b) with sourced inputs, the rule judges every QT steel fully hardened at the test surface by the criterion in step 3, so it cannot change any steel's hardness. In both cases the prior runs without it (full martensite assumed), and the paper says which case applied. Status 15 Nov 2026: inputs sourced for the 120 structural steels; for the 12 spring steels, case (a) applies until NIMS sheets 59, 60 and 63 arrive.
5. **Independent check from a sourced microstructure observation.** NRIM SR-93-02 section 2.2 reports that S35C, S45C, SMn438 and SMn443 "were not fully transformed into martensite deep inside the materials, even after rapid water quenching, and presented partly ferritic or bainitic structures", while the other low-alloy steels "showed ordinary fine tempered-martensitic structures". This is metallography, not fatigue data. Before Gate A, the A255 rule at r = 4 mm is checked against it: it should flag S35C, S45C and the SMn steels (42 steels) and no S55C, SCr, SCM, SNC or SNCM steel. Disagreement is reported. "Deep inside" may not reach r = 4 mm, so a partial match is possible and is reported as found, not tuned away. **If the two disagree, the prior uses the A255 result** (it is the codified rule); the metallography is reported as the check, and the disagreement is a Gate A finding, not a reason to change the rule.
6. **Fallback if the full A255 cannot be obtained** (not needed since 17 Nov 2026: A255-10 (2018) in hand; kept for the record): the not-fully-hardened set is the set named in the report (S35C, S45C, SMn438/443; 42 steels, column `grade`). The size of their hardness reduction still needs a sourced rule (step 3); if none can be sourced, these steels are marked with a flag and the prior is reported with and without excluding them, rather than with an invented reduction.

## 4. Sources

| Relation | Source | Status |
| --- | --- | --- |
| GHP tempering parameter P = (T_F + 460)(18 + log t_h) × 10⁻³ | Grange, Hribal and Porter, Metall. Trans. A 8 (1977) 1775, Fig. 21 | Verified against original, 13 Nov 2026. (The secondary source's worked value of 26.23 for 1 h at 950 °F does not match this formula, which gives 25.38.) Cross-check only. |
| GHP base hardness HV_base(C) at each temperature | Same, Fig. 7 | Source in hand; to digitize |
| GHP alloy increments ΔHV_i(x_i) at each temperature | Same, Figs. 11 to 17 for the QT range | Source in hand; to digitize |
| GHP composition levels, hardness scale, validity | Same, Table I and pp. 1776, 1781, 1784 | Verified against original, 13 Nov 2026 |
| A255 calculation range: C 0.10 to 0.70, Mn 0.50 to 1.65, Si 0.15 to 0.60, Ni ≤ 1.50, Cr ≤ 1.35, Mo ≤ 0.55, Cu ≤ 0.35, V ≤ 0.20 wt%; factor-only ranges in 10.1.1 | ASTM A255-10 (2018), sections 10.1 and 10.1.1 (same main range as the A255-20a preview, sections 1.3 and 10.1) | Verified against the full standard, 17 Nov 2026. Outside the main range: 40 of 132 QT steels (Si 9, Ni 30, Mn below 0.50: 3); 31 of 120 confirmatory steels (Ni 30, Mn 3, 2 in both). None of the 120 is outside the 10.1.1 ranges |
| A255 multiplying factors (C at grain size 7, Mn, Si, Ni, Cr, Mo, Cu); IH; distance hardness dividing factors | ASTM A255-10 (2018): Table 6 (equations Table 11); Table 7; Tables 2 and 3 (equations Tables 15 and 16); grain size 7 assumed, section 10.3 | Located and checked 17 Nov 2026; values to be transcribed from the equations and checked against the tables |
| Grossmann H by medium and agitation | ASM Handbook Vol. 4 (1991), "Quenching of Steel", Table 1, after Hollomon and Jaffe, *Ferrous Metallurgical Design* (Wiley, 1947), p. 176 | Verified 17 Nov 2026 |
| Lamont charts, r/R = 0, 0.5, 0.8 | Totten (ed.), *Steel Heat Treatment: Metallurgy and Technologies*, 2nd ed. (CRC, 2006), Figs. 5.49 to 5.51, after Lamont, Iron Age 152 (1943) 64 to 70; ASM Vol. 4, "Quenching of Steel", Fig. 41 and Table 12 | In hand 17 Nov 2026; to digitize |
| HV to HRC, HRC 20 to 68 | ASTM E140-12b (2019), Eq. (A1.1) in A1.1.1, and Table 1 | Verified 17 Nov 2026 |
| σw0 ≅ 1.6 HV ± 0.1 HV, valid for HV ≤ 400 | Murakami, *Metal Fatigue*, 2nd ed. (Elsevier, 2019), Eq. (1.2), Eq. (18.1); Garwood, Zurburg and Erickson (ASM, 1951), reproduced as Murakami Fig. 1.6 | Verified 17 Nov 2026 |

## 5. Why the affine calibration matters

In the BO comparison, every prior enters as m(x) = a + b·s(x), with a and b fitted on the initial design (see the research plan). The factor 1.6 and any constant offset in HV are therefore absorbed by b and a. What the BO arms test is the shape and ranking of s(x) across the pool. Absolute accuracy matters only for the independent validation in section 8.

## 6. Known limitations of v0.2

- **Hardenability (now a likely core issue, see DECISION_LOG entry 2).** GHP assume full martensite before tempering. Low-hardenability plain-carbon steels quenched as bars may not reach full martensite, so the prior will overestimate their hardness. Within each tempering temperature in the QT pool, fatigue rises with Cr and Mo and falls slightly with C. A carbon-dominated GHP prior with no hardenability term may therefore rank rows wrongly within a tempering temperature. The rule family is now fixed in section 3 (hardenability rule); its inputs and factors must be sourced before Gate A, not tuned to the QT targets. Grain size 7 (against NRIM's 8 to 10) biases the rule toward judging steels more hardened than they are; the Lamont position is interpolated rather than taken at r/R = 0.5 so as not to add a second bias in the same direction.
- **Silicon spring steels.** The 9 silicon spring steels (12 rows, Si 1.51 to 2.05 wt%) are above both the GHP silicon range (0.85) and the A255 range (0.60). They are among the strongest rows in the QT pool (fatigue up to 906 MPa), so the rule for out-of-range contents (step 1) decides how they rank.
- **Inclusions and upstream processing.** The fatigue relation ignores inclusion size, which the source says controls fatigue at high hardness. Inclusion data exist in the original file but not in this copy.
- **Copper.** GHP give no ΔHV for Cu (0.01 to 0.26 wt% in the data), so the GHP step gives Cu no effect on tempered hardness; Cu enters only through the A255 hardenability factor.
- **High-carbon rows.** 51 rows have C above 0.5 wt%. All are inside the GHP carbon range (to 0.98 wt%) and the A255 range (to 0.70 wt%).

## 7. Secondary branches (full-pool analysis only)

- **C (carburized, 48 rows):** case hardness after a low-temperature temper (TT 160 to 200 °C) from an assumed case carbon level, then σw from the case. Specification deferred until the QT branch passes Gate A.
- **N (normalized only, 11 rows):** ferrite-pearlite hardness from composition, then σw ≈ 1.6 HV. Candidate relation: the ferrite-pearlite equation in Ion and Anisdahl, attributed to Maynier; verify against the original before use.

## 8. Validation plan (before Gate A)

All NIMS correlations below are unblinded (DECISION_LOG entries 2 and 5); the independent checks in 1 and 2 are the main evidence that the prior is right.

1. **Independent check of step 1 (main evidence):** compare GHP predictions with published hardness of tempered steels not from NIMS. Report error in HV. Sources checked 17 Nov 2026 (ASM Handbook Vol. 4, "Tempering of Steel"):
    - Fig. 9 (three Mo steels, 1 h tempers): usable.
    - Table 1 (about 30 grades, HRC after 2 h tempers, 25 mm bars fully hardened): rough check only, because the tempers are 2 h (time-corrected with the GHP parameter), compositions are nominal, and several rows are identical (1330, 2330 and 3130; 4130, 5130 and 8630), which suggests typical rather than measured values.
    - Not independent of GHP, so not used: Fig. 6 (Grange and Baughman 1956), Fig. 10 (a redrawing of GHP's element charts, used only to cross-check the digitizing) and GHP's own Figs. 19 and 20.
    - Further 1 h tempering data for common grades (1045, 4140, 4340) still to be found.
2. **Independent check of step 2:** compare 1.6 HV with published pairs of fatigue limit and hardness from sources other than NIMS: Garwood et al. (1951) as reproduced in Murakami Fig. 1.6. Murakami Fig. 1.7 (Nishijima 1980) is NRIM data and is not opened before Gate A (DECISION_LOG entry 10).
3. **NIMS QT prior quality:** Spearman ρ between the unfitted prior and measured fatigue: overall; within-TT for the 100-steel cohort (ρ at 550, 600 and 650 °C, averaged into one cohort value); within-TT for the 20-steel cohort (averaged over 580, 630 and 680 °C, reported but not gating, since its sampling SE is about 0.2); all on the 360-row confirmatory pool; the same quantities are reported on the 378-row secondary pool. All intervals are 95% bootstrap intervals that resample steels (`steel_id`), 10,000 resamples. Counts of steels and rows reported for every subset.
4. **Heuristic reference priors**, computed and reported beside the codified prior: s = −TT and s = C·(700 − TT) (ρ = 0.51 and 0.46 on the 378-row QT pool, seen 12 Nov; their values on the 360-row confirmatory pool are not computed until Gate A). These show what tempering temperature alone achieves. Neither has within-TT skill: s = −TT is constant within a tempering temperature, and s = C·(700 − TT) reduces to C there, which correlates slightly negatively with fatigue (about −0.1). The within-TT criterion below therefore measures what the codified prior adds beyond tempering temperature.
5. **Gate A criteria (proposed, to freeze before any codified-prior correlation is computed):**
    - GO requires all of: overall ρ ≥ 0.4; the steel-level paired bootstrap of ρ_prior − ρ_heuristic, against the fixed heuristic reference s = −TT on the same rows, has its lower 95% bound above 0; and the 100-steel cohort within-TT ρ is at least 0.2 with its lower 95% bound above 0. (On the 378-row pool, beating s = −TT implied the 0.4 criterion; on the 360-row pool that is not known in advance, so the 0.4 criterion is applied in its own right.)
    - Adjust: overall ρ ≥ 0.2 but any GO criterion fails. The paper then reports that the codified prior adds nothing beyond tempering temperature, and the decision on the confirmatory pool (DECISION_LOG entry 3) is revisited.
    - Reframe: overall ρ below 0.2.
    - **Robustness to the extension rule and quench severity (R9):** the GO criteria are evaluated under every combination of rule H or E (applied to every element together, DECISION_LOG entry 17) and the low and high ends of the H range for each quench medium. GO requires GO under all combinations. GO under some but not all counts as Adjust, and the paper reports which combinations passed.
    - **Pre-stated subgroup report (not gating):** within-TT ρ in the 100-steel cohort, separately for Cr ≤ 0.5 wt% (53 steels: S35C, S45C, S55C, SMn) and Cr > 0.5 wt% (47 steels: SCr440, SCM, SNC631). 0.5 wt% is the threshold in the published warning recorded in DECISION_LOG entry 12.

## 9. Open items for Asad

- [x] Obtain GHP 1977 (in hand 13 Nov 2026) and record its validity ranges (done).
- [x] Confirm GHP's carbon range covers 0.63 wt% (yes) and whether its silicon range covers 2.05 wt% (no: tested to 0.85).
- [ ] Digitize Fig. 7 and Figs. 11 to 17 at fixed contents per element, recording the end of each drawn curve (x_max). The pages with Figs. 8 to 17 are native 300 dpi, 1-bit scans (2550 × 3300 px, checked with pdfimages, 16 Nov 2026); Fig. 7 is a separate 400 × 516 px, 150 ppi grayscale image (about 1.5 HV per pixel; checked 17 Nov 2026). No rescan is possible from this PDF: extract them with `pdfimages -png` without resampling, and take care where thin curves break at crossings. Two independent passes: Asad with WebPlotDigitizer, and a second pass here. Report the largest and mean difference between passes in HV, per chart, at least for Fig. 7 and the Cr curves at 1000 to 1300 °F; then check each curve by overlay. Digitized files carry a header naming the paper and figure, and stating they are digitized values (M18). Pass C (Claude) done 17 Nov 2026: `prior/digitized/pass_claude/`, method and reading notes in `prior/digitize/README.md`. Pass A (Asad) received 23 Nov 2026 for Fig. 7 at 1000 to 1300 °F and Figs. 14 to 17 (`prior/digitized/pass_asad/`); compared in `prior/digitized/comparison/` (largest difference 2.0 HV on Fig. 7, 1.2 HV on Cr; DECISION_LOG entry 17). Combined values in `prior/digitized/combined/` (23 Nov 2026). Open: a second pass of Fig. 7 at 700 to 900 °F and Figs. 11 to 13, needed only for the secondary pool's spring steels (420 to 500 °C, 788 to 932 °F, which also use Fig. 7 at 1000 °F and Fig. 14, already read in both passes). Either it is done before Gate A, or secondary-pool results are labelled "single digitizing pass" (decided 23 Nov 2026, DECISION_LOG entry 17).
- [x] Rule for the BO arms: H for Cr (and Si in the secondary pool), E as sensitivity analysis, decided 17 Nov 2026 (DECISION_LOG entry 16). Gate A uses both.
- [x] Obtain the full ASTM A255: A255-10 (reapproved 2018) in hand, 17 Nov 2026; table numbers checked (section 3, steps 1 to 3). A255-26 is current but not obtained; differences from A255-10 are not known.
- [ ] Transcribe the A255-10 factors from the Table 11, 15 and 16 equations, and check them against Tables 6, 2 and 3 and Table 7.
- [x] NIMS bar and specimen sizes for the structural steels (NRIM SR-93-02, 15 Nov 2026). Spring steels: awaiting sheets 59, 60, 63.
- [x] H central values and ranges for water and oil entered from ASM Handbook Vol. 4, 17 Nov 2026 (section 3, step 2).
- [x] Lamont's charts obtained (Totten 2006, r/R = 0, 0.5, 0.8; ASM Vol. 4 Fig. 41), 17 Nov 2026.
- [ ] Digitize the Lamont r/R = 0 and 0.5 charts for bar diameters 19 to 23 mm, two passes, and report the reading error in mm of Jominy distance.
- [ ] Optional: Grossmann (1942), Trans. AIME 150, for carbon factors by grain size (grain size 8 to 10 sensitivity).
- [x] Hardness-reduction rule chosen: Athavale and Van Aken hybrid (step 3), 16 Nov 2026.
- [ ] Obtain Crafts and Lamont (1947) Figs. 2 and 4 (OneMine), or digitize the reproductions in the dissertation.
- [x] ASTM E140-12b obtained, Eq. (A1.1) and Table 1, 17 Nov 2026.
- [x] σw ≈ 1.6 HV checked in Murakami (2nd ed., 2019), 17 Nov 2026; no plateau source exists there, and none is now needed (section 3, output and range handling).
- [ ] Further non-NIMS 1 h tempering data for common grades (section 8.1).
