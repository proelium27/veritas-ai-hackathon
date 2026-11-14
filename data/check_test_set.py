"""Check data/test_sentences.csv for mistakes before we use it.

What this script does, in plain English:
  1. Opens the CSV file of test sentences.
  2. Checks that the column names are exactly the ones the notebook expects.
  3. Goes through every row and looks for problems:
       - empty cells that must be filled in
       - values that are not on the allowed list (for example "female" instead of "woman")
       - the same id used twice
       - Cyrillic letters (а, б, ш, ж ...) in the Serbian, which must be Latin only
       - Serbian that looks typed without the marks (sta instead of šta)
       - 您 (formal "you") marked formal=no, or 你 (informal "you") marked formal=yes
  4. Prints a table counting the rows in each category, so we can compare
     against the target mix in data/README.md.

"Errors" must be fixed. "Warnings" are worth a look but may be fine.
The script ends with exit code 0 when there are no errors, and 1 otherwise.

How to run it (from the top folder of the repo):
    python3 data/check_test_set.py
    python3 data/check_test_set.py path/to/another_copy.csv

It only uses Python's built-in modules, so nothing needs installing.
"""

import csv
import io
import sys
import unicodedata
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# The rules the file must follow
# ---------------------------------------------------------------------------

# The exact column names, in order. The notebook relies on these names.
EXPECTED_HEADER = [
    "id",
    "mandarin",
    "english_meaning",
    "speaker_gender",
    "listener_gender",
    "formal",
    "what_it_tests",
    "correct_serbian",
    "notes",
    "split",
]

# Columns that must not be empty on a real (non-example) row.
# "notes" is the only optional column.
REQUIRED_COLUMNS = [name for name in EXPECTED_HEADER if name != "notes"]

# The values each labelled column is allowed to hold.
ALLOWED_VALUES = {
    "speaker_gender": {"man", "woman"},
    "listener_gender": {"man", "woman", "group"},
    "formal": {"yes", "no"},
    "split": {"practice", "test"},
}

# what_it_tests can hold one or more of these, joined with "+".
ALLOWED_TESTS = ["speaker_gender", "listener_gender", "formality", "control"]

# Example rows have a notes cell that starts with this text.
EXAMPLE_MARKER = "EXAMPLE - delete before use"

# Target number of rows for each kind of sentence (from data/README.md).
TARGET_TESTS = {
    "speaker_gender": 24,
    "listener_gender+formality": 16,
    "formality": 16,
    "listener_gender": 8,
    "speaker_gender+formality": 8,
    "control": 8,
}
TARGET_SPLIT = {"practice": 20, "test": 60}

# Common words that need a mark, as people type them when the marks are left off:
# sta (šta, "what"), cao (ćao, "hi/bye"), sto (što, "why/that"), jos (još, "still/yet").
# ("sto" is also a real word, "hundred" or "table", which is why this is only a warning.)
MISSING_MARK_GIVEAWAYS = {"sta", "cao", "sto", "jos"}

# The Serbian Latin letters that carry a mark (dž is d + ž, so ž covers it).
MARKED_LETTERS = set("čćšžđČĆŠŽĐ")

# By default, check the CSV that sits next to this script.
DEFAULT_PATH = Path(__file__).parent / "test_sentences.csv"


# ---------------------------------------------------------------------------
# Small helper functions
# ---------------------------------------------------------------------------

def cyrillic_letters_in(text):
    """Return the Cyrillic letters found in text (Serbian must be Latin only).

    unicodedata.name() gives every character its official Unicode name,
    e.g. "CYRILLIC SMALL LETTER ES" for с, or
    "LATIN SMALL LETTER S WITH CARON" for š. So any letter whose name
    contains "CYRILLIC" is a Cyrillic letter. This also catches Cyrillic
    letters that look exactly like Latin ones (Cyrillic а, е, о, с, р).
    """
    found = []
    for character in text:
        if character.isalpha() and "CYRILLIC" in unicodedata.name(character, ""):
            found.append(character)
    return found


