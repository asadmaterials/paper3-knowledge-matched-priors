# Decision log

Every design decision, with the date and what had been seen of the QT fatigue targets at the time. The QT targets are also the confirmatory data, so anything learned from them before the preregistration is recorded here.

## Entry 1, 3 Nov 2026: primary pool is QT

- Decision: the 378 QT rows are the confirmatory pool; the full 437-row pool is secondary.
- Reason: every row in the top 1% and top 5% of the full pool is carburized, so the full pool mainly tests route identification.
- Seen on 3 Nov, in the data profiling for this decision: route counts and fatigue ranges per route; Spearman of TT with fatigue on QT (−0.51, reported to Asad in chat on 3 Nov); Spearman of C with fatigue on QT (computed; value not retained); the 10 highest-fatigue QT rows with their composition, through-hardening and tempering conditions; the count of QT rows with Si above 1.0 wt% (12); the QT composition and TT ranges in SPEC section 2.

## Entry 2, 12 Nov 2026: what the QT targets show (review round 2, N1)

Seen, and checked independently in this repo:

- 18 of 378 QT rows are tempered at 500 °C or below (TT 420, 430, 490, 500). They are 18 of the top 19 rows and include all 4 top-1% rows. 12 of the 18 are silicon spring steels (Si ≥ 1.31 wt%, 9 distinct compositions).
- The next tempering temperature is 550 °C, where the maximum fatigue is 638 MPa. The maximum over TT ≥ 550 °C is 643 MPa, at 580 °C.
- Heuristic priors on QT: s = −TT gives ρ = 0.51; s = C·(700 − TT) gives ρ = 0.46. Both pass the original Gate A GO threshold of 0.4.
- With n₀ = 10, P(the initial design contains at least one TT ≤ 500 °C row) = 0.39.
- Within each tempering temperature with 100 rows (550, 600, 650 °C): ρ(Cr, fatigue) ≈ 0.83, ρ(Mo, fatigue) 0.66 to 0.72, ρ(Mn + Ni + Cr + Mo, fatigue) 0.76 to 0.82, ρ(C, fatigue) −0.08 to −0.14. C and total alloy content (Mn + Ni + Cr + Mo, wt%) are anticorrelated: Spearman ρ = −0.42 within the 100-steel cohort at any one of its tempering temperatures, −0.37 at steel level, −0.34 on all QT rows (corrected 12 Nov; first recorded without the subset). Across all six tempering temperatures with at least 20 rows, ρ(C, fatigue) ranges from −0.06 to −0.23.

Consequences:

- Gate A criteria in SPEC section 8 now require the codified prior to beat the heuristic references and to show within-TT skill.
- The within-TT pattern is consistent with a hardenability effect (alloy steels fully hardened, plain carbon steels not) but has not been tested. It may also reflect cleanliness or grade. Any hardenability term must be chosen and sourced on metallurgical grounds, not tuned to these numbers, and this entry must be cited in the paper as prior exposure.

## Entry 3, open: confirmatory pool and initial design

To decide before the preregistration (14 Dec 2026), among:

1. Full QT pool (378 rows), with a TT ≥ 550 °C sensitivity analysis (360 rows).
2. TT ≥ 550 °C as the confirmatory pool.
3. Full QT pool with the initial design stratified by tempering temperature.

Whichever is chosen, report per seed whether D₀ contains a TT ≤ 500 °C row, and break results down by it.

Added 12 Nov (review round 3, R1): the 18 low-temper rows are 12 steels that appear at no tempering temperature of 550 °C or above, a separate sub-campaign from the 100-steel and 20-steel designs. This strengthens option 2: TT ≥ 550 °C is a clean 120-steel design with three tempering temperatures per steel. Whichever option is chosen, report a steel-level success measure as secondary (a hit is any row of a top-k steel), and state in the paper that one query is informative about a steel's other rows.

Added 16 Nov (pool reasons, inputs or targets marked). Option 2 (TT ≥ 550 °C, 120 steels, 360 rows) is recommended by the reviewing chat and by this chat; awaiting Asad's decision:
- (a) clean 120-steel × 3-temperature design (inputs only; R1);
- (b) the 12 low-temper steels are a separate campaign that dominates the top of the QT pool (target-informed; seen 12 Nov, entry 2);
- (c) the low-temper steels are exactly the 12 spring steels (SUP7, SUP9A, SUP12), whose hardenability inputs cannot be sourced without MatNavi access (inputs only; entry 11);
- (d) the spring steels are the only QT steels above GHP's tested Si level, so excluding them removes the Si extension rule from the confirmatory analysis (inputs only).
If option 2 is chosen, the full QT pool (132 steels) is the secondary analysis, with spring-steel hardenability "not applicable (inputs not sourced)". The top-1% and top-5% thresholds of the 360-row pool are computed only after the decision, and that computation is logged as target exposure of the endpoint thresholds.

## Entry 4, 12 Nov 2026: THQCr in the LLM arms

