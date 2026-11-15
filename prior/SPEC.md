# Codified metallurgical prior: specification v0.2 (draft)

Status: draft v0.2, 3 November 2026, updated 12, 13 and 15 November 2026. To be frozen before Gate A (30 November 2026). No coefficient may be coded until its row in the source table below is marked "verified against original". Every change after 12 November is recorded in `prior/DECISION_LOG.md`, with what had been seen of the QT targets at the time.

## 1. Scope

- Primary pool: the 378 QT rows of the NIMS fatigue data (through-hardened, quenched and tempered). Decision taken 3 November 2026, because every row in the top 1% and top 5% of the full pool is carburized (see `data/DATA_CARD.md`).
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
| Through-hardening cooling rate THQCr | 8 (276 rows) or 24 (102 rows) | unit not stated in any source found |

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

79 of the 132 QT steels have at least one element above the tested level. Contents below the lowest tested level are not a problem, since each ΔHV curve runs to zero. **Drawn range against tested levels.** The charts draw several curves beyond the Table I tested levels: on Fig. 12 (800 °F) the Cr curve runs to about 0.95% and Si to about 1.0%; on Fig. 15 (1100 °F) Cr runs to about 0.8% (read by eye, 15 Nov 2026; exact ends come from digitizing). GHP's caveat is against extrapolating "beyond that given in Figs. 8 through 17", i.e. beyond the drawn curve. So the extension point x_max(i, T) is the end of the drawn curve for element i on the chart for temperature T, and the counts above use the stricter Table I levels. After digitizing, the counts are reported both ways.

**Rule above the drawn end** (exact coordinates; R8 in review round 6). For element i at temperature T, with x_max the end of the drawn curve:

- **Rule H (hold):** ΔHV_i(x) = ΔHV_i(x_max) for x > x_max.
- **Rule E (extend in log content, matching the chart axis):** ΔHV_i(x) = ΔHV_i(x_max) + s · (log₁₀ x − log₁₀ x_max) for x > x_max, where s is the least-squares slope of ΔHV against log₁₀ x over the last 0.3 decade of the drawn curve (x_max/10^0.3 to x_max; the whole drawn curve if it is shorter), in HV per decade of content, floored at 0. A 0.3-decade window is used because digitizing error of a few HV over a 0.1-decade window would give slope errors of tens of HV per decade.
- **Nickel:** GHP's own straight line, ΔHV = 10 × Ni/1.5 at every temperature, for all Ni contents. This is used at all contents under both rules; beyond 1.5% Ni it is an extrapolation and is reported as such.
- The same rule is applied to Si and Cr and to every steel. Gate A is evaluated under both rules (section 8.5). The rule used in the BO arms is fixed in section 9 before the preregistration; the other rule is reported as a sensitivity analysis.

### Step 2: fatigue limit from hardness (Murakami; Garwood et al.)

```latex
\sigma_w \approx 1.6\, HV
```

with σw in MPa and HV in kgf/mm². The scatter reported is ±0.1 HV, and the relation is stated as valid up to a material-specific hardness of about 400 to 500 HV, above which inclusions control the fatigue limit.

No hardness-to-tensile-strength step is used, which removes one approximate conversion from the chain.

### Output and range handling

- Prior score: s(x) = σw from step 2, in MPa.
- High hardness: a hard cap is not used, because it would give the top rows tied scores, and those rows decide the endpoint. Instead σw follows a monotone plateau above the linear range. **The plateau form and its source must be fixed in this file before any Gate A correlation is computed.** Gate A reports ρ with and without the plateau, and the number of QT rows above the linear range.
- Composition outside the GHP validity ranges: inputs are clipped to the edge of the range and the row is flagged. Counts are reported per element.
- Through-hardening temperature and THQCr are not used for hardness in v0.2. Whether full martensite is reached is decided by the hardenability rule below.

### Hardenability rule (family fixed before any codified-prior correlation)

Written down on 12 Nov 2026, after the within-TT statistics in DECISION_LOG entry 2 had been seen (see entry 5). The family below is fixed; only its tabulated factors and inputs, taken from the cited sources, may be filled in. No variant is to be chosen by its correlation with NIMS fatigue.

