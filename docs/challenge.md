# The challenge

Source: the official "Project Briefs" PDF (22 pages), linked from https://highschoolhackathon.org/briefs. Read Sat Nov 14, 1:20 AM ET. PDF: https://drive.google.com/file/d/15tYD48XRmCgWbk1_lLDtc8lebi6qm-4-/view. The brief also mentions a "Hacker Guide": https://drive.google.com/file/d/1_XIisoApHfiuIzkPev6hKJ4SlViGH4pm/view (read Sat 8:20 AM; notes below).

## The short version

Pick **one of four tracks** (Health, Finance, Climate, Languages) and build **one AI project** for it. Each track has 3-4 suggested projects with datasets and steps, plus "your own idea". Suggested projects are optional. **If we use one, we must add something of our own** (our own user, our own data, or our own question). Teams that only follow the steps score toward the bottom.

There is no kickoff call and nothing live this weekend. The organizers give no technical help, only submission help (contact@veritasai.com).

## What every project must show (section 3)

1. **Who it's for:** one specific user and the moment they'd use it.
2. **What goes in and what comes out:** a real input producing a result.
3. **Does it beat a simple baseline?** Report the baseline's score next to ours.
4. **Where does it fail?** At least one wrong example, and why.

All results on test data the model never saw.

## The tracks

### AI + Health
**Challenge:** help one specific person catch a health problem sooner, or manage one better.
**Must:** name the user; report missed cases (false negatives) and false alarms (false positives) separately; include "This project is a prototype and is not medical advice."; public data only, never real patient records.
**Judges look for:** a clear user, honest missed cases and false alarms, checking the model works equally across groups (age, sex, skin tone for skin images).

| Project | Level | Data | Notes |
|---|---|---|---|
| Pneumonia screening from chest X-rays | Beginner | PneumoniaMNIST (`pip install medmnist`, pre-split) or Kaggle Chest X-Ray | Baseline "always pneumonia" scores high (about 3:1 pneumonia). Report pneumonia recall and false alarms. Own ideas: a real setting like a rural clinic, test on X-rays from another source, how to handle unsure scans. |
| Heart disease risk from checkup data | Intermediate | UCI Heart Disease, `fetch_ucirepo(id=45)`, ~300 patients, 13 measurements | Make target 0 vs any disease; handle missing `ca`/`thal`; logistic regression vs most-common baseline; accuracy, recall, top measurements. Own ideas: test on other hospitals (Hungary, Switzerland, Long Beach), design for a nurse or patient, check men vs women and age groups. |
| Country-level health risk | Advanced | WHO Global Health Observatory, Our World in Data | Train on earlier years, test on recent years; baseline "this year = last year"; top 10 at-risk countries. |
| Own idea | | | Examples: sign language recognition, mood journal with an emotion classifier, reading medicine labels aloud. |

### AI + Finance
**Challenge:** help a person or small business make a safer or fairer money decision, and show it beats a simple rule.
**Must:** compare with at least one simple baseline; pick the right measure (precision and recall for rare events); with dates, train on earlier and test on later; include "This project is a prototype and is not financial advice."
**Judges look for:** the right measure of success, a fair baseline comparison, whether a real person could trust it; checking unfair treatment of a group stands out.

| Project | Level | Data | Notes |
|---|---|---|---|
| Scam text filter | Beginner | SMS Spam Collection (UCI, also on Hugging Face), 5,574 messages, ~13% spam | Stratified split, TF-IDF + logistic regression or naive Bayes; baseline "not spam" is ~87% accurate and catches nothing; report spam precision and recall, 5 misses. Own ideas: test on today's scams in our country or language (the data is 10+ years old), explain why a message was flagged, design for an elderly relative. |
| Card fraud detection | Intermediate | Kaggle Credit Card Fraud (needs a Kaggle account), 284,807 transactions, 492 fraud | Accuracy is useless (99.8% by guessing "not fraud"); balanced logistic regression then a random forest; precision, recall, PR-AUC. |
| Fairness audit of a loan model | Intermediate | Statlog German Credit, `fetch_ucirepo(id=144)`, 1,000 applicants | Compare approval rates for under-25 vs 25+; find features driving any gap. Own ideas: features that stand in for age, a fix and its accuracy cost (bad approval costs 5x a wrong rejection). |
| News headlines and the stock market | Advanced | Kaggle "Daily News for Stock Market Prediction", yfinance, FRED | Split by date; sentiment with FinBERT or VADER; two baselines (always up, same as yesterday); report honestly even if "not really". |
| Own idea | | | Examples: budgeting help for teens with a first debit card, a city inflation tracker, explaining bank fees in plain language. |