- Decision: both LLM arms (A3, A4) receive THQCr as a unitless code ("cooling-rate code 8" or "24"), since its unit is not stated in any source found and it varies in the QT pool. Omitting it would give the GP an input the LLM arms lack.
- Reversible until the preregistration. The exact prompt string will live in `llm/prompts/` so the preregistration can point to it.
- Added 15 Nov (review round 7, R15): the wording for the spring steels (SUP7, SUP9A, SUP12), "oil quench", is provisional. If sheets 59, 60 and 63 show another medium, the wording changes for all arms; before the preregistration this is an update, after it a reported deviation.
- Updated 12 Nov (review round 4, R6): all arms get the same wording for THQCr. Until the NIMS sheets confirm what it encodes, the LLM arms see "cooling-rate code 8" or "24" and the codified prior does not use it. If the sheets confirm a quench medium, every arm sees that medium by name (for example "oil quench", "water quench"), and the codified prior may use it for quench severity.

## Entry 5, 12 Nov 2026: unequal exposure to the targets (review round 3, R2)

- The designer of the codified prior has now seen QT target statistics (entries 1 and 2), including that Cr and Mo drive fatigue within a tempering temperature. The LLM arms have not. This could favour the codified prior (A2) over the LLM arms (A3, A4).
- Mitigations: the hardenability rule family and its source are written into SPEC section 3 before any codified-prior correlation is computed; the non-NIMS validation (SPEC section 8.1) is the main evidence that the rule is right; in the paper, the Gate A correlations are described as unblinded, only the BO comparison is confirmatory, and this exposure and its likely direction are stated.

## Entry 6, 12 Nov 2026: THQCr and steel type (inputs only, review round 4, R6)

- Seen, from inputs only (no target values): THQCr is constant within every QT steel. Of the 132 QT steels, all 34 with THQCr = 24 are plain carbon (Cr < 0.3, Mo < 0.05 and Ni < 0.3 wt%); THQCr = 8 covers 76 alloy steels and 22 plain-carbon steels.
- Hypothesis, not confirmed: 24 and 8 encode water and oil quenching, matching common practice. To be checked against the NIMS fatigue data sheets.
- Closed 15 Nov 2026: confirmed for the structural steels by NRIM SR-93-02 Table 3 (entry 8).
- Adds no exposure to the targets.

## Entry 7, 13 Nov 2026: grades, source ranges and SNCM447 molybdenum (inputs only)

- Seen, from inputs only (no target values): the inferred JIS grade of each QT steel (data/DATA_CARD.md); THQCr = 24 in exactly the 34 plain-carbon S-C steels and 8 in all 98 alloy and spring steels; the 6 SNCM447 steels have Mo = 0.00; counts of QT steels above the GHP tested composition levels (Si 9, Ni 30, Cr 75; 79 steels in all) and outside the A255 calculation range (40 steels).
- Verified from the original GHP paper: the method is graphical (Fig. 7 and Figs. 8 to 17), hardness is HV, and the tempering-parameter form in SPEC section 3 is correct.
- Adds no exposure to the targets.

## Entry 8, 15 Nov 2026: NRIM SR-93-02 used for inputs only

