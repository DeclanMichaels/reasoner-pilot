## B1a. Roster and protocol

**The panel.** `models.json` registers 15 models. 11 answered every cell; 4 are absent from every cell for the infrastructural reasons B1 gives. Roster keys are the names used throughout; a swapped model gets its own key (decision 10).

| roster key | provider | model string | in the grid |
|---|---|---|---|
| deepseek_v4 | together | `deepseek-ai/DeepSeek-V4-Pro` | yes |
| gpt55 | openai | `gpt-5.5` | yes |
| grok45 | xai | `grok-4.5` | yes |
| inkling | together | `thinkingmachines/Inkling` | yes |
| kimi_k3 | together | `moonshotai/Kimi-K3` | yes |
| llama33 | together | `meta-llama/Llama-3.3-70B-Instruct-Turbo` | yes |
| minimax | together | `MiniMaxAI/MiniMax-M3` | yes |
| mistral_large | mistral | `mistral-large-2512` | yes |
| o3 | openai | `o3` | yes |
| opus | anthropic | `claude-opus-4-8` | yes |
| sonnet | anthropic | `claude-sonnet-5` | yes |
| command_a | cohere | `command-a-plus-05-2026` | no |
| gemini35flash | google | `gemini-3.5-flash` | no |
| gemini3pro | google | `gemini-3.1-pro-preview` | no |
| kimi | together | `moonshotai/Kimi-K2.6` | no |

**Request.** One user message carrying the questionnaire; the framing instruction, where there is one, as the system prompt; nothing else. Anthropic receives it in the `system` field, OpenAI, xAI, Together and Mistral as a `role: system` message, Google as `systemInstruction`; Google and Cohere are configured and served no cell here. We send a request seed where the provider accepts one (OpenAI, xAI, Together as `seed`, Mistral as `random_seed`); the English framed runner uses 20260721 plus the iteration, the in-language runner 20260722 plus the iteration. Token ceilings are per provider: Anthropic 3072, OpenAI and xAI 4096, Together 6144, Mistral 2048, Google 6144, Cohere 2048. We send no temperature, so each model ran at its provider's default, which the run records do not capture; a pinned value would have documented the setting and would not have made stochasticity equivalent across models. We do not reconstruct the defaults from provider documentation, which is not dated to the collection window and changes.

**The self-report system prompt** of the two `selfreport` baseline variants, English, verbatim from `run_validity.py`:

> You are completing a self-report questionnaire about yourself. Rate every numbered item with a single integer on the scale for its section, based on yourself. Answer every item. Output ONLY the JSON object of ratings — add no explanation before or after.

**The framing instruction**, English, verbatim from `run_framed.py` with the country substituted:

> You are completing a self-report questionnaire AS a typical, ordinary person living in {country}. Answer every item the way a representative person from {country} would answer about themselves — reflecting the moral outlook and values that are common in {country}, not your own. Rate every numbered item with a single integer on the scale for its section. Answer every item. Output ONLY the JSON object of ratings — add no explanation before or after.

The in-language framing instructions are our translations of that template, one per language, AI-assisted and disclosed as such, varying only the country name and the demonym. Each cell records the instruction it was sent verbatim in its `system_prompt` field, and the runner asserts at start-up that the Arabic template still reproduces the Egypt prompt byte for byte as first collected.

**The translated framing instructions**, ours, AI-assisted and disclosed as such, one per language with only the country name and the demonym varying; each is quoted as sent, from the first framed cell of its language, via the collection record.

Arabic, framed as Egypt:

> أنت تُكمل استبيانًا للتقييم الذاتي بصفتك شخصًا عاديًا نموذجيًا يعيش في مصر. أجب عن كل بند كما يجيب شخص مصري نموذجي عن نفسه، بما يعكس النظرة الأخلاقية والقيم الشائعة في مصر، لا آراءك أنت. قيِّم كل بند مرقّم بعدد صحيح واحد على المقياس الخاص به. أجب عن جميع البنود. Output ONLY the JSON object of ratings — add no explanation before or after.

Spanish, framed as Argentina:

> Estás completando un cuestionario de autoevaluación como una persona corriente y típica que vive en Argentina. Responde a cada ítem como respondería sobre sí misma una persona argentina representativa, reflejando la perspectiva moral y los valores comunes en Argentina, no tus propias opiniones. Califica cada ítem numerado con un solo número entero en la escala de su sección. Responde a todos los ítems. Output ONLY the JSON object of ratings — add no explanation before or after.

