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

## Entry 3, decided 16 Nov 2026: confirmatory pool and initial design

**Decision (Asad, 16 Nov 2026): option 2.** The confirmatory pool is TT ≥ 550 °C (120 steels, 360 rows; column `confirmatory` in the cleaned data, asserted in `clean_nims.py`). The full QT pool (132 steels, 378 rows) is the secondary analysis, with spring-steel hardenability "not applicable (inputs not sourced)". Reasons (a) to (d) below; (b) is target-informed, (a), (c) and (d) are from inputs only. The initial-design choice (stratified or not) is still open. Decided 17 Nov 2026: not stratified, 10 distinct steels (entry 16).

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
- Also not opened before Gate A (added 17 Nov 2026, review round 8, M23): Murakami, *Metal Fatigue*, 2nd ed., Fig. 1.7 (Nishijima 1980, hardness against fatigue limit for NRIM normalized and QT steels), which is NIMS fatigue data. Not viewed.
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

## Entry 14, 16 Nov 2026: endpoint thresholds on the confirmatory pool (target exposure, logged)

- Computed after the decision in entry 3, and only these quantities: for the 360-row pool, top 1% = ceil(0.01 × 360) = 4 rows, threshold 634 MPa, next value below 631 MPa; top 5% = ceil(0.05 × 360) = 18 rows, threshold 604 MPa, next value below 603 MPa. No ties at either cutoff. Each top-k set contains one row per steel (4 and 18 steels).
- Rule, fixed now: the top-k set is the k highest rows; if a later data change creates a tie at the cutoff, all tied rows are included and the rule is reported.
- Exposure: these two thresholds and the fact that each set has one row per steel. Nothing else about the targets on this pool was computed.


## Entry 15, 17 Nov 2026: hardenability inputs and the fatigue relation (review round 8; inputs and sources only)

- Sources checked 16 and 17 Nov 2026: ASTM A255-10 (2018), full; A255-20a, 4-page preview; A255-02, superseded; ASTM E140-12b (2019); ASM Handbook Vol. 4 (1991); Totten (2006) section 5.5.1; Murakami, *Metal Fatigue*, 2nd ed. (2019). None is committed to the repo.
- Grain size: 7, as A255-10 section 10.3 assumes. Bias stated: NRIM reports 8 to 10, so D_I is overstated and fewer steels are flagged. Grain size 8 to 10 only as a sensitivity analysis, if sourced carbon factors are obtained.
- A255 validity: 31 of the 120 confirmatory steels are outside the main composition range of section 10.1, within the factor-only ranges of 10.1.1. Computed with the 10.1.1 factors and flagged; sensitivity analysis treats them as fully hardened.
- Below HRC 20: hybrid not applicable where Q, IH or RQ is below HRC 20 (E140 forbids converting outside its range); RT = Q, flagged and counted; extrapolated Eq. (A1.1) as sensitivity analysis.
- Lamont position: equivalent Jominy distance interpolated linearly in r/R between the r/R = 0 and 0.5 charts at each steel's r/R; the two charts alone as bounds.
- Quench severity: water 0.9 to 1.5 (central 1.1), oil 0.25 to 0.5 (central 0.35), from no agitation to good agitation.
- Fatigue relation: σw = 1.6 HV at all hardness, no plateau, described as Murakami's ideal upper bound; flat hold at 640 MPa above 400 HV as a BO sensitivity analysis only. Spearman ρ, and so Gate A, is unchanged by any strictly increasing σw(HV).
- Withdrawn argument: in the 16 Nov source check, the plateau was said to matter little because the confirmatory pool's top row (643 MPa) is about 400 HV. That used a measured target (already logged in entry 2) and is withdrawn as a reason; what matters is the prior's predicted HV, not yet computed. The choice above does not depend on it.
- Exposure: nothing new about the targets was seen. Murakami Fig. 1.7 (NRIM data) was not viewed (entry 10).

## Entry 16, 17 Nov 2026: Cr extension rule, initial design, LLM models (decided by Asad)

