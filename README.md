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

Our project helps [TO FILL: the specific user from "The problem", a few words] by taking a Mandarin sentence plus who is speaking, who is listening and how formal it is, and giving back Serbian with the right endings, or a warning when it had to guess.

**Track:** AI + Languages

## Try it

Main project (this is what to run):
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/proelium27/veritas-ai-hackathon/blob/main/notebook/model.ipynb)

Model check (our first test that all three models load and run):
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/proelium27/veritas-ai-hackathon/blob/main/notebook/model_check.ipynb)

Click **Runtime → Run all**. It needs no sign-in, keys or uploads. A GPU (Runtime → Change runtime type → T4 GPU) makes the translation faster but isn't required. A full run takes about [TO FILL: minutes from a fresh-Colab Run all, with and without GPU] minutes; the first run spends a few of those downloading the models.

While the repo is private, the buttons only work if you've connected Colab to GitHub and allowed private repositories (Colab: File → Open notebook → GitHub).

## The problem

In Serbian, the words change depending on who is speaking and who they're talking to. A woman says "Proverila sam" (I checked it) and a man says "Proverio sam". You say "ti si" to a friend but "Vi ste" to your boss. Mandarin shows politeness (您 is the polite "you", 你 the casual one) but usually doesn't show the speaker's gender at all.

Many translation tools go Mandarin → English → Serbian. English has one "you" and no gendered verbs, so on the way through, the gender and the politeness are lost, and the Serbian usually comes out masculine and at a guessed level of politeness.