def missing_mark_giveaways(text):
    """Return giveaway words (sta, cao, sto, jos) if the text has no marked letters.

    If the answer already has any of č, ć, š, ž, đ, the writer is using the
    marks, so we stay quiet. Otherwise we look for whole words that are
    usually šta, ćao, što or još typed without their marks.
    """
    if any(character in MARKED_LETTERS for character in text):
        return []
    # Turn every non-letter (spaces, commas, ?) into a space, then split into words.
    letters_only = "".join(c if c.isalpha() else " " for c in text.lower())
    return [word for word in letters_only.split() if word in MISSING_MARK_GIVEAWAYS]


def tidy_tests(value):
    """Put the parts of what_it_tests in a standard order for counting.

    "formality+listener_gender" and "listener_gender+formality" mean the
    same thing, so both are counted as "listener_gender+formality".
    """
    parts = [part.strip() for part in value.split("+")]
    known = [name for name in ALLOWED_TESTS if name in parts]
    unknown = [part for part in parts if part not in ALLOWED_TESTS]
    return "+".join(known + unknown)


def print_counts(title, counter, targets=None):
    """Print one small table: each value, how many rows have it, and the target."""
    print(f"\n  {title}")
    values = list(counter)
    if targets:
        # Show every target category, even ones with 0 rows so far.
        values = list(targets) + [v for v in counter if v not in targets]
    for value in values:
        shown = value if value else "(empty)"
        line = f"    {shown:<28} {counter.get(value, 0):>4}"
        if targets and value in targets:
            line += f"   (target {targets[value]})"
        print(line)


# ---------------------------------------------------------------------------
# The main check
# ---------------------------------------------------------------------------