French, framed as Belgium:

> Vous remplissez un questionnaire d'auto-évaluation en tant que personne ordinaire et typique vivant en Belgique. Répondez à chaque item comme y répondrait à son sujet une personne belge représentative, en reflétant la perspective morale et les valeurs courantes en Belgique, et non vos propres opinions. Évaluez chaque item numéroté par un seul nombre entier sur l'échelle de sa section. Répondez à tous les items. Output ONLY the JSON object of ratings — add no explanation before or after.

Japanese, framed as Japan:

> あなたは日本に住むごく普通の典型的な人として自己報告式の質問票に回答しています。各項目に、日本の代表的な人が自分自身について答えるように回答してください。あなた自身の意見ではなく、日本で一般的な道徳観や価値観を反映させてください。番号付きの各項目を、その尺度上の整数1つで評価してください。すべての項目に回答してください。Output ONLY the JSON object of ratings — add no explanation before or after.

Farsi, framed as Iran:

> شما در حال تکمیل یک پرسشنامه خودگزارشی به عنوان یک فرد عادی و معمولی ساکن ایران هستید. به هر عبارت همان‌طور پاسخ دهید که یک فرد معمولی و نماینده از ایران درباره خودش پاسخ می‌دهد، به گونه‌ای که نگرش اخلاقی و ارزش‌های رایج در ایران را بازتاب دهد، نه نظرات شخصی شما را. هر عبارت شماره‌دار را با یک عدد صحیح روی مقیاس مربوط ارزیابی کنید. به همه عبارت‌ها پاسخ دهید. Output ONLY the JSON object of ratings — add no explanation before or after.

Russian, framed as Russia:

> Вы заполняете опросник самоотчёта как обычный, типичный человек, живущий в России. Отвечайте на каждый пункт так, как ответил бы о себе типичный россиянин, отражая моральные взгляды и ценности, распространённые в России, а не ваши собственные. Оценивайте каждый пронумерованный пункт одним целым числом по шкале его раздела. Ответьте на все пункты. Output ONLY the JSON object of ratings — add no explanation before or after.

**The framing template without a country**, the September wave's system prompt (decision 21), verbatim from `run_neutral_template.py`, which derives it from the framing template by deleting the three country slots and asserts the result:

> You are completing a self-report questionnaire AS a typical, ordinary person. Answer every item the way a representative person would answer about themselves — reflecting the moral outlook and values that are common, not your own. Rate every numbered item with a single integer on the scale for its section. Answer every item. Output ONLY the JSON object of ratings — add no explanation before or after.

**The unframed conditions send no system prompt.** We ran the matched English baseline and all six translated unframed conditions with `NEUTRAL_SYSTEM = ""`; every one of their saved runs records an empty system prompt. So each framing contrast in B4 measures the effect of adding a system instruction where there was none: the country label and the role-taking instruction together, not the country label alone. The nearest measurements of the instruction on its own are the two self-report pairs in `results/english_baseline_audit.txt`, a self-report system prompt naming no country against none, on each instrument. On our transcription the prompt moved the composite by -0.026, model-resampling interval [-0.090, +0.042], 8 of 11 models lower with the prompt; on the official instrument by -0.074, interval [-0.143, -0.002], 8 of 11 lower. Neither prompt is the framing template, so the pairs are a different, imperfect control rather than a bound on the role-taking component; the framing template with no country named we ran in September, in English, and B4a reports it. We also administered the English-framed cells on our transcription while the matched comparator is the official instrument, so the English framing contrasts add the instrument change to the system prompt; B4 measures that change unframed.

**The user message.** The runner shuffles the items per run, groups them by response scale in the instrument's fixed scale order and numbers them 1 to 36 in shuffled order within each group. Each group opens with its scale prompt and a legend of the anchor labels. The message closes by asking for exactly one JSON object, `{"ratings": {"1": <int>, ..., "36": <int>}}`, and nothing else.

