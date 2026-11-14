# Readiness guide: get ready before the challenge drops

Written Fri Nov 13, 2026 for a team of three beginners. Read it once today, do the checklists, then keep it open during the hackathon.

**Rule reminder:** no model, notebook, server or frontend code before Sat Nov 14, 12:00 AM ET. Everything below is clicking and planning, not coding. When a step says "practice", practice only the clicking (open a public sample notebook, find a menu, add a secret). Do not start any hackathon code early.

Contents: [1. Accounts](#1-accounts-and-access-checklist) | [2. Workflow how-tos](#2-workflow-how-tos) | [3. Approach playbook](#3-approach-playbook-by-challenge-type) | [4. Kickoff hour](#4-kickoff-hour-60-minute-script)

---

## Do these tonight (Fri Nov 13)

- [ ] **Registration closes tonight at 11:59 PM ET.** Confirm all three teammates are added.
- [ ] Everyone sends Caleb their GitHub username. The repo is created at kickoff (nothing is committed before then), and Caleb sends the invites right away.
- [ ] Everyone finishes their own account checklist below.
- [ ] Everyone does the practice steps in section 2 so none of it is new at 3 AM.
- [ ] Pick one group chat and one video-call link for the weekend.

---

## 1. Accounts and access checklist

### Everyone (all three of us)

**GitHub**
- [ ] Have a GitHub account. Tell Caleb your username.
- [ ] At kickoff, accept the collaborator invite to the private repo `proelium27/veritas-ai-hackathon` (it does not exist before then):
  1. Open the email from GitHub titled something like "Invitation to collaborate on proelium27/veritas-ai-hackathon" and click **View invitation**. No email? Go straight to `github.com/proelium27/veritas-ai-hackathon/invitations` while signed in.
  2. Click **Accept invitation**.
  3. Check it worked: the repo page now opens for you, without a 404.
- [ ] Turn on two-factor sign-in if GitHub asks. It is quick and protects the repo.

**Google Colab**
- [ ] Sign in at `colab.research.google.com` with a Google account.
- [ ] Open any sample notebook from the Welcome page and run one cell, so you know Colab works for you.
- [ ] Find the GPU switch: **Runtime > Change runtime type**, then pick a GPU (a T4 is usually on offer on the free plan). You will only need it for image or big-text work. Free GPU time is limited, so turn it on only when you need it.
- [ ] Practice connecting Colab to GitHub (section 2.1) with any public repo. The first time you do it, GitHub asks you to authorize Colab, and you must tick the option that includes **private repositories** or our repo will not show up once it exists.

**Hugging Face** (where we store the trained model, and where many pre-trained models come from)
- [ ] Make an account at `huggingface.co` and confirm your email.
- [ ] Tell Caleb your username.

**YouTube**
- [ ] Have a Google account that can upload to YouTube. Open `studio.youtube.com` once and click through any "create a channel" prompt. Do not leave this for Sunday night.

### Who needs what extra

| Person | Extra job |
|---|---|
| **Teammate 2 (notebook owner)** | Create the Hugging Face **write token** (below) and store it in Colab Secrets. This person uploads the trained model. |
| **Teammate 3 (data, write-up, video)** | Own the YouTube upload. Pick a backup uploader in case their account has trouble. |
| **Caleb (repo owner)** | Create the repo and add collaborators at kickoff; make the repo public before submitting. Steps below. |

### Hugging Face write token (Teammate 2; Caleb too if he will also upload)

A token is a password for tools. A **write** token lets the notebook upload the trained model.

- [ ] On huggingface.co, click your profile picture, then **Settings > Access Tokens > Create new token**.
- [ ] Choose a token that can **write** (the classic "Write" type is simplest). Name it something like `hackathon-colab`.
- [ ] Copy it once. You cannot view it again later.
- [ ] **Never** paste the token into the notebook, the repo, a chat, the write-up or a screenshot. Judges can read all of those.
- [ ] If it leaks anywhere, go back to Access Tokens, delete it, and make a new one.

### Storing the token safely in Colab Secrets

Colab Secrets is a private locker attached to your Google account, not to the notebook file, so it is not saved to GitHub.

1. In Colab, click the **key icon** in the left sidebar (the label says "Secrets").
2. Click **Add new secret**.
3. Name: `HF_TOKEN`. Value: paste your token.
4. Switch on **Notebook access** for the notebook you are using. This switch is per notebook, so you have to turn it on again for each new notebook or copy.
5. In the notebook, the code asks Colab for the secret by name (Colab's `userdata` helper). The notebook only ever contains the name `HF_TOKEN`, never the value.

Two things to remember:
- Secrets belong to *your* Google account. Other teammates, and the judges, will not have your token. Build the notebook so that it **still runs top to bottom without a token**: the "upload to Hugging Face" step should be skipped, or fail politely, when no token exists. A notebook that crashes for a judge on that step costs us points.
- Make the uploaded model repo **public** so the server and the judges can download it without a token.

### Caleb: repo owner tasks

**Add the collaborators (at kickoff, right after the commander creates the repo)**
- [ ] On GitHub open the repo, then **Settings > Collaborators > Add people**.
- [ ] Type each teammate's GitHub username or email, pick them, and choose to add them. They get access once they accept the invite. (If you do not see Collaborators, you are not looking at the repo's own Settings tab.)
- [ ] Confirm both teammates show as collaborators, not "pending", by Saturday morning.

**Make the repo public (before submitting, target Sun 10:00 PM)**
- [ ] Look through the repo first for anything private: tokens, keys, personal data. If a token was ever committed, treat it as leaked and replace it. Deleting the file later does not erase it from history.
- [ ] Repo **Settings > General**, scroll to the **Danger Zone**, click **Change visibility > Make public**, and follow the prompts (it asks you to type the repo name).
- [ ] Open the repo in a **private/incognito window, signed out of GitHub**. If you can see the code, the judges can too.
- [ ] Open the final notebook link in that same signed-out window and confirm it loads in Colab (section 2.4).

---

## 2. Workflow how-tos

### 2.1 Open a GitHub notebook in Colab

1. Go to `colab.research.google.com`.
2. **File > Open notebook**, then click the **GitHub** tab.
3. First time only: click the authorize / sign-in link, sign in to GitHub, and allow Colab access. **Tick the option to include private repos.**
4. In the search box type `proelium27/veritas-ai-hackathon` and press Enter. Choose the branch (normally `main`), then click `notebook/model.ipynb`.
5. It opens in a new tab. This is a **working copy**: your edits do not change GitHub until you save to GitHub (next step).

Shortcut once the repo is public: put the notebook's GitHub address after `colab.research.google.com/github/`. For us that is `colab.research.google.com/github/proelium27/veritas-ai-hackathon/blob/main/notebook/model.ipynb`. This is the link to give judges and to put near the top of the README.

### 2.2 Save the notebook back to GitHub from Colab

1. In Colab, **File > Save a copy in GitHub**. (Allow GitHub access if it asks again, and again include private repos.)
2. Pick the repository `proelium27/veritas-ai-hackathon`, the branch, and the file path (`notebook/model.ipynb` for the main notebook).
3. Write a short commit message in plain English, for example "Add baseline model and test scores".
4. Click **OK**. Then open the file on GitHub and check the commit shows up.

Important facts:
- Saving to a file path that already exists **replaces that file**. If two people save to `notebook/model.ipynb`, the second save wipes out the first. This is why only one person saves the main notebook (next section).
- Run the notebook **before** you save, so the saved copy shows the output (numbers and charts). Judges and teammates then see results without running anything.
- Colab does not auto-save to GitHub. **File > Save** only saves to Google Drive. Save to GitHub often, every time a section works.
- Do not try to pull changes into an open Colab tab. To get the latest version, re-open it from GitHub (2.1).

### 2.3 Only one person edits the main notebook

Teammate 2 is the notebook owner. Everyone else keeps out of `notebook/model.ipynb`.

**For teammates who are not the owner:**
1. Open the latest notebook from GitHub (2.1), then **File > Save a copy in Drive**. Work in that copy. Name it clearly, for example `caleb-eda-section3`.
2. When your section works, send it to the owner. Easiest ways: paste the finished cells in the group chat or a shared Google Doc, or use **File > Save a copy in GitHub** with a *different* path such as `notebook/drafts/teammate3-section7.ipynb`. Never use the main notebook's path.
3. Tell the owner which sections you changed, and say what the cells need (for example "needs the `test_df` table from section 4").

**For the owner:**
1. Open the draft or the pasted cells, paste them into the main notebook in the right section, and run the notebook top to bottom to be sure it still works.
2. Save to `notebook/model.ipynb` (2.2) and post in the chat: "Saved version 7, includes baseline. Everyone re-open from GitHub before you start."
3. Do not edit the notebook in two places at once. If Claude Code is editing the notebook file in the repo, the owner should not be editing it in Colab at the same time. Pick one at a time, say which in the chat, and re-open the latest version before switching.

**Handoff rule:** say it out loud in the chat before and after each save to the main notebook ("I'm editing the main notebook now" / "Done, saved"). Only one person says "I'm editing" at a time.

### 2.4 Check "Run all in a fresh runtime"

This is the test that proves a judge can run our notebook. Do it at least once on Saturday night, and again on Sunday afternoon and just before submitting.

1. Open the notebook from GitHub (2.1), not from your old working tab.
2. **Runtime > Disconnect and delete runtime**. Confirm. This wipes all installed libraries, variables and downloaded files, like a brand-new Colab session.
3. If the notebook needs a GPU, set it again: **Runtime > Change runtime type**.
4. **Runtime > Run all**.
5. Watch it finish. Pass means: no red errors, all sections run in order, the numbers match what the write-up says, and the demo cell works.
6. Write the result and how long it took in `docs/log.md`.

Extras that catch real problems:
- Do the test from a **teammate's account**, not the owner's. If it works for someone who has no secrets and no files in their Drive, it will work for a judge.
- If it asks for a token, a file upload, or a Drive file, that is a bug to fix.
- If it takes over about 20 minutes, think about training on a smaller sample in the notebook, or loading the already-trained model from Hugging Face. Say so clearly in the notebook if you do. Judges have limited time.

---

## 3. Approach playbook by challenge type

**The pattern for every type:** (1) split off a test set first and do not touch it, (2) build a **baseline**, the simplest thing that could work, (3) build a **stronger model**, (4) report the same metric for both on the test set, (5) show **3-5 examples it gets wrong and why**. This pattern is where the "Testing and honesty" points come from. Always say what the baseline scored; a model without one proves nothing.

Other habits: fix the random seed; record every result (even the bad ones) in `docs/log.md`; credit every dataset, library and model; check each model's license on its Hugging Face page. Model names below were right as of writing, but open the model page before relying on one, because names and access rules can change.

If the challenge does not fit one of these four (audio, time series, recommendations, a mix of text and images), use the same pattern: a dumb baseline, a pre-trained model, one honest metric, and real failures.

### 3.1 Text classification
*Examples: spam or not, sentiment, topic, "is this claim reliable", toxic or not.*

- **Baseline:** predicting the most common class (scikit-learn's dummy classifier) as the floor, then **TF-IDF word counts plus logistic regression** in scikit-learn. It trains in seconds and is surprisingly hard to beat.
- **Stronger option:**
  - Fine-tune a small pre-trained language model such as `distilbert-base-uncased` or `distilroberta-base` (needs a Colab GPU; a few epochs on tens of thousands of short texts is fine).
  - Cheaper and still strong: turn each text into a vector with `sentence-transformers/all-MiniLM-L6-v2`, then train logistic regression on those vectors. No GPU needed.
  - If you have no labels, zero-shot with `facebook/bart-large-mnli`.
  - For tweets and sentiment, `cardiffnlp/twitter-roberta-base-sentiment-latest` is already trained for the job (credit it, and still test it on our own split).
- **Metric:** accuracy **and macro F1** (macro F1 treats every class equally, so it exposes a model that ignores the rare class). Add a confusion matrix.
- **Show failures:** list wrongly classified test texts, sorted so that the ones the model was most confident about come first. Pick 3-5 that show different reasons: sarcasm, negation ("not bad"), very short text, slang, a label that is arguably wrong, or a topic that was rare in training. Write one sentence of reason for each.

### 3.2 Image classification
*Examples: plant disease, trash sorting, real vs generated photos, medical scans.*

- **Baseline:** majority class as the floor, then logistic regression on shrunken, flattened pixels, or a tiny convolutional network trained from scratch. Expect these to be weak, which is fine. They show how much the pre-trained model helps.
- **Stronger option (transfer learning, the standard beginner win):**
  - Fine-tune a pre-trained model such as `microsoft/resnet-50`, `facebook/convnext-tiny-224` or `google/vit-base-patch16-224` on our images. Needs a GPU.
  - No-training option: get image vectors from `openai/clip-vit-base-patch32` and train logistic regression on them. CLIP can also classify with no training by matching images to class names (zero-shot), which makes a nice extra comparison.
- **Metric:** accuracy, plus precision and recall per class, plus a confusion matrix. For rare-class problems (disease, defects) lead with recall on that class and say why.
- **Show failures:** display a small grid of wrongly classified test images, each labelled with true class, predicted class and confidence. Explain each: blurry, bad lighting, the object is tiny or half hidden, two classes that look alike, background giving it away, or a mislabelled image. Check that the model is not winning because of the background rather than the object.

### 3.3 Tabular prediction
*Examples: predict a price, churn, loan default, disease risk from a spreadsheet of columns.*

- **Baseline:** predict the average (regression) or the most common class (classification) using scikit-learn's dummy models, then **linear or logistic regression**.
- **Stronger option:** tree-based models are the usual best choice on tables: scikit-learn's `RandomForest` and `HistGradientBoosting`, or the `XGBoost` / `LightGBM` libraries. They need almost no tuning and no GPU. Compare 2-3 of them using cross-validation (five rounds of splitting) on the training set, then score the winner **once** on the test set.
- **Metric:**
  - Predicting a number: MAE (average error in real units, easy to explain) plus RMSE and R².
  - Predicting a category: F1 and ROC-AUC (not only accuracy, since classes are often lopsided).
- **Show failures:** take the rows with the largest errors (or the wrongly classified rows the model was most sure about). Look for what they share: rare category values, extreme numbers, missing values we filled in, or one group the model treats worse. Also report which columns mattered most, and check for **leakage** (a column that secretly contains the answer, such as an outcome recorded after the event). A suspiciously perfect score usually means leakage.

### 3.4 LLM and generation tasks
*Examples: summarize, answer questions over documents, rewrite, explain, translate, a chatbot for a topic.*

- **Baseline:** something with no clever model. For summaries, the **first three sentences of the text**. For question answering, keyword match or "return the most similar passage". Or the same language model with a bare, one-line prompt, so that the improved version can be compared against it.
- **Stronger option:** open models that run in free Colab and that judges can run without keys:
  - Summarizing and rewriting: `facebook/bart-large-cnn` (summaries) or `google/flan-t5-base` / `google/flan-t5-large` (many tasks, follows instructions).
  - Small chat models: `Qwen/Qwen2.5-1.5B-Instruct` or `HuggingFaceTB/SmolLM2-1.7B-Instruct`.
  - The improvement can be in the *method* rather than the model: a better prompt, a few worked examples in the prompt, or retrieval (look up relevant passages first with `sentence-transformers/all-MiniLM-L6-v2`, then answer from them).
  - Avoid depending on a paid API in the notebook. Judges will not have our key. If we use one for an extra, keep it outside the main scoring path and the notebook must still run without it.
  - Some models (the Llama family, for example) are "gated": you must accept the license on the model page and use your token. That is a trap for judges. Prefer ungated models.
- **Metric:** pick one that fits the task and say how it works in one line.
  - Summaries: ROUGE (word overlap with a reference summary).
  - Question answering: exact match and F1 against known answers.
  - Multiple choice or labels: plain accuracy.
  - Open-ended answers: a small **hand-scored sample** (say 30-50 outputs, each marked good/okay/bad against a short rubric) is honest and acceptable. If an AI model grades the outputs, say so plainly and spot-check some by hand.
- **Show failures:** for each of 3-5 bad outputs, show the input, the model's output, what a good answer looks like, and the reason: made-up facts (hallucination), ignored the instruction, too long or cut off, correct but missing the key point, or confused by a long input. Hallucinations are worth showing, since owning the model's limits scores well and is the honest thing to do.

### Speed and size tips (all types)
- Start small: develop on a few thousand rows or images so a full run takes a minute. Scale up only when the pipeline works end to end.
- Free Colab disconnects after idle time and has limits on GPU hours. Save results as you go.
- Judges have limited time and we do not know how long they will wait. Keep the full Run all short.

---

## 4. Kickoff hour: 60-minute script

Clock starts when the challenge is revealed (Sat Nov 14, 12:00 AM ET). If the team wants sleep and starts in the morning, run the same script then, because the plan's timeline has the idea and data decided by the end of Saturday morning. The 48-hour deadline does not move either way, so do not wait long.

Set up first: all three on one video call, a shared doc or `docs/plan.md` open, and the group chat ready. Assign one **note-taker** (suggest Teammate 3) and one **timekeeper** (anyone) who calls out each block.

| Time | Do this | Output |
|---|---|---|
| **0:00-0:10** | **Read the challenge.** Everyone reads the official text silently first, then reads the key lines out loud together. Note: the track, what the task actually asks for, any starter kit or provided dataset, required formats, **where to submit**, and any rule that differs from our notes. | Official text pasted into the "Fill in at kickoff" block of `docs/plan.md`. `docs/competition.md` updated if the rules differ. |
| **0:10-0:20** | **Frame the problem.** Answer together: What goes in? What comes out? Who is the user? Which of the four types in section 3 is it? What would "it works" mean in numbers? | Two sentences: the problem, and the input-to-output. |
| **0:20-0:35** | **Brainstorm ideas.** Each person pitches one or two ideas in 2-3 minutes each, no arguing yet. Then give every idea 1-5 on the judging table: *Technical execution* (can we build and score it on free Colab?), *Originality* (a specific angle, not a tutorial), *Impact and track fit* (who it helps, tied to the challenge), *Testing and honesty* (is there a clear baseline and test set?), *Communication* (could all three of us explain it?). | A short list with scores. Top 2 ideas circled. |
| **0:35-0:50** | **Find the data**, in parallel. Teammate 3 and Caleb search; Teammate 2 checks the starter kit if there is one. Good places: the starter kit first, then Hugging Face Datasets, Kaggle, the UCI repository, Google Dataset Search. Test each candidate against the checklist below. | A link and license for the dataset behind each of the top 2 ideas. |
| **0:50-0:55** | **Decide.** Pick one idea, and name the fallback. Set the trip-wire: if the data will not load, or the baseline is not working by a fixed time (say Sat 11:00 AM), switch to the fallback without a long debate. | One decision and one fallback. |
| **0:55-1:00** | **Lock it in.** Fill in the plan block (track, challenge, idea, dataset with link and license, where to submit). Add a "Decisions" line to `docs/log.md`. Paste the kickoff prompt from `docs/plan.md` (with the challenge text) into Claude Code. Teammate 2 opens a fresh Colab notebook. Agree when you next check in. | Plan filled in. Repo layout being created. Everyone knows their next task. |

### Dataset checklist (check each candidate)
- [ ] It loads from a public link with **no sign-in on a laptop** (rule: data comes from a public source, never from someone's laptop). Datasets on Hugging Face or at a plain public URL are easiest. Kaggle usually needs an account and API key, which makes a fresh-Colab run harder, so only choose it if there is a clean way for a judge to load it.
- [ ] The license allows our use, and we have the credit line ready for the README.
- [ ] It has **labels** (or the task does not need them) and enough rows: a few thousand is workable; hundreds of thousands will be slow on free Colab.
- [ ] Size fits Colab: roughly under 1-2 GB, and not far larger than we can load in a couple of minutes.
- [ ] We can hold out a proper test set (about 20%) that the model never sees.
- [ ] It is not obviously leaky (a column that gives away the answer).
- [ ] The classes are not so lopsided that a trivial model scores 99%. If they are, plan to use F1 or recall rather than accuracy.

### Common ways the first hour goes wrong
- **Picking the biggest, coolest idea.** Choose the one you can finish and explain. A small idea tested honestly beats a big one that does not run.
- **Spending 45 minutes on the idea and 5 on the data.** An idea without loadable data is not an idea. Keep the time blocks.
- **Skipping the fallback.** Name it now, while nobody is tired.
- **One person quietly deciding.** All three of us must be able to explain the choice to a judge.
