# Team plan

Source: the "Our plan" tab of the team Google Doc, cleaned up. Where the doc gave two versions of the notebook outline, this file keeps the fuller 10-section one, because its baseline, demo and limits sections earn points under "Testing and honesty" and "Communication".

## Fill in at kickoff

- Tracks: Health, Finance, Climate, Languages (pick one). Full brief in [challenge.md](challenge.md).
- Challenge: one AI project for one track. Show who it's for, input → output, a baseline comparison, and where it fails. Suggested projects are fine, but we must add our own user, data or question.
- Track: AI + Health
- Idea: Hidden Allergen Checker. Helps a kid with a peanut allergy by taking an ingredient list and giving back "looks safe" or "check this one". Baseline: keyword search for "peanut". Model: TF-IDF + logistic regression. Our angle: train on English labels, test on French and Spanish labels, then fix by retraining with more languages.
- Dataset: Open Food Facts (https://world.openfoodfacts.org), ODbL license. Loading route still being decided; see docs/log.md, Sat 10:15 AM.
- Where to submit: the Airtable form at https://airtable.com/appypCyHN77hElIcS/shrXA5VBFdugmoXl6. One person submits; resubmitting is allowed.

## Who does what

Not decided yet. Until the team splits roles, every task here belongs to the team as a whole.

## Repo layout

Created Sat 9 AM: README, requirements.txt, notebook/model.ipynb (section headings, setup, scoring helper), docs/writeup.md (template). server/ and frontend/ wait until the notebook is solid.

```
README.md               what it does, how to run it, results, credits
requirements.txt        libraries to install
notebook/model.ipynb    the AI part judges run in Colab
server/app.py           FastAPI: loads the model once, POST /predict -> prediction + confidence
server/requirements.txt
frontend/               input box, button, result, and a line on what the model can't do
docs/writeup.md         the one-page write-up
data/                   small files only; big data loads from its source in the notebook
```

How it connects: someone types into the website, the website sends it to the server, the model predicts, and the answer shows on the page.

## Notebook sections

0. **Intro:** the problem in one line and who it helps. No names or school: Round 1 review is blind.
1. **Setup:** installs, fixed random seed
2. **Data:** load from a public source, show a few rows, credit the source
3. **Explore:** 2-3 quick charts (counts, missing values)
4. **Clean and split:** fix gaps, lock away a test set (about 80% train, 20% test)
5. **Baseline:** the simplest model that could work
6. **Main model:** pre-trained or stronger model, credited
7. **Evaluate:** test scores vs the baseline, plus 3-5 misses and why
8. **Demo:** one cell that takes a new input and shows the answer (film this)
9. **Limits and credits:** what it can't do, all sources, how we used AI

Save the trained model to Hugging Face so the server can load it.

## Workflow

1. **Pick the idea:** video call Sat morning, write it above.
2. **Data:** starter kit or a public dataset; note the source.
3. **Build:** Claude Code on the notebook in this shared GitHub repo, opened in Colab.
4. **Test:** run it in Colab and log real results, including failures, in docs/log.md.
5. **Understand it:** have Claude Code explain each part so all of us can answer questions.
6. **Write-up:** one page, in docs/writeup.md or a shared Google Doc.
7. **Video:** screen recording of the notebook running, uploaded unlisted.
8. **Submit:** by 10:59 PM Sunday.

## Timeline

| Block | Goal |
|---|---|
| Sat morning | Read the challenge, pick track and idea, find the dataset, set up the repo layout |
| Sat afternoon | Notebook sections 0-5 working: data loaded, explored, split, baseline scored |
| Sat evening | Main model trained (section 6); first real test numbers logged |
| Sun morning | Evaluate and find misses (section 7); improve the model; start server and website |
| Sun afternoon | Demo cell, limits and credits; fresh-Colab Run all check; write-up draft |
| Sun evening | Record video, final checks, submit by 10:59 PM |

## Kickoff prompt for Claude Code

Paste this at kickoff and add the challenge text at the bottom.

> Set up this repo with the layout in docs/plan.md. The notebook must run top to bottom in a fresh Colab session with Run all, load its data from a public source, and have a plain-English heading above each of the sections listed in docs/plan.md. The server uses FastAPI, loads the model once, and has POST /predict returning the prediction and confidence. The frontend has an input, a button and the result, and calls /predict. The README explains how to run each part and credits every dataset, library and model. Explain each file to us in plain English as you write it. We're beginners.
>
> Challenge:
