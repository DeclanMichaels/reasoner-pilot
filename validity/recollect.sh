#!/bin/zsh
# Re-collect the whole in-language MFQ-2 study in one window, one protocol.
# Waits out the run already in flight, archives every cell collected before today,
# then re-runs each condition. Archived cells stay on disk as the prior record.
set -u
cd "$HOME/Code/reasoner-pilot" || exit 1
V=validity
STAMP=2026-07
CUT='2026-08-21 10:20'

echo "=== WAITING for the in-flight run to finish, $(date) ==="
while pgrep -f 'run_framed(_lang)?\.py' > /dev/null; do sleep 20; done
echo "=== in-flight run finished $(date) ==="

mkdir -p "$V/archive-$STAMP/runs_framed_lang" "$V/archive-$STAMP/runs_framed" "$V/archive-$STAMP/runs"

echo "=== ARCHIVING pre-today cells ==="
n=0
for f in $V/runs_framed_lang/*.json; do
  [ -e "$f" ] || continue
  if [ -z "$(find "$f" -newermt "$CUT")" ]; then mv "$f" "$V/archive-$STAMP/runs_framed_lang/"; n=$((n+1)); fi
done
echo "  runs_framed_lang: archived $n"
n=0
for f in $V/runs_framed/*.json; do
  [ -e "$f" ] || continue
  if [ -z "$(find "$f" -newermt "$CUT")" ]; then mv "$f" "$V/archive-$STAMP/runs_framed/"; n=$((n+1)); fi
done
echo "  runs_framed: archived $n"
n=0
for f in $V/runs/*_mfq2_*.json; do
  [ -e "$f" ] || continue
  mv "$f" "$V/archive-$STAMP/runs/"; n=$((n+1))
done
echo "  runs (mfq2 only, mfq30 and pvq40 untouched): archived $n"

echo
echo "=== REMAINING in place (collected today, new protocol) ==="
echo "  runs_framed_lang: $(ls $V/runs_framed_lang/*.json 2>/dev/null | wc -l | tr -d ' ')"
echo "  runs_framed:      $(ls $V/runs_framed/*.json 2>/dev/null | wc -l | tr -d ' ')"

echo
echo "=== PLAN, no spend ==="
python3 -u $V/run_framed_lang.py --plan | head -2
python3 -u $V/run_framed.py --countries "Egypt,India,Iran,Japan,Nigeria,Sweden,United States" --count | head -2
python3 -u $V/run_validity.py --instruments mfq2 --count | head -3

echo
echo "=== IN-LANGUAGE $(date) ==="
python3 -u $V/run_framed_lang.py
echo "=== ENGLISH FRAMED $(date) ==="
python3 -u $V/run_framed.py --countries "Egypt,India,Iran,Japan,Nigeria,Sweden,United States"
echo "=== ENGLISH UNFRAMED $(date) ==="
python3 -u $V/run_validity.py --instruments mfq2
echo "=== ALLDONE $(date) ==="
