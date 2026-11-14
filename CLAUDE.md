# Veritas AI Hackathon — project context

Read this first in every session. The full rules are in [docs/competition.md](docs/competition.md), the team plan in [docs/plan.md](docs/plan.md), and the running record of decisions and results in [docs/log.md](docs/log.md).

## What this is

A 48-hour AI contest, not a web-dev contest. Judges score an AI model that solves the track's challenge, how honestly we test it, and how clearly we explain it. All times are Eastern.

- Kickoff: Sat Nov 14, 12:00 AM ET (challenge revealed)
- Hard deadline: Sun Nov 15, 11:59 PM ET. **Our target is 10:59 PM.** No late entries.
- Live finals for teams that advance: Sat Nov 21

Team of three beginners. Roles aren't decided yet, so treat tasks as team-wide.

**The challenge is in [docs/challenge.md](docs/challenge.md):** pick one of four tracks (Health, Finance, Climate, Languages) and build one AI project. If we start from a suggested project, we must add our own user, data or question. Submit through the Airtable form linked there.

## Hard rules (break these and we're out)

1. **All code is written during the 48 hours.** Before kickoff this repo holds docs only. Write no model, notebook, server or frontend code before Sat Nov 14 12:00 AM ET.
2. AI tools are OK for debugging, explaining and routine code, but **all three of us must be able to explain every part**. Judges question finalists live.
3. **Credit every dataset, library and pre-trained model**, in the README and in the notebook's last section.
4. Data loads from a public source, never from a file on someone's laptop.

## How to work in this repo

- **Explain every file in plain English as you write it.** The team are beginners; a teammate must be able to explain the code to a judge.
- **The notebook comes first.** Judges open and run `notebook/model.ipynb` in Colab. It scores the points; the server and website are extras that only matter once the notebook is solid.
- The notebook must run top to bottom in a **fresh Colab session with Run all**. Fix the random seed. Put a plain-English heading above each section (sections are listed in docs/plan.md).
- **Record real results, including failures**, in docs/log.md as you go. "Testing and honesty" is 15 of 100 points: show test scores against a baseline and 3-5 examples the model gets wrong, with reasons.
- Only one person edits the main notebook. Others work in their own Colab copies and send sections over.
- Keep big data and model weights out of git (see .gitignore). Trained models go to Hugging Face.

## Judging (Round 1, out of 100; counts 30% of the final ranking, live finals 70%)

| Criterion | Points | What earns it |
|---|---|---|
| Technical execution | 30 | It runs and shows results in numbers |
| Originality | 20 | Our own angle, not a tutorial copy |
| Impact and track fit | 20 | Clear who it helps, tied to the challenge |
| Testing and honesty | 15 | How we tested it and where it fails |
| Communication | 15 | Clear write-up and video; all of us can explain it |

Check every decision against this table.

Round 1 is **blind**: reviewers don't see names or school, so keep both out of the notebook, write-up and video. Finals (5-minute live demo plus Q&A) use their own rubric: Demo and clarity 30, Technical depth 30, Impact 20, Q&A 20. Official site: highschoolhackathon.org. Challenge briefs and submission details arrive by email. More in [docs/research.md](docs/research.md).