1. **Ideal critical diameter** D_I, by the Grossmann multiplying-factor method as standardized in ASTM A255 (Standard Test Methods for Determining Hardenability of Steel): D_I = D_I,base(C, austenite grain size) × Π f_i(x_i), over the elements A255 tabulates (Mn, Si, Ni, Cr, Mo, Cu as available). Factors to be transcribed from the A255 tables. Grain size: NRIM SR-93-02 (Nishijima 1993) section 2.2 reports austenitic grain size numbers of about 8 to 10 for the structural steels; the prior uses 9, with 8 and 10 as pre-stated sensitivity values. The report's number is taken as equivalent to the ASTM E112 number: both scales define grain size number G by a grain count that doubles with each unit of G (ISO 643, on which the JIS method is based, uses 8 × 2^G grains per mm²; E112 corresponds to about 7.75 × 2^G per mm²), so they differ by about 0.05 in G. Citation of JIS G 0551 and E112 to be added from the standards themselves. For the spring steels, grain size awaits NIMS sheets 59, 60 and 63.
2. **Section check at the test surface:** rotating-bending fatigue is controlled by the specimen surface, so the check is made at the depth of the fatigue specimen's test-section surface within the heat-treated blank, not at the bar centre. Inputs, sourced for the structural steels from NRIM SR-93-02 (Table 1, section 2.2 and Fig. 2a; checked against the report 15 Nov 2026): bars of 19 to 22 mm diameter (SMn 19 to 23 mm, SNCM447 19 to 20 mm) were cut into pieces of about 200 mm and heat-treated whole in salt baths; the rotating-bending specimen has an 8 mm test-section diameter. The test surface is therefore at r = 4 mm in a 19 to 22 mm bar, about 5.5 to 7 mm below the quenched surface (r/R about 0.36 to 0.42). Each steel's bar diameter is taken per grade from the report. Grossmann D_I is defined for 50% martensite at the centre of a round bar, so the rule needs a relation from D_I to hardness at that depth. Source: ASTM A255 itself, which converts D_I into a calculated Jominy curve using its distance hardness dividing factors (table numbers to confirm from the standard), so steps 1 and 2 share one source. The remaining link, from a bar position under quench severity H to an equivalent Jominy distance, is taken from a cited handbook chart. Quench severity H: from the quench medium, now confirmed for the structural steels (NRIM SR-93-02 Table 3: THQCr 24 = water quench, 8 = oil quench; DECISION_LOG entry 8). H values for each medium and agitation are taken from the cited handbook source for the chart above.
3. **Effect on hardness:** a steel judged not fully hardened gets a lower as-quenched hardness before tempering. The reduction rule (for example, the hardness at the expected martensite fraction from a cited relation) is to be sourced, not fitted.
4. **Not applicable, decided before computing any correlation**, in either of two cases: (a) the blank size, test-section depth or quench medium cannot be sourced (grain size may be assumed, per step 1); or (b) with sourced inputs, the rule judges every QT steel fully hardened at the test surface by the criterion in step 3, so it cannot change any steel's hardness. In both cases the prior runs without it (full martensite assumed), and the paper says which case applied. Status 15 Nov 2026: inputs sourced for the 120 structural steels; for the 12 spring steels, case (a) applies until NIMS sheets 59, 60 and 63 arrive.
5. **Independent check from a sourced microstructure observation.** NRIM SR-93-02 section 2.2 reports that S35C, S45C, SMn438 and SMn443 "were not fully transformed into martensite deep inside the materials, even after rapid water quenching, and presented partly ferritic or bainitic structures", while the other low-alloy steels "showed ordinary fine tempered-martensitic structures". This is metallography, not fatigue data. Before Gate A, the A255 rule at r = 4 mm is checked against it: it should flag S35C, S45C and the SMn steels (42 steels) and no S55C, SCr, SCM, SNC or SNCM steel. Disagreement is reported. "Deep inside" may not reach r = 4 mm, so a partial match is possible and is reported as found, not tuned away. **If the two disagree, the prior uses the A255 result** (it is the codified rule); the metallography is reported as the check, and the disagreement is a Gate A finding, not a reason to change the rule.
6. **Fallback if the full A255 cannot be obtained:** the not-fully-hardened set is the set named in the report (S35C, S45C, SMn438/443; 42 steels, column `grade`). The size of their hardness reduction still needs a sourced rule (step 3); if none can be sourced, these steels are marked with a flag and the prior is reported with and without excluding them, rather than with an invented reduction.

