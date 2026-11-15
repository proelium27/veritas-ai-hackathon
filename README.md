# Lost in Translation: Mandarin to Serbian that keeps who's talking

<!--
HOW TO USE THIS FILE
This README is also our one-page write-up. The sections follow the official
write-up template (Project name, Track, The problem, What we built, What we added,
How it works, Results, What we'd do next, Sources).
Every [TO FILL: ...] marks something the team still has to write. The hint says
what goes there and roughly how long. Replace the whole bracket, hint included.
Every number must match what notebook/model.ipynb prints on the test rows.
Delete these HTML comments before submitting (they don't show on GitHub, but
judges may read the raw file).

NO NAMES OR SCHOOL ANYWHERE IN THIS FILE. Round 1 review is blind. Team member
names, emails and school go only in the Airtable submission form, which collects
them separately. That is why there is no "Team" line under the title.
-->

Our project helps a Mandarin speaker writing to Serbian colleagues at work by taking a Mandarin sentence plus who is speaking, who is listening and how formal it is, and giving back Serbian with the right endings, or a warning when it had to guess.

**Track:** AI + Languages

## Try it

Main project (this is what to run):
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/proelium27/veritas-ai-hackathon/blob/main/notebook/model.ipynb)

Model check (our first test that all three models load and run):
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/proelium27/veritas-ai-hackathon/blob/main/notebook/model_check.ipynb)

Click **Runtime → Run all**. It needs no sign-in, keys or uploads. A GPU (Runtime → Change runtime type → T4 GPU) makes the translation faster but isn't required. Our last full run took 84 seconds on a laptop CPU with the models already downloaded. A fresh Colab session first has to download the three models, which adds a few minutes.

**Demo app** (for the demo video; optional): a small web page that shows the three translations side by side for one sentence. It runs the notebook's own section 8 code, so it gives the same answers. On a laptop, from the repo's top folder: `pip install -r requirements.txt`, then `python app/demo.py`, and open http://127.0.0.1:7860. How to run it in Colab is at the top of [app/demo.py](app/demo.py).

## The problem

In Serbian, the words change depending on who is speaking and who they're talking to. A woman says "Proverila sam" (I checked it) and a man says "Proverio sam". You say "ti si" to a friend but "Vi ste" to your boss. Mandarin shows politeness (您 is the polite "you", 你 the casual one) but usually doesn't show the speaker's gender at all.

Many translation tools go Mandarin → English → Serbian. English has one "you" and no gendered verbs, so on the way through, the gender and the politeness are lost, and the Serbian usually comes out masculine and at a guessed level of politeness.

Our user is a Mandarin speaker writing to Serbian colleagues at work, for example at one of the Chinese-run companies in Serbia, who doesn't read Serbian well enough to spot a wrong ending. When a woman types "I already notified the driver", the route through English gives her *Obavestio sam vozača*, a man's sentence. A polite question to a manager can come out casual (*Jesi li zaboravio…* for 您, t51). The writer can't see either mistake, so they come across as the wrong gender, or as rude, without knowing it.

## What we built

**Input:** a Mandarin sentence, plus three choices: who is speaking (man or woman), who you're talking to (man, woman or a group) and whether it's formal or casual.

**Output:** a Serbian sentence in Latin letters with the right endings, or NLLB's best answer with a "had to guess" warning when none of its options fit the choices.

**One example:**

| Mandarin | Through English (baseline) | NLLB direct | Ours | Correct Serbian |
|---|---|---|---|---|
| 我已经通知司机了 ("I already notified the driver", said by a woman; test row t09) | Obavestio sam vozača. | Ja sam obavestio vozača. | Ja sam obavestila vozača. | Već sam obavestila vozača |

## What we added

The brief's "Translation quality test" uses NLLB and chrF on a public benchmark. What's ours:

- **Our own test set:** 60 short workplace sentences we wrote for this project, each with the Mandarin, the English meaning, the correct Serbian, and labels for speaker gender, listener gender and formality. Public benchmarks don't label who is speaking or listening, so they can't measure this.
- **Our picker and repair rules:** rules about Serbian word endings that read NLLB's options and choose the one that matches the speaker, listener and formality. When none matches, repair rules fix the endings of an option (*popravio → popravila*), and if that fails too, the user gets a "had to guess" warning. Our Serbian speaker checked every rule.
- **Our question:** does going through English lose speaker gender and formality, and can choosing among a model's own options fix it without retraining anything?

