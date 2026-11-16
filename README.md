# Lost in Translation: Mandarin to Serbian that keeps who's talking

Our project helps a Mandarin speaker writing to Serbian colleagues at work by taking a Mandarin sentence plus who is speaking, who is listening and how formal it is, and giving back Serbian with the right endings, or a warning when it had to guess.

**Track:** AI + Languages

## Try it

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/proelium27/veritas-ai-hackathon/blob/main/notebook/model.ipynb)

Click **Runtime → Run all**: no sign-in, keys or uploads; GPU optional; about 1.5 minutes on a CPU after a first model download. **Demo app** (optional): `python app/demo.py` ([how to run it](docs/details.md#demo-app)).

## The problem

In Serbian, words change with the speaker's gender and with politeness: a woman says *Proverila sam* ("I checked it"), a man *Proverio sam*; a friend gets *ti si*, a boss *Vi ste*. Mandarin rarely shows gender, and tools that go through English (one "you", no gendered verbs) lose both, so the Serbian usually comes out masculine.

Our user writes to Serbian colleagues, for example at a Chinese-run company in Serbia, and can't spot a wrong ending. Through English, a woman's "I already notified the driver" becomes a man's sentence (*Obavestio sam vozača*), and a polite question to a manager can come out casual.

## What we added

On top of the brief's NLLB + chrF project:

- **Our own test set:** 60 workplace sentences labelled for speaker gender, listener gender and formality (public benchmarks have no such labels), with correct Serbian from a native speaker.
- **Our picker and repair rules** for Serbian endings, checked by that speaker.
- **Our question:** can choosing among a model's own options fix what going through English loses, without retraining?
- **A human check** of every test answer, by that speaker.

NLLB usually knows the right form but doesn't rank it first: for 37 of 40 test sentences that check an ending, a fitting option was in its top 32.

## How it works

Three systems, from pre-trained models used as they are:

1. **Baseline (through English):** opus-mt-zh-en, then opus-mt-tc-base-en-sh, the way many apps work.
2. **NLLB direct:** Meta's NLLB translates Mandarin straight to Serbian; we take its top answer.
3. **Ours:** NLLB's top 32 answers, then our picker: **Match** takes the first whose endings fit the user's choices, **Repair** fixes the endings of the best one it can (*popravio → popravila*), and otherwise it warns "had to guess".

![Flowchart: the user enters a Mandarin sentence and sets speaker gender, listener gender and formality. NLLB writes 32 Serbian translations, ranked most to least likely. Take one option and check: labels fit? Yes: use this translation. No: sentences left out of the 32? Yes: try the next one. No: repair the best option. Labels fit now? Yes: use the repaired translation. No: use the best option with a "had to guess" warning. The Serbian translation is shown to the user.](docs/how-it-works.svg)

**The rules, in short:** gender shows in the word next to *sam* (I am) or *si* (you are), and formality in the word for "you" (*Vi*, *Vaš* formal; *ti*, *tvoj* casual). Match reads those words and Repair rewrites them. Every rule came from our Serbian speaker; the notebook tests them on 50 and 49 hand-written examples.

**Data:** [data/test_sentences.csv](data/test_sentences.csv), written by our team (see credits). We built the rules on 15 practice rows, froze them (commit `ad6b1a7`), then scored the 45 test rows once.

| Test row t09, said by a woman | Through English | NLLB direct | Ours | Correct |
|---|---|---|---|---|
| 我已经通知司机了 ("I already notified the driver") | Obavestio sam vozača. | Ja sam obavestio vozača. | Ja sam obavestila vozača. | Već sam obavestila vozača |

## Results

**Human check (the main result).** Our native Serbian speaker graded every system's 45 test answers by hand for **meaning** and for **endings** (speaker's gender, listener's gender, formality; 40 rows test one). Grades: [data/human_check.csv](data/human_check.csv); notebook section 7.1.

| System | Meaning right | Endings right | Both right |
|---|---|---|---|
| Baseline (through English) | **41/45** | 19/40 | 17/40 |
| NLLB direct | 23/45 | 19/40 | 11/40 |
| Ours (NLLB top 32 + picker) | 27/45 | **38/40** | **23/40** |

Ours gets the endings right twice as often as either usual route and is best when both must be right. The route through English keeps the meaning best: ours only chooses among NLLB's answers, and NLLB often picks the wrong word.

**Automatic scores** on the same 45 rows (notebook section 7):

| System | chrF | Gender correct | Formality correct | All tested endings right |
|---|---|---|---|---|
| Baseline (through English) | 42.5 | 42.9% (9/21) | 63.6% (14/22) | 47.5% (19/40) |
| NLLB direct | 39.3 | 40.0% (8/20) | 84.2% (16/19) | 47.5% (19/40) |
| Ours (NLLB top 32 + picker) | 43.1 | 100.0% (26/26) | 100.0% (21/21) | 97.5% (39/40) |

**Caveats:**

- **The automatic scores are partly circular:** `detect()`, which grades gender and formality, is the reader our picker chooses with. The human check is independent, and it agrees with `detect()` on 119 of 120 endings grades.
- **Small test:** 45 sentences, one grader. A bootstrap check says our gender lead over NLLB direct is bigger than chance (+60.0 points, 95% interval +36.8 to +81.2); our formality lead isn't (+15.8, interval +0.0 to +33.3).
- **A possible slip:** t20, ours *Da li si umoran?*, is word for word our correct Serbian but was marked wrong on endings; we count it as graded.

## Where it fails

Three of the five real misses in notebook section 7 (all five graded wrong in meaning):

1. **t30** 你先去休息吧 ("Get some rest first"): all 32 NLLB options were *Ne, ne, ne…* ("no, no, no"); the warning fired, but nothing good was left.
2. **t11** 我把货物都清点完了 ("I finished counting the goods", a woman): *Ja sam završila čišćenje*, "I finished cleaning". Right ending, wrong word.
3. **t08** 我昨天生病了 ("I got sick yesterday", a man): *Ja sam juče bolestan*, "I am sick yesterday". Right ending, broken tense.

## What we'd do next

1. Check meaning before endings: skip options with made-up or non-Serbian words (*vinkar*, *Sastanao*, *ѓubre*), our main failure.
2. Try the bigger NLLB models, which might know words like *viljuškar* (forklift), and write more test sentences.

## More detail

[docs/details.md](docs/details.md): files, data counts, practice-row results, the full rules, all our limits and the demo app. Running record, failures included: [docs/log.md](docs/log.md).

## Sources and credits

**Pre-trained models** (Hugging Face, used as they are; licences checked on each model page):

- [Helsinki-NLP/opus-mt-zh-en](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en) (baseline step 1), CC BY 4.0, University of Helsinki (OPUS-MT)
- [Helsinki-NLP/opus-mt-tc-base-en-sh](https://huggingface.co/Helsinki-NLP/opus-mt-tc-base-en-sh) (baseline step 2), CC BY 4.0, the same group
- [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) (NLLB direct and ours), CC BY-NC 4.0, Meta AI. Non-commercial use only.

**Data:** our own: [data/test_sentences.csv](data/test_sentences.csv) and [data/human_check.csv](data/human_check.csv). Mandarin drafted with Claude and checked by our native Mandarin speaker; correct Serbian and grades by our native Serbian speaker, without translation tools. No outside dataset.

**Libraries** ([requirements.txt](requirements.txt)): [numpy](https://numpy.org/), [pandas](https://pandas.pydata.org/), [matplotlib](https://matplotlib.org/), [PyTorch](https://pytorch.org/), [transformers](https://github.com/huggingface/transformers), [sentencepiece](https://github.com/google/sentencepiece), [sacremoses](https://github.com/hplt-project/sacremoses), [sacrebleu](https://github.com/mjpost/sacrebleu) (chrF), and [Gradio](https://www.gradio.app/) (Apache 2.0) for the demo page only. Run on [Google Colab](https://colab.research.google.com/). **Tutorials:** none copied; model calls follow the model pages.

**Video images** (demo video only; all rights stay with their owners, used for a non-commercial student project): [Serbia map](https://ichef.bbci.co.uk/ace/standard/976/cpsprodpb/14FB0/production/_128363958_bbcm_serbia_country_profile_map_200123.png) (BBC); [photo](https://cdn.sanity.io/images/nxpteyfv/goguides/9975e53bddbaab08fd1f6d2e02d321a78aa6c4c2-1600x1067.jpg) (Go Guides); [photo](https://cds.chinadaily.com.cn/dams/capital/image/202201/09/61da44e5e4b013b65bf0490f.jpg) (China Daily); [photo](https://cepa.org/wp-content/uploads/2022/09/2021-01-16T091258Z_192625533_RC2X8L98ML29_RTRMADP_3_HEALTH-CORONAVIRUS-SERBIA-CHINA-VACCINE-1-8.jpg) (Reuters, via CEPA); and one image generated with ChatGPT (OpenAI).

**AI tools:** [Claude](https://www.anthropic.com/claude) (Anthropic), through Claude Code: drafting the Mandarin test and demo sentences, code help and debugging, and drafting the notebook's explanations and this write-up. [ChatGPT](https://chatgpt.com/) (OpenAI): one image in the demo video. No AI tool wrote the correct Serbian or the grades.

## License

Code: MIT (see [LICENSE](LICENSE)). The NLLB model keeps its own CC BY-NC 4.0 licence.