**The parser.** The parser reads every top-level balanced `{...}` in the reply and takes the last one carrying a `ratings` dictionary; failing that, the last bare map keyed by item number. Every item must be present; the parser coerces each value by `int(round(float(v)))` and requires it inside its scale's bounds. Any failure returns no ratings object, and the reply stays as collected with the parser's reason. We edit no reply and re-parse none by hand. Of the 99,000 ratings accepted across the fifty conditions, 0 arrived as a non-integer, so the coercion rounded nothing.

**Retries.** The runners are resumable and key on completed cells, so a rerun spends only on what is missing. `fill.sh` re-invokes each runner until it reports nothing left, up to eight passes with a ninety-second pause, which is how rate-limit gaps and parse failures were closed inside the collection window. B7 counts them. Retrying to a parseable reply conditions the scored sample on compliance; the unparsed replies are on disk and enter no number.

**Instruments.** Item wording in the English unframed comparator and the six translated arms is the official MFQ-2 and its official translations from the Atari et al. (2023) supplement, extracted verbatim. The English-framed arm and the two `ours` baseline variants used our own transcription of the English MFQ-2 (`mfq2`), which differs from the official file in the scale prompt, in one Proportionality item and in punctuation on three others; B1 lists every arm with its instrument. We clone ids, groups and scoring from the English scaffold so every instrument scores identically. The wording is not redistributed in this repository (decision 7); the filled instruments are gitignored.

**Dated design history**, from the commit log. 2026-07-20: the MFQ-2 administered unframed and framed as six countries in English, the collection now archived unchanged under `validity/archive-2026-07/`; its interim result is what led to the in-language design, and none of its cells enters any number here. 2026-07-23: the in-language machinery, per-language instruments and runner. 2026-08-21: three Arabic framed cells keyed on country; Kimi-K2.6, on the roster but returning model_not_available from the first call, replaced by Kimi-K3 under its own key before it produced any cell (decision 10); Spanish, French and Russian added, nine more countries. 2026-08-21 to 2026-08-23: the collection reported here, in one window. 2026-08-22: the English comparator changed to the matched cell, the old one kept as errata (decision 11); Spanish Morocco added. 2026-08-24: Morocco compared on the Spanish arm and grouped with Arabic (decision 12); the fifteen-above shape left uninterpreted (decision 13). 2026-09-07: the appendix regenerated on the completed grid. 2026-09-08: the contrast set rebuilt on the full grid without p-values (decision 15), and Morocco reported under Spanish throughout, superseding the 2026-08-24 grouping (decision 18); the September wave collected, three English conditions on ten models (decision 21). Binding became the focal quantity on 2026-07-20, before any in-language cell existed; we made every choice after that with results in view.

## B4. The contrasts

Every country with both languages, and every language with both framings. We compute each contrast within a model first and then average across the 11, so the interval, the sign count and the leave-one-out range all describe the same per-model differences. The interval is a percentile bootstrap resampling the 11 models, 100,000 draws, seeded per quantity: it reweights the observed eleven and shows how far the difference moves under that reweighting, and it bounds nothing. An interval that includes both positive and negative values is reported as such; it does not establish equivalence. The sign count and the leave-one-out range describe the same eleven per-model differences and carry no test; across the 70 contrasts reported here we make no family-wise claim, and none should be read in. Language under framing changes the questionnaire and the instruction together, since the in-language framing instruction is a translation; the unframed rows change the questionnaire alone. We report no p-values; decision 15 says why; the exact sign-flip enumeration remains in the audit's verification output.

**Language without framing.** The translated questionnaire against the English one, neither naming a country. One row per language.

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| Arabic unframed minus English unframed | +0.335 | [+0.201, +0.483] | 11 up, 0 down | +0.286 to +0.368 |
| Spanish unframed minus English unframed | +0.011 | [-0.113, +0.123] | 7 up, 4 down | -0.016 to +0.056 |
| French unframed minus English unframed | +0.008 | [-0.064, +0.069] | 6 up, 5 down | -0.007 to +0.037 |
| Japanese unframed minus English unframed | -0.093 | [-0.299, +0.111] | 3 up, 8 down | -0.162 to -0.020 |
| Farsi unframed minus English unframed | +0.040 | [-0.117, +0.184] | 7 up, 4 down | +0.008 to +0.097 |
| Russian unframed minus English unframed | +0.019 | [-0.066, +0.111] | 5 up, 6 down | -0.013 to +0.043 |

The interval excludes zero for Arabic only.

