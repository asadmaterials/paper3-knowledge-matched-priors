"""Download the NIMS steel fatigue dataset (GitHub copy) and verify its checksum.

Source: https://github.com/qq-shu/Fatigue-Dataset (commit a2e3d7e, Dec 2020),
a copy of the dataset released with Agrawal et al., Integrating Materials and
Manufacturing Innovation 3, 8 (2014), doi:10.1186/2193-9772-3-8 (CC BY 2.0).

Usage: python data/fetch_nims.py
"""
import hashlib
import pathlib
import urllib.request

URL = ("https://raw.githubusercontent.com/qq-shu/Fatigue-Dataset/"
       "a2e3d7e2a7634f8733ddedf56b758b9e8636accd/Fatigue-Dataset.csv")
SHA256 = "b7438823ff6c03686d894e5d9e40cd4021abb30119599fdeac423e8f8e91fda4"
OUT = pathlib.Path(__file__).parent / "raw" / "Fatigue-Dataset.csv"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if not OUT.exists():
        urllib.request.urlretrieve(URL, OUT)
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    if digest != SHA256:
        raise SystemExit(f"Checksum mismatch: {digest} != {SHA256}")
    print(f"OK {OUT} sha256={digest}")


if __name__ == "__main__":
    main()
