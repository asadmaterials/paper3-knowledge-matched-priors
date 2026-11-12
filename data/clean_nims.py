"""Clean the NIMS fatigue data and assign each row a processing route.

Encoding in the source file: a heat-treatment step that was not performed has
its temperature set to 30 (room temperature, degC) and its time and cooling
rate set to 0.

Routes (from which steps are present):
  N  : normalized only (THT == 30 and CT == 30)
  QT : normalized, through-hardened, quenched and tempered (THT > 30)
  C  : normalized, carburized, quenched and tempered (CT > 30)

Usage: python data/clean_nims.py
"""
import pathlib

import numpy as np
import pandas as pd

from sentinels import step_flags

HERE = pathlib.Path(__file__).parent
RAW = HERE / "raw" / "Fatigue-Dataset.csv"
OUT = HERE / "processed" / "nims_fatigue_clean.csv"

COMPOSITION = ["C", "Si", "Mn", "P", "S", "Ni", "Cr", "Cu", "Mo"]  # wt%
PROCESS = ["NT", "THT", "THt", "THQCr", "CT", "Ct", "DT", "Dt", "QmT",
           "TT", "Tt", "TCr"]
TARGET = "Fatigue"  # rotating-bending fatigue strength at 1e7 cycles, MPa


def load() -> pd.DataFrame:
    df = pd.read_csv(RAW, encoding="utf-8-sig")
    expected = set(COMPOSITION + PROCESS + [TARGET])
    if set(df.columns) != expected:
        raise SystemExit(f"Unexpected columns: {sorted(set(df.columns) ^ expected)}")
    return df


def assign_route(df: pd.DataFrame) -> pd.Series:
    flags = step_flags(df)  # also checks the skip codes are consistent
    carburized = flags["carburizing_done"]
    hardened = flags["through_hardening_done"]
    if (carburized & hardened).any():
        raise SystemExit("Row is both carburized and through-hardened")
    return pd.Series(np.where(carburized, "C", np.where(hardened, "QT", "N")),
                     index=df.index, name="route")


def check_qt(df: pd.DataFrame) -> None:
    """Facts the QT-pool design relies on. Fail loudly if the data change."""
    qt = df[df["route"] == "QT"]
    if len(qt) != 378:
        raise SystemExit(f"QT pool has {len(qt)} rows, expected 378")
    if not (qt["Tt"] == 60).all():
        raise SystemExit("Tempering time is not 60 min for every QT row")
    if not step_flags(qt)["tempering_done"].all():
        raise SystemExit("A QT row has no tempering step")


def main() -> None:
    df = load()
    if df.isna().any().any():
        raise SystemExit("Missing values found")
    feats = COMPOSITION + PROCESS
    n_dup = int(df.duplicated(subset=feats).sum())
    if n_dup:
        raise SystemExit(f"{n_dup} duplicate input rows; decide merge rule first")
    df = df.copy()
    df.insert(0, "row_id", np.arange(len(df)))
    df["route"] = assign_route(df)
    check_qt(df)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df[["row_id", "route"] + COMPOSITION + PROCESS + [TARGET]].to_csv(OUT, index=False)
    print(f"Wrote {OUT}: {len(df)} rows")
    print(df["route"].value_counts().to_string())


if __name__ == "__main__":
    main()