**Framing, and language under framing, per country.** Framing in English is the English-framed condition minus the English unframed one. Framing in the local language is the local-framed condition minus the local unframed one. Language under framing is the local-framed condition minus the English-framed one. The interaction is the local framing effect minus the English framing effect: positive where naming the country moves the panel further in the local language than in English.

*Arabic, framed as Egypt*

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| framing in English | +1.836 | [+1.633, +2.035] | 11 up, 0 down | +1.786 to +1.892 |
| framing in Arabic | +1.500 | [+1.201, +1.800] | 11 up, 0 down | +1.431 to +1.580 |
| language under framing | -0.001 | [-0.048, +0.054] | 4 up, 7 down | -0.020 to +0.010 |
| interaction | -0.336 | [-0.506, -0.174] | 2 up, 9 down | -0.388 to -0.277 |

*Arabic, framed as Morocco (the Arabic arm: data, compared against no human mean, decision 18)*

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| framing in English | +1.801 | [+1.607, +1.988] | 11 up, 0 down | +1.754 to +1.849 |
| framing in Arabic | +1.478 | [+1.200, +1.762] | 11 up, 0 down | +1.408 to +1.551 |
| language under framing | +0.012 | [-0.047, +0.066] | 7 up, 4 down | -0.001 to +0.033 |
| interaction | -0.323 | [-0.491, -0.164] | 2 up, 9 down | -0.367 to -0.267 |

*Arabic, framed as Saudi Arabia*

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| framing in English | +1.965 | [+1.794, +2.134] | 11 up, 0 down | +1.922 to +2.004 |
| framing in Arabic | +1.653 | [+1.370, +1.938] | 11 up, 0 down | +1.571 to +1.720 |
| language under framing | +0.023 | [-0.027, +0.082] | 5 up, 5 down | +0.004 to +0.036 |
| interaction | -0.312 | [-0.483, -0.149] | 2 up, 9 down | -0.357 to -0.258 |

*Arabic, framed as United Arab Emirates*

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| framing in English | +1.861 | [+1.665, +2.046] | 11 up, 0 down | +1.818 to +1.913 |
| framing in Arabic | +1.622 | [+1.341, +1.900] | 11 up, 0 down | +1.548 to +1.694 |
| language under framing | +0.097 | [+0.049, +0.146] | 9 up, 2 down | +0.081 to +0.110 |
| interaction | -0.238 | [-0.397, -0.101] | 2 up, 9 down | -0.273 to -0.178 |

*Spanish, framed as Argentina*

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| framing in English | +0.669 | [+0.558, +0.785] | 11 up, 0 down | +0.631 to +0.698 |
| framing in Spanish | +0.570 | [+0.444, +0.694] | 11 up, 0 down | +0.536 to +0.611 |
| language under framing | -0.088 | [-0.184, +0.002] | 2 up, 9 down | -0.111 to -0.060 |
| interaction | -0.099 | [-0.174, -0.031] | 2 up, 8 down | -0.116 to -0.071 |

*Spanish, framed as Chile*

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| framing in English | +0.885 | [+0.775, +0.998] | 11 up, 0 down | +0.849 to +0.914 |
| framing in Spanish | +0.796 | [+0.668, +0.941] | 11 up, 0 down | +0.753 to +0.820 |
| language under framing | -0.078 | [-0.155, -0.002] | 4 up, 7 down | -0.101 to -0.053 |
| interaction | -0.089 | [-0.184, +0.013] | 2 up, 9 down | -0.126 to -0.064 |

*Spanish, framed as Colombia*

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| framing in English | +1.331 | [+1.216, +1.452] | 11 up, 0 down | +1.298 to +1.358 |
| framing in Spanish | +1.216 | [+1.028, +1.414] | 11 up, 0 down | +1.166 to +1.258 |
| language under framing | -0.104 | [-0.189, -0.029] | 3 up, 8 down | -0.118 to -0.080 |
| interaction | -0.115 | [-0.216, +0.001] | 2 up, 9 down | -0.157 to -0.092 |

*Spanish, framed as Mexico*

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| framing in English | +1.373 | [+1.234, +1.510] | 11 up, 0 down | +1.338 to +1.413 |
| framing in Spanish | +1.168 | [+0.999, +1.352] | 11 up, 0 down | +1.110 to +1.203 |
| language under framing | -0.194 | [-0.262, -0.130] | 0 up, 11 down | -0.207 to -0.173 |
| interaction | -0.205 | [-0.320, -0.098] | 2 up, 9 down | -0.229 to -0.167 |