### AI + Climate
**Challenge:** help a community, city or energy system measure, predict or reduce its climate impact.
**Must:** one location or region; for forecasts, train on earlier dates and test on later, never shuffle; compare with the persistence baseline ("tomorrow = today"); say what decision the prediction supports and who makes it.
**Judges look for:** a fair comparison with a simple forecast, a link from prediction to a decision, an unseen test period. Small and tied to a real place beats "the whole planet".

| Project | Level | Data | Notes |
|---|---|---|---|
| Next-day solar energy forecast | Beginner | NASA POWER (CSV download, no code), Open-Meteo | Target = tomorrow's `ALLSKY_SFC_SW_DWN`; last year as test; persistence baseline vs linear regression; MAE. The baseline is hard to beat, so any gain counts. Own ideas: our own city, two climates, turn it into a real decision, how many days ahead it stays useful. |
| Next-day air quality forecast | Intermediate | OpenAQ (free API key) or Open-Meteo air quality API (no key, model estimates), Open-Meteo weather | Daily PM2.5 for one city; add wind and rain; persistence baseline; MAE on recent months. Own ideas: a city where it matters, focus on bad days (> 35 µg/m³), what drives pollution. |
| Land-use mapping from satellite images | Advanced | EuroSAT (`torchvision.datasets.EuroSAT`, 27,000 tiles, 10 classes), Global Forest Watch | Fine-tune ResNet-18 on a GPU; per-class accuracy and confusion matrix. |
| Own idea | | | Examples: largest emitters with Climate TRACE, building energy use, meal carbon footprint from a photo, which streets flood. |

### AI + Languages
**Challenge:** help people understand each other, learn a language or be understood, especially in a language technology serves poorly.
**Must:** results per language or accent, not just an average; real examples (model output next to the correct output); public data or our own voice and writing only.
**Judges look for:** side-by-side examples, results broken down by language or accent, checks by a real speaker.

| Project | Level | Data | Notes |
|---|---|---|---|
| Language identification | Beginner | Tatoeba sentences file | 5-10 languages, equal sentences each; character n-gram TF-IDF + logistic regression or naive Bayes; per-language accuracy, confusion matrix, compare with `langdetect`. Own ideas: a language we speak that detectors get wrong, short or mixed text, Malay vs Indonesian. |
| Translation quality test | Intermediate | `facebook/nllb-200-distilled-600M`, FLORES+ (Hugging Face account and accepting terms needed) | Translate 100 sentences into a widely spoken and a less served language; chrF with sacrebleu; 5 worst side by side. |
| Speech recognition across accents | Advanced | Mozilla Common Voice, FLEURS, `openai/whisper-small` | Word error rate per accent with jiwer; needs a GPU. |
| Own idea | | | Examples: plain-language forms for new speakers, translating street signs, a conversation partner. With an LLM API, judges focus on what we add around it. |

## Project levels

| Level | For teams that | Tools |
|---|---|---|
| Beginner | have never coded or know the basics | Teachable Machine, or Colab with starter notebooks |
| Intermediate | can write some Python | Colab, pandas, scikit-learn, Gradio |
| Advanced | have trained models before | PyTorch or Hugging Face Transformers on a free GPU |

## Rules (section 2) that change anything for us

- Pretrained models, **AI APIs (for example the free Gemini API tier)**, tutorial code and coding assistants are all allowed. Cite every one.
- AI or machine learning must do the project's main job. A normal app built with AI coding tools doesn't count.
- Only public or synthetic data. No one's personal info without permission.
- Health and finance projects need the disclaimer line.
- Report the results we actually got, including weak ones.
- One project, one track, chosen on the submission form.

## Submitting (section 5)

- **Form:** https://airtable.com/appypCyHN77hElIcS/shrXA5VBFdugmoXl6. One person submits for the team. Resubmit as often as we like; the latest counts.
- **Required:** code link (Colab or GitHub, viewable by anyone with the link, **notebook saved with outputs visible**), write-up (about one page: Google Doc with link sharing, GitHub README, or PDF/Word upload), track, every member's full name, email and school, and credits (every dataset, model, tutorial and AI tool, with links).
- **Optional but recommended:** demo video, up to 2 minutes, YouTube unlisted or Drive link.
- Complete once both code and write-up links work. **Submit a first version a few hours early**, then resubmit.
- Write-up template sections: Project name, Track, Team; The problem; What we built; What we added; How it works; Results (baseline X, model Y, where it fails); What we'd do next; Sources.
- Video: problem 15s, demo 60s, how it works 30s, next steps 15s. A screen recording with voice-over is enough.