**1. Cr extension rule in the BO arms: rule H.** Above the end of the drawn GHP curve x_max(Cr, T), ΔHV_Cr is held at its value at x_max; between GHP's tested level (0.63 wt%) and x_max the chart is read as drawn. Rule E is a sensitivity analysis. Gate A evaluates both, as before (SPEC 8.5).
- Affected: 67 of the 120 confirmatory steels are above 0.63% Cr (47 of the 100 main-design steels and all 20 SNCM steels). How many are above x_max is known only after digitizing.
- Reasons (sources only): GHP give no assurance for extrapolation beyond the curves drawn in their Figs. 8 to 17, and rule H adds nothing they did not draw, while rule E adds a slope they did not measure. Athavale and Van Aken (Athavale, PhD dissertation, Missouri S&T, 2019) report GHP-based predictions that are too high above 538 °C for SAE 4130 and 4142 (0.86% Cr) and 5160 (0.65% Cr). That error is present at or near GHP's tested range, so it is not caused by extrapolation and rule H does not fix it; rule H only avoids adding to it (rule E gives values at least as high as H, since its slope is floored at 0).
- Not used as evidence: GHP Fig. 20 (SAE 6145, 0.92% Cr, errors up to 7 HRC above 538 °C), because GHP attribute that error to undissolved vanadium carbides, and the NIMS steels report no V.
- Not a reason: the within-TT Cr pattern in the targets (entry 2). Disclosure: rule H flattens the ranking among Cr steels, which runs against that pattern, so the choice was not tuned toward the targets.
- Si: no confirmatory steel exceeds GHP's tested Si level (maximum 0.35%); the 9 QT steels above 0.85% are all SUP7 and SUP12. Rule H for Si in the secondary pool, with E as sensitivity. Mn, Mo and C are within GHP's tested levels in the confirmatory pool.

**2. Initial design D₀.** n₀ = 10 rows, drawn uniformly at random subject to coming from 10 distinct steels (`steel_id`), not stratified by TT, shared across all arms for a seed. Sampler: draw 10 rows uniformly without replacement and redraw the whole set if any steel repeats (rejection sampling, uniform over valid sets). On the confirmatory pool every steel has 3 rows, so this equals 10 random steels with 1 random row each; on the secondary pool (1 to 3 rows per steel) the two differ, and the rejection sampler is the rule. Reason (inputs only): with plain random draws, 22.8% of seeds would contain two rows of one steel (1 − Π_{i=0..9} (360 − 3i)/(360 − i)).

**3. LLM models: four, none to be dropped.**

| Role | Model | ID or weights |
| --- | --- | --- |
| Frontier, Anthropic | Claude Opus 5.5 | `claude-opus-5-5` |
| Frontier, OpenAI | GPT-6.1 Sol | `gpt-6.1-sol` |
| Large open weights | gpt-oss-120b | Hugging Face weights, Apache 2.0 |
| Small open weights | gpt-oss-20b | Hugging Face weights, Apache 2.0; replaces the plan's ~8B model |

