#!/bin/zsh
# Fill every gap left by rate limits, parse failures, and the kimi outage.
# Waits out whatever is running, then re-invokes each runner until it reports
# nothing left to do. The runners are resumable and key on completed cells, so a
# pass only spends on what is actually missing.
set -u
cd "$HOME/Code/reasoner-pilot" || exit 1
V=validity
MAXPASS=8
PAUSE=90

echo "=== WAITING for the current job, $(date) ==="
while pgrep -f 'run_framed(_lang)?\.py|run_validity\.py' > /dev/null; do sleep 20; done
echo "=== clear, starting fill $(date) ==="

remaining() {  # $1 = the plan/count command
  eval "$1" 2>/dev/null | grep -oE 'to_run=[0-9]+' | head -1 | cut -d= -f2
}

fill() {  # $1 label, $2 plan cmd, $3 run cmd
  local label=$1 plan=$2 run=$3 pass=1 left
  while (( pass <= MAXPASS )); do
    left=$(remaining "$plan")
    [[ -z "$left" ]] && left=unknown
    echo "--- $label pass $pass: to_run=$left  $(date +%H:%M:%S)"
    [[ "$left" == "0" ]] && { echo "--- $label COMPLETE"; return 0; }
    eval "$run"
    pass=$((pass+1))
    sleep $PAUSE
  done
  echo "--- $label STOPPED after $MAXPASS passes, to_run=$(remaining "$plan")"
}

fill "in-language" \
     "python3 -u $V/run_framed_lang.py --plan" \
     "python3 -u $V/run_framed_lang.py"

fill "english-framed" \
     "python3 -u $V/run_framed.py --countries 'Egypt,India,Iran,Japan,Nigeria,Sweden,United States,Morocco,Saudi Arabia,United Arab Emirates,Argentina,Chile,Colombia,Mexico,Peru,France,Belgium,Switzerland,Russia' --count" \
     "python3 -u $V/run_framed.py --countries 'Egypt,India,Iran,Japan,Nigeria,Sweden,United States,Morocco,Saudi Arabia,United Arab Emirates,Argentina,Chile,Colombia,Mexico,Peru,France,Belgium,Switzerland,Russia'"

fill "english-unframed" \
     "python3 -u $V/run_validity.py --instruments mfq2 --count" \
     "python3 -u $V/run_validity.py --instruments mfq2"

echo "=== FILL DONE $(date) ==="
python3 - <<'PY'
import json, glob
from collections import Counter
def rep(pat, keyf, label, target=55):
    c, m = Counter(), {}
    for f in glob.glob(pat):
        d = json.load(open(f))
        if not d.get("ratings"): continue
        k = keyf(d); c[k] += 1; m.setdefault(k, set()).add(d["model"])
    print(label)
    for k in sorted(c, key=str):
        flag = "" if (c[k] == target and len(m[k]) == 11) else "   <-- INCOMPLETE"
        print(f"  {str(k):<42} {c[k]:>3}/{target}  models {len(m[k]):>2}/11{flag}")
rep("validity/runs_framed_lang/*.json",
    lambda d: (d["instrument"], d.get("country") or "-"), "IN-LANGUAGE")
rep("validity/runs_framed/*_mfq2_*.json", lambda d: d["country"], "ENGLISH FRAMED")
rep("validity/runs/*_mfq2_*.json", lambda d: "en_unframed", "ENGLISH UNFRAMED")
PY
