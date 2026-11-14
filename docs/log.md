# Decisions and results log

Record what we decided, what we tried, and the real numbers, including what failed. This feeds the write-up and the "Testing and honesty" score.

Format: `Day time ET — who — what happened / numbers / why`.

## Decisions

- Fri Nov 13 — setup — Planning docs written locally only. Nothing is committed or pushed until kickoff (rule: all code written during the 48 hours); the GitHub repo is created at kickoff.
- Sat Nov 14, 1:20 AM — commander — Challenge found: four tracks (Health, Finance, Climate, Languages), brief PDF linked from highschoolhackathon.org/briefs. The 12:30 AM routine missed the PDF link and found no Veritas email in Gmail. Summary in docs/challenge.md. Track and idea not picked yet.
- Sat Nov 14, 1:25 AM — commander — GitHub repo created (private) with the planning docs.
- Sat Nov 14, 7:50 AM — commander — The 7:00 AM backup routine again missed the brief PDF and found no Veritas email; its phone notification saying "challenge not found" is out of date (the brief is in docs/challenge.md). The team Google Doc is unchanged since last night. Wrote docs/kickoff-brief.md: recommended pick is the scam text filter (Finance) tested on modern scams, fallback is pneumonia screening (Health). The team decides on the first call.
- Sat Nov 14, 8:30 AM — commander — Read the kickoff email (forwarded to Gmail), the Hacker Guide and the official sample submission. The sample is a scam text filter for grandparents tested on modern scams, the same as our first pick, so the recommendation changed to heart disease risk tested across four hospitals (Health), with pneumonia screening as the fallback. Checked: all four UCI heart files download with no sign-in (303/294/123/200 rows); every Swiss patient has cholesterol recorded as 0 and 115 of 123 are sick.
- Sat Nov 14, 9:00 AM — commander — Repo set up: README with an Open in Colab button, requirements.txt, notebook/model.ipynb (all 10 section headings, a setup cell with the seed, an optional HF_TOKEN check, and a report() helper that scores missed cases and false alarms separately), docs/writeup.md template. Tested: the notebook runs top to bottom with no token. Idea-specific code waits for the team's pick.
- Sat Nov 14, 9:30 AM — commander — Asked 3 Sonnet agents for ideas independently. All 3 suggested heart across hospitals and Malay-vs-Indonesian language ID (the brief's own hints), so both are likely common. 2 of 3 ranked a school heat warning first. Added to kickoff-brief.md and the team guide; the team should pick the idea someone has a personal hook for.
- Sat Nov 14, 10:00 AM — team — Picked the idea: Hidden Allergen Checker (Health). Peanut detection in ingredient lists; train on English labels, test on French and Spanish, fix by retraining with more languages. Slides: https://claude.ai/artifact/2pBJM1KkB36FoPjoZqAuK6
- Sat Nov 14, 10:15 AM — commander — Data check. (1) Hugging Face `openfoodfacts/product-database` is public and not gated, but `food.parquet` is 8.05 GB. DuckDB can read its schema remotely (has `lang`, `ingredients_text` per language, `allergens_tags`, `traces_tags`), but a full query got HTTP 429 (rate limited) after about 2 minutes. (2) The Open Food Facts search API works with no key: 7,177 products tagged `en:peanuts` sold in France, real labels like "CACAHUETES..." and "Arachide 100%". Repeat calls were rate limited within seconds. Conclusion: a live download in the notebook is fragile for judges. Plan: build a small snapshot CSV once with a slow, documented script, commit it to the repo, and have the notebook load it from the repo's public URL.
- Sat Nov 14, 10:15 AM — commander — Catch: Open Food Facts fills `allergens_tags` partly by matching ingredient words in many languages (it knows "arachide" and "cacahuetes"). So the answer labels come from its own multilingual word list, and a multilingual keyword list would score almost perfectly. The fair baselines are an English-only keyword search and that multilingual list; say this in the write-up. `traces_tags` ("may contain") is separate from `allergens_tags` ("contains").

## Experiments and results

| When | Model / change | Data split | Metric(s) | Result | Notes |
|---|---|---|---|---|---|

## Known failures and limits

-
