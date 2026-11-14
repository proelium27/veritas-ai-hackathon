# Lost in Translation: Mandarin to Serbian that keeps who's talking

**Track:** AI + Languages · Veritas AI International High School Hackathon, Nov 14-15, 2026.

## What it does

In Serbian, the words change depending on who is speaking and who they're talking to. A woman says "Проверила сам" (I checked it) and a man says "Проверио сам". You say "ти си" to a friend but "Ви сте" to your boss. Mandarin shows politeness (您 is the polite "you", 你 the casual one) but usually doesn't show the speaker's gender at all.

Many translation tools go Mandarin → English → Serbian. English has one "you" and no gendered verbs, so on the way through, the gender and the politeness are lost, and the Serbian usually comes out masculine and at a guessed level of politeness.

**Who it helps:** a Mandarin speaker writing to Serbian colleagues at work, for example someone at one of the Chinese-run companies in Serbia, who doesn't read Serbian well enough to notice a wrong ending, and who would come across as rude or as the wrong gender without knowing it.

**Input → output:** you type a Mandarin sentence and say who is speaking (man or woman), who you're talking to (man or woman) and whether it's formal or casual. You get back a Serbian sentence with the right endings, or a warning when the model couldn't find a version that fits and had to guess.

**How it works:** we compare three systems on the same test sentences, which we wrote ourselves:

1. **Baseline:** Mandarin → English → Serbian, with two Helsinki-NLP translation models.
2. **Direct:** Meta's NLLB model translates Mandarin straight to Serbian (its top answer).
3. **Ours:** NLLB lists its top 8 answers, and our rules about Serbian word endings pick the first one that matches the speaker, listener and formality. If none matches, it uses NLLB's top answer and says it had to guess.

**What's ours:** the test set (60-80 workplace sentences with Mandarin, the English meaning, the correct Serbian, and labels for speaker gender, listener gender and formality), the picker rules, and the question of whether going through English is what breaks these.

## Open the notebooks in Colab

Main project (this is what to run):
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/proelium27/veritas-ai-hackathon/blob/main/notebook/model.ipynb)

Model check (our first test that all three models load and run):
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/proelium27/veritas-ai-hackathon/blob/main/notebook/model_check.ipynb)

Click **Runtime → Run all**. It needs no sign-in, keys or uploads. A GPU (Runtime → Change runtime type → T4 GPU) makes the translation faster but isn't required. The first run downloads the models, which takes a few minutes.

While the repo is private, the buttons only work if you've connected Colab to GitHub and allowed private repositories (Colab: File → Open notebook → GitHub).

## What's in here

| Path | What it is |
|---|---|
| [notebook/model.ipynb](notebook/model.ipynb) | The AI project. This is what judges open and run. |
| [notebook/model_check.ipynb](notebook/model_check.ipynb) | First check: do the three models load with no sign-in, how fast are they, and do NLLB's 8 options include the forms we need? |
| [data/test_sentences.csv](data/test_sentences.csv) | Our test set: Mandarin, English meaning, correct Serbian, the labels, and whether each row is for practice or testing. |
| [docs/writeup.md](docs/writeup.md) | The one-page write-up. |
| [docs/plan.md](docs/plan.md) | The plan: the three systems, build order, notebook sections and timeline. |
| [docs/log.md](docs/log.md) | Decisions and real results, including failures. |
| [docs/challenge.md](docs/challenge.md) | The official brief, summarized: tracks, rules, submitting, judging. |
| [docs/competition.md](docs/competition.md) | Dates, judging and the before-we-submit checklist. |
| [docs/kickoff-brief.md](docs/kickoff-brief.md) | Earlier ideas we considered before picking this one. |
| [docs/data-options.md](docs/data-options.md) | Datasets we checked for the earlier ideas. |
| requirements.txt | Libraries, for running outside Colab. |

## Results

To be filled in from the notebook, on the test rows only: chrF score, % right speaker gender, % right formality, how often the right form was among NLLB's 8 options, how often the "had to guess" warning was right, and the worst misses.

## Credits

**Pre-trained models** (all from Hugging Face, used as they are, not retrained):

- [Helsinki-NLP/opus-mt-zh-en](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en) (Mandarin → English), CC BY 4.0, by the Language Technology Research Group at the University of Helsinki
- [Helsinki-NLP/opus-mt-tc-base-en-sh](https://huggingface.co/Helsinki-NLP/opus-mt-tc-base-en-sh) (English → Serbo-Croatian, used for Serbian Cyrillic), CC BY 4.0, by the same group
- [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) (No Language Left Behind, Mandarin → Serbian), CC BY-NC 4.0 (non-commercial use), by Meta AI

**Data:** the test sentences in `data/test_sentences.csv` were written and labelled by our team for this project.

**Libraries:** [numpy](https://numpy.org/), [pandas](https://pandas.pydata.org/), [scikit-learn](https://scikit-learn.org/), [matplotlib](https://matplotlib.org/), [transformers](https://github.com/huggingface/transformers) (Hugging Face), [PyTorch](https://pytorch.org/), [sacrebleu](https://github.com/mjpost/sacrebleu) (for the chrF score), [sentencepiece](https://github.com/google/sentencepiece) and [sacremoses](https://github.com/hplt-project/sacremoses) (used by the translation models to split text into pieces).

**AI tools:** to be filled in: each tool and what we used it for.
