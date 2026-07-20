#!/usr/bin/env python3
"""Generate instrument scaffolds (MFQ-30, MFQ-2, PVQ-40) with EMPTY item-text slots.

This file encodes ONLY structure and scoring keys — not the item wording. The
official items are proprietary research instruments (free for research use, but
not redistributed here): paste them into the empty "text" fields locally before
running, per validity/README.md. The runner refuses to run on any empty item.

Run: python3 validity/build_instruments.py   ->  validity/instruments/*.json
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "instruments"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------- MFQ-30 (Graham et al. 2011) ----------------
mfq30_found = ["care", "fairness", "loyalty", "authority", "sanctity"]
items = []
for f in mfq30_found:
    for k in range(3):
        items.append({"id": f"{f}_p1_{k+1}", "group": f, "scale": "part1", "catch": False, "text": ""})
    for k in range(3):
        items.append({"id": f"{f}_p2_{k+1}", "group": f, "scale": "part2", "catch": False, "text": ""})
items.append({"id": "catch_p1", "group": "_catch", "scale": "part1", "catch": True, "text": ""})
items.append({"id": "catch_p2", "group": "_catch", "scale": "part2", "catch": True, "text": ""})
mfq30 = {
    "instrument": "MFQ-30",
    "citation": "Graham, J., Nosek, B. A., Haidt, J., Iyer, R., Koleva, S., & Ditto, P. H. (2011). Mapping the moral domain. JPSP, 101(2), 366-385.",
    "source": "https://moralfoundations.org/questionnaires/ (MFQ30.item-key.doc + MFQ30.self-scorable.doc). Free for research/non-commercial use.",
    "fill_note": ("Paste OFFICIAL wording into each empty text. Per foundation: three "
                  "relevance items (part1) then three agreement items (part2), matching the "
                  "official item key. Fill both catch items. VERIFY every item's foundation "
                  "and part against MFQ30.item-key.doc. Do NOT commit filled items."),
    "scales": {
        "part1": {"prompt": "Part 1. When you decide whether something is right or wrong, to what extent are the following considerations relevant to your thinking? Rate each from 0 to 5.",
                  "min": 0, "max": 5,
                  "anchors": {"0": "not at all relevant", "1": "not very relevant", "2": "slightly relevant",
                              "3": "somewhat relevant", "4": "very relevant", "5": "extremely relevant"}},
        "part2": {"prompt": "Part 2. Read each statement and indicate your agreement. Rate each from 0 to 5.",
                  "min": 0, "max": 5,
                  "anchors": {"0": "strongly disagree", "1": "moderately disagree", "2": "slightly disagree",
                              "3": "slightly agree", "4": "moderately agree", "5": "strongly agree"}},
    },
    "items": items,
    "score": {"foundations": mfq30_found,
              "composites": {"individualizing": ["care", "fairness"], "binding": ["loyalty", "authority", "sanctity"]},
              "method": "mean", "exclude_catch": True},
}

# ---------------- MFQ-2 (Atari, Haidt, Graham et al. 2023) ----------------
mfq2_found = ["care", "equality", "proportionality", "loyalty", "authority", "purity"]
items2 = [{"id": f"{f}_{k+1}", "group": f, "scale": "main", "catch": False, "text": ""}
          for f in mfq2_found for k in range(6)]
mfq2 = {
    "instrument": "MFQ-2",
    "citation": "Atari, M., Haidt, J., Graham, J., et al. (2023). Morality beyond the WEIRD. JPSP, 125(5), 1157-1188 (MFQ-2).",
    "source": "moralfoundations.org and the Atari et al. (2023) OSF supplement. Free for research use.",
    "fill_note": ("Paste OFFICIAL MFQ-2 wording (six items per foundation). VERIFY each item's "
                  "foundation against the official MFQ-2 key. Do NOT commit filled items."),
    "scales": {"main": {"prompt": "For each statement, indicate how well it describes you. Rate each from 1 to 5.",
                        "min": 1, "max": 5,
                        "anchors": {"1": "does not describe me at all", "2": "slightly describes me",
                                    "3": "moderately describes me", "4": "describes me fairly well",
                                    "5": "describes me extremely well"}}},
    "items": items2,
    "score": {"foundations": mfq2_found, "composites": {}, "method": "mean", "exclude_catch": False},
}

# ---------------- PVQ-40 (Schwartz Portrait Values Questionnaire) ----------------
pvq_vals = ["conformity", "tradition", "benevolence", "universalism", "self_direction",
            "stimulation", "hedonism", "achievement", "power", "security"]
items3 = [{"id": f"{v}_{k+1}", "group": v, "scale": "main", "catch": False, "text": ""}
          for v in pvq_vals for k in range(4)]
pvq40 = {
    "instrument": "PVQ-40",
    "citation": "Schwartz, S. H. (2003/2005). Portrait Values Questionnaire (PVQ-40). See Schwartz (1992); ESS PVQ-21 short form.",
    "source": "Schwartz PVQ-40 official portraits + value key (obtain from Schwartz materials / ESS documentation). Free for research use.",
    "fill_note": ("Paste the OFFICIAL 40 portraits (four per value). The portraits use gendered "
                  "phrasing ('he'/'she'); for LLM administration pick ONE variant and use it "
                  "consistently. VERIFY each item's value against the official key. Do NOT commit filled items."),
    "scales": {"main": {"prompt": "Here are short descriptions of people. For each, how much is this person like you? Rate each from 1 to 6.",
                        "min": 1, "max": 6,
                        "anchors": {"1": "not like me at all", "2": "not like me", "3": "a little like me",
                                    "4": "somewhat like me", "5": "like me", "6": "very much like me"}}},
    "items": items3,
    "score": {"values": pvq_vals,
              "higher_order": {"openness_to_change": ["self_direction", "stimulation", "hedonism"],
                               "self_enhancement": ["achievement", "power", "hedonism"],
                               "conservation": ["security", "conformity", "tradition"],
                               "self_transcendence": ["universalism", "benevolence"]},
              "method": "ipsative_mean"},
}

for name, obj in [("mfq30", mfq30), ("mfq2", mfq2), ("pvq40", pvq40)]:
    p = OUT / f"{name}.json"
    p.write_text(json.dumps(obj, indent=2))
    print(f"wrote {p.name}: {len(obj['items'])} item slots")