## 4. Sources

| Relation | Source | Status |
| --- | --- | --- |
| GHP tempering parameter P = (T_F + 460)(18 + log t_h) × 10⁻³ | Grange, Hribal and Porter, Metall. Trans. A 8 (1977) 1775, Fig. 21 | Verified against original, 13 Nov 2026. (The secondary source's worked value of 26.23 for 1 h at 950 °F does not match this formula, which gives 25.38.) Cross-check only. |
| GHP base hardness HV_base(C) at each temperature | Same, Fig. 7 | Source in hand; to digitize |
| GHP alloy increments ΔHV_i(x_i) at each temperature | Same, Figs. 11 to 17 for the QT range | Source in hand; to digitize |
| GHP composition levels, hardness scale, validity | Same, Table I and pp. 1776, 1781, 1784 | Verified against original, 13 Nov 2026 |
| A255 calculation range: C 0.10 to 0.70, Mn 0.50 to 1.65, Si 0.15 to 0.60, Ni ≤ 1.50, Cr ≤ 1.35, Mo ≤ 0.55, Cu ≤ 0.35, V ≤ 0.20 wt% | ASTM A255-20a, sections 1.3 and 10.1 | Verified from the 4-page preview, 13 Nov 2026. 40 QT steels fall outside (Si 9, Ni 30, Mn below 0.50: 3) |
| A255 D_I base table, multiplying factors, distance hardness dividing factors | ASTM A255-20a, Tables 2 onward | Not in the preview; full standard needed |
| σw ≈ 1.6 HV, valid to about 400 to 500 HV | Murakami, Metal Fatigue (Elsevier); Garwood, Zurburg and Erickson (1951), as reviewed in Metals 12 (2022) 1066 | Confirmed in the review; verify in Murakami |

## 5. Why the affine calibration matters

In the BO comparison, every prior enters as m(x) = a + b·s(x), with a and b fitted on the initial design (see the research plan). The factor 1.6 and any constant offset in HV are therefore absorbed by b and a. What the BO arms test is the shape and ranking of s(x) across the pool. Absolute accuracy matters only for the independent validation in section 8.

## 6. Known limitations of v0.2

- **Hardenability (now a likely core issue, see DECISION_LOG entry 2).** GHP assume full martensite before tempering. Low-hardenability plain-carbon steels quenched as bars may not reach full martensite, so the prior will overestimate their hardness. Within each tempering temperature in the QT pool, fatigue rises with Cr and Mo and falls slightly with C. A carbon-dominated GHP prior with no hardenability term may therefore rank rows wrongly within a tempering temperature. The rule family is now fixed in section 3 (hardenability rule); its inputs and factors must be sourced before Gate A, not tuned to the QT targets.
- **Silicon spring steels.** The 9 silicon spring steels (12 rows, Si 1.51 to 2.05 wt%) are above both the GHP silicon range (0.85) and the A255 range (0.60). They are among the strongest rows in the QT pool (fatigue up to 906 MPa), so the rule for out-of-range contents (step 1) decides how they rank.
- **Inclusions and upstream processing.** The fatigue relation ignores inclusion size, which the source says controls fatigue at high hardness. Inclusion data exist in the original file but not in this copy.
- **High-carbon rows.** 51 rows have C above 0.5 wt%. All are inside the GHP carbon range (to 0.98 wt%) and the A255 range (to 0.70 wt%).

## 7. Secondary branches (full-pool analysis only)

- **C (carburized, 48 rows):** case hardness after a low-temperature temper (TT 160 to 200 °C) from an assumed case carbon level, then σw from the case. Specification deferred until the QT branch passes Gate A.
- **N (normalized only, 11 rows):** ferrite-pearlite hardness from composition, then σw ≈ 1.6 HV. Candidate relation: the ferrite-pearlite equation in Ion and Anisdahl, attributed to Maynier; verify against the original before use.

## 8. Validation plan (before Gate A)

All NIMS correlations below are unblinded (DECISION_LOG entries 2 and 5); the independent checks in 1 and 2 are the main evidence that the prior is right.

1. **Independent check of step 1 (main evidence):** compare GHP predictions with published hardness of tempered steels not from NIMS (for example, handbook tempering curves for 1045, 4140 and 4340 after a 1 h temper). Report error in HV.
2. **Independent check of step 2:** compare 1.6 HV with published fatigue limits and hardness pairs from sources other than NIMS.
3. **NIMS QT prior quality:** Spearman ρ between the unfitted prior and measured fatigue: overall; within-TT for the 100-steel cohort (ρ at 550, 600 and 650 °C, averaged into one cohort value); within-TT for the 20-steel cohort (averaged over 580, 630 and 680 °C, reported but not gating, since its sampling SE is about 0.2); and with the 12 low-temper steels excluded. All intervals are 95% bootstrap intervals that resample steels (`steel_id`), 10,000 resamples. Counts of steels and rows reported for every subset.
4. **Heuristic reference priors**, computed and reported beside the codified prior: s = −TT (ρ = 0.51 on QT) and s = C·(700 − TT) (ρ = 0.46). These show what tempering temperature alone achieves. Neither has within-TT skill: s = −TT is constant within a tempering temperature, and s = C·(700 − TT) reduces to C there, which correlates slightly negatively with fatigue (about −0.1). The within-TT criterion below therefore measures what the codified prior adds beyond tempering temperature.
5. **Gate A criteria (proposed, to freeze before any codified-prior correlation is computed):**
    - GO requires all of: overall ρ ≥ 0.4; the steel-level paired bootstrap of ρ_prior − ρ_heuristic, against the fixed heuristic reference s = −TT on the same rows, has its lower 95% bound above 0; and the 100-steel cohort within-TT ρ is at least 0.2 with its lower 95% bound above 0. (The 0.4 criterion is implied by beating s = −TT, whose ρ is 0.51; it is kept for continuity with the research plan.)
    - Adjust: overall ρ ≥ 0.2 but any GO criterion fails. The paper then reports that the codified prior adds nothing beyond tempering temperature, and the decision on the confirmatory pool (DECISION_LOG entry 3) is revisited.
    - Reframe: overall ρ below 0.2.
    - **Robustness to the extension rule (R9):** the GO criteria are evaluated under all four combinations of rule H or E for Si and for Cr (section 3, step 1). GO requires GO under all four. GO under some but not all counts as Adjust, and the paper reports which combinations passed.

## 9. Open items for Asad

- [x] Obtain GHP 1977 (in hand 13 Nov 2026) and record its validity ranges (done).
- [x] Confirm GHP's carbon range covers 0.63 wt% (yes) and whether its silicon range covers 2.05 wt% (no: tested to 0.85).
- [ ] Digitize Fig. 7 and Figs. 11 to 17 at fixed contents per element, recording the end of each drawn curve (x_max). Two independent passes: Asad from a 300 dpi scan with WebPlotDigitizer, and a second pass from the PDF. Report the largest and mean difference between passes in HV, per chart, at least for Fig. 7 and the Cr curves at 1000 to 1300 °F; then check each curve by overlay. Digitized files carry a header naming the paper and figure, and stating they are digitized values (M18).
- [ ] Choose rule H or E for the BO arms (section 3, step 1), before the preregistration. Gate A uses both.
- [ ] Obtain the full ASTM A255-20a (the preview stops before the calculation tables). If it cannot be obtained, step 6 of the hardenability rule applies.
- [x] NIMS bar and specimen sizes for the structural steels (NRIM SR-93-02, 15 Nov 2026). Spring steels: awaiting sheets 59, 60, 63.
- [ ] Source H values for water and oil quenching and the bar-position to Jominy-distance chart.
- [ ] Source the hardness-reduction rule for a steel not fully hardened (step 3).
- [ ] Check the σw ≈ 1.6 HV relation in Murakami directly.