def check(path):
    errors = []    # must be fixed
    warnings = []  # worth a look

    # --- Read the raw file -------------------------------------------------
    try:
        raw_bytes = Path(path).read_bytes()
    except FileNotFoundError:
        print(f"ERROR: file not found: {path}")
        return 1

    # A "BOM" is 3 invisible bytes some programs (like Excel) put at the start.
    # It would sneak into the first column name, so the notebook could not find "id".
    if raw_bytes.startswith(b"\xef\xbb\xbf"):
        errors.append("File starts with a BOM (invisible bytes, often added by Excel). "
                      "Re-save it as plain UTF-8, e.g. download it from Google Sheets.")
        raw_bytes = raw_bytes[3:]

    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        print("ERROR: the file is not UTF-8, so Chinese characters and letters like č would break. "
              "Download it again from Google Sheets as CSV.")
        return 1

    # --- Check the header row ----------------------------------------------
    # csv.DictReader turns each row into a dictionary: {"id": "1", "mandarin": ...}
    # io.StringIO lets the csv module read the text as if it were a file.
    reader = csv.DictReader(io.StringIO(text, newline=""))
    header = reader.fieldnames or []
    if header != EXPECTED_HEADER:
        print("ERROR: the header row (column names) is wrong.")
        print(f"  expected: {','.join(EXPECTED_HEADER)}")
        print(f"  found:    {','.join(header)}")
        return 1  # nothing else can be checked reliably

    # --- Check every row ---------------------------------------------------
    seen_ids = {}          # id -> line number where we first saw it
    counts = {name: Counter() for name in
              ["speaker_gender", "listener_gender", "formal", "what_it_tests", "split"]}
    total_rows = 0
    example_rows = 0

    for row in reader:
        line = reader.line_num  # line number in the file, for the messages

        # A row with too many cells puts the extras under the key None;
        # a row with too few cells has None as some values.
        if None in row:
            errors.append(f"line {line}: too many cells. A cell with a comma in it "
                          f"probably needs \"double quotes\" around it.")
            continue
        if any(value is None for value in row.values()):
            errors.append(f"line {line}: too few cells (some commas are missing).")
            continue

        # Remove spaces at the start/end of every cell.
        row = {name: value.strip() for name, value in row.items()}

        # Skip rows that are completely empty (spreadsheets sometimes add them).
        if not any(row.values()):
            continue

        total_rows += 1
        row_id = row["id"] or f"(no id, line {line})"
        where = f"line {line}, id {row_id}"
        is_example = row["notes"].startswith(EXAMPLE_MARKER)
        if is_example:
            example_rows += 1

        # 1. Required cells must be filled in (example rows may leave split empty).
        for column in REQUIRED_COLUMNS:
            if row[column] == "":
                if is_example and column == "split":
                    continue
                errors.append(f"{where}: '{column}' is empty.")

        # 2. Labelled columns must use an allowed value.
        for column, allowed in ALLOWED_VALUES.items():
            value = row[column]
            if value and value not in allowed:
                errors.append(f"{where}: '{column}' is '{value}', "
                              f"must be one of: {', '.join(sorted(allowed))}.")

        # 3. what_it_tests: every part joined with "+" must be allowed.
        tests_value = row["what_it_tests"]
        if tests_value:
            parts = [part.strip() for part in tests_value.split("+")]
            for part in parts:
                if part not in ALLOWED_TESTS:
                    errors.append(f"{where}: what_it_tests has '{part}', "
                                  f"must be from: {', '.join(ALLOWED_TESTS)}.")
            if len(parts) != len(set(parts)):
                errors.append(f"{where}: what_it_tests repeats a part: '{tests_value}'.")
            if "control" in parts and len(parts) > 1:
                errors.append(f"{where}: 'control' means nothing is tested, "
                              f"so it can't be joined with anything else.")

        # 4. Ids must be unique.
        if row["id"]:
            if row["id"] in seen_ids:
                errors.append(f"{where}: id '{row['id']}' is already used "
                              f"on line {seen_ids[row['id']]}.")
            else:
                seen_ids[row["id"]] = line

        # 5. The Serbian must be Latin only (the notebook converts the models'
        #    Cyrillic output to Latin, so the answers must be Latin to compare).
        cyrillic = cyrillic_letters_in(row["correct_serbian"])
        if cyrillic:
            errors.append(f"{where}: correct_serbian has Cyrillic letters "
                          f"{''.join(cyrillic)!r}; write it in Latin letters only.")

        # 5b. Warn if the Serbian looks typed without the marks (sta, not šta).
        giveaways = missing_mark_giveaways(row["correct_serbian"])
        if giveaways:
            warnings.append(f"{where}: correct_serbian has {', '.join(giveaways)} and no "
                            f"č/ć/š/ž/đ at all; were the marks left off (šta, ćao, što, još)?")

        # 6. 您 is formal "you", 你 is informal "you". Warn if the label disagrees.
        if "您" in row["mandarin"] and row["formal"] == "no":
            warnings.append(f"{where}: Mandarin has 您 (formal you) but formal=no.")
        if "你" in row["mandarin"] and row["formal"] == "yes":
            warnings.append(f"{where}: Mandarin has 你 (informal you) but formal=yes.")

        # Add this row to the summary counts.
        for column in counts:
            value = row[column]
            if column == "what_it_tests":
                value = tidy_tests(value)
            counts[column][value] += 1

    if example_rows:
        warnings.append(f"{example_rows} example row(s) still in the file. "
                        f"Delete them before the file is used for testing.")
    if total_rows == 0:
        errors.append("The file has a header but no rows.")

    # --- Print the report --------------------------------------------------
    print(f"Checked {path}")
    print(f"Rows: {total_rows} ({example_rows} example, {total_rows - example_rows} real)")

    print(f"\nErrors: {len(errors)}")
    for message in errors:
        print(f"  ERROR    {message}")
    print(f"\nWarnings: {len(warnings)}")
    for message in warnings:
        print(f"  WARNING  {message}")

    print("\nSummary (counts include example rows):")
    print_counts("speaker_gender", counts["speaker_gender"])
    print_counts("listener_gender", counts["listener_gender"])
    print_counts("formal", counts["formal"])
    print_counts("what_it_tests", counts["what_it_tests"], TARGET_TESTS)
    print_counts("split", counts["split"], TARGET_SPLIT)

    if errors:
        print("\nResult: fix the errors above.")
        return 1
    print("\nResult: no errors.")
    return 0


if __name__ == "__main__":
    # Use the path given on the command line, or the default file.
    csv_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    sys.exit(check(csv_path))
