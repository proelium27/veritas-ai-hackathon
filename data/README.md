# Test sentences: how to fill them in

`test_sentences.csv` is our own test set: short workplace sentences (factory floor, supervisor and worker) in Mandarin, each with the correct Serbian translation. The notebook uses it to check whether a translation gets the Serbian endings right for:

- **who is speaking** (a woman says *Proverila sam*, a man says *Proverio sam*),
- **who is listening** (to a woman *došla*, to a man *došao*),
- **how formal it is** (您 becomes *Vi / ste*, 你 becomes *ti / si*).

The notebook loads it from `https://raw.githubusercontent.com/proelium27/veritas-ai-hackathon/main/data/test_sentences.csv`, so the version in the repo is the one that counts.

The file starts with 4 example rows (`ex1` to `ex4`). Read them, then delete them before adding real rows.

## The columns

| Column | What goes in it | Allowed values | Who fills it |
|---|---|---|---|
| `id` | A unique row number: `1`, `2`, `3`, ... | any text, no repeats | Mandarin speaker |
| `mandarin` | The sentence in Mandarin (simplified characters) | | Mandarin speaker |
| `english_meaning` | What the sentence means, in plain English | | Mandarin speaker |
| `speaker_gender` | Who is talking | `man`, `woman` | Mandarin speaker |
| `listener_gender` | Who is being spoken to | `man`, `woman`, `group` | Mandarin speaker |
| `formal` | Is it polite/formal (您, talking to a manager)? | `yes`, `no` | Mandarin speaker |
| `what_it_tests` | Which ending the sentence checks. Join several with `+` | `speaker_gender`, `listener_gender`, `formality`, `control` (e.g. `speaker_gender+formality`) | Mandarin speaker |
| `correct_serbian` | The correct Serbian, in Latin letters with the marks (č, ć, š, ž, đ, dž) | | **Serbian speaker only** |
| `notes` | Anything worth knowing (optional) | | either |
| `split` | `practice` or `test` (see below) | `practice`, `test` | Mandarin speaker |

`control` means the sentence has no speaker gender, listener gender or formality in it at all (for example "The machine is broken."). Controls show whether a translation tool is right for the right reason.

If more than one Serbian answer is correct, the Serbian speaker writes the most natural one in `correct_serbian` and puts the others in `notes` as `also OK: ...`. If a label looks wrong, say so in `notes` and talk to the Mandarin speaker; don't quietly change it.

## Target mix (80 rows)

| Kind of sentence | `what_it_tests` | Rows | Balance inside the group |
|---|---|---|---|
| "I did X" | `speaker_gender` | 24 | 12 woman / 12 man speakers; 12 formal / 12 informal |
| "Did you do X?" to one person, informal (你) | `listener_gender+formality` | 16 | 8 to a woman / 8 to a man; all `formal=no` |
| "Did you do X?" to one person, formal (您) | `formality` | 16 | 8 to a woman / 8 to a man; all `formal=yes` |
| "Did you all do X?" to a group (你们) | `listener_gender` | 8 | `listener_gender=group`; 4 formal / 4 informal |
| "I did X for you" (speaker and listener both show) | `speaker_gender+formality` | 8 | 4 woman / 4 man speakers; 4 formal / 4 informal |
| No gender or formality at all | `control` | 8 | 4 woman / 4 man speakers; 4 formal / 4 informal |
| **Total** | | **80** | |

Across all 80 rows that gives 40 women and 40 men speaking, and 40 formal and 40 informal. In every group, also split the speaker 50/50 between women and men. Of the 80 rows, 20 are `practice` and 60 are `test` (one in four of each kind; see below).

With formal Vi, Serbian normally uses the plural form (*došli*) for both a man and a woman, so the listener's gender usually doesn't show. That is why formal "Did you...?" rows test only `formality`. The Serbian speaker has the final say on what is correct.

## Rules

