# Knowledge-matched priors for LLM-guided steel optimization

Paper 3 of the research line on reliable LLM-guided materials optimization. The study asks whether an explicit, validated metallurgical prior gives the same Bayesian-optimization speed-up as an LLM-derived prior on the NIMS steel fatigue data.

## Layout

```
data/       download, cleaning, data card (raw files are not committed)
prior/      codified prior: frozen spec, implementation, tests, validation
llm/        prompts, schema, elicitation scripts, cached scores and formulas
bo/         BO loop, prior interface, arm configs
analysis/   estimand, bootstrap, figures
prereg/     preregistration and frozen config
env/        pinned requirements
```

## Reproduce the data

```
pip install -r env/requirements.txt
python -m data.fetch_nims
python -m data.clean_nims
```

Run all scripts from the repo root with `python -m`, so that `data`, `prior`, `llm`, `bo` and `analysis` import as packages. Requirements use lower bounds for now; exact versions are pinned at the preregistration freeze.

## Status

- Week 1 (3 to 9 Nov 2026): data obtained, checksummed, cleaned; data card written.
- 3 Nov 2026: primary pool set to the 378 QT rows (all top-1% and top-5% rows of the full pool are carburized). Codified prior spec v0.1 drafted in `prior/SPEC.md`; coefficients pending the original GHP 1977 source.
- 12 Nov 2026: review rounds 1 and 2 addressed; spec v0.2 (direct GHP table lookup at 1 h, plateau instead of cap, Gate A against heuristic references and within-TT skill); decision log started in `prior/DECISION_LOG.md`.
- 16 Nov 2026: confirmatory pool set to the 360 QT rows tempered at 550 °C or above (120 steels, column `confirmatory`); the 378 QT rows are secondary.
- 17 Nov 2026: hardenability and fatigue-relation sources checked (A255-10, E140-12b, ASM Vol. 4, Lamont charts, Murakami); grain size 7, quench severity ranges, Lamont interpolation, HRC 20 rule and linear σw = 1.6 HV recorded (DECISION_LOG entry 15).
- 17 Nov 2026: Cr extension rule H for the BO arms, initial design from 10 distinct steels, and four LLM models (Claude Opus 5.5, GPT-6.1 Sol, gpt-oss-120b, gpt-oss-20b) recorded (DECISION_LOG entry 16).
- 17 Nov 2026: GHP 1977 Fig. 7 and Figs. 11 to 17 digitized, pass C (Claude): `prior/digitized/pass_claude/`, scripts and reading notes in `prior/digitize/`. Pass A (WebPlotDigitizer) pending.
- 23 Nov 2026: pass A (WebPlotDigitizer) of Fig. 7 at 1000 to 1300 °F and Figs. 14 to 17 added and compared with pass C (largest difference 2.0 HV); Fig. 17 patch readings and the low-content rule recorded (DECISION_LOG entry 17).
- 25 Nov 2026: combined GHP curves (mean of passes A and C, single pass flagged) in `prior/digitized/combined/`; low-content rule, rule H for every element, Cu = 0 and the secondary-pool second pass recorded (DECISION_LOG entry 17).
- 25 Nov 2026: Crafts and Lamont D and f (dissertation reproductions) and Lamont r/R = 0 and 0.5 charts (Totten vector paths) digitized, pass C; pass A pending.