What we found along the way: NLLB usually knows the right form but doesn't put it first. For 37 of the 40 test sentences that check an ending, a fitting option was already among its 32 answers.

## How it works

### Data

- **Our test set:** 60 sentences in [data/test_sentences.csv](data/test_sentences.csv), loaded from the repo's public web address. Speakers: 30 women, 30 men. Listeners: 27 men, 27 women, 6 groups. Formality: 27 formal, 33 casual. Six are control sentences that show no gender or formality. The 45 test rows have 25 women and 20 men speaking, 19 formal and 26 casual rows, and 5 controls.
- **How we made it:** the Mandarin was drafted with an AI tool, then read and corrected by a native Mandarin speaker, who also wrote the English meaning and the labels. The correct Serbian was written by a native Serbian speaker from the English meaning and the labels, without any translation app.
- **Split:** 15 practice rows and 45 test rows, fixed before any model saw them. We built the picker rules on the practice rows only and looked at test results once, after the rules were final (frozen at commit `ad6b1a7`). Nothing changed after we saw the test results. We found one bug afterwards (`to_latin()` misses the letter ѓ, t21) and left it unfixed on purpose, so the test numbers stay as scored.
- **Script:** the correct Serbian is in Latin letters with č, ć, š, ž, đ, dž.

### Model

We use three pre-trained translation models as they are (no training) and compare three systems on the same sentences:

1. **Baseline (through English):** Mandarin → English with opus-mt-zh-en, then English → Serbian with opus-mt-tc-base-en-sh. This is how many apps work.
2. **NLLB direct:** Meta's NLLB model translates Mandarin straight to Serbian, and we take its top answer.
3. **Ours:** NLLB lists its top 32 answers, and our picker makes two decisions:
   - **Match:** it checks the Serbian endings of each answer and picks the first one that fits the speaker, listener and formality.
   - **Repair:** if none fits, repair rules written by our Serbian speaker try to fix the endings of each answer, best first, and keep the first fix that fits (for example *dodao → dodala* for a woman, *Vi → ti* for casual).
   - If neither works, it shows NLLB's top answer with a "had to guess" warning.