1. **Write the Serbian from the English meaning plus the labels only.** Never look at Google Translate, DeepL, ChatGPT or any other translation app or model output while writing it. If the answers come from a machine, the test is worthless.
2. **One script: Latin, with the marks.** Write `correct_serbian` in Latin letters and always use č, ć, š, ž, đ and dž, never plain c, s, z or d in their place. The marks are part of the spelling: without them a word is misspelled (*sta* for *šta*) or becomes a different word (*kuca* "knocks" for *kuća* "house"), and the notebook would count a correct model answer as wrong. The translation models write Cyrillic and the notebook converts their output to Latin letter for letter, so our answers must be in Latin to compare fairly. No Cyrillic letters in `correct_serbian` (the checker flags them). To type the marks, add the Serbian (Latin) keyboard in your computer's or phone's settings.
3. **Keep sentences short: one clause each**, like "I already turned the machine off." Workplace topics only.
4. **No real names or personal information.** Use "the manager", "the machine", "line 3", not anyone's name.
5. The Mandarin can be drafted with an AI tool, but the Mandarin speaker must read and fix every sentence and its labels.

## Practice and test rows

- **Practice** (20 rows): we look at these freely, run translation models on them, and use them to build and fix the rules that check the Serbian endings.
- **Test** (60 rows): locked. Nobody looks at model output for test rows until the checking rules are final. Then we run every model on them once and report the score, even if it's bad.
- Set `split` when the row is written, before any model has seen it: mark one row in four of each kind as `practice`. Never move a row between practice and test after seeing results. That would be cheating our own test.

## How to edit the file

**Option A: Google Sheets (easiest)**

1. In Google Sheets: File > Import > Upload, and pick `test_sentences.csv`.
2. Separator: comma. **Untick "Convert text to numbers, dates and formulas"** so nothing gets changed.
3. Edit the rows.
4. File > Download > Comma-separated values (.csv).
5. Send the downloaded file to the teammate who manages the repo.

Avoid opening the CSV straight in Excel: it can scramble Chinese characters and Serbian letters like č and š.

**Option B: edit in the repo.** Open `data/test_sentences.csv` in a code editor (VS Code shows it as plain text). Any cell that contains a comma must be wrapped in double quotes, like `"one, two"`. Commit and push as usual.

## Check the file before sending it

From the top folder of the repo, run:

```bash
python3 data/check_test_set.py
```

It lists problems (wrong column names, empty cells, values that aren't allowed, repeated ids, Cyrillic letters in the Serbian, Serbian that looks typed without the č/ć/š/ž/đ marks, 您/你 that don't match `formal`) and prints counts for each column so you can compare against the target mix above. Empty `correct_serbian` cells show up as errors until the Serbian speaker fills them in; that's expected while the work is in progress. To check a downloaded copy instead, give its path: `python3 data/check_test_set.py ~/Downloads/test_sentences.csv`.

## Source and credit

The sentences are written by our team: the Mandarin was drafted with an AI tool and checked and corrected by a native Mandarin speaker; the Serbian was written by a native Serbian speaker from the English meaning and labels, without any translation tool.

## The human check: `human_check.csv`

`human_check.csv` holds our native Serbian speaker's hand grades of the 45 **test** rows (same ids as `test_sentences.csv`). For each row it has the exact Serbian answer of all three systems (`picker_output` for ours, `direct_output` for NLLB direct, `baseline_output` for the route through English), copied from the notebook's saved test outputs, and two yes/no grades per system:

- `*_meaning`: `y` if the Serbian means what the English meaning says, `n` if not.
- `*_endings`: `y` if the speaker's gender, the listener's gender and the formality are right, `n` if not. On the 5 `control` rows there is no ending to test, so the notebook doesn't count this column there.

Our native Serbian speaker graded every answer by hand in a shared spreadsheet, without any translation tool and without the notebook's `detect()` reader. We copied the grades into this file unchanged. The notebook loads it from `https://raw.githubusercontent.com/proelium27/veritas-ai-hackathon/main/data/human_check.csv` (section 7.1).
