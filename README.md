# Blok 70: Mandarin to Serbian that keeps who's talking

*Named after Blok 70 in New Belgrade, the neighbourhood best known for Belgrade's Chinese community and market, where Mandarin and Serbian meet every day.*

For a Mandarin speaker writing to Serbian colleagues at work: type a Mandarin sentence, say who is speaking, who is listening and how formal it is, and get Serbian with the right endings, or a warning when it had to guess.

**Track:** AI + Languages

## Try it

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/proelium27/veritas-ai-hackathon/blob/main/notebook/model.ipynb)

**Demo video (2 min):** [watch on YouTube](https://www.youtube.com/watch?v=aC2AZEAdeUs)

Click **Runtime → Run all**. No sign-in, keys or uploads; a GPU is optional. The first run in a fresh Colab session also downloads about 3 GB of models (a few minutes); after that it takes about 1.5 minutes on a CPU. **Demo app** (optional): `python app/demo.py` ([how to run it](docs/details.md#demo-app)).

## The problem

In Serbian, words change with the speaker's gender and with politeness. A woman says *Proverila sam* ("I checked it"), a man *Proverio sam*. A friend gets *ti si*, a boss *Vi ste*. Mandarin rarely shows gender, and tools that go through English (one "you", no gendered verbs) lose both, so the Serbian usually comes out masculine.

Our user writes to Serbian colleagues, for example at a Chinese-run company in Serbia, and can't spot a wrong ending. Through English, a woman's "I already notified the driver" turns into a man's sentence (*Obavestio sam vozača*), and a polite question to a manager can come out casual.

## What we built

A one-sentence translator. In: Mandarin, plus who is speaking (man or woman), who is listening (man, woman or a group) and formal or casual. Out: Serbian in Latin letters with matching endings, or NLLB's best answer with a "had to guess" warning.

## What we added

We started from the brief's suggested "Translation quality test" (NLLB, scored with chrF) and added:

- **Our own test set:** 60 workplace sentences labelled for speaker gender, listener gender and formality (FLORES+, the brief's suggested dataset, has no such labels), with correct Serbian from a native speaker.
- **Our picker and repair rules** for Serbian endings, checked by that speaker.
- **Our question:** can choosing among a model's own options fix what going through English loses, without retraining?
- **A human check** of every test answer, by that speaker.

NLLB usually knows the right form but doesn't rank it first: for 37 of the 40 test sentences that check an ending, a fitting option was in its top 32. Repair fixed 2 more, which is why ours gets 39 of 40 below.

## How it works

Three systems, from pre-trained models used as they are:

1. **Baseline (through English):** opus-mt-zh-en, then opus-mt-tc-base-en-sh.
2. **NLLB direct:** Meta's NLLB translates Mandarin straight to Serbian, and we take its top answer.
3. **Ours:** NLLB's top 32 answers, then our picker. **Match** takes the first whose endings fit the user's choices. Otherwise **Repair** fixes the endings of the best one it can (*popravio → popravila*). If that fails too, it shows NLLB's top answer and warns "had to guess".

![Flowchart: the user enters a Mandarin sentence and sets speaker gender, listener gender and formality. NLLB writes 32 Serbian translations, ranked most to least likely. Take one option and check: labels fit? Yes: use this translation. No: sentences left out of the 32? Yes: try the next one. No: repair the best option. Labels fit now? Yes: use the repaired translation. No: use the best option with a "had to guess" warning. The Serbian translation is shown to the user.](docs/how-it-works.svg)

**The rules, in short:** gender shows in the word next to *sam* (I am) or *si* (you are), and formality in the word for "you" (*Vi*, *Vaš* formal; *ti*, *tvoj* casual). Match reads those words and Repair rewrites them. Our Serbian speaker checked and corrected every rule, and the notebook tests them on 50 and 49 hand-written examples.

**Data:** [data/test_sentences.csv](data/test_sentences.csv): Claude drafted the Mandarin, our Mandarin speaker checked it, and our Serbian speaker wrote the correct Serbian (see credits). We built the rules on 15 practice rows, froze them (commit `ad6b1a7`), then scored the 45 test rows once.

| Test row t09, said by a woman | Through English | NLLB direct | Ours | Correct |
|---|---|---|---|---|
| 我已经通知司机了 ("I already notified the driver") | Obavestio sam vozača. | Ja sam obavestio vozača. | Ja sam obavestila vozača. | Već sam obavestila vozača |

## Results

**Human check (the main result).** Our native Serbian speaker graded all 45 test answers from each system by hand, for **meaning** and for **endings** (speaker's gender, listener's gender, formality; 40 of the rows test an ending). Grades: [data/human_check.csv](data/human_check.csv); notebook section 7.1.

| System | Meaning right | Endings right | Both right |
|---|---|---|---|
| Baseline (through English) | **41/45** | 19/40 | 17/40 |
| NLLB direct | 23/45 | 19/40 | 11/40 |
| Ours (NLLB top 32 + picker) | 27/45 | **38/40** | **23/40** |

Ours gets the endings right twice as often as either usual route and has the most answers with both right. The route through English keeps the meaning best, because ours can only choose among NLLB's answers and NLLB often picks the wrong word.

**Automatic scores** on the same 45 rows (notebook section 7):

| System | chrF | Gender correct | Formality correct | All tested endings right |
|---|---|---|---|---|
| Baseline (through English) | 42.5 | 42.9% (9/21) | 63.6% (14/22) | 47.5% (19/40) |
| NLLB direct | 39.3 | 40.0% (8/20) | 84.2% (16/19) | 47.5% (19/40) |
| Ours (NLLB top 32 + picker) | 43.1 | 100.0% (26/26) | 100.0% (21/21) | 97.5% (39/40) |

Totals differ by system because `detect()` skips rows where it can't read the ending in that system's answer.

**Caveats:**

- **The automatic gender and formality scores are partly circular.** They are graded by `detect()`, the same code our picker uses to choose. The human check doesn't use `detect()`, and the two agree on 119 of 120 endings grades.
- **The human check wasn't blind:** our Serbian speaker saw which system wrote each answer, and also wrote the correct Serbian and checked our rules.
- **The test is small:** 45 sentences and one grader. A bootstrap check says our gender lead over NLLB direct is bigger than chance (+60.0 points, 95% interval +36.8 to +81.2). Our formality lead isn't (+15.8, interval +0.0 to +33.3).
- **One grade may be a slip.** For t20, ours gave *Da li si umoran?*, word for word our correct Serbian, but it was marked wrong on endings. We count it as graded.

## Where it fails

Three of the five real misses in notebook section 7 (all five graded wrong in meaning):

1. **t30** 你先去休息吧 ("Get some rest first"): all 32 NLLB options were *Ne, ne, ne…* ("no, no, no"). The warning fired, but there was nothing good left to pick.
2. **t11** 我把货物都清点完了 ("I finished counting the goods", said by a woman): *Ja sam završila čišćenje*, "I finished cleaning". The ending is right and the word is wrong.
3. **t08** 我昨天生病了 ("I got sick yesterday", said by a man): *Ja sam juče bolestan*, "I am sick yesterday". The ending is right and the tense is broken.

## What we'd do next

1. Check meaning before endings: skip options with made-up or non-Serbian words (*vinkar*, *Sastanao*, *ѓubre*). Those are our main failure.
2. Try the bigger NLLB models, which might know words like *viljuškar* (forklift), and write more test sentences.

## More detail

[docs/details.md](docs/details.md): files, data counts, practice-row results, the full rules, all our limits and the demo app. Running record, failures included: [docs/log.md](docs/log.md).

## Sources and credits

**Pre-trained models** (from Hugging Face, used as they are; we checked each licence on the model page):

- [Helsinki-NLP/opus-mt-zh-en](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en) (baseline step 1), CC BY 4.0, University of Helsinki (OPUS-MT)
- [Helsinki-NLP/opus-mt-tc-base-en-sh](https://huggingface.co/Helsinki-NLP/opus-mt-tc-base-en-sh) (baseline step 2), CC BY 4.0, the same group
- [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) (NLLB direct and ours), CC BY-NC 4.0, Meta AI. Non-commercial use only.

**Data:** our own, [data/test_sentences.csv](data/test_sentences.csv) and [data/human_check.csv](data/human_check.csv). Claude drafted the Mandarin, and our native Mandarin speaker checked and corrected it. Our native Serbian speaker wrote the correct Serbian and the grades without translation tools. We used no outside dataset.

**Libraries** ([requirements.txt](requirements.txt)): [numpy](https://numpy.org/), [pandas](https://pandas.pydata.org/), [matplotlib](https://matplotlib.org/), [PyTorch](https://pytorch.org/), [transformers](https://github.com/huggingface/transformers), [sentencepiece](https://github.com/google/sentencepiece), [sacremoses](https://github.com/hplt-project/sacremoses) and [sacrebleu](https://github.com/mjpost/sacrebleu) (chrF), plus [Gradio](https://www.gradio.app/) (Apache 2.0) for the demo page only. We ran it on [Google Colab](https://colab.research.google.com/). **Tutorials:** we copied none; the model calls follow the model pages.

**Video images** (demo video only; all rights stay with their owners, used for a non-commercial student project): [Serbia map](https://ichef.bbci.co.uk/ace/standard/976/cpsprodpb/14FB0/production/_128363958_bbcm_serbia_country_profile_map_200123.png) (BBC); [photo](https://cdn.sanity.io/images/nxpteyfv/goguides/9975e53bddbaab08fd1f6d2e02d321a78aa6c4c2-1600x1067.jpg) (Go Guides); [photo](https://cds.chinadaily.com.cn/dams/capital/image/202201/09/61da44e5e4b013b65bf0490f.jpg) (China Daily); [photo](https://cepa.org/wp-content/uploads/2022/09/2021-01-16T091258Z_192625533_RC2X8L98ML29_RTRMADP_3_HEALTH-CORONAVIRUS-SERBIA-CHINA-VACCINE-1-8.jpg) (Reuters, via CEPA); and one image made with ChatGPT (OpenAI).

**AI tools:** [Claude](https://www.anthropic.com/claude) (Anthropic), through Claude Code, for drafting the Mandarin test and demo sentences, for code help and debugging, and for drafting the notebook's explanations and this write-up. [ChatGPT](https://chatgpt.com/) (OpenAI) made one image in the demo video. No AI tool wrote the correct Serbian or the grades.

## License

Code: MIT (see [LICENSE](LICENSE)). The NLLB model keeps its own CC BY-NC 4.0 licence.
