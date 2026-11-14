# Kickoff brief

For the team's first call, Sat Nov 14. Written by the commander at 7:50 AM ET and revised at 8:30 AM after reading the kickoff email, the official sample submission and the Hacker Guide. Nothing here is decided until the team agrees on the call.

## The challenge in a few lines

Pick one of four tracks (Health, Finance, Climate, Languages) and build one AI project for it. Every project must name one user, show a real input turning into an output, beat a simple baseline on test data the model never saw, and show at least one case it gets wrong. The brief suggests projects for each track. We can use one, but only if we add our own user, data or question; plain tutorial copies score low. Any public dataset is allowed if we credit it. Health and finance projects need a "prototype, not medical/financial advice" line. Submit through the Airtable form by Sun 11:59 PM (our target is 10:59 PM). Full details are in [challenge.md](challenge.md).

The organizers' own advice: "A simple project that works beats an ambitious one that doesn't."

## What the sample submission changes

Veritas published a finished example: **ScamCheck, a scam text filter for grandparents** (Finance). It trains on the SMS Spam data, then tests on 40 modern scam and normal texts the team wrote, and explains which words looked suspicious. That was almost exactly our first recommendation, so **the scam filter is off the table**: a judge would see it as a copy of their own example.

The sample is still the best guide to what judges want: one specific user, a baseline, something of our own (a new test set), and honest misses. The idea below copies that *pattern* on a different problem.

## Ideas, scored against the judging table

Scores are the commander's guesses, 1 (weak) to 5 (strong). "Total" weights each score by its points in CLAUDE.md (Technical 30, Originality 20, Impact 20, Testing 15, Communication 15), out of 100. All datasets load in a fresh Colab with no sign-in (see [data-options.md](data-options.md)).

| Idea (our own angle in bold) | Track | Dataset | Tech | Orig | Impact | Test | Comm | Total |
|---|---|---|---|---|---|---|---|---|
| Heart disease risk. **Train on one US hospital's patients, then test on hospitals in Hungary, Switzerland and Long Beach.** Does a risk model still work somewhere else? | Health | UCI Heart Disease (4 hospital files) | 4 | 4 | 4 | 5 | 4 | **83** |
| Pneumonia screening. **A "not sure, send to a doctor" zone** for a clinic with no radiologist, and how many scans land in it. | Health | PneumoniaMNIST | 4 | 3 | 4 | 5 | 4 | 79 |
| Language ID. **Close pairs that detectors confuse** (Malay vs Indonesian, or a language one of us speaks), compared with `langdetect`. | Languages | Tatoeba | 5 | 3 | 3 | 4 | 4 | 78 |
| Solar forecast. **Our own city**, tied to one decision (when to run a big appliance). | Climate | NASA POWER | 4 | 3 | 3 | 4 | 4 | 72 |
| Loan fairness audit. **Under-25 vs 25+ approval gap**, and what a fix costs in accuracy. | Finance | German Credit | 4 | 3 | 3 | 4 | 3 | 69 |
| ~~Scam text filter tested on modern scams~~ | Finance | SMS Spam | 5 | 1 | 4 | 5 | 5 | ~~80~~ |

Why these scores, briefly:
- **Heart across hospitals** asks a real question that matters outside the hackathon: models trained at one hospital often get used at others. The test is built into the data (four hospitals), so we don't have to write our own test set. Only about 300 patients per hospital means noisy numbers, which we should say.
- **Pneumonia** is strong on testing (missed cases vs false alarms are required anyway) and is the Hacker Guide's own example of a well-scoped project, which also makes it the most common choice.
- **Language ID** is very easy to build, but its impact depends on whether one of us speaks a language that detectors get wrong.
- **Solar** has a baseline ("tomorrow = today") that is hard to beat, and "who uses this" is harder to make vivid.
- **Loan fairness** is a good honesty story, but 1994 German data makes the user hard to picture.
- **Scam filter** scores well on everything except originality, and originality is what kills it.

## Checked with other AIs (Sat 9:30 AM)

Three separate AI models (Sonnet) were asked for ideas from the brief alone, without seeing this file. All three suggested the heart-across-hospitals idea and the Malay-vs-Indonesian language ID idea, partly because the brief prints those angles itself, so other teams will likely build them. Two of the three ranked a heat warning for a school coach (Open-Meteo weather, "tomorrow = today" baseline) as their top pick. Two also said heart disease is the weakest on originality, since it's a heavily used tutorial dataset, so its Originality score above is probably too high.

What no AI can copy is the part only we have: a language one of us speaks, our own school and town, or a real person we know. **Ask about those first on the call**, and pick the idea someone has a personal hook for. With no hook, the heat warning for our own school is the freshest beginner-friendly option.

## Recommendation

**Pick: heart disease risk across hospitals (Health).**

- User: a nurse at a small clinic who wants to know which patients to send for a heart check first, using a tool that was built somewhere else.
- One-sentence test (from the Hacker Guide): "Our project helps a clinic nurse by taking a patient's checkup measurements and giving back a heart disease risk, and tells them how much to trust it at their own clinic."
- Data: the four UCI hospital files (Cleveland 303, Hungary 294, Switzerland 123, VA Long Beach 200 patients). Checked at 8:25 AM: all four download with no sign-in.
- Baseline: "always predict the most common answer". Main model: logistic regression, then maybe a small decision tree or random forest.
- What we report: missed cases and false alarms separately, first on held-out Cleveland patients, then on each other hospital. Also check men vs women and age groups, which the brief asks for.
- Catches we already know: lots of missing values (the Switzerland file records cholesterol as 0 for every patient, which means "missing"), and the hospitals have very different shares of sick patients. Both are honest findings to write up, not reasons to quit.
- Disclaimer line: "This project is a prototype and is not medical advice."

**Fallback: pneumonia screening (Health) with the "not sure" zone.** Pick it if the heart data gets messy, or if the team would rather work with images. PneumoniaMNIST is 4 MB and already split.

Per the brief's own rule: if the data won't load within about 30 minutes, switch.

## Decisions for the call

1. Track and idea (the table above, or something else).
2. Our own angle in one sentence, and who the user is.
3. Who edits the main notebook (only one person does).
4. Whether names go in the write-up's "Team" line. Round 1 is blind, but the official sample puts (fictional) names in its write-up, so names there seem to be expected. The commander still leans toward leaving them out of the notebook and video.
5. Whether we make the optional 2-minute video. The sample team skipped it to spend more time testing.
6. Check-in times, and when each of us sleeps (the Hacker Guide says at least 7 hours on Saturday night).
7. Everyone's GitHub username, so the repo invites can go out.
