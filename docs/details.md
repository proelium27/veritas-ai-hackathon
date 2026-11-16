# More detail

The one-page write-up is the [README](../README.md). This page has the longer version. Every number here comes from [notebook/model.ipynb](../notebook/model.ipynb); the running record of decisions and results is [docs/log.md](log.md).

## Files in this repo

| Path | What it is |
|---|---|
| [notebook/model.ipynb](../notebook/model.ipynb) | The AI project. This is what judges open and run. |
| [notebook/experiments/model_check.ipynb](../notebook/experiments/model_check.ipynb) | First check: do the three models load with no sign-in, how fast are they, and do NLLB's options include the forms we need? |
| [notebook/experiments/more_options.ipynb](../notebook/experiments/more_options.ipynb) | Experiment: does NLLB's top 8, 16 or 32 include a form that fits the labels? |
| [data/test_sentences.csv](../data/test_sentences.csv) | Our test set: Mandarin, English meaning, correct Serbian, the labels, and whether each row is for practice or testing. |
| [data/human_check.csv](../data/human_check.csv) | Our Serbian speaker's hand grades (meaning right, endings right) of all three systems' answers on the 45 test rows. |
| [data/README.md](../data/README.md) | How the test set was written, the rules for filling it in, and what the human check file holds. |
| [data/check_test_set.py](../data/check_test_set.py) | Checks the test set for mistakes (missing cells, Cyrillic letters, missing č/ć/š/ž/đ marks, 您/你 that don't match the formality label). |
| [docs/how-it-works.svg](how-it-works.svg) | The flowchart in the README. |
| [docs/log.md](log.md) | Decisions and real results, including failures. |
| [app/demo.py](../app/demo.py) | The demo page for the video (Gradio). It runs the notebook's section 8 code on one sentence and shows the three systems side by side. Changes no score. |
| [requirements.txt](../requirements.txt) | Libraries, for running outside Colab. |

## Running it

**Main notebook:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/proelium27/veritas-ai-hackathon/blob/main/notebook/model.ipynb)

Click **Runtime → Run all**. It needs no sign-in, keys or uploads. A GPU (Runtime → Change runtime type → T4 GPU) makes translation faster, but you don't need one. Our last full run took 84 seconds on a laptop CPU with the models already downloaded. A fresh Colab session first has to download the three models (about 3 GB), which adds a few minutes.

**Model check** (our first test that all three models load and run): [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/proelium27/veritas-ai-hackathon/blob/main/notebook/experiments/model_check.ipynb)

## Demo app

An optional small web page we made for the demo video. It shows the three translations of one sentence side by side. It runs the notebook's own section 8 code, so it gives the same answers. On a laptop, from the repo's top folder: `pip install -r requirements.txt`, then `python app/demo.py`, and open http://127.0.0.1:7860. The steps for Colab are at the top of [app/demo.py](../app/demo.py); there, Gradio prints a public link to open instead.

## What we built, in full

**Input:** a Mandarin sentence, plus three choices: who is speaking (man or woman), who you're talking to (man, woman or a group) and whether it's formal or casual. The demo page takes one listener, a man or a woman.

**Output:** a Serbian sentence in Latin letters with the right endings, or NLLB's best answer with a "had to guess" warning when none of its options fit the choices.

## Data

- **Our test set:** 60 sentences in [data/test_sentences.csv](../data/test_sentences.csv), loaded from the repo's public web address. Speakers: 30 women, 30 men. Listeners: 27 men, 27 women, 6 groups. Formality: 27 formal, 33 casual. Six are control sentences that show no gender or formality. The 45 test rows have 25 women and 20 men speaking, 19 formal and 26 casual rows, and 5 controls.
- **How we made it:** the Mandarin was drafted with an AI tool, then read and corrected by a native Mandarin speaker, who also wrote the English meaning and the labels. The correct Serbian was written by a native Serbian speaker from the English meaning and the labels, without any translation app.
- **Split:** 15 practice rows and 45 test rows, fixed before any model saw them. We built the picker rules on the practice rows only and looked at test results once, after the rules were final (frozen at commit `ad6b1a7`). Nothing changed after we saw the test results. We found one bug afterwards (`to_latin()` misses the letter ѓ, t21) and left it unfixed on purpose, so the test numbers stay as scored.
- **Script:** the correct Serbian is in Latin letters with č, ć, š, ž, đ, dž.
- **Human check:** [data/human_check.csv](../data/human_check.csv) holds our native Serbian speaker's yes/no grades (meaning right, endings right) for every answer of all three systems on the 45 test rows, next to the exact answers graded.

## The model and the rules, in full

We use three pre-trained translation models as they are (no training) and compare three systems on the same sentences:

1. **Baseline (through English):** Mandarin → English with opus-mt-zh-en, then English → Serbian with opus-mt-tc-base-en-sh.
2. **NLLB direct:** Meta's NLLB model translates Mandarin straight to Serbian, and we take its top answer.
3. **Ours:** NLLB lists its top 32 answers, and our picker makes two decisions:
   - **Match:** it checks the Serbian endings of each answer and picks the first one that fits the speaker, listener and formality.
   - **Repair:** if none fits, our repair rules try to fix the endings of each answer, best first, and keep the first fix that fits (for example *dodao → dodala* for a woman, *Vi → ti* for casual).
   - If neither works, it shows NLLB's top answer with a "had to guess" warning.

