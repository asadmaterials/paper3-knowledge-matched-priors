"""Clean the NIMS fatigue data and assign each row a processing route.

Encoding in the source file: a heat-treatment step that was not performed has
its temperature set to 30 (room temperature, degC) and its time and cooling
rate set to 0.

Routes (from which steps are present):
  N  : normalized only (THT == 30 and CT == 30)
  QT : normalized, through-hardened, quenched and tempered (THT > 30)
  C  : normalized, carburized, quenched and tempered (CT > 30)

Usage: python -m data.clean_nims   (from the repo root)
"""
import pathlib

import numpy as np
import pandas as pd

from data.sentinels import step_flags

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


STEEL_KEY = COMPOSITION + ["NT", "THT", "THt", "THQCr", "CT", "Ct", "DT", "Dt", "QmT"]


def assign_steel(df: pd.DataFrame) -> pd.Series:
    """One id per steel: same composition and pre-temper processing.

    Rows of one steel differ only in tempering. Use steel_id to resample
    steels, not rows, in any bootstrap.
    """
    return df.groupby(STEEL_KEY, sort=False).ngroup().rename("steel_id")


def check_qt(df: pd.DataFrame) -> None:
    """Facts the QT-pool design relies on. Fail loudly if the data change."""
    qt = df[df["route"] == "QT"]
    if len(qt) != 378:
        raise SystemExit(f"QT pool has {len(qt)} rows, expected 378")
    if not (qt["Tt"] == 60).all():
        raise SystemExit("Tempering time is not 60 min for every QT row")
    if not step_flags(qt)["tempering_done"].all():
        raise SystemExit("A QT row has no tempering step")
    if qt["steel_id"].nunique() != 132:
        raise SystemExit("QT pool is not 132 steels")
    if df["steel_id"].nunique() != 179:
        raise SystemExit("Full pool is not 179 steels")
    if qt.duplicated(["steel_id", "TT"]).any():
        raise SystemExit("A QT steel appears twice at one tempering temperature")


# Steels (heats) per grade in the QT pool, from NRIM SR-93-02 Table 1
# (Nishijima 1993) for the structural steels; spring-steel counts are
# inferred from composition until NIMS sheets 59, 60 and 63 arrive.
GRADE_COUNTS = {
    "S35C": 12, "S45C": 11, "S55C": 11, "SMn438/443": 19, "SCr440": 8,
    "SCM435/440": 29, "SNC631": 10, "SNCM439": 14, "SNCM447": 6,
    "SUP7": 3, "SUP9A": 3, "SUP12": 6,
}
WATER_QUENCH_GRADE = {865: "S35C", 845: "S45C", 825: "S55C"}  # THT, degC

# SNCM447 Mo is 0.00 in the source file, a coding error: NRIM SR-93-02
# Table 2 gives 0.17 to 0.21 wt% (ladle analysis). Midpoint used until
# per-heat values arrive from NIMS (sheet 26). See DECISION_LOG entry 9.
SNCM447_MO = 0.19


def assign_grade(df: pd.DataFrame) -> pd.Series:
    """JIS grade of each QT row, from composition and processing (inputs only).

    SMn438/SMn443 and SCM435/SCM440 overlap in carbon and are not split.
    Rows outside the QT route get the route name.
    """
    def one(r: pd.Series) -> str:
        if r["route"] != "QT":
            return {"N": "S25C", "C": "carburizing"}[r["route"]]
        if r["Si"] >= 1.2:
            return "SUP7" if r["Cr"] < 0.3 else "SUP12"
        if r["THQCr"] == 24:
            return WATER_QUENCH_GRADE[r["THT"]]
        if r["Cr"] >= 0.6 and r["Mn"] >= 0.65 and r["C"] >= 0.5:
            return "SUP9A"
        if r["Ni"] > 2.0:
            return "SNC631"
        if r["Ni"] > 1.3:
            # Carbon separates the grades (SNCM439 0.37 to 0.43, SNCM447
            # 0.44 to 0.49 in this file); Mo is not used, as it gets corrected.
            return "SNCM447" if r["C"] >= 0.44 else "SNCM439"
        if r["Mn"] >= 1.2:
            return "SMn438/443"
        if r["Mo"] >= 0.1:
            return "SCM435/440"
        return "SCr440"
    return df.apply(one, axis=1).rename("grade")


def check_grades(df: pd.DataFrame) -> None:
    qt = df[df["route"] == "QT"]
    got = qt.groupby("grade")["steel_id"].nunique().to_dict()
    if got != GRADE_COUNTS:
        raise SystemExit(f"Grade counts {got} differ from {GRADE_COUNTS}")


def correct_mo(df: pd.DataFrame) -> pd.DataFrame:
    """Replace the SNCM447 Mo coding error; flag the imputed rows."""
    df = df.copy()
    fix = df["grade"] == "SNCM447"
    if not (df.loc[fix, "Mo"] == 0).all():
        raise SystemExit("SNCM447 Mo is no longer 0; recheck the correction")
    df["mo_imputed"] = fix
    df.loc[fix, "Mo"] = SNCM447_MO
    return df


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
    df["steel_id"] = assign_steel(df)
    check_qt(df)
    df["grade"] = assign_grade(df)
    check_grades(df)
    df = correct_mo(df)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cols = (["row_id", "steel_id", "route", "grade"] + COMPOSITION + PROCESS
            + ["mo_imputed", TARGET])
    df[cols].to_csv(OUT, index=False)
    print(f"Wrote {OUT}: {len(df)} rows")
    print(df["route"].value_counts().to_string())


if __name__ == "__main__":
    main()