- Option (a) adopted: both open-weights models from one family, for a clean size comparison. Stated limitation: three of the four models are from OpenAI, so results may not generalize beyond these two vendors.
- Claude Opus 5.5 rather than Fable: Fable access was suspended from 12 June to 1 July 2026 under US export controls, and a preregistered study needs a model that stays reachable for reruns.
- API only, no chat apps; no tools or browsing; identical prompts for every model.
- Sampling: all four are reasoning models. Pre-stated: reasoning effort medium for GPT-6.1 Sol (checked: options low to max, default medium) and for both gpt-oss models; the Claude thinking setting is fixed in the preregistration; temperature is set only where the API allows it. Reproducibility comes from caching every output and from the repeat elicitations, not from temperature 0. (The research plan's "temperature 0" line is to be updated.)
- Version records: GPT-6.1 Sol has no dated snapshots (checked on the OpenAI model page, 17 Nov 2026; knowledge cutoff 30 April 2026), so its run dates are recorded and all elicitations run in a short window. For Claude, the model ID and run dates. For gpt-oss: Hugging Face commit hash, inference engine and version, quantization and hardware. Exact reruns are claimed only for local runs of the open weights; if a hosted provider serves gpt-oss-120b, the provider is recorded and the claim is dropped for that model. Colab's GPU memory is to be checked before planning the 120b there (it needs about 80 GB).
- Memorization: every model's training data postdate 2014, so all four are assumed to have seen the NIMS data; the memorization controls apply to all four.
- Disclosure in the paper: Claude assisted with the code and prompts; no prompt was tuned against model outputs on the targets.

## Entry 17, 23 Nov 2026: digitizing pass A, comparison with pass C, and the Fig. 17 patch (inputs only)

- **Pass A** (Asad, WebPlotDigitizer) received 23 Nov 2026: Fig. 7 at 1000 to 1300 °F and Figs. 14 to 17 (Mn, Si, Cr, Mo, P), stored in `prior/digitized/pass_asad/` with source headers added and values unchanged. The WebPlotDigitizer project files contain the figures and are not committed.
- **Independence disclosure:**
  - Asad saw the pass C overlay PDF and the values quoted in the pass C message before starting pass A.
  - During pass A, the reviewing chat helped with calibration and curve identification, using only the chart images, never the pass C files.
  - Curve identification is therefore not fully independent between the passes. The point readings in pass A are Asad's own.
  - Pass C recorded its own reading of the Fig. 17 patch before opening any pass A file.
- **Comparison** (`prior/digitize/compare.py`, results in `prior/digitized/comparison/`; differences are pass A minus pass C):
  - Fig. 7 at 1000 to 1300 °F: largest difference 1.4 to 2.0 HV, mean +0.1 to +0.6 HV.
  - Cr at 1000 to 1300 °F: largest 0.7 to 1.2 HV, mean −0.3 to +0.1 HV.
  - All 20 element curves: largest 1.8 HV, mean absolute difference 0.1 to 0.6 HV.
  - No curve where the passes followed different lines.
  - Drawn ends agree within 4% of content, except Mn at 1300 °F (pass A 1.20%, pass C 1.10%).
  - The ΔHV at the drawn end, which rule H holds, differs by at most 0.9 HV.
- **Fig. 7 calibration:** the "100" label is printed beside the bottom frame, but 100 HV is the heavy gridline 13 px above it. Both passes use the gridline.
- **Fig. 17 patch:** confirmed as an inverted region, with gridlines and curves white on black.
  - The one steep white mark that pass C read before opening pass A (0.129%, 3.0 HV) matches pass A's Cr within 0.1 HV, assigned to the same curve.
  - The three shallow marks match pass A's Mo within 0.3 HV, but only on a pixel measurement made after opening pass A. Pass C's blind reading by eye was 0.7 to 0.9 HV higher.
  - Decisions:
    - **Cr at 1300 °F:** pass A's patch readings are primary below 0.15%. They agree with the blind pass C mark.
    - **Mo at 1300 °F:** the Mo curve is extended down to 0.113% using the Mo dashes above the patch, which both passes saw. No row needs Mo below 0.113% (Mo in the data is 0 or 0.15 to 0.24%), so the shallow marks inside the patch decide nothing.
    - **Mn and Si inside the patch:** pass A only. No row needs them (Si at least 0.16%, Mn at least 0.37%).
- **Low contents (as stated by Asad, 23 Nov 2026, in the pass A note):** below the first readable point of a curve, ΔHV is a straight line in content from zero at zero content to that point. This applies to P below 0.02% on every chart, Cr at the 1000 to 1300 °F lower ends, and anything below pass A's first patch reading at 1300 °F. As a sensitivity analysis, pass A's patch readings are replaced by this line.
- **Still open:** the rule for combining the two passes into the values the prior uses; and a second pass of Figs. 11 to 13 and of Fig. 7 at 400 to 900 °F, which only the secondary pool needs.
