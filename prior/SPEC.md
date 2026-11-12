# Codified metallurgical prior: specification v0.1 (draft)

Status: draft, 3 November 2026. To be frozen before Gate A (30 November 2026). No coefficient may be coded until its row in the source table below is marked "verified against original".

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

GHP estimate the hardness of tempered martensite as a carbon-dependent base hardness plus additive increments for each alloying element, both functions of the tempering parameter. Their parameter, as reproduced in secondary sources, is:

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
- Hardness above 450 HV: σw is computed as written, and the row is flagged. The count of flagged rows is reported. (Threshold within the 400 to 500 HV range of the source; to be fixed when the hardness range of the pool is known.)
- Composition outside the GHP validity ranges: inputs are clipped to the edge of the range and the row is flagged. Counts are reported per element.
- Through-hardening temperature and THQCr are not used in v0.1 (full martensite is assumed). See section 6.

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

## 6. Known limitations of v0.1

- **Hardenability.** GHP assume full martensite before tempering. Low-hardenability plain-carbon steels quenched as bars may not reach full martensite, so the prior will overestimate their hardness. A hardenability correction (for example, an ideal-critical-diameter check against specimen size) is a candidate for v0.2, if the NIMS specimen and bar sizes can be found.
- **Silicon spring steels.** The 12 rows with Si of 1.31 wt% or more may fall outside the GHP silicon range. They are among the strongest rows in the QT pool (fatigue up to 906 MPa), so how they are handled affects the top of the ranking.
- **Inclusions and upstream processing.** The fatigue relation ignores inclusion size, which the source says controls fatigue at high hardness. Inclusion data exist in the original file but not in this copy.
- **High-carbon rows.** 51 rows have C above 0.5 wt%. Whether they are inside the GHP carbon range is to be checked.

## 7. Secondary branches (full-pool analysis only)

- **C (carburized, 48 rows):** case hardness after a low-temperature temper (TT 160 to 200 °C) from an assumed case carbon level, then σw from the case. Specification deferred until the QT branch passes Gate A.
- **N (normalized only, 11 rows):** ferrite-pearlite hardness from composition, then σw ≈ 1.6 HV. Candidate relation: the ferrite-pearlite equation in Ion and Anisdahl, attributed to Maynier; verify against the original before use.

## 8. Validation plan (before Gate A)

1. **Independent check of step 1:** compare GHP predictions with published hardness of tempered steels not from NIMS (for example, handbook tempering curves for 1045, 4140 and 4340 after a 1 h temper). Report error in HV.
2. **Independent check of step 2:** compare 1.6 HV with published fatigue limits and hardness pairs from sources other than NIMS.
3. **NIMS QT prior quality:** Spearman ρ between the unfitted prior and measured fatigue, overall, within each tempering temperature, and with the spring-steel rows excluded. Counts reported for every subset.
4. **Gate A thresholds** (from the research plan): ρ ≥ 0.4 GO; 0.2 to 0.4 adjust; below 0.2 reframe.

## 9. Open items for Asad

- [ ] Obtain GHP 1977, or a handbook reproduction with attribution, and transcribe the base-hardness curve, the ΔHV table and the validity ranges.
- [ ] Confirm whether GHP's carbon range covers 0.63 wt% and whether its silicon range covers 2.05 wt%.
- [ ] Look up the NIMS specimen and bar sizes, to decide whether a hardenability correction is needed.
- [ ] Check the σw ≈ 1.6 HV relation in Murakami directly.