[TO FILL: 2-3 sentences. Name one specific person, the moment they'd use this, and what goes wrong for them today. Pick one of the two options in the comment below.]

<!--
User story options (the team picks one and deletes the other):
A. The general workplace user: a Mandarin speaker writing to Serbian colleagues at
   work, for example at one of the Chinese-run companies in Serbia, who doesn't read
   Serbian well enough to notice a wrong ending, and would come across as rude or as
   the wrong gender without knowing it.
B. One specific person: a woman from China working as a supervisor or engineer at a
   factory in Serbia, whose messages to her Serbian team come out masculine ("Proverio
   sam") and too casual or too formal, and who can't tell.
(Option B is a sharper version of A, written for this template. If the team had a
different second option in mind, replace B with it.)
-->

## What we built

**Input:** a Mandarin sentence, plus three choices: who is speaking (man or woman), who you're talking to (man, woman or a group) and whether it's formal or casual.

**Output:** a Serbian sentence in Latin letters with the right endings, or NLLB's best answer with a "had to guess" warning when none of its options fit the choices.

**One example:**

| Mandarin | Through English (baseline) | NLLB direct | Ours | Correct Serbian |
|---|---|---|---|---|
| 我检查过了 ("I checked it", said by a woman) | Proverio sam. | Proverio sam. | [TO FILL: our output for this row] | Proverila sam. |

<!-- Replace this row with a real one from the final notebook run (a practice row,
or a test row once the test results are unlocked). The two "Proverio sam." outputs
come from the early model check, not the final run. -->

## What we added

The brief's "Translation quality test" uses NLLB and chrF on a public benchmark. What's ours:

- **Our own test set:** 60 short workplace sentences we wrote for this project, each with the Mandarin, the English meaning, the correct Serbian, and labels for speaker gender, listener gender and formality. Public benchmarks don't label who is speaking or listening, so they can't measure this.
- **Our picker and repair rules:** rules about Serbian word endings that read NLLB's options and choose the one that matches the speaker, listener and formality, plus [TO FILL: one line on the repair rules if we add them, or delete this part].
- **Our question:** does going through English lose speaker gender and formality, and can choosing among a model's own options fix it without retraining anything?

[TO FILL: 1-2 sentences on anything else we added or found along the way, or delete.]

## How it works

### Data

- **Our test set:** 60 sentences in [data/test_sentences.csv](data/test_sentences.csv), loaded from the repo's public web address. [TO FILL: final counts, for example "30 woman / 30 man speakers, N formal / N casual, 6 control sentences with no gender or formality".]
- **How we made it:** the Mandarin was drafted with an AI tool, then read and corrected by a native Mandarin speaker, who also wrote the English meaning and the labels. The correct Serbian was written by a native Serbian speaker from the English meaning and the labels, without any translation app.
- **Split:** 15 practice rows and 45 test rows, fixed before any model saw them. We built the picker rules on the practice rows only and looked at test results once, after the rules were final. [TO FILL: say here if we changed anything after seeing test results.]
- **Script:** the correct Serbian is in Latin letters with č, ć, š, ž, đ, dž.

### Model

We use three pre-trained translation models as they are (no training) and compare three systems on the same sentences:

1. **Baseline (through English):** Mandarin → English with opus-mt-zh-en, then English → Serbian with opus-mt-tc-base-en-sh. This is how many apps work.
2. **NLLB direct:** Meta's NLLB model translates Mandarin straight to Serbian, and we take its top answer.
3. **Ours:** NLLB lists its top 32 answers. Our picker checks the Serbian endings of each one and picks the first that matches the speaker, listener and formality. If none matches, we use NLLB's top answer and flag it "had to guess". [TO FILL: one sentence on the repair rules if we add them: what they change and when they run.]

The models write Serbian in Cyrillic, so the notebook converts every output to Latin letter for letter before checking or scoring it.

**How we score:** chrF (a standard translation score from the sacrebleu library that compares our Serbian with the correct Serbian letter by letter), % with the right speaker or listener gender, % with the right formality, and how often a fitting form is somewhere in NLLB's 32 options (the best the picker could ever do). [TO FILL: add "had to guess" flag accuracy here if the notebook reports it.]

## Results

On the 45 test rows only.

| System | chrF | Gender correct % | Formality correct % | Right form among 32 % |
|---|---|---|---|---|
| Baseline (through English) | [TO FILL] | [TO FILL] | [TO FILL] | n/a |
| NLLB direct | [TO FILL] | [TO FILL] | [TO FILL] | [TO FILL] |
| Ours (NLLB top 32 + picker) | [TO FILL] | [TO FILL] | [TO FILL] | [TO FILL] |

**Headline finding:** [TO FILL: 1-2 sentences with the one number that matters most, for example how often each system got a woman speaker right, and what it means for the user.]

<!-- Early observation from docs/log.md (more-options experiment, Sat ~1:45 PM): NLLB's top
answer fit 0 of 12 woman speakers, and with its top 32 options a fitting option existed for
91% of rows (49 of 54). That was on AI-drafted sentences with rough detectors and NO
human-checked Serbian, practice and test rows together. Don't quote it as a result; use the
final test-row numbers instead. -->

## Where it fails

[TO FILL: 3-5 real misses from the test rows, each in the format below. One line each for "why". Pick different kinds of failure if you can (a wrong word that still has the right ending, no option fitting, the picker choosing the wrong one, a control sentence going wrong).]

1. [TO FILL] Mandarin: ... / What we produced: ... / Correct: ... / Why: ...
2. [TO FILL] Mandarin: ... / What we produced: ... / Correct: ... / Why: ...
3. [TO FILL] Mandarin: ... / What we produced: ... / Correct: ... / Why: ...
4. [TO FILL, optional] Mandarin: ... / What we produced: ... / Correct: ... / Why: ...
5. [TO FILL, optional] Mandarin: ... / What we produced: ... / Correct: ... / Why: ...

## Limits

- **Small test set:** 60 sentences, 45 of them test rows, so each percentage moves by about 2 points per sentence.
- **Workplace sentences only:** short, one-clause sentences about work. We haven't tested long or casual text.
- **The user has to say who's speaking and to whom.** The system doesn't guess gender or formality from the Mandarin; it needs the three choices.
- **Non-commercial model:** NLLB is licensed CC BY-NC 4.0, so this can't be used in a paid product as it is.
- **Cyrillic converted to Latin:** the models write Cyrillic; we convert letter for letter, which is exact for Serbian but means we never score the models' own Latin output.
- **AI-drafted Mandarin:** the Mandarin sentences were drafted with an AI tool and then checked by a native speaker, so they may read more like textbook Mandarin than real workplace messages.
- **Fitting endings aren't always right meanings:** the picker checks endings, so it can pick an option with the right gender but the wrong word.
- [TO FILL, optional: any other limit we found.]

## What we'd do next

1. [TO FILL: one concrete next step, one sentence.]
2. [TO FILL, optional: a second next step, one sentence.]

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
| [requirements.txt](requirements.txt) | Libraries, for running outside Colab. |

Earlier ideas we considered before picking this one are in [docs/kickoff-brief.md](docs/kickoff-brief.md) and [docs/data-options.md](docs/data-options.md).

## Sources and credits

**Pre-trained models** (all from Hugging Face, used as they are, not retrained):

- [Helsinki-NLP/opus-mt-zh-en](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en) (Mandarin → English), CC BY 4.0, by the Language Technology Research Group at the University of Helsinki
- [Helsinki-NLP/opus-mt-tc-base-en-sh](https://huggingface.co/Helsinki-NLP/opus-mt-tc-base-en-sh) (English → Serbo-Croatian, used for Serbian Cyrillic), CC BY 4.0, by the same group
- [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) (No Language Left Behind, Mandarin → Serbian), CC BY-NC 4.0 (non-commercial use), by Meta AI

**Data:** the test sentences in [data/test_sentences.csv](data/test_sentences.csv) were written and labelled by our team for this project (the Mandarin drafted with an AI tool and corrected by a native speaker; the Serbian written by a native speaker without translation tools). No outside dataset is used.

**Libraries:** [numpy](https://numpy.org/), [pandas](https://pandas.pydata.org/), [scikit-learn](https://scikit-learn.org/), [matplotlib](https://matplotlib.org/), [transformers](https://github.com/huggingface/transformers) (Hugging Face), [PyTorch](https://pytorch.org/), [sacrebleu](https://github.com/mjpost/sacrebleu) (for the chrF score), [sentencepiece](https://github.com/google/sentencepiece) and [sacremoses](https://github.com/hplt-project/sacremoses) (used by the translation models to split text into pieces). [TO FILL: check this list against the notebook's imports and remove any we don't use.]

**Tutorials:** [TO FILL: any tutorial or docs page we copied code from, with a link, or "None".]

**AI tools** (name each tool and exactly what we used it for):

- [TO FILL: tool]: used to draft the Mandarin test sentences, which a native Mandarin speaker then checked and corrected.
- [TO FILL: tool, e.g. Claude Code]: used to [TO FILL: what, e.g. write and debug notebook code, which we read and can explain].
- [TO FILL, optional: tool]: used to [TO FILL: what].

## License

[TO FILL, optional: for example "Code: MIT. Test sentences: CC BY 4.0." or delete this section.]

<!-- Team decision: whether to license the repo at all. NLLB's non-commercial license
applies to the model, not to our code or our test sentences. -->
