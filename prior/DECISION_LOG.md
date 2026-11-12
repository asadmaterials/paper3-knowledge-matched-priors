# Decision log

Every design decision, with the date and what had been seen of the QT fatigue targets at the time. The QT targets are also the confirmatory data, so anything learned from them before the preregistration is recorded here.

## Entry 1, 3 Nov 2026: primary pool is QT

- Decision: the 378 QT rows are the confirmatory pool; the full 437-row pool is secondary.
- Reason: every row in the top 1% and top 5% of the full pool is carburized, so the full pool mainly tests route identification.
- Seen: route counts and fatigue ranges per route; Spearman of TT with fatigue on QT (−0.51).

## Entry 2, 12 Nov 2026: what the QT targets show (review round 2, N1)

Seen, and checked independently in this repo:

- 18 of 378 QT rows are tempered at 500 °C or below (TT 420, 430, 490, 500). They are 18 of the top 19 rows and include all 4 top-1% rows. 12 of the 18 are silicon spring steels (Si ≥ 1.31 wt%, 9 distinct compositions).
- The next tempering temperature is 550 °C, where the maximum fatigue is 638 MPa. The maximum over TT ≥ 550 °C is 643 MPa, at 580 °C.
- Heuristic priors on QT: s = −TT gives ρ = 0.51; s = C·(700 − TT) gives ρ = 0.46. Both pass the original Gate A GO threshold of 0.4.
- With n₀ = 10, P(the initial design contains at least one TT ≤ 500 °C row) = 0.39.
- Within each tempering temperature with 100 rows (550, 600, 650 °C): ρ(Cr, fatigue) ≈ 0.83, ρ(Mo, fatigue) 0.66 to 0.72, ρ(Mn + Ni + Cr + Mo, fatigue) 0.76 to 0.82, ρ(C, fatigue) −0.08 to −0.14. C and total alloy content are anticorrelated (ρ = −0.42). Across all six tempering temperatures with at least 20 rows, ρ(C, fatigue) ranges from −0.06 to −0.23.

Consequences:

- Gate A criteria in SPEC section 8 now require the codified prior to beat the heuristic references and to show within-TT skill.
- The within-TT pattern is consistent with a hardenability effect (alloy steels fully hardened, plain carbon steels not) but has not been tested. It may also reflect cleanliness or grade. Any hardenability term must be chosen and sourced on metallurgical grounds, not tuned to these numbers, and this entry must be cited in the paper as prior exposure.

## Entry 3, open: confirmatory pool and initial design

To decide before the preregistration (14 Dec 2026), among:

1. Full QT pool (378 rows), with a TT ≥ 550 °C sensitivity analysis (360 rows).
2. TT ≥ 550 °C as the confirmatory pool.
3. Full QT pool with the initial design stratified by tempering temperature.

Whichever is chosen, report per seed whether D₀ contains a TT ≤ 500 °C row, and break results down by it.

## Entry 4, 12 Nov 2026: THQCr in the LLM arms

- Decision: both LLM arms (A3, A4) receive THQCr as a unitless code ("cooling-rate code 8" or "24"), since its unit is not stated in any source found and it varies in the QT pool. Omitting it would give the GP an input the LLM arms lack.
- Reversible until the preregistration.
