#!/usr/bin/env python3
"""Build per-language mfq2_<code>.filled.json instruments from the official OSF
translations. Structure-clones the English mfq2.filled.json (ids, groups, scales,
score block) and swaps in the translated item text, scale anchors, and scale
prompt. Item n maps to id by the official cycle (care,equality,proportionality,
loyalty,authority,purity), independently confirmed by the Farsi file's scoring
block. The output-format instruction stays English (plumbing, not instrument).
Run from reasoner-pilot/validity/:  python3 build_lang_instruments.py
"""
import json, re
from pathlib import Path

VDIR = Path(__file__).resolve().parent
EXTRACTED = VDIR / "instruments" / "mfq2_translations_extracted.json"
BASE = VDIR / "instruments" / "mfq2.filled.json"
CODES = {"english":"en","arabic":"ar","japanese":"ja","chinese":"zh","french":"fr",
         "spanish":"es","russian":"ru","farsi":"fa"}
CYCLE = ["care","equality","proportionality","loyalty","authority","purity"]

base = json.load(open(BASE))
tr = json.load(open(EXTRACTED))

# scale label -> anchor number: labels carry (1)..(5) or Persian digit prefix
PDIG = str.maketrans("۰۱۲۳۴۵۶۷۸۹","0123456789")
def anchor_num(label):
    m = re.search(r"\((\d)\)", label)
    if m: return m.group(1)
    m = re.match(r"^([۰-۹\d])\s*[–\-)]", label.translate(PDIG).translate(PDIG))
    lab = label.translate(PDIG)
    m = re.match(r"^(\d)", lab)
    return m.group(1)
def anchor_text(label):
    lab = re.sub(r"\(\d\)", "", label)
    lab = re.sub(r"^[\d۰-۹]\s*[–\-)]\s*", "", lab.strip())
    return lab.strip()

for lang, code in CODES.items():
    t = tr[lang]
    out = json.loads(json.dumps(base))
    out["instrument"] = f"mfq2_{code}"
    out["source"] = (f"Official {lang} translation, Atari et al. 2023 supplemental "
                     f"materials (osf.io/srtxn), file: {t['source_file']}")
    out["fill_note"] = ("Item text, scale anchors, and scale prompt are the official "
                        "translation verbatim; ids/groups/score cloned from mfq2. "
                        "Output-format instruction remains English (plumbing).")
    anchors = {}
    for lab in t["scale_labels"]:
        anchors[anchor_num(lab)] = anchor_text(lab)
    assert sorted(anchors) == ["1","2","3","4","5"], (lang, anchors)
    out["scales"]["main"]["anchors"] = anchors
    out["scales"]["main"]["prompt"] = t["instruction"]
    counts = {g: 0 for g in CYCLE}
    for i, item in enumerate(t["items"]):
        g = CYCLE[i % 6]; counts[g] += 1
        iid = f"{g}_{counts[g]}"
        match = [x for x in out["items"] if x["id"] == iid]
        assert len(match) == 1, (lang, iid)
        match[0]["text"] = item["text"]
    assert all(c == 6 for c in counts.values()), (lang, counts)
    dest = VDIR / "instruments" / f"mfq2_{code}.filled.json"
    json.dump(out, open(dest, "w"), ensure_ascii=False, indent=2)
    print("wrote", dest.name, "| anchors ok | 36 items")
print("done")
