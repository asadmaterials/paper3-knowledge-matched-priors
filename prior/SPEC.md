# Codified metallurgical prior: specification v0.2 (draft)

Status: draft v0.2, 3 November 2026, updated 12 November 2026. To be frozen before Gate A (30 November 2026). No coefficient may be coded until its row in the source table below is marked "verified against original". Every change after 12 November is recorded in `prior/DECISION_LOG.md`, with what had been seen of the QT targets at the time.

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

GHP estimate the hardness of tempered martensite as a carbon-dependent base hardness plus additive increments for each alloying element, tabulated for 1 h tempers at fixed temperatures (reported as 204 to 704 °C, which covers the QT range of 420 to 680 °C; to confirm from the original).

**Primary rule:** because every QT row is tempered for exactly 1 h, the prior reads the GHP tables directly at the row's tempering temperature, interpolating linearly in temperature between tabulated steps. The tempering parameter is not needed for the QT pool. This avoids the unresolved discrepancy in the secondary source (section 4).

**Cross-check only:** the GHP tempering parameter, as reproduced in secondary sources, is:

```latex
P = (T_{F} + 460)\,(18 + \log_{10} t_{h}) \times 10^{-3}
```

with T_F the tempering temperature in °F and t_h the time in hours. For the QT pool, t_h = 1, so P = (T_F + 460) × 0.018.

```latex
HV_T = HV_{base}(C, P) + \sum_{i} \Delta HV_i(P)\, x_i
```

with x_i the wt% of element i (Mn, Si, Ni, Cr, Mo, P and any others GHP give).

**Coefficients: not yet transcribed.** The base-hardness curve and the ΔHV table must be taken from the original paper (Metallurgical Transactions A 8, 1775 to 1785, 1977) or from a handbook that reproduces it with attribution. They will not be reconstructed from memory or secondary summaries.

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

1. **Ideal critical diameter** D_I, by the Grossmann multiplying-factor method as standardized in ASTM A255 (Standard Test Methods for Determining Hardenability of Steel): D_I = D_I,base(C, austenite grain size) × Π f_i(x_i), over the elements A255 tabulates (Mn, Si, Ni, Cr, Mo, Cu as available). Factors to be transcribed from the A255 tables; grain size to be taken from the NIMS data sheets, or else assumed at one value for all rows (proposed: ASTM grain size 7, typical of fine-grained, aluminium-killed steels of these grades; the value and its justifying source are fixed here before any codified-prior correlation).
2. **Section check at the test surface:** rotating-bending fatigue is controlled by the specimen surface, so the check is made at the depth of the fatigue specimen's test-section surface within the heat-treated blank, not at the bar centre. Inputs from the NIMS sheets: the blank diameter at heat treatment (were blanks treated before or after rough machining?) and the final test-section diameter. Grossmann D_I is defined for 50% martensite at the centre of a round bar, so the rule needs a relation from D_I to hardness at that depth. Source: ASTM A255 itself, which converts D_I into a calculated Jominy curve using its distance hardness dividing factors (table numbers to confirm from the standard), so steps 1 and 2 share one source. The remaining link, from a bar position under quench severity H to an equivalent Jominy distance, is taken from a cited handbook chart. Quench severity H: from the quench medium on the NIMS sheets. THQCr is a candidate (DECISION_LOG entry 6: code 24 occurs only in plain-carbon steels, consistent with water against oil) but is used only if the NIMS sheets confirm what it encodes.
3. **Effect on hardness:** a steel judged not fully hardened gets a lower as-quenched hardness before tempering. The reduction rule (for example, the hardness at the expected martensite fraction from a cited relation) is to be sourced, not fitted.
4. **Not applicable, decided before computing any correlation**, in either of two cases: (a) the blank size, test-section depth or quench medium cannot be sourced (grain size may be assumed, per step 1); or (b) with sourced inputs, the rule judges every QT steel fully hardened at the test surface by the criterion in step 3, so it cannot change any steel's hardness. In both cases the prior runs without it (full martensite assumed), and the paper says which case applied.

## 4. Sources

| Relation | Source | Status |
| --- | --- | --- |
| GHP tempering parameter P = (T_F + 460)(18 + log t_h) × 10⁻³ | Grange, Hribal and Porter, Metall. Trans. A 8 (1977) 1775 | Form seen in a secondary source (Politecnico di Torino thesis); verify against original. The thesis's own worked values do not reproduce exactly: 1 h at 950 °F gives 25.38 by this formula, not the 26.23 it reports. |
| GHP base hardness HV_base(C, P) | Same | To obtain |
| GHP alloy increments ΔHV_i(P) | Same | To obtain |
| GHP validity ranges (C, each element, P) | Same | To obtain |
| σw ≈ 1.6 HV, valid to about 400 to 500 HV | Murakami, Metal Fatigue (Elsevier); Garwood, Zurburg and Erickson (1951), as reviewed in Metals 12 (2022) 1066 | Confirmed in the review; verify in Murakami |

## 5. Why the affine calibration matters

In the BO comparison, every prior enters as m(x) = a + b·s(x), with a and b fitted on the initial design (see the research plan). The factor 1.6 and any constant offset in HV are therefore absorbed by b and a. What the BO arms test is the shape and ranking of s(x) across the pool. Absolute accuracy matters only for the independent validation in section 8.

## 6. Known limitations of v0.2

- **Hardenability (now a likely core issue, see DECISION_LOG entry 2).** GHP assume full martensite before tempering. Low-hardenability plain-carbon steels quenched as bars may not reach full martensite, so the prior will overestimate their hardness. Within each tempering temperature in the QT pool, fatigue rises with Cr and Mo and falls slightly with C. A carbon-dominated GHP prior with no hardenability term may therefore rank rows wrongly within a tempering temperature. The rule family is now fixed in section 3 (hardenability rule); its inputs and factors must be sourced before Gate A, not tuned to the QT targets.
- **Silicon spring steels.** The 12 rows with Si of 1.31 wt% or more may fall outside the GHP silicon range. They are among the strongest rows in the QT pool (fatigue up to 906 MPa), so how they are handled affects the top of the ranking.
- **Inclusions and upstream processing.** The fatigue relation ignores inclusion size, which the source says controls fatigue at high hardness. Inclusion data exist in the original file but not in this copy.
- **High-carbon rows.** 51 rows have C above 0.5 wt%. Whether they are inside the GHP carbon range is to be checked.

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

## 9. Open items for Asad

- [ ] Obtain GHP 1977, or a handbook reproduction with attribution, and transcribe the base-hardness curve, the ΔHV table and the validity ranges.
- [ ] Confirm whether GHP's carbon range covers 0.63 wt% and whether its silicon range covers 2.05 wt%.
- [ ] Look up the NIMS specimen and bar sizes, to decide whether a hardenability correction is needed.
- [ ] Check the σw ≈ 1.6 HV relation in Murakami directly.