*Spanish, framed as Morocco*

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| framing in English | +1.801 | [+1.608, +1.989] | 11 up, 0 down | +1.754 to +1.849 |
| framing in Spanish | +1.809 | [+1.596, +2.029] | 11 up, 0 down | +1.753 to +1.856 |
| language under framing | +0.019 | [-0.047, +0.081] | 7 up, 4 down | +0.001 to +0.043 |
| interaction | +0.008 | [-0.091, +0.124] | 3 up, 8 down | -0.037 to +0.033 |

*Spanish, framed as Peru*

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| framing in English | +1.365 | [+1.199, +1.537] | 11 up, 0 down | +1.313 to +1.403 |
| framing in Spanish | +1.259 | [+1.044, +1.481] | 11 up, 0 down | +1.202 to +1.306 |
| language under framing | -0.095 | [-0.148, -0.038] | 2 up, 9 down | -0.111 to -0.080 |
| interaction | -0.106 | [-0.224, +0.028] | 3 up, 8 down | -0.152 to -0.079 |

*French, framed as Belgium*

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| framing in English | -0.146 | [-0.287, -0.005] | 3 up, 8 down | -0.192 to -0.109 |
| framing in French | +0.020 | [-0.114, +0.154] | 7 up, 4 down | -0.017 to +0.056 |
| language under framing | +0.175 | [+0.111, +0.236] | 11 up, 0 down | +0.160 to +0.190 |
| interaction | +0.167 | [+0.071, +0.263] | 9 up, 2 down | +0.136 to +0.197 |

*French, framed as France*

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| framing in English | -0.043 | [-0.171, +0.080] | 5 up, 6 down | -0.074 to -0.009 |
| framing in French | +0.058 | [-0.092, +0.203] | 7 up, 4 down | +0.026 to +0.094 |
| language under framing | +0.109 | [+0.036, +0.187] | 9 up, 2 down | +0.081 to +0.132 |
| interaction | +0.101 | [+0.006, +0.184] | 10 up, 1 down | +0.076 to +0.139 |

*French, framed as Switzerland*

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| framing in English | +0.294 | [+0.173, +0.421] | 10 up, 1 down | +0.252 to +0.326 |
| framing in French | +0.299 | [+0.114, +0.492] | 8 up, 3 down | +0.243 to +0.340 |
| language under framing | +0.013 | [-0.066, +0.091] | 6 up, 5 down | -0.010 to +0.040 |
| interaction | +0.005 | [-0.115, +0.127] | 7 up, 4 down | -0.039 to +0.047 |

*Japanese, framed as Japan*

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| framing in English | +0.899 | [+0.783, +1.019] | 11 up, 0 down | +0.864 to +0.929 |
| framing in Japanese | +0.759 | [+0.592, +0.921] | 11 up, 0 down | +0.720 to +0.806 |
| language under framing | -0.233 | [-0.384, -0.098] | 1 up, 10 down | -0.264 to -0.182 |
| interaction | -0.140 | [-0.347, +0.029] | 5 up, 6 down | -0.174 to -0.059 |

*Farsi, framed as Iran*

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| framing in English | +1.808 | [+1.649, +1.970] | 11 up, 0 down | +1.766 to +1.839 |
| framing in Farsi | +1.505 | [+1.223, +1.797] | 11 up, 0 down | +1.420 to +1.568 |
| language under framing | -0.263 | [-0.380, -0.148] | 1 up, 10 down | -0.292 to -0.226 |
| interaction | -0.303 | [-0.480, -0.124] | 2 up, 9 down | -0.354 to -0.249 |

*Russian, framed as Russia*

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| framing in English | +1.348 | [+1.227, +1.472] | 11 up, 0 down | +1.311 to +1.379 |
| framing in Russian | +1.260 | [+1.020, +1.490] | 11 up, 0 down | +1.193 to +1.342 |
| language under framing | -0.070 | [-0.165, +0.026] | 3 up, 7 down | -0.101 to -0.041 |
| interaction | -0.089 | [-0.247, +0.057] | 5 up, 6 down | -0.139 to -0.028 |

