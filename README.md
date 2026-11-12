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
