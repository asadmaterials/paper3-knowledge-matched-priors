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
| Through hardening | THT, THt, THQCr | °C, min, quench code (24 = water quench, 8 = oil quench; NRIM SR-93-02 Table 3) |
| Carburizing | CT, Ct, DT, Dt, QmT | °C, min, °C, min, °C |
| Tempering | TT, Tt, TCr | °C, min, cooling code (24 = water cooled after tempering, for the QT steels; NRIM SR-93-02 Table 3) |
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

The second design is one grade family: exactly the SNCM439 (14) and SNCM447 (6) steels, all with Ni 1.62 to 1.92 wt%, above GHP's tested nickel level, so this cohort depends entirely on the nickel extension in the prior (SPEC section 3).
| Low-temper steels | 12 | 6 at 420 and 490, or 430 and 500; 6 at 430 or 500 alone | 18 |

- The 12 low-temper steels appear at no tempering temperature of 550 °C or above. They include the 9 silicon spring-steel compositions (12 rows).
- No steel appears twice at one tempering temperature.
- Consequences: any interval on a correlation or BO outcome resamples steels (effective n about 132), not rows; within-TT correlations in the main design are the same 100 steels measured three times; in BO, querying one row is informative about the steel's other rows.

## JIS grades and NIMS data sheets (inferred 13 Nov 2026, confirmed 15 Nov 2026)

The file has no grade label. Grades are assigned in `clean_nims.py` (column `grade`) from composition and processing, inputs only, and matched to the room-temperature data sheets in the NIMS catalogue (Furuya et al., Sci. Technol. Adv. Mater. 20 (2019) 1055, Table 1). For the structural steels the assignment is confirmed by NRIM SR-93-02 (Nishijima 1993), Table 1: the heat counts per grade match exactly (S35C 12, S45C 11, S55C 11, SMn 19, SCr440 8, SCM 29, SNC631 10, SNCM439 14, SNCM447 6), and the water-quench hardening temperatures (865, 845 and 825 °C) separate S35C, S45C and S55C. One steel is one heat. SMn438/SMn443 and SCM435/SCM440 overlap in carbon and are not split. Spring-steel grades remain inferred until sheets 59, 60 and 63 arrive.

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

THQCr = 24 occurs in exactly the plain-carbon S-C grades and THQCr = 8 in every alloy and spring grade. NRIM SR-93-02 Table 3 confirms water quenching for S35C, S45C and S55C and oil quenching for the alloy grades. For the spring steels (also code 8), oil quenching is likely but awaits their sheets.

Checked against NRIM SR-93-02 Table 3 on 15 Nov 2026: every normalizing temperature (NT) and hardening temperature (THT) in this file matches the report, except SNC631, which the report quenches from 850 °C and this file records as 845 °C for all 10 steels. The file value is kept, since the prior does not use THT and the GP effect of 5 °C is negligible; to check against data sheet 24 when available.

Table 1 notes that a few SNCM439 heats were supplied as bars of about 50 mm and hot rolled to size at NRIM; which heats is not stated. All bars were 19 to 22 mm (SMn 19 to 23, SNCM447 19 to 20) when cut into 200 mm pieces for heat treatment.

## Suspected missing values coded as 0

- **Mo in SNCM447 (corrected):** the 6 SNCM447 steels all have Mo = 0.00 in the source file. NRIM SR-93-02 Table 2 gives 0.17 to 0.21 wt% for the heats tested, so this is a coding error. `clean_nims.py` sets Mo = 0.19 (the midpoint) for these 18 rows and flags them in column `mo_imputed`; every arm sees the corrected value. Per-heat values have been requested from NIMS (sheet 26) and will replace the midpoint if they arrive (DECISION_LOG entry 9).
- **Mo in other grades:** 76 QT steels and all 11 normalized steels have Mo = 0. For S-C, SMn, SCr440 and SNC631, NRIM SR-93-02 lists Mo as "—" (not specified), so 0 means "not reported", not a measured zero. Kept as 0. The LLM arms will see "Mo 0.00", which is how such grades are usually reported.

## Differences from the published description

- The paper describes 25 features. This copy has 21. The four absent are RedRatio (reduction ratio, ingot to bar) and the inclusion area fractions dA (deformed by plastic work), dB (discontinuous arrays) and dC (isolated), per Table 1 as reproduced in Kookalani et al. (ISARC 2025). No arm sees them, so they create no input asymmetry between arms. If Additional file 1 becomes the source of record, this must be revisited.
- The paper says missing-step temperatures were set to the austenitization temperature or a mean value. This copy uses 30 instead. Treat this copy as a re-encoding of the original file.
- The GitHub README describes composition as "atomic fraction". The values match wt% (for example C 0.17 to 0.63), as the paper states.
- The paper reports 371 carbon and low-alloy, 48 carburizing and 18 spring steels. The file has no grade label. The 48 carburized rows match; 12 QT rows have Si above 1.0 wt%, consistent with silicon spring steels, but the 18 spring steels cannot be identified exactly.

## Open items

- [ ] Download Additional file 1 from the journal page by hand and diff it against this copy column by column (names, units, values, row order, skip encoding), and record the result here.
- [x] Meaning of THQCr and TCr in the QT pool: confirmed 15 Nov 2026 (THQCr 24 = water quench, 8 = oil quench; TCr 24 = water cooled after tempering). All arms now see the quench medium by name (DECISION_LOG entries 4 and 8). The values 0.5 for TCr and 0 elsewhere occur only outside the QT pool and remain unexplained.
- [ ] Confirm redistribution terms for the NIMS-derived data. Check first whether Additional file 1 is covered by the article's CC BY 2.0 licence; if so, redistribution with attribution may already be allowed, independent of the NIMS MatNavi terms for the underlying sheets. Until confirmed, data/raw/ and data/processed/ stay out of git; only the fetch script, checksum and this card are published.

## Design implication (see README)

The top 1% and top 5% of the full pool are all carburized rows. On the full pool, the task largely reduces to identifying route C.
