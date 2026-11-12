# Data card: NIMS steel fatigue dataset

Checked 3 November 2026.

## Source

- File used: `Fatigue-Dataset.csv` from https://github.com/qq-shu/Fatigue-Dataset, commit `a2e3d7e` (21 Dec 2020).
- SHA-256: `b7438823ff6c03686d894e5d9e40cd4021abb30119599fdeac423e8f8e91fda4`
- Original release: Agrawal et al., "Exploration of data science techniques to predict fatigue strength of steel from composition and processing parameters", Integrating Materials and Manufacturing Innovation 3, 8 (2014), doi:10.1186/2193-9772-3-8, Additional file 1. The article is open access under CC BY 2.0.
- Underlying data: NIMS MatNavi fatigue data sheets.

## Contents

437 rows, 21 inputs, 1 target. No empty cells; skipped heat-treatment steps are encoded as 30 (temperatures) or 0 (times and cooling rates), so missingness is present but coded (see "Skipped-step codes"). No duplicate input rows.

| Group | Columns | Units |
| --- | --- | --- |
| Composition | C, Si, Mn, P, S, Ni, Cr, Cu, Mo | wt% |
| Normalizing | NT | °C |
| Through hardening | THT, THt, THQCr | °C, min, cooling rate (unit not stated) |
| Carburizing | CT, Ct, DT, Dt, QmT | °C, min, °C, min, °C |
| Tempering | TT, Tt, TCr | °C, min, cooling rate (unit not stated) |
| Target | Fatigue | MPa, rotating bending, 10^7 cycles |

A step that was not performed has temperature 30 and time and cooling rate 0.

## Skipped-step codes

Rows coded as skipped, per column. The codes are consistent within each step (temperature 30 exactly when time and cooling rate are 0); `data/sentinels.py` checks this.

| Step | Columns | Full pool (437) | QT pool (378) |
| --- | --- | --- | --- |
| Normalizing | NT | 0 | 0 |
| Through hardening | THT, THt, THQCr | 59 | 0 |
| Carburizing | CT, Ct, DT, Dt, QmT | 389 | 378 |
| Tempering | TT, Tt, TCr | 11 | 0 |

Handling rule, used by every arm (`data/sentinels.py`): the codified prior branches on step flags, never on raw temperatures; LLM prompts and LLM-written formulas see a skipped step as "not performed"; the GP drops columns that are constant on the pool and, for steps skipped in only some rows, adds a 0/1 "step performed" flag and fills the code with the median of the performed rows. On the QT pool the carburizing columns, Tt (always 60 min) and TCr (always 24) are constant and are dropped from the GP inputs.

## Processing routes

| Route | Rule | Rows | Fatigue range (MPa) | Carbon (wt%) |
| --- | --- | --- | --- | --- |
| QT: through-hardened, quenched and tempered | THT > 30 | 378 | 325 to 906 | 0.28 to 0.63 |
| C: carburized, quenched and tempered | CT > 30 | 48 | 838 to 1,190 | 0.17 to 0.23 |
| N: normalized only | neither | 11 | 225 to 275 | 0.22 to 0.28 |

Within QT, tempering time is 60 min for every row (zero variance, asserted in `clean_nims.py`), so the tempering parameter varies only through tempering temperature (420 to 680 °C). Through-hardening temperature takes four values (825 to 865 °C).

## Differences from the published description

- The paper describes 25 features. This copy has 21. The four absent are RedRatio (reduction ratio, ingot to bar) and the inclusion area fractions dA (deformed by plastic work), dB (discontinuous arrays) and dC (isolated), per Table 1 as reproduced in Kookalani et al. (ISARC 2025). No arm sees them, so they create no input asymmetry between arms. If Additional file 1 becomes the source of record, this must be revisited.
- The paper says missing-step temperatures were set to the austenitization temperature or a mean value. This copy uses 30 instead. Treat this copy as a re-encoding of the original file.
- The GitHub README describes composition as "atomic fraction". The values match wt% (for example C 0.17 to 0.63), as the paper states.
- The paper reports 371 carbon and low-alloy, 48 carburizing and 18 spring steels. The file has no grade label. The 48 carburized rows match; 12 QT rows have Si above 1.0 wt%, consistent with silicon spring steels, but the 18 spring steels cannot be identified exactly.

## Open items

- [ ] Download Additional file 1 from the journal page by hand and diff it against this copy column by column (names, units, values, row order, skip encoding), and record the result here.
- [ ] Find the units of THQCr and TCr (values 0, 8, 24 and 0, 0.5, 24). Until found, decide one rule for both LLM arms: omit the columns, or pass them as a unitless code. In the QT pool only THQCr varies (8 or 24).
- [ ] Confirm redistribution terms for the NIMS-derived data. Until confirmed, data/raw/ and data/processed/ stay out of git; only the fetch script, checksum and this card are published.

## Design implication (see README)

The top 1% and top 5% of the full pool are all carburized rows. On the full pool, the task largely reduces to identifying route C.