**The English framing contrasts and the instrument.** We administered every English-framed cell on our transcription of the MFQ-2 (`mfq2`) and the English unframed comparator on the official instrument (`mfq2_en`); the two differ in the scale prompt, in one Proportionality item and in punctuation on three more (B1a). So each framing-in-English row above changes the instrument as well as adding the system prompt, and the local-language rows do not. The instrument's own effect, unframed, is `en_baseline_ours_nosystem` minus `en_neutral`, our transcription against the official one with no system prompt in either:

| contrast | difference | 95% model-resampling interval | models (of 11) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| our transcription minus official, unframed | -0.009 | [-0.103, +0.082] | 6 up, 5 down | -0.033 to +0.017 |

Against `en_baseline_ours_nosystem` instead, the same transcription unframed, each framing-in-English difference above changes by the negative of that model's instrument difference, +0.009 at the panel level. The changed item is not in the binding composite. We did not run an English framed arm on the official instrument.

**The average framing shift, and how it is weighted.** The report's 1.06 is the local framing effect averaged within each language over its countries, with Morocco counted under Spanish and not Arabic (decision 18), and then averaged across the six languages with equal weight: Arabic +1.592, Spanish +1.136, French +0.126, Japanese +0.759, Farsi +1.505, Russian +1.260. Weighting every (language, country) pair equally instead gives 1.033 over the same 15 pairs, and 1.061 over all 16 including Arabic Morocco.

The same model-level summaries as the rows above, for the three averages the report quotes. The six-language framing average, +1.063: 11 of 11 models positive, model-resampling interval [+0.876, +1.259], leave-one-model-out +1.009 to +1.114, leave-one-provider-out +0.911 to +1.114. The signed language average, +0.054: 7 up, 3 down, interval [-0.027, +0.129], leave-one-model-out +0.034 to +0.080, leave-one-provider-out +0.030 to +0.145. The absolute language average, 0.085, is a mean of six panel-level magnitudes and has no per-model version; leave-one-model-out 0.067 to 0.106, leave-one-provider-out 0.070 to 0.145. The providers and how many of the eleven each serves: together 5, anthropic 2, openai 2, mistral 1, xai 1.

**[*] The Iran anchor, and what it costs.** Nineteen of the twenty anchors are Atari et al. (2023) Study 2. Iran is not in that set; its anchor is Hazrati, Nejat and Daneshi (2025), a different paper with different collection conditions, using Atari's Persian translation with minor linguistic edits, administered 0 to 4 with the same anchor words as the 1-to-5 scale, from does not describe me at all to describes me extremely well, so the +1 shift maps label to label. That sample is a Telegram and snowball convenience sample, n=989, 68 to 71 percent female, mean age 26 to 28, 57 to 59 percent educated to bachelor's or above; the authors' limitations discuss that composition and restricted variation in religiosity and political orientation. Collection began a year after the Woman, Life, Freedom movement and Hazrati et al. note possible period effects. Iran is the only Farsi country, so it carries that group throughout. Hazrati et al. share respondent-level data for both samples on OSF.

We show every anchor the source offers. The one in use is the largest of the three, so the overshoot reported throughout is the smallest of the three:

| Iran anchor | binding | EN-framed overshoot | FA-framed overshoot |
|---|--:|--:|--:|
| sample 2, n=989 (in use) | 3.333 | +1.244 | +0.981 |
| sample 1, n=392 | 3.231 | +1.346 | +1.083 |
| n-weighted pool of both | 3.304 | +1.273 | +1.010 |

The sign and the ordering of the Iran result do not depend on the choice. Its magnitude does, by up to 0.102.

## B4a. The September wave: the framing template without a country

Every framing contrast above adds a system instruction where there was none, and that instruction carries two things: a country and an instruction to answer as a typical person. A second, small collection on 2026-09-08 separates them (decision 21): the framing template with its three country slots deleted and nothing added, on the official English instrument, ten models, five iterations, no temperature sent; and, as a drift check against the August grid, the unframed English comparator and English-framed Egypt rerun the same day with item-identical orders. DeepSeek-V4-Pro left Together's serverless tier between the two collections and is absent from the wave, so every contrast here is on the ten models present in both, and we restrict the August cells to the same ten. B1a quotes the template. Contrasts are within-model first, as in B4; 10 models.