- Source: Nishijima, "Basic Fatigue Properties of JIS Steels for Machine Structural Use", NRIM Special Report No. 93-02 (1993), from NIMS MDR. In copyright; the PDF is not committed.
- Read (in review round 6, by the reviewing chat, and again on 15 Nov 2026 in this repo's working chat to check it): PDF pages 5 to 9 only, printed pp. 2 to 6: Tables 1 to 3, sections 1 to 2.4, Figs. 1 and 2. The fatigue-result figures (printed p. 9 onwards) were not opened by either reader, and are not to be opened before Gate A.
- Taken from it: heat counts per grade (Table 1); SNCM447 Mo 0.17 to 0.21 wt% (Table 2); quench medium, hardening and tempering temperatures and cooling (Table 3); bar diameters 19 to 22 mm, heat treatment of about 200 mm bar pieces in salt baths, austenitic grain size number about 8 to 10, and the metallography of S35C, S45C, SMn438 and SMn443 (section 2.2); rotating-bending specimen with 8 mm test-section diameter (Fig. 2a).
- Cross-checked against the data file (inputs only): the water-quench hardening temperatures 865, 845 and 825 °C split the carbon steels 12, 11 and 11, matching the Table 1 heat counts; all other grade counts match. One discrepancy, confirmed on rereading: SNC631 is quenched from 850 °C in Table 3 but recorded as 845 °C in the file. All other NT and THT values match Table 3. File value kept (see data card).
- Consequence for entry 4: the quench medium is confirmed for the structural steels, so all arms see "water quench" or "oil quench" by name (`data/sentinels.py`, `QUENCH_MEDIUM`), and the codified prior may use quench severity. The spring steels are assumed oil-quenched (code 8) pending their sheets.
- The metallography is a microstructure observation, not fatigue data, but it does say which steels are likely softer at depth. It is used only as the pre-stated check and fallback in SPEC section 3 (hardenability, steps 5 and 6).
- Adds no exposure to the targets.

## Entry 9, 15 Nov 2026: SNCM447 molybdenum corrected for all arms

- The 6 SNCM447 steels (18 rows) have Mo = 0.00 in the source file; NRIM SR-93-02 Table 2 gives 0.17 to 0.21 wt%. Corrected in `clean_nims.py` to 0.19 (midpoint), flagged in column `mo_imputed`, before any arm uses the data, so every arm sees the same value.
- Per-heat values requested from NIMS (sheet 26, email to datasht@nims.go.jp). If they arrive before the preregistration, they replace the midpoint; after it, the change is reported as a deviation.
- The correction raises the codified prior for these steels, since GHP's Mo increment is largest at high tempering temperatures (580 to 680 °C here). Decided without reference to any target value.

## Entry 10, 15 Nov 2026: no NIMS strength data before Gate A (adopted 15 Nov, review round 7, R13)

- NRIM SR-93-02 section 2.3.1 says Vickers hardness (196 N) was measured on the Charpy specimens of every material condition, so the NIMS data sheets almost certainly carry hardness per heat and tempering temperature. Not seen.
- With σw ≈ 1.6 HV, measured hardness is close to a proxy for the target. Looking at it would be exposure to the targets in all but name, and would make an excellent but unblinded check of GHP step 1.
- Rule (adopted): no NIMS measured hardness, tensile strength, proof stress, elongation, impact energy or other mechanical-property data, from the data sheets or from NRIM SR-93-02 beyond PDF page 9, is opened before Gate A. Fatigue limit is about 0.5 times tensile strength, so strength is at least as target-adjacent as hardness. The independent check of GHP step 1 uses non-NIMS published tempering data (SPEC section 8.1). After Gate A, these data may be used for diagnosis, reported as post hoc.
- Reading protocol for NIMS data sheets before Gate A (sheets 26, 59, 60, 63 and any other): read only the material, chemical composition, heat-treatment and specimen sections. Do not view any results table or figure. Record in this log, as a new entry, the sheet, the pages read and what was taken from them, as in entry 8. If a page mixes inputs and results, record that and what was visible.

## Entry 11, 16 Nov 2026: NIMS data sheets unavailable

- NIMS will not supply data sheets by email; MatNavi needs a DICE account with a registered institutional email domain (ID Workflow guide). Sheets 59, 60, 63 (SUP7, SUP9A, SUP12) and 26 (SNCM447 per-heat Mo) are unavailable for now.
- Consequences: SNCM447 keeps Mo = 0.19 (entry 9); spring-steel hardenability is "not applicable (inputs not sourced)" (SPEC section 3, step 4(a)); the spring steels' "oil quench" wording stays provisional (entry 4). Every structural steel's inputs are sourced from NRIM SR-93-02.
- Route if needed later: an HMC email address, with HMC registering its domain with DICE.

## Entry 12, 16 Nov 2026: published expectation about high-Cr steels, recorded before any codified-prior correlation

- Source, read in text 16 Nov 2026: Athavale and Van Aken (2017), Paper I of Athavale's dissertation (2019). Above 482 °C their GHP-based hybrid "had difficulty predicting hardness for steels with greater than 0.5 mass% chromium"; at 593 °C it over-estimated the tempered hardness of SAE 4142 (Q too large, D too small); above 538 °C predicted hardness exceeded measured hardness in general. GHP's own prediction for SAE 6145 (0.92% Cr) erred by up to 7 HRC at 649 °C (GHP Fig. 20). The authors conclude that predicting tempering response from chemistry alone "may not be possible, since contribution to hardening from each element may not be additive". GHP tested Cr only from 0.10 to 0.63%.
- QT steels concerned (inputs only): 47 of the 100 main-cohort steels have Cr > 0.5% (SCM 29, SNC631 10, SCr440 8), tempered at 550 to 650 °C; the 20 SNCM steels (Cr 0.68 to 0.96%) are tempered at 580 to 680 °C.
- Expectation, stated now: the codified prior's absolute hardness, and so its σw, will be least accurate, most likely too high, for these steels at these temperatures. This is a statement about accuracy. It does not predict the within-TT criterion's result, because a uniform overestimate for the Cr steels changes their rank against the other steels only if it differs between steels; and since entry 2 already shows that Cr steels have higher fatigue within a tempering temperature, an overestimate for them would not by itself lower the rank correlation. The stronger reading proposed in review ("weakest where Gate A tests it") is therefore not adopted as a prediction.
- Pre-stated report: within-TT ρ separately for Cr ≤ 0.5 and Cr > 0.5 (SPEC section 8.5).

## Entry 13, 16 Nov 2026: composition check against NRIM SR-93-02 Table 2 (inputs only)

- Every structural QT steel's composition was compared with the tested-material ranges (ladle analysis) in Table 2, with a tolerance of 0.005 wt%. 48 values in 42 steels fall outside, nearly all by 0.01 to 0.08 wt%, consistent with the file holding check or product analyses rather than the report's ladle analyses.
- One clear outlier: steel 37 (S55C) has Mn 0.37 wt%, against 0.67 to 0.84 tested and a JIS minimum of 0.60. Probably a data error, but there is no source for the true value without data sheet 4. Kept as is for all arms; the codified prior is reported with this steel's Mn set to the S55C median as a sensitivity check. Mn affects both the GHP increment and the A255 hardenability of this water-quenched steel.

