# Team plan

Source: the "Our plan" tab of the team Google Doc, cleaned up, then switched to our final project, "Lost in Translation", on Sat Nov 14. Earlier ideas are recorded in [kickoff-brief.md](kickoff-brief.md) and [log.md](log.md); they are no longer the plan.

## The project (filled in at kickoff)

- Tracks: Health, Finance, Climate, Languages (pick one). Full brief in [challenge.md](challenge.md).
- Challenge: one AI project for one track. Show who it's for, input → output, a baseline comparison, and where it fails. Suggested projects are fine, but we must add our own user, data or question.
- **Track:** AI + Languages
- **Idea:** "Lost in Translation". A Mandarin speaker writing to a Serbian colleague at work needs the Serbian to show who is speaking (man or woman), who they're talking to (man or woman) and how polite it is (formal 您 / Ви or informal 你 / ти). Apps that route through English lose all three, so the Serbian often comes out masculine and at the wrong politeness. We translate Mandarin straight to Serbian, have the model list its top 8 options, and use rules about Serbian word endings to pick the option that matches; when none matches, we say so instead of guessing silently.
- **Our own data and question (what's new):** our own test set of 60-80 workplace sentences, written by the team, each labelled with speaker gender, listener gender and formality. The question: does going through English break these, and can a simple picker fix them?
- **Data and models** (all load in Colab with no sign-in; checked in [model_check.ipynb](../notebook/model_check.ipynb)):

| What | Link | License | Used for |
|---|---|---|---|
| Our test set | [data/test_sentences.csv](../data/test_sentences.csv), loaded from the repo's public raw URL | Ours | Every score in the notebook |
| opus-mt-zh-en | [Helsinki-NLP/opus-mt-zh-en](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en) | CC BY 4.0 | Baseline, step 1: Mandarin → English |
| opus-mt-tc-base-en-sh | [Helsinki-NLP/opus-mt-tc-base-en-sh](https://huggingface.co/Helsinki-NLP/opus-mt-tc-base-en-sh) | CC BY 4.0 | Baseline, step 2: English → Serbian (input starts with `>>srp_Cyrl<<`) |
| NLLB-200 distilled 600M | [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) | CC BY-NC 4.0 (non-commercial; fine for a school contest) | Direct Mandarin → Serbian (`zho_Hans` → `srp_Cyrl`), top 1 and top 8 |

- **Where to submit:** the Airtable form at https://airtable.com/appypCyHN77hElIcS/shrXA5VBFdugmoXl6. One person submits; resubmitting is allowed.

## The three systems we compare

All three translate the same test sentences, and all are scored the same way.

1. **Baseline (through English):** Mandarin → English with opus-mt-zh-en, then English → Serbian with opus-mt-tc-base-en-sh. This is how many apps work, and it's what we expect to lose gender and formality.
2. **Direct:** NLLB translates Mandarin straight to Serbian and we take its top answer.
3. **Ours (direct + picker):** NLLB gives its top 8 answers. A rule-based picker reads the Serbian endings (for example -о vs -ла for "I did", Ви/сте vs ти/си for "you") and picks the first answer that matches the sentence's known speaker, listener and formality. If none matches, it uses NLLB's top answer and flags it "had to guess".

**Fair-test rule:** Adam writes the picker's rules using only the ~20 rows marked "practice". The other rows are the locked "test" rows. Nobody looks at test scores until the rules are final; once we've seen them, we don't change the rules to chase a better number (or, if we do, we say so in the log and the write-up).

**How we score:** chrF (a standard translation score from the sacrebleu library, comparing our Serbian to Adam's correct Serbian letter by letter), % with the right speaker gender, % with the right formality, how often the right form is somewhere in NLLB's 8 options (the best the picker could ever do), how often the "had to guess" flag is right, and the 3-5 worst misses shown side by side with why.

**Optional improvement (Phase 6):** add a gender hint to the Mandarin input (for example 她说： "she said:") and check whether NLLB then gets the gender right on its own.

## Who does what

- **Adam (Serbian):** writes the correct Serbian (Cyrillic) for every test sentence, and the picker's rules about Serbian endings, using only the practice rows. Checks that options make sense in meaning, not just endings.
- **David (Mandarin):** writes the Mandarin sentences, their English meaning, and the labels (speaker gender, listener gender, formality, practice/test).
- **Caleb (code):** the notebook: loading the models and data, running the three systems, scoring, and the demo cell.
- **Whole team:** the write-up, the video, the final checks and submitting. All three of us must be able to explain every part.

The day-to-day checklist lives in the team Google Doc "Lost in Translation: Team Checklist".

## Build order

| Phase | What | Status |
|---|---|---|
| 0. Lock it in | Track, idea, roles and the three systems agreed | Done |
| 1. Model check | All three models load in Colab with no sign-in; NLLB's 8 options do include the feminine and formal forms ([model_check.ipynb](../notebook/model_check.ipynb), results in [log.md](log.md)) | Done |
| 2. Test set | David writes 60-80 workplace sentences with labels; Adam writes the correct Serbian; ~20 rows marked practice, the rest test; saved as `data/test_sentences.csv` | In progress |
| 3. Notebook | Load the CSV, run the baseline and NLLB direct on every row, score them | To do |
| 4. Picker | Adam's rules on the practice rows; NLLB top 8 + picker on every row | To do |
| 5. Honest testing | Score all three on the test rows only; flag accuracy; 3-5 worst misses with reasons; log the numbers, including failures | To do |
| 6. Optional improvement | Gender hint in the Mandarin input; report it as a separate row in the results | Only if time |
| 7. Deliverables | Demo cell, limits and credits, fresh-Colab Run all check, write-up, video, submit | To do |

## Repo layout

```
README.md                 what it does, how to run it, results, credits
requirements.txt          libraries to install (for running outside Colab)
notebook/model.ipynb      the AI part judges run in Colab
notebook/model_check.ipynb  Phase 1: do the three models load and run?
data/test_sentences.csv   our labelled test sentences (small, so it lives in git)
docs/writeup.md           the one-page write-up
server/, frontend/        optional extras, only if the notebook is finished early
```

The notebook loads `data/test_sentences.csv` from the repo's public web address, not from someone's laptop, so it works in a fresh Colab. That address only works once the repo is public, which judges need anyway to open the notebook. While the repo is still private, Colab can't download the file from that address, so make the repo public before the final fresh-Colab Run all check. We don't train or upload a model: we use the three pre-trained models as they are, plus our own rules.

A website or server is optional. If we build one, it does the same thing as the notebook's demo cell: type Mandarin, choose speaker/listener/formality, get Serbian and a warning when it had to guess.

## Notebook sections

0. **Intro:** the problem in one line and who it helps. No names or school: Round 1 review is blind.
1. **Setup:** installs, fixed random seed
2. **Data:** load our test sentences from the repo's public link, show a few rows, explain each column
3. **Explore:** counts by label (speaker, listener, formality) and by practice/test
4. **Split:** use the practice/test column as it is; rules are built on practice only, and we don't look at test results until the rules are final
5. **Baseline:** Mandarin → English → Serbian
6. **Main model:** NLLB direct (top 1), then NLLB top 8 + our picker
7. **Evaluate:** chrF, gender %, formality %, right form in the 8 options %, flag accuracy, 3-5 worst misses and why
8. **Demo:** type Mandarin, choose speaker/listener/formality, get Serbian plus a warning when it had to guess (film this)
9. **Limits and credits:** what it can't do, all sources, how we used AI

## Workflow

1. **Pick the idea:** done (see above and log.md).
2. **Data:** David and Adam fill in the test-set CSV; it's committed to `data/` so the notebook can load it from the repo.
3. **Build:** Claude Code on the notebook in this shared GitHub repo, opened in Colab. Only one person edits `notebook/model.ipynb`; others work in their own Colab copies and send sections over.
4. **Test:** run it in Colab and log real results, including failures, in docs/log.md.
5. **Understand it:** have Claude Code explain each part so all of us can answer questions.
6. **Write-up:** one page, in docs/writeup.md or a shared Google Doc.
7. **Video:** screen recording of the notebook running, uploaded unlisted.
8. **Submit:** by 10:59 PM Sunday.

## Timeline

| Block | Goal |
|---|---|
| Sat morning | Track and idea picked, roles set (done); Phase 1 model check (done) |
| Sat afternoon | Phase 2: test set written and labelled; Phase 3: notebook sections 0-5 working on it |
| Sat evening | Phase 3-4: NLLB direct scored; Adam's picker rules written on the practice rows |
| Sun morning | Phase 5: score all three on the test rows; find and explain the worst misses; log the numbers |
| Sun afternoon | Phase 6 if time; demo cell, limits and credits; fresh-Colab Run all check; write-up draft |
| Sun evening | Phase 7: record video, final checks, submit by 10:59 PM |