**Inside the rules.** Serbian shows gender in the word next to "sam" (I am) or "si" (you are): *proverio sam* is a man, *proverila sam* a woman. Formality shows in the word for "you": *Vi* / *Vaš* is formal, *ti* / *tvoj* casual. Match reads those words in each option, and Repair rewrites them when no option fits. Our Serbian speaker checked and corrected every rule and word list, and the notebook tests the rules on hand-written examples (50 for Match, 49 for Repair).

The models write Serbian in Cyrillic, so the notebook converts every output to Latin letters, one letter at a time, before checking or scoring it.

**How we score:**

- **chrF:** a standard translation score from the sacrebleu library. It compares our Serbian with the correct Serbian letter by letter.
- **Gender and formality:** the % of answers with the right speaker or listener gender, and with the right formality. `detect()`, the same code Match uses, reads both.
- **Fitting form in the 32:** how often a fitting form is somewhere in NLLB's 32 options. That is the best the picker could do without repair.
- **Human check:** our Serbian speaker's hand grades for meaning and endings.

## Results, in full

**Automatic scores, rows left out.** Rows where `detect()` couldn't read the gender or formality at all are left out of that column (gender: 5 for the baseline, 6 for NLLB direct; formality: 3 for NLLB direct, 1 for ours). For ours, a fitting form was among NLLB's 32 options on 37 of 40 rows (92.5%). The picker matched 37, repaired 2 and had to guess on 1. `detect()` read all 45 of our own correct test sentences right.

**What the automatic scores show:** the two usual routes mostly fall back to the man's form. They got the gender right on 9 of 21 and 8 of 20 test sentences, and ours got 26 of 26. Our user can't spot this mistake on their own.

**Practice rows** (15, the ones the rules were written on, so they flatter us), as baseline / NLLB direct / ours: chrF 54.5 / 35.6 / 35.7, gender 71.4% / 57.1% / 100.0%, formality 50.0% / 62.5% / 100.0%.

**Chance.** A bootstrap check (2,000 resamples of the 45 test rows) says our gender lead over NLLB direct is bigger than chance (+60.0 points, 95% interval +36.8 to +81.2). The formality lead isn't (+15.8 points, interval +0.0 to +33.3, which touches 0).

**chrF** only shows that the three systems are close (42.5, 39.3, 43.1). It compares letters, so it can't tell a wrong ending from a wrong word. On the practice rows the baseline won it, 54.5 to 35.7.

**Human check against `detect()`.** On the 40 rows that test an ending, our Serbian speaker and `detect()` agree on 40 of 40 for the baseline, 40 of 40 for NLLB direct and 39 of 40 for ours. The one disagreement is t20: ours, *Da li si umoran?*, is word for word our correct Serbian but was marked wrong on endings, so it may be a grading slip. We count it as graded.

## The three misses, in full

All five real misses are in section 7 of the notebook, and our Serbian speaker marked all five wrong in meaning. Here are three of them.

1. **t30** Mandarin: 你先去休息吧 ("Get some rest first") / What we produced: *Ne, ne, ne, ne, …* ("no, no, no…") / Correct: *Idi prvo da se odmoriš.* / Why: NLLB broke and all 32 options were the same repeat, so nothing fit; our "had to guess" warning fired, but there was nothing good to give.
2. **t11** Mandarin: 我把货物都清点完了 ("I finished counting and checking the goods", a woman) / What we produced: *Ja sam završila čišćenje.* ("I finished cleaning") / Correct: *Završila sam prebrojavanje i proveru robe.* / Why: the woman's ending is right, but NLLB read 清点 "count and check" as 清 "clean", and our picker checks endings, not meaning.
3. **t08** Mandarin: 我昨天生病了 ("I got sick yesterday", a man) / What we produced: *Ja sam juče bolestan.* ("I am sick yesterday") / Correct: *Juče sam se razboleo.* / Why: the man's ending is right but the tense is broken, which our rules can't see; the route through English got this one exactly right.

## Limits

The full list, with examples, is also in section 10 of the notebook.

- **Small test set:** 60 sentences, 15 practice and 45 test, so each test percentage moves by 2 to 3 points per sentence. One person graded the human check.
- **Endings, not words:** the picker can only choose among NLLB's 32 options and repair only changes endings, so a wrong word or a broken tense stays (t11, t08). Our Serbian speaker marked 18 of our 45 test answers wrong in meaning, against 4 for the route through English.
- **NLLB's own mistakes:** made-up words (*vinkar* for forklift, *Sastanao sam*), words and letters from neighbouring languages (Macedonian ѓ, Russian-looking *opozdao*, Croatian- or Bosnian-style phrasing), and once a breakdown into *Ne, ne, ne…* (t30). The neighbouring-language readings are ours; our Serbian speaker hasn't confirmed them yet.
- **The user has to say who's speaking and to whom.** The system doesn't guess gender or formality from the Mandarin.
- **Workplace sentences only:** short, one-part messages about work. We haven't tested long, casual or technical text.
- **AI-drafted Mandarin:** drafted with an AI tool and then checked by a native speaker, so it may read more like textbook Mandarin than real messages.
- **A small model:** NLLB's 600M distilled version, the smallest one. We didn't test the bigger ones.
- **No Mac GPU:** on Apple's GPU (`mps`) NLLB gave broken, repeating Serbian, so the notebook uses an NVIDIA GPU if there is one and the CPU otherwise.
- **Not a replacement for a human translator:** this is a student project tested on 45 sentences. If a message matters (safety, money, health, a contract), have someone who speaks Serbian check it. The demo page says the same: it checks endings, not meaning.
- **Non-commercial model:** NLLB is licensed CC BY-NC 4.0, so this can't be used in a paid product as it is.
