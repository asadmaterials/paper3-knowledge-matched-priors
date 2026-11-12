"""One rule for skipped heat-treatment steps, imported by every arm.

In the NIMS file a step that was not performed has its temperature set to 30
and its time and cooling rate set to 0. These values are codes, not
measurements. Every arm must translate them the same way:

- Codified prior: branch from `step_flags`, never from raw temperatures.
- LLM prompts (A3) and LLM-written formulas (A4): pass the step as
  "not performed" via `prompt_value`; never show 30 or 0 for a skipped step.
- GP: use `gp_features`, which drops columns constant on the pool and, for
  columns that are only sometimes skipped, adds a 0/1 "step performed" flag
  and fills the code with the median of the performed rows.
"""
import pandas as pd

SENTINEL_TEMP = 30
SENTINEL_ZERO = 0

# step name -> (temperature column, other columns coded 0 when skipped)
STEPS = {
    "normalizing": ("NT", []),
    "through_hardening": ("THT", ["THt", "THQCr"]),
    "carburizing": ("CT", ["Ct", "DT", "Dt", "QmT"]),
    "tempering": ("TT", ["Tt", "TCr"]),
}
# DT and QmT are temperatures, so their skip code is 30, not 0.
_TEMP_COLS = {"NT", "THT", "CT", "DT", "QmT", "TT"}


def _skip_code(col: str) -> int:
    return SENTINEL_TEMP if col in _TEMP_COLS else SENTINEL_ZERO


def step_flags(df: pd.DataFrame) -> pd.DataFrame:
    """True where the step was performed. Checks the code is consistent."""
    out = {}
    for step, (tcol, others) in STEPS.items():
        skipped = df[tcol] == SENTINEL_TEMP
        for c in others:
            if not ((df[c] == _skip_code(c)) == skipped).all():
                raise ValueError(f"Inconsistent skip code: {tcol} vs {c}")
        out[f"{step}_done"] = ~skipped
    return pd.DataFrame(out, index=df.index)


def step_columns(step: str) -> list[str]:
    tcol, others = STEPS[step]
    return [tcol] + others


def prompt_value(df: pd.DataFrame, row: int, col: str) -> str:
    """Value of `col` for an LLM prompt, with skipped steps as 'not performed'."""
    for step, (tcol, others) in STEPS.items():
        if col == tcol or col in others:
            if df.at[row, tcol] == SENTINEL_TEMP:
                return "not performed"
    return str(df.at[row, col])


def gp_features(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """GP input matrix for the given pool, before [0, 1] scaling."""
    flags = step_flags(df)
    feats = {}
    for c in cols:
        step = next((s for s, (t, o) in STEPS.items() if c == t or c in o), None)
        x = df[c].astype(float)
        if step is not None:
            done = flags[f"{step}_done"]
            if not done.any():
                continue                      # step never performed in pool
            if not done.all():
                x = x.where(done, x[done].median())
                feats[f"{step}_done"] = done.astype(float)
        if x.nunique() > 1:
            feats[c] = x
    return pd.DataFrame(feats, index=df.index).loc[:, lambda d: ~d.columns.duplicated()]
