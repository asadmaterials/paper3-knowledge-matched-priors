# Data card: NIMS steel fatigue dataset

Checked 3 November 2026. Updated 12 November 2026.

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

Handling rule, used by every arm (`data/sentinels.py`): the codified prior branches on step flags, never on raw temperatures; LLM prompts and LLM-written formulas see a skipped step as "not performed"; the GP drops columns that are constant on the pool and, for steps skipped in only some rows, adds a 0/1 "step performed" flag and fills the code with the median of the performed rows. On the QT pool the carburizing columns, THt (always 30 min), Tt (always 60 min) and TCr (always 24) are constant and are dropped from the GP inputs. Note that THt = 30 is a real time of 30 min, not the temperature skip code 30.

## Processing routes

| Route | Rule | Rows | Fatigue range (MPa) | Carbon (wt%) |
| --- | --- | --- | --- | --- |
| QT: through-hardened, quenched and tempered | THT > 30 | 378 | 325 to 906 | 0.28 to 0.63 |
| C: carburized, quenched and tempered | CT > 30 | 48 | 838 to 1,190 | 0.17 to 0.23 |
| N: normalized only | neither | 11 | 225 to 275 | 0.22 to 0.28 |

Within QT, tempering time is 60 min for every row (zero variance, asserted in `clean_nims.py`), so the tempering parameter varies only through tempering temperature (420 to 680 °C). Through-hardening temperature takes four values (825 to 865 °C).

## Steel structure of the QT pool

The 378 QT rows are 132 steels, not 378 independent samples. A steel is one composition with one normalizing, through-hardening and quench condition (`steel_id` in the cleaned file); its rows differ only in tempering temperature. The 132 compositions are all distinct.

| Cohort | Steels | Tempering temperatures (°C) | Rows |
| --- | --- | --- | --- |
| Main design | 100 | 550, 600, 650 | 300 |
| Second design | 20 | 580, 630, 680 | 60 |
| Low-temper steels | 12 | 6 at 420 and 490, or 430 and 500; 6 at 430 or 500 alone | 18 |

- The 12 low-temper steels appear at no tempering temperature of 550 °C or above. They include the 9 silicon spring-steel compositions (12 rows).
- No steel appears twice at one tempering temperature.
- Consequences: any interval on a correlation or BO outcome resamples steels (effective n about 132), not rows; within-TT correlations in the main design are the same 100 steels measured three times; in BO, querying one row is informative about the steel's other rows.

## Likely JIS grades and NIMS data sheets (inferred from composition, 13 Nov 2026)

The file has no grade label. Grades below are inferred from composition and processing (inputs only) and matched to the room-temperature data sheets in the NIMS catalogue (Furuya et al., Sci. Technol. Adv. Mater. 20 (2019) 1055, Table 1). To confirm against the heat lists in the sheets.

| Inferred grade | QT steels | THQCr | TT (°C) | Data sheet No. (DOI 10.11503/nims.…) |
| --- | --- | --- | --- | --- |
| S35C, S45C, S55C (C 0.32 to 0.57) | 34 | 24 | 550/600/650; some 580/630/680 | 2 (1066), 3 (1067), 4 (1068) |
| SCr440 | 8 | 8 | 550/600/650 | 8 (1072) |
| SCM435, SCM440 | 29 | 8 | 550/600/650 | 9 (1073), 10 (1074) |
| SMn438, SMn443 | 19 | 8 | 550/600/650 | 16 (1080), 17 (1081) |
| SNC631 | 10 | 8 | 550/600/650 | 24 (1088) |
| SNCM439 | 14 | 8 | 580/630/680 | 25 (1089) |
| SNCM447 | 6 | 8 | 580/630/680 | 26 (1090) |
| SUP7 (Si-Mn spring) | 3 | 8 | 430 and 500 | 59 (1123) |
| SUP9A (Mn-Cr spring) | 3 | 8 | 420 and 490 | 60 (1124) |
| SUP12 (Si-Cr spring) | 6 | 8 | 430 or 500 | 63 (1127) |

Outside QT: the 11 normalized steels match S25C (sheet 1, DOI 1065); the 36 carburized steels match SCr420, SCM420, SNCM220 and SNCM420 (sheets 37, 43, 50, 51). Sheet 0 (DOI 1064) explains the project, including the common test procedure.

On this inference, THQCr = 24 occurs in exactly the plain-carbon S-C grades and THQCr = 8 in every alloy and spring grade, including the plain-carbon-like SMn and SUP7 grades. This fits water against oil quenching by grade (to confirm from the sheets).

## Suspected missing values coded as 0

- **Mo in SNCM447:** the 6 steels inferred as SNCM447 all have Mo = 0.00, although the grade specifies about 0.15 to 0.30 wt% Mo and the 14 SNCM439 steels have Mo 0.16 to 0.24. Probably not reported, then coded 0. To check against sheet 26.
- **Mo in other grades:** 82 QT steels and all 11 normalized steels have Mo = 0. These are grades with no Mo specification, so 0 may mean "not analysed" rather than measured zero. The effect on any prior is small at residual levels, but the LLM arms will see "Mo 0.00" as a fact.

## Differences from the published description

- The paper describes 25 features. This copy has 21. The four absent are RedRatio (reduction ratio, ingot to bar) and the inclusion area fractions dA (deformed by plastic work), dB (discontinuous arrays) and dC (isolated), per Table 1 as reproduced in Kookalani et al. (ISARC 2025). No arm sees them, so they create no input asymmetry between arms. If Additional file 1 becomes the source of record, this must be revisited.
- The paper says missing-step temperatures were set to the austenitization temperature or a mean value. This copy uses 30 instead. Treat this copy as a re-encoding of the original file.
- The GitHub README describes composition as "atomic fraction". The values match wt% (for example C 0.17 to 0.63), as the paper states.
- The paper reports 371 carbon and low-alloy, 48 carburizing and 18 spring steels. The file has no grade label. The 48 carburized rows match; 12 QT rows have Si above 1.0 wt%, consistent with silicon spring steels, but the 18 spring steels cannot be identified exactly.

## Open items

- [ ] Download Additional file 1 from the journal page by hand and diff it against this copy column by column (names, units, values, row order, skip encoding), and record the result here.
- [ ] Find the units of THQCr and TCr (values 0, 8, 24 and 0, 0.5, 24). Rule decided 12 Nov 2026 (prior/DECISION_LOG.md, entry 4): both LLM arms receive THQCr as a unitless code. In the QT pool only THQCr varies (8 or 24).
- [ ] Confirm redistribution terms for the NIMS-derived data. Check first whether Additional file 1 is covered by the article's CC BY 2.0 licence; if so, redistribution with attribution may already be allowed, independent of the NIMS MatNavi terms for the underlying sheets. Until confirmed, data/raw/ and data/processed/ stay out of git; only the fetch script, checksum and this card are published.

## Design implication (see README)

The top 1% and top 5% of the full pool are all carburized rows. On the full pool, the task largely reduces to identifying route C.
