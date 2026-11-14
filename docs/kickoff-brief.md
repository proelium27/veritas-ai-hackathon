# Kickoff brief

For the team's first call, Sat Nov 14. Written by the commander at 7:50 AM ET. Nothing here is decided until the team agrees on the call.

## The challenge in a few lines

Pick one of four tracks (Health, Finance, Climate, Languages) and build one AI project for it. Every project must name one user, show a real input turning into an output, beat a simple baseline on test data the model never saw, and show at least one case it gets wrong. The brief suggests projects for each track. We can use one, but only if we add our own user, data or question; plain tutorial copies score low. Health and finance projects need a "prototype, not medical/financial advice" line. Submit through the Airtable form by Sun 11:59 PM (our target is 10:59 PM). Full details are in [challenge.md](challenge.md).

## Ideas, scored against the judging table

The scores are the commander's guesses, 1 (weak) to 5 (strong), so the team should argue with them. "Total" weights each score by its points in CLAUDE.md (Technical 30, Originality 20, Impact 20, Testing 15, Communication 15), out of 100. All six datasets load in a fresh Colab with no sign-in (see [data-options.md](data-options.md)).

| Idea (our own angle in bold) | Track | Dataset | Tech | Orig | Impact | Test | Comm | Total |
|---|---|---|---|---|---|---|---|---|
| Scam text filter. **Does a filter trained on 2011 texts catch 2026 scams?** We build a small labeled set of modern scam texts (package delivery, fake bank, crypto) and test on it. | Finance | SMS Spam (UCI / Hugging Face) | 5 | 4 | 4 | 5 | 5 | **92** |
| Pneumonia screening. **A "not sure, send to a doctor" zone** for a clinic with no radiologist, and how many scans land in it. | Health | PneumoniaMNIST | 4 | 3 | 4 | 5 | 4 | 79 |
| Heart disease risk. **Train on Cleveland patients, test on hospitals in Hungary, Switzerland and Long Beach.** Does it still work somewhere else? | Health | UCI Heart Disease (raw files) | 4 | 4 | 3 | 5 | 4 | 79 |
| Language ID. **Close pairs that detectors confuse** (Malay vs Indonesian, or a language one of us speaks), compared with `langdetect`. | Languages | Tatoeba | 5 | 3 | 3 | 4 | 4 | 78 |
| Solar forecast. **Our own city**, tied to one decision (when to run a big appliance). | Climate | NASA POWER | 4 | 3 | 3 | 4 | 4 | 72 |
| Loan fairness audit. **Under-25 vs 25+ approval gap**, and what a fix costs in accuracy. | Finance | German Credit | 4 | 3 | 3 | 4 | 3 | 69 |

Why these scores, briefly:
- **Scam filter** is the easiest to build and explain, has a clear baseline ("never spam" is 87% accurate but catches nothing), and the modern-scams test gives us an honest, interesting failure story that is ours, not the tutorial's.
- **Pneumonia** and **heart** are strong on testing (missed cases vs false alarms are required anyway). Pneumonia is the more common tutorial. Heart has the better original angle, but loading the other hospitals' raw files hasn't been tested and only ~300 Cleveland patients means noisy numbers.
- **Language ID** is very easy to build, but its impact depends on whether one of us speaks a language that detectors get wrong.
- **Solar** has a baseline ("tomorrow = today") that is hard to beat, so results may look weak, and "who uses this" is harder to make vivid.
- **Loan fairness** is a good honesty story, but 1994 German data makes the user harder to picture.

## Recommendation

**Pick: the scam text filter (Finance), with the "2011 filter vs 2026 scams" test.**

- User: an older relative who gets scam texts and wants a second opinion before tapping a link.
- Baseline: "always not spam". Main model: TF-IDF + logistic regression. Stretch: a pretrained text model from Hugging Face, credited.
- Our own data: about 50 modern texts (scams and normal ones) that we write ourselves, modeled on public warnings from sources like the FTC, and labeled as synthetic in the notebook. No one's real messages. Any public examples we copy get a credit line.
- What we report: spam precision and recall on the old test split and on our new set, side by side, plus 3-5 misses and why. If it does badly on 2026 scams, that is the finding, not a failure.
- Risk: the data is small and old. That's fine; it's the point of the angle.

**Fallback: pneumonia screening (Health) with the "not sure" zone.** Choose it instead if the team would rather do images, or if writing our own scam texts feels like too much. PneumoniaMNIST is 4 MB and already split, so it loads in minutes.

Per the brief's own rule: if the data won't load within about 30 minutes, switch.

## Decisions for the call

1. Track and idea (the table above, or something else).
2. Our own angle in one sentence, and who the user is.
3. Who edits the main notebook (only one person does).
4. Whether names go in the write-up's "Team" line. Round 1 is blind and the form collects names separately, so the commander's suggestion is to leave them out.
5. Whether we make the optional 2-minute video (recommended).
6. Check-in times for today and tomorrow.
7. Everyone's GitHub username, so the repo invites can go out.
