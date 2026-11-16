# Our test set and human check

`test_sentences.csv` is our own test set: 60 short workplace sentences (factory floor, supervisor and worker) in Mandarin, each with the correct Serbian translation. The notebook uses it to check whether a translation gets the Serbian endings right for:

- **who is speaking** (a woman says *Proverila sam*, a man says *Proverio sam*),
- **who is listening** (to a woman *došla*, to a man *došao*),
- **how formal it is** (您 becomes *Vi / ste*, 你 becomes *ti / si*).

The notebook loads it from `https://raw.githubusercontent.com/proelium27/veritas-ai-hackathon/main/data/test_sentences.csv`, so the version in the repo is the one that counts.

This page started as the instructions our team followed while writing the sentences. The rules below are the ones we used.

## The columns

| Column | What goes in it | Allowed values | Who fills it |
|---|---|---|---|
| `id` | A unique row id: `t01` to `t60` | any text, no repeats | Mandarin speaker |
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

If more than one Serbian answer is correct, the Serbian speaker writes the most natural one in `correct_serbian` and puts the others in `notes` as `also OK: ...`. If a label looks wrong, say so in `notes` and talk to the Mandarin speaker instead of quietly changing it.

## The mix (60 rows)

We planned 80 rows and wrote 60, three quarters of each kind:

| Kind of sentence | `what_it_tests` | Rows (practice + test) |
|---|---|---|
| "I did X" | `speaker_gender` | 18 (4 + 14) |
| "Did you do X?" to one person, casual (你) | `listener_gender+formality` | 12 (3 + 9) |
| "Did you do X?" to one person, formal (您) | `formality` | 12 (3 + 9) |
| "Did you all do X?" to a group (你们) | `listener_gender` | 6 (2 + 4) |
| "I did X for you" (speaker and listener both show) | `speaker_gender+formality` | 6 (2 + 4) |
| No gender or formality at all | `control` | 6 (1 + 5) |
| **Total** | | **60 (15 + 45)** |

Across all 60 rows, 30 women and 30 men are speaking; the listeners are 27 men, 27 women and 6 groups; 27 rows are formal and 33 casual.

With formal *Vi*, Serbian normally uses the plural form (*došli*) for both a man and a woman, so the listener's gender usually doesn't show. That is why the formal "Did you...?" rows test only `formality`. The Serbian speaker has the final say on what is correct.

## Rules

1. **Write the Serbian from the English meaning plus the labels only.** Never look at Google Translate, DeepL, ChatGPT or any other translation app or model output while writing it. If the answers come from a machine, the test is worthless.
2. **One script: Latin, with the marks.** Write `correct_serbian` in Latin letters and always use č, ć, š, ž, đ and dž, never plain c, s, z or d in their place. The marks are part of the spelling. Without them a word is misspelled (*sta* for *šta*) or turns into a different word (*kuca* "knocks" for *kuća* "house"), and the notebook would count a correct model answer as wrong. The translation models write Cyrillic, and the notebook converts their output to Latin one letter at a time, so our answers must be in Latin for a fair comparison. No Cyrillic letters in `correct_serbian` (the checker flags them). To type the marks, add the Serbian (Latin) keyboard in your computer's or phone's settings.
3. **Keep sentences short, one clause each**, like "I already turned the machine off." Workplace topics only.
4. **No real names or personal information.** Use "the manager", "the machine", "line 3", not anyone's name.
5. The Mandarin can be drafted with an AI tool, but the Mandarin speaker must read and fix every sentence and its labels.

## Practice and test rows

- **Practice** (15 rows): we looked at these freely, ran the translation models on them, and used them to build and fix the rules that check the Serbian endings.
- **Test** (45 rows): locked. Nobody looked at model output for test rows until the checking rules were final. Then we ran every model on them once and reported the score, bad or not.
- `split` was set when each row was written, before any model had seen it, with about one row in four of each kind marked `practice`. A row never moves between practice and test after we see results; that would be cheating our own test.

## Checking the file

From the top folder of the repo, run:

```bash
python3 data/check_test_set.py
```

It lists problems: wrong column names, empty cells, values that aren't allowed, repeated ids, Cyrillic letters in the Serbian, Serbian that looks typed without the č/ć/š/ž/đ marks, and 您/你 that don't match `formal`. It also prints counts for each column. Its "target" counts are the original plan of 80 rows, so on our 60 rows each count shows as lower than its target; that is expected. To check a downloaded copy instead, give its path: `python3 data/check_test_set.py ~/Downloads/test_sentences.csv`.

## Source and credit

Our team wrote the sentences. Claude (an AI tool) drafted the Mandarin, and a native Mandarin speaker checked and corrected it. A native Serbian speaker wrote the Serbian from the English meaning and the labels, without any translation tool.

## The human check: `human_check.csv`

`human_check.csv` holds our native Serbian speaker's hand grades of the 45 **test** rows (same ids as `test_sentences.csv`). For each row it has the exact Serbian answer of all three systems (`picker_output` for ours, `direct_output` for NLLB direct, `baseline_output` for the route through English), copied from the notebook's saved test outputs, and two yes/no grades per system:

- `*_meaning`: `y` if the Serbian means what the English meaning says, `n` if not.
- `*_endings`: `y` if the speaker's gender, the listener's gender and the formality are right, `n` if not. The 5 `control` rows have no ending to test, so the notebook doesn't count this column there.

Our native Serbian speaker graded every answer by hand in a shared spreadsheet, without any translation tool and without the notebook's `detect()` reader. We copied the grades into this file unchanged. The notebook loads it from `https://raw.githubusercontent.com/proelium27/veritas-ai-hackathon/main/data/human_check.csv` (section 7.1).
