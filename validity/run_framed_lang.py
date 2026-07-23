#!/usr/bin/env python3
"""In-language society framing: administer an official-translation MFQ-2 with the
country framing GIVEN IN THAT LANGUAGE, plus a neutral in-language condition.

Mirrors run_framed.py's protocol exactly (same seeds base, shuffle, parse, resume,
output schema + a 'language'/'condition' field). The framed system prompts below are
OUR translations of run_framed.frame_system (disclosed as such); items/anchors/scale
prompt come from the official translation files. Neutral condition = empty system
prompt, in-language items — the control that separates answering-in-Arabic from
answering-as-an-Egyptian.

  python3 validity/run_framed_lang.py --plan
  python3 validity/run_framed_lang.py            # runs everything not yet done
"""
import argparse, glob, json, os, random, sys, time
from pathlib import Path

VDIR = Path(__file__).resolve().parent
sys.path.insert(0, str(VDIR))
import run_validity as rv
rr = rv.rr

OUT = VDIR / "runs_framed_lang"

# (instrument, language, country, framed system prompt in that language)
CELLS = [
    ("mfq2_ar", "arabic", "Egypt",
     "أنت تُكمل استبيانًا للتقييم الذاتي بصفتك شخصًا عاديًا نموذجيًا يعيش في مصر. "
     "أجب عن كل بند كما يجيب شخص مصري نموذجي عن نفسه، بما يعكس النظرة الأخلاقية والقيم "
     "الشائعة في مصر، لا آراءك أنت. قيِّم كل بند مرقّم بعدد صحيح واحد على المقياس الخاص به. "
     "أجب عن جميع البنود. Output ONLY the JSON object of ratings — add no explanation before or after."),
    ("mfq2_ja", "japanese", "Japan",
     "あなたは日本に住むごく普通の典型的な人として自己報告式の質問票に回答しています。"
     "各項目に、日本の代表的な人が自分自身について答えるように回答してください。あなた自身の意見ではなく、"
     "日本で一般的な道徳観や価値観を反映させてください。番号付きの各項目を、その尺度上の整数1つで評価してください。"
     "すべての項目に回答してください。Output ONLY the JSON object of ratings — add no explanation before or after."),
    ("mfq2_fa", "farsi", "Iran",
     "شما در حال تکمیل یک پرسشنامه خودگزارشی به عنوان یک فرد عادی و معمولی ساکن ایران هستید. "
     "به هر عبارت همان‌طور پاسخ دهید که یک فرد معمولی و نماینده از ایران درباره خودش پاسخ می‌دهد، "
     "به گونه‌ای که نگرش اخلاقی و ارزش‌های رایج در ایران را بازتاب دهد، نه نظرات شخصی شما را. "
     "هر عبارت شماره‌دار را با یک عدد صحیح روی مقیاس مربوط ارزیابی کنید. به همه عبارت‌ها پاسخ دهید. "
     "Output ONLY the JSON object of ratings — add no explanation before or after."),
]
NEUTRAL_SYSTEM = ""  # pilot-matched neutral: no system prompt at all

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="")
    ap.add_argument("--iters", type=int, default=5)
    ap.add_argument("--plan", action="store_true")
    a = ap.parse_args()

    panel = rr.REG.get("_decisions", {}).get("pilot_roster") or list(rr.REG["models"])
    models = a.models.split(",") if a.models else panel
    bad = [m for m in models if m not in rr.REG["models"]]
    if bad: sys.exit(f"unknown model(s): {bad}")

    conds = []
    for (instr_name, lang, country, sys_prompt) in CELLS:
        conds.append((instr_name, lang, "framed", country, sys_prompt))
        conds.append((instr_name, lang, "neutral", None, NEUTRAL_SYSTEM))

    planned = [(m, c, it) for m in models for c in range(len(conds)) for it in range(1, a.iters + 1)]
    OUT.mkdir(parents=True, exist_ok=True)
    done = set()
    for f in glob.glob(str(OUT / "*.json")):
        d = json.load(open(f))
        if d.get("ratings"):
            done.add((d["model"], d["instrument"], d["condition"], d["iter"]))
    todo = [(m, ci, it) for (m, ci, it) in planned
            if (m, conds[ci][0], conds[ci][2], it) not in done]
    print(f"panel={len(models)} conds={len(conds)} iters={a.iters} "
          f"planned={len(planned)} done={len(planned)-len(todo)} to_run={len(todo)}")
    if a.plan:
        for i,(n,l,cond,c,_) in enumerate(conds):
            print(f"  cond{i}: {n} {cond}" + (f" as {c}" if c else ""))
        return

    instrs = {}
    for (instr_name, *_ ) in CELLS:
        instr, missing = rv.load_instrument(instr_name)
        if missing: sys.exit(f"[{instr_name}] {len(missing)} empty items")
        instrs[instr_name] = instr
    for key in {rr.REG["models"][m]["env_key"] for m in models}:
        if not os.environ.get(key): sys.exit(f"missing env key {key}; aborting before spend")

    for (m, ci, it) in todo:
        instr_name, lang, cond, country, sys_prompt = conds[ci]
        instr = instrs[instr_name]
        bounds = {x["id"]: (instr["scales"][x["scale"]]["min"], instr["scales"][x["scale"]]["max"])
                  for x in instr["items"]}
        cfg = rr.REG["models"][m]
        seed = 20260722 + it
        rng = random.Random(f"{m}|{instr_name}|{cond}|{it}")
        order = list(instr["items"]); rng.shuffle(order)
        user, id_by_num = rv.build_prompt(instr, order)
        rid = f"{m}_{instr_name}_{cond}_{it}"
        try:
            text, usage = rr.call_model(cfg, sys_prompt, user, rid, seed)
        except Exception as e:
            print(f"  ! {rid}: call failed: {e}"); continue
        ratings, err = rv.parse_ratings(text, id_by_num, bounds)
        ts = time.strftime("%Y%m%dT%H%M%S")
        out = {"model": m, "instrument": instr_name, "language": lang, "condition": cond,
               "country": country, "iter": it, "seed": seed,
               "presentation_order": [id_by_num[str(i+1)] for i in range(len(id_by_num))],
               "ratings": ratings, "parse_error": err, "usage": usage, "raw_text": text,
               "framing_translation": "ours (AI-assisted), disclosed; items/anchors official"}
        (OUT / f"{m}_{instr_name}_{cond}_{it}_{ts}.json").write_text(json.dumps(out, indent=2))
        print(f"  {rid}: {'OK' if ratings else 'PARSE-FAIL: ' + str(err)}")

if __name__ == "__main__":
    main()
