#!/usr/bin/env python3
"""Build the self-contained Reasoner viewer in one step.
Injects the shared house CSS and the viewer data into viewer_template.html and
writes scenario-bank/viewer.html. Run AFTER build_viewer_data.py.

Usage: python3 analysis/build_viewer.py
Env:   REASONER_ROOT overrides the scenario-bank project root.
"""
import os
from pathlib import Path
SB = Path(os.environ.get("REASONER_ROOT", Path(__file__).resolve().parents[1]))  # scenario-bank
ROOT = SB  # ClaudeStuff (holds shared/)
tpl = (SB / "analysis" / "viewer_template.html").read_text()
css = (ROOT / "shared" / "styles" / "reasoner-viewer.css").read_text()
data = (SB / "results" / "viewer_data.json").read_text()
out = tpl.replace("__CSS__", css).replace("__DATA__", data)
assert "__CSS__" not in out and "__DATA__" not in out, "unfilled placeholder"
dst = SB / "viewer.html"
dst.write_text(out)
print("wrote", dst, round(len(out) / 1e6, 2), "MB")