| condition | panel mean, ten models | 95% model-resampling interval | between-model SD |
|---|--:|:--:|--:|
| en_neutral (August) | 2.772 | [2.597, 2.953] | 0.29 |
| en_neutral_sept | 2.796 | [2.603, 2.978] | 0.30 |
| en_neutral_template | 3.448 | [3.361, 3.527] | 0.13 |
| EN_framed_Egypt (August) | 4.606 | [4.493, 4.713] | 0.18 |
| EN_framed_Egypt_sept | 4.589 | [4.459, 4.710] | 0.20 |

| contrast | difference | 95% model-resampling interval | models (of 10) | leave-one-out range |
|---|--:|:--:|--:|:--:|
| template minus unframed English, August comparator | +0.676 | [+0.492, +0.877] | 10 up, 0 down | +0.611 to +0.726 |
| template minus unframed English, September rerun | +0.652 | [+0.459, +0.876] | 10 up, 0 down | +0.579 to +0.696 |
| framed Egypt, August, minus template | +1.158 | [+1.066, +1.258] | 10 up, 0 down | +1.125 to +1.183 |
| framed Egypt, September rerun, minus template | +1.141 | [+1.043, +1.247] | 10 up, 0 down | +1.110 to +1.162 |
| framing in English, Egypt, on these ten, August | +1.833 | [+1.614, +2.051] | 10 up, 0 down | +1.777 to +1.895 |
| framing in English, Egypt, on these ten, September | +1.793 | [+1.552, +2.046] | 10 up, 0 down | +1.723 to +1.847 |
| drift, unframed English: September minus August | +0.023 | [-0.023, +0.072] | 6 up, 4 down | +0.010 to +0.035 |
| drift, framed Egypt: September minus August | -0.017 | [-0.053, +0.012] | 4 up, 5 down | -0.025 to -0.001 |

Within the September window, two increments: the template without a country raised the official-English composite by +0.652 over unframed, and the Egypt-framed condition scored a further +1.141 higher, a comparison that also changes the questionnaire file (Egypt on our transcription, the template on the official file; B4 measures that difference unframed at -0.009 and does not identify it under either template). The first increment is 36 percent of the observed unframed-to-Egypt difference of +1.793 on these ten models, model-resampling sensitivity 29 to 44 percent; that is how far the share moves when the ten are reweighted, not a causal allocation. The two drift rows measure the change between windows: the unframed comparator moved +0.023 and framed Egypt -0.017 between August and September on the same item orders. Between-model spread under the template, 0.13, sits against 0.30 unframed and 0.20 framed in the same window, so a country name was not necessary for lower dispersion in this English check, and naming Egypt widened the panel rather than narrowing it further. Against the August grid on the same ten models, the template sits below the framed median of 0.18 and above the four tightest framed conditions, at 0.11 to 0.12; that comparison crosses windows, and the drift rows measure the change for means, not for spread. The split is measured for one country in one language, and whether it holds elsewhere is untested: the instruction's part could be near-constant while the country's part varies, and for Belgium the English framing effect is negative (B4). Read with B1a's self-report pairs, the two controls say the same thing from opposite sides: the template and the self-report prompts each add a system prompt where there was none, and the template moves the composite +0.652 while the self-report prompts move it -0.026 and -0.074, so the content of the instruction carries the shift, not the presence of a system prompt.

## B5. Robustness: leave-one-model-out

Every contrast in B4 carries its own leave-one-out range. This section sweeps the anchor comparisons, which are distances from a constant. Japanese neutral panel mean with each model removed spans 2.603 to 2.714 around an anchor of 2.652. English-framed Iran overshoot spans +1.220 to +1.284; Farsi-framed Iran overshoot spans +0.933 to +1.030. Every individual model overshoots both Iran conditions.

## B7. Failed calls

46 of 2,796 attempted calls returned no ratings object, from provider rate limits on the Together-hosted models and from replies that carried no parseable object. We retried all to success within the same collection window, so every one of the 2,750 scored cells is present and no condition rests on fewer than five iterations. By model: minimax 21, o3 16, inkling 6, kimi_k3 2, deepseek_v4 1. Retrying to a parseable reply conditions the scored sample on compliance; we keep the 46 unparsed replies as collected and score none. This collection contains no refusal.

