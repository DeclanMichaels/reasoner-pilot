#!/usr/bin/env python3
"""Build the self-contained CMRB viewer in one step.
Injects the shared house CSS and the viewer data into viewer_template.html and
writes scenario-bank/cmrb_viewer.html. Run AFTER build_viewer_data.py.

Usage: python3 private/viz/build_viewer.py
Env:   CMRB_ROOT overrides the scenario-bank project root.
"""
import os
from pathlib import Path
SB = Path(os.environ.get("CMRB_ROOT", Path(__file__).resolve().parents[2]))  # scenario-bank
ROOT = SB.parent  # ClaudeStuff (holds shared/)
tpl = (SB / "private" / "viz" / "viewer_template.html").read_text()
css = (ROOT / "shared" / "styles" / "ccas-viewer.css").read_text()
data = (SB / "private" / "reanalysis" / "viewer_data.json").read_text()
out = tpl.replace("__CSS__", css).replace("__DATA__", data)
assert "__CSS__" not in out and "__DATA__" not in out, "unfilled placeholder"
dst = SB / "cmrb_viewer.html"
dst.write_text(out)
print("wrote", dst, round(len(out) / 1e6, 2), "MB")