## Kickoff email (Sat 12:00 AM, read 8:20 AM)

Sent to the team lead's email at 11:49 PM Fri and forwarded to Gmail Sat morning. What it adds:

- **Reply "Got it"** to the email so the organizers know it arrived. The coder has to do this himself.
- **Any public dataset is allowed**, not just the ones in the briefs, as long as it's credited.
- Each member gets a certificate, which is why the form asks for everyone's name, email and school.
- Their advice: "A simple project that works beats an ambitious one that doesn't. If you get stuck, cut your idea in half and finish it."
- **Starter notebook** (optional): https://colab.research.google.com/drive/1AWwKHP2oBsZozPHXDZA45MgBZBx3frmZ. A 45-minute Colab intro that trains a first model on the Breast Cancer Wisconsin data built into scikit-learn.
- **Sample submission**: Drive folder https://drive.google.com/drive/folders/18B409gf0fjcrsGCj7RAZahwRNdmKoT8E (a PDF plus a Colab notebook). See below.

### The sample submission

"ScamCheck, a scam text filter for grandparents" (Finance, made by Veritas with a fictional team). It trains TF-IDF + logistic regression on SMS Spam, then tests on 40 modern texts the team wrote (20 scams, 20 normal). Baseline "always not spam": 86.6% accuracy, catches 0 of 20 modern scams. First model: 97.3% accuracy but catches 3 of 20. With balanced class weights: 98.4%, catches 16 of 20, 3 false alarms. It explains each warning with the top three suspicious words, and lists its misses ("family emergency" and "wrong number" scams). No video.

What it tells us:
- **The scam filter idea is taken.** Copying their example would score badly on originality.
- **The submission form asks for:** project title, building as team or solo, team name, team members (name, email, school), track, **starting point** (which suggested project, if any), **one-sentence pitch**, code link, write-up link, demo video link, **what we added**, datasets/models/AI tools used, and **"New to AI?"** (probably feeds the Best Beginner Build award).
- The sample write-up puts (fictional) names on its "Team" line and the disclaimer right under the title.
- How it credits AI tools: "ChatGPT, used to debug a pandas error and to suggest the class_weight setting, which we read about in the scikit-learn documentation before using it." We should credit Claude Code the same way.

## Hacker Guide (extra points not already above)

- **One-sentence test for any idea:** "Our project helps [a specific person] by taking [an input] and giving back [an output]." If we can't fill in all three, the idea needs more thought.
- Their plan: idea and data loading in the first 2 hours; baseline by midday Saturday; first model Saturday afternoon; input to output working Saturday evening; **sleep at least 7 hours Saturday night**; one measured improvement Sunday morning; demo runs cleanly by Sunday midday; write-up and video Sunday afternoon; submit with 2 hours to spare.
- **Stop adding features about six hours before the deadline.**
- Save often (commit to GitHub or save a Colab copy every couple of hours) and keep notes on what we tried.
- Stuck on one bug for 30 minutes: simplify, switch dataset, or ask for help.
- Common mistakes: results too good to be true (test data leaked into training), reusing a tutorial dataset without a new question, a write-up that lists tools but not what we learned, links judges can't open.
- Finals questions to prepare for: "How do you know it works?", "What would cause it to fail?", "Who would use this?" Agree beforehand who answers which kind.
- Check whether the model works equally well across groups, and say so if it doesn't.

## Judging (section 6)

Round 1 is a blind review by the Veritas AI team. The brief names four criteria: **technical quality** (works, sound approach, fair testing), **impact** (a real problem for real people), **creativity** (a fresh approach, not a repeated tutorial), **clarity** (a judge gets it in two minutes). The judges page still shows the 100-point table in CLAUDE.md; the two line up. An honest, modest result beats an unexplained high one. Shortlist and finalists are emailed Wed Nov 18; finals are Sat Nov 21 at 11:00 AM ET.

**Open question for the team:** the write-up template has a "Team: names" line, but Round 1 is blind. The form collects names separately, so leaving names out of the write-up seems safer. Decide together.

## Their suggested schedule

| By | Where we should be |
|---|---|
| Saturday, first 2 hours | Track and idea picked, data loading in the notebook |
| Saturday evening | Baseline and first model working |
| Sunday midday | One improvement made and measured, demo runs start to finish |
| Sunday, 2 hours before the deadline | Write-up done, video uploaded, project submitted |

If the data won't load within about 30 minutes, switch dataset or idea.
