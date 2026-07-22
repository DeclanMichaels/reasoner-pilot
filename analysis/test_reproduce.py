#!/usr/bin/env python3
"""Characterization / reproducibility test for the Reasoner pilot analysis.

Re-runs each analysis script and verifies its outputs are byte-for-byte identical
to the published values recorded in reproduce_manifest.json (sha256). This PINS the
pilot's numbers: any change to analysis code or data that alters a published output
fails here. No API keys or network needed (pure stdlib analysis of the local runs).

  python3 analysis/test_reproduce.py           # re-run all scripts, then verify
  python3 analysis/test_reproduce.py --check    # verify existing outputs only (fast)

Exit 0 = every output reproduces; nonzero = a mismatch/missing output.
"""
import hashlib, json, os, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("REASONER_ROOT", HERE.parent))
MANIFEST = HERE / "reproduce_manifest.json"
# dependency order: build_viewer needs viewer_data.json to exist first
SCRIPTS = ["build_appendix.py", "build_viewer_data.py", "build_csv.py",
           "build_figures.py", "build_viewer.py"]

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def run_scripts():
    for s in SCRIPTS:
        print(f"  running {s} ...", flush=True)
        r = subprocess.run([sys.executable, str(HERE / s)], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  ERROR running {s}:\n{r.stderr[-1500:]}")
            sys.exit(2)

def verify():
    with open(MANIFEST) as f:
        manifest = json.load(f)
    ok = bad = missing = 0
    for rel, expected in sorted(manifest.items()):
        p = ROOT / rel
        if not p.exists():
            print(f"  MISSING  {rel}"); missing += 1; continue
        got = sha256(p)
        if got == expected:
            ok += 1
        else:
            print(f"  MISMATCH {rel}\n    expected {expected}\n    got      {got}"); bad += 1
    print(f"\n{ok} reproduced, {bad} mismatched, {missing} missing (of {len(manifest)})")
    return bad == 0 and missing == 0

if __name__ == "__main__":
    check_only = "--check" in sys.argv
    if not check_only:
        print("re-running analysis scripts (no API keys / no network) ...")
        run_scripts()
    print("verifying outputs against reproduce_manifest.json ...")
    ok = verify()
    print("PASS: pilot outputs reproduce exactly." if ok else "FAIL: outputs drifted.")
    sys.exit(0 if ok else 1)