![Flowchart: NLLB writes 32 Serbian options. For each option in order: find the helper word sam or si, read the endings next to it for gender, read the words for "you" for formality, then Match asks "do all labels fit?" (yes: pick it, 37 of 40 test sentences; no: try the next option). If none of the 32 fit, Repair rewrites the endings and checks again (fits: use it, 2 of 40). Otherwise show NLLB's top answer with a "had to guess" warning (1 of 40).](docs/how-it-works.svg)

**Inside the rules.** Serbian shows gender in the word next to "sam" (I am) or "si" (you are): *proverio sam* is a man, *proverila sam* a woman. Formality shows in the word for "you": *Vi* / *Vaš* is formal, *ti* / *tvoj* casual. Match reads those words in each option, and Repair rewrites them when no option fits. Every rule and word list came from our Serbian speaker, and the notebook tests each rule on hand-written examples (50 for Match, 49 for Repair).

The models write Serbian in Cyrillic, so the notebook converts every output to Latin letter for letter before checking or scoring it.

**How we score:** chrF (a standard translation score from the sacrebleu library that compares our Serbian with the correct Serbian letter by letter), % with the right speaker or listener gender, % with the right formality (both read by `detect()`, the same code Match uses), and how often a fitting form is somewhere in NLLB's 32 options (the best the picker could do without repair).

## Results

On the 45 test rows, scored once after the rules were frozen (notebook section 7).

| System | chrF | Gender correct | Formality correct | All tested endings right |
|---|---|---|---|---|
| Baseline (through English) | 42.5 | 42.9% (9/21) | 63.6% (14/22) | 47.5% (19/40) |
| NLLB direct | 39.3 | 40.0% (8/20) | 84.2% (16/19) | 47.5% (19/40) |
| Ours (NLLB top 32 + picker) | 43.1 | 100.0% (26/26) | 100.0% (21/21) | 97.5% (39/40) |

Rows where `detect()` couldn't read the gender or formality at all are left out of that column (gender: 5 for the baseline, 6 for NLLB direct; formality: 3 for NLLB direct, 1 for ours). For ours, a fitting form was among NLLB's 32 options on 37 of 40 rows (92.5%). The picker matched 37, repaired 2 and had to guess on 1.

*Practice rows (15, the ones the rules were written on, so they flatter us), as baseline / NLLB direct / ours: chrF 54.5 / 35.6 / 35.7, gender 71.4% / 57.1% / 100.0%, formality 50.0% / 62.5% / 100.0%.*

**Headline finding:** the two usual routes mostly fall back to the man's form. They got the gender right on 9 of 21 and 8 of 20 test sentences; ours got 26 of 26. That is exactly the mistake our user can't spot on their own.

**Read these numbers carefully:**

- **Partly circular.** Gender and formality are graded by `detect()`, the same reader the picker uses to choose, so our 100% is partly built in. `detect()` did read all 45 of our own correct test sentences right.
- **Chance.** A bootstrap check (2,000 resamples of the 45 test rows) says our gender lead over NLLB direct is bigger than chance (+60.0 points, 95% interval +36.8 to +81.2). The formality lead isn't (+15.8 points, interval +0.0 to +33.3, which touches 0).
- **chrF** only shows the three systems are close. It compares letters, so it can't tell a wrong ending from a wrong word, and on the practice rows the baseline won it, 54.5 to 35.7.

**Human check (the fair test).** Our Serbian speaker is reading every test answer from all three systems by hand, for meaning and for endings. [TO FILL after the human check: meaning right X/45, endings right Y/40 for each system]

## Where it fails

Three of the five real misses we found on the test rows, each a different kind of failure (all five are in section 7 of the notebook):

1. **t30** Mandarin: 你先去休息吧 ("Get some rest first") / What we produced: *Ne, ne, ne, ne, …* ("no, no, no…") / Correct: *Idi prvo da se odmoriš.* / Why: NLLB broke and all 32 options were the same repeat, so nothing fit; our "had to guess" warning fired, but there was nothing good to give.
2. **t11** Mandarin: 我把货物都清点完了 ("I finished counting and checking the goods", a woman) / What we produced: *Ja sam završila čišćenje.* ("I finished cleaning") / Correct: *Završila sam prebrojavanje i proveru robe.* / Why: the woman's ending is right, but NLLB read 清点 "count and check" as 清 "clean", and our picker checks endings, not meaning.
3. **t08** Mandarin: 我昨天生病了 ("I got sick yesterday", a man) / What we produced: *Ja sam juče bolestan.* ("I am sick yesterday") / Correct: *Juče sam se razboleo.* / Why: the man's ending is right but the tense is broken, which our rules can't see; the route through English got this one exactly right.

## Limits

The full list, with examples, is in section 10 of the notebook.

- **Small test set:** 60 sentences, 15 practice and 45 test, so each test percentage moves by 2 to 3 points per sentence.
- **Endings, not words:** the picker can only choose among NLLB's 32 options and repair only changes endings, so a wrong word or a broken tense stays (t11, t08).
- **NLLB's own mistakes:** made-up words (*vinkar* for forklift, *Sastanao sam*), words and letters from neighbouring languages (Macedonian ѓ, Russian-looking *opozdao*, Croatian- or Bosnian-style phrasing), and once a breakdown into *Ne, ne, ne…* (t30).
- **The user has to say who's speaking and to whom.** The system doesn't guess gender or formality from the Mandarin.
- **Workplace sentences only:** short, one-part messages about work. We haven't tested long or casual text.
- **AI-drafted Mandarin:** drafted with an AI tool and then checked by a native speaker, so it may read more like textbook Mandarin than real messages.
- **A small model:** NLLB's 600M distilled version, the smallest one. We didn't test the bigger ones.
- **Non-commercial model:** NLLB is licensed CC BY-NC 4.0, so this can't be used in a paid product as it is.

## What we'd do next

1. Check meaning before endings: have the picker skip options with made-up or non-Serbian words (*vinkar*, *Sastanao*, *ѓubre*), since "right ending, wrong word" is our main failure.
2. Try the bigger NLLB models (1.3B and 3.3B), which might know workplace words like *viljuškar* (forklift), and write more test sentences so a formality gain can be told apart from chance.

## Files in this repo

| Path | What it is |
|---|---|
| [notebook/model.ipynb](notebook/model.ipynb) | The AI project. This is what judges open and run. |
| [notebook/model_check.ipynb](notebook/model_check.ipynb) | First check: do the three models load with no sign-in, how fast are they, and do NLLB's options include the forms we need? |
| [notebook/more_options.ipynb](notebook/more_options.ipynb) | Experiment: does NLLB's top 8, 16 or 32 include a form that fits the labels? |
| [data/test_sentences.csv](data/test_sentences.csv) | Our test set: Mandarin, English meaning, correct Serbian, the labels, and whether each row is for practice or testing. |
| [data/README.md](data/README.md) | How the test set was written, and the rules for filling it in. |
| [docs/plan.md](docs/plan.md) | The plan: the three systems, build order, notebook sections and timeline. |
| [docs/log.md](docs/log.md) | Decisions and real results, including failures. |
| [docs/challenge.md](docs/challenge.md) | The official brief, summarized: tracks, rules, submitting, judging. |
| [docs/competition.md](docs/competition.md) | Dates, judging and the before-we-submit checklist. |
| [app/demo.py](app/demo.py) | The demo page for the video (Gradio). It runs the notebook's section 8 code on one sentence and shows the three systems side by side. Changes no score. |
| [requirements.txt](requirements.txt) | Libraries, for running outside Colab. |

Earlier ideas we considered before picking this one are in [docs/kickoff-brief.md](docs/kickoff-brief.md) and [docs/data-options.md](docs/data-options.md).

## Sources and credits

**Pre-trained models** (from Hugging Face, used as they are, not retrained; licences checked on each model's page):

- [Helsinki-NLP/opus-mt-zh-en](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en) (baseline step 1: Mandarin → English), CC BY 4.0, by the Language Technology Research Group at the University of Helsinki (OPUS-MT)
- [Helsinki-NLP/opus-mt-tc-base-en-sh](https://huggingface.co/Helsinki-NLP/opus-mt-tc-base-en-sh) (baseline step 2: English → Serbian; the model covers Serbian, Croatian and Bosnian), CC BY 4.0, by the same group
- [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) (No Language Left Behind: Mandarin → Serbian, top 32 options), CC BY-NC 4.0, by Meta AI. Non-commercial use only: fine for a student contest project, not for a paid product.

**Data:** our own test set, [data/test_sentences.csv](data/test_sentences.csv): 60 workplace sentences. The Mandarin was drafted with Claude (an AI tool, see below) and then checked and corrected by our team's native Mandarin speaker, who also wrote the English meaning and the labels. The correct Serbian was written by our team's native Serbian speaker, without any translation tool. No outside dataset is used. The three demo sentences in the notebook's section 8 are new and were also drafted with Claude.

**Libraries** (everything in [requirements.txt](requirements.txt)): [numpy](https://numpy.org/), [pandas](https://pandas.pydata.org/), [matplotlib](https://matplotlib.org/), [PyTorch](https://pytorch.org/), [transformers](https://github.com/huggingface/transformers) (Hugging Face), [sentencepiece](https://github.com/google/sentencepiece) and [sacremoses](https://github.com/hplt-project/sacremoses) (used by the translation models to cut text into pieces), [sacrebleu](https://github.com/mjpost/sacrebleu) (the chrF score) and [scikit-learn](https://scikit-learn.org/) (listed in requirements.txt, but the final notebook doesn't use it). For the demo page only: [Gradio](https://www.gradio.app/) (Apache 2.0), which builds the web page in [app/demo.py](app/demo.py). Plus Python's built-in modules, and [Google Colab](https://colab.research.google.com/) to run the notebook.

**Tutorials:** none copied. The way we call each model (the `>>srp_Cyrl<<` tag, NLLB's language codes) follows the model pages linked above.

**AI tools:** [Claude](https://www.anthropic.com/claude) (by Anthropic), used through Claude Code:

- to draft the Mandarin test sentences and the demo sentences (our Mandarin speaker checked and corrected the test sentences);
- for code help: writing and explaining the notebook code;
- for debugging (for example, the broken output on Apple's GPU);
- to help draft the notebook's explanations and this write-up.

No AI tool wrote the correct Serbian answers: our Serbian speaker wrote them. Our Serbian speaker also checked and corrected every rule the picker uses.

## License

[TO FILL, optional: for example "Code: MIT. Test sentences: CC BY 4.0." or delete this section.]

<!-- Team decision: whether to license the repo at all. NLLB's non-commercial license
applies to the model, not to our code or our test sentences. -->
