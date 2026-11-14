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

## Experiments and results

| When | Model / change | Data split | Metric(s) | Result | Notes |
|---|---|---|---|---|---|

## Known failures and limits

-
