"""
Lost in Translation: the demo page
==================================

What this file does
-------------------
It opens a small web page (made with Gradio) where you type a Mandarin sentence, choose
who is speaking, who they are talking to and whether it's formal, and see three Serbian
translations side by side: through English (the baseline), NLLB direct, and ours
(NLLB + our picker). We use it to film the demo video.

The graded project is notebook/model.ipynb. This page is an extra: it changes no score.

Why a plain Python file, and why it reads the notebook
------------------------------------------------------
- One file you can read top to bottom, and it runs the same way on a laptop and in Colab.
- It holds NO translation rules. It opens notebook/model.ipynb and runs the notebook cells
  that define to_latin(), detect(), repair(), pick() and translate_one(). So the notebook
  stays the one place where the rules live: change a rule there, and this page changes too.
- It skips the cells that translate and score our 60 test sentences (sections 4, 7, 7b
  and most of 3, 5 and 6), so it starts faster and uses less memory.
- To fill in the page, it calls the notebook's own translate_one(). While translate_one()
  runs, we note down what two of its helpers, translate() and pick(), hand back (see
  translate_and_record below). So the cards show exactly the answers the notebook prints.

How to run it
-------------
On a laptop, from the repo's top folder:
    pip install -r requirements.txt
    python app/demo.py
then open http://127.0.0.1:7860 in a browser. The page only works on your own computer
(no public link). Stop it with Ctrl+C.

In Google Colab, in a new notebook, one cell:
    !pip install -q gradio sentencepiece sacremoses sacrebleu
    !wget -q -O demo.py https://raw.githubusercontent.com/proelium27/veritas-ai-hackathon/main/app/demo.py
    %run demo.py
Gradio prints a public link ending in .gradio.live: open it in a new tab. (Colab doesn't have the repo, so this file downloads the
notebook from GitHub.)

The first start downloads the three models (about 3 GB). After that, starting takes
about half a minute, and each sentence a few seconds on a laptop CPU.
"""

import ast              # reads Python code as a tree, so we can keep only some lines of a cell
import contextlib       # lets us catch what translate_one() prints
import html             # makes model output safe to put inside a web page
import io               # a "file" that lives in memory (for the caught printout)
import json             # a .ipynb notebook file is JSON
import os
import sys              # to tell whether we are running inside Google Colab
import threading        # loads the models in the background while the page is already open
import time
import urllib.request   # downloads the notebook when it isn't on this computer (Colab)
from pathlib import Path

# The notebook imports matplotlib. We draw no charts, so tell it not to open any windows.
os.environ.setdefault("MPLBACKEND", "Agg")

import gradio as gr     # builds the web page


# ---------------------------------------------------------------------------
# 1. Read the notebook
# ---------------------------------------------------------------------------

NOTEBOOK_PATH = Path(__file__).resolve().parent.parent / "notebook" / "model.ipynb"
NOTEBOOK_URL = ("https://raw.githubusercontent.com/proelium27/veritas-ai-hackathon/"
                "main/notebook/model.ipynb")


def read_notebook():
    """Return the notebook's cells: from the repo if it's here, otherwise from GitHub (Colab)."""
    if NOTEBOOK_PATH.exists():
        text = NOTEBOOK_PATH.read_text(encoding="utf-8")
    else:
        print("notebook/model.ipynb isn't on this computer, so we download it from GitHub.")
        with urllib.request.urlopen(NOTEBOOK_URL, timeout=30) as response:
            text = response.read().decode("utf-8")
    return json.loads(text)["cells"]


CELLS = read_notebook()
CODE_CELLS = [(number, "".join(cell["source"])) for number, cell in enumerate(CELLS)
              if cell["cell_type"] == "code"]


def find_cell(marker):
    """Find the one code cell that contains this piece of text. Stop with a clear message if
    it's missing or appears more than once (that means someone changed the notebook)."""
    found = [(number, source) for number, source in CODE_CELLS if marker in source]
    if len(found) != 1:
        raise RuntimeError(f"Expected exactly 1 notebook cell containing {marker!r}, found {len(found)}. "
                           "Update the lists at the top of app/demo.py.")
    return found[0]


def definitions_only(source):
    """Keep only a cell's imports, function definitions and settings written in CAPITALS
    (like N_OPTIONS = 32). Drop the rest, which works on our 60 test sentences."""
    tree = ast.parse(source)
    keep = []
    for statement in tree.body:
        if isinstance(statement, (ast.Import, ast.ImportFrom, ast.FunctionDef)):
            keep.append(statement)
        elif isinstance(statement, ast.Assign) and all(
                isinstance(target, ast.Name) and target.id.isupper() for target in statement.targets):
            keep.append(statement)
    return ast.Module(body=keep, type_ignores=[])


# The notebook cells we run, found by a piece of text only that cell contains.
# These cells only set things up, so we run them whole:
RUN_WHOLE_CELL = {
    "SEED = 42":                        "imports, the fixed seed, GPU or CPU",
    "def load_test_set(":               "our 60 sentences (only to warn if you type one of them)",
    "def translate(":                   "load() and translate()",
    "def to_latin(":                    "to_latin(): Cyrillic letters to Latin letters",
    "facebook/nllb-200-distilled-600M": "loads NLLB",
    "def detect(":                      "detect(): reads the endings",
    "def repair(":                      "repair(): fixes the endings",
    "def translate_one(":               "section 8: loads the baseline models again, translate_one()",
}
# These cells also translate or score the 60 sentences, so we take only their definitions:
DEFINITIONS_ONLY = {
    "def tests_property(": "tests_property(): does a row test the speaker, listener or formality?",
    "N_OPTIONS =":       "N_OPTIONS (32)",
    "PROPERTY_CHECKS =": "PROPERTY_CHECKS, tested() and fits()",
    "def pick(":         "pick(): the picker",
}

# The three example sentences are the ones in section 8 of the notebook (its MANDARIN,
# SPEAKER, LISTENER and FORMAL settings), so the buttons match the notebook.
EXAMPLES = []
for _, source in CODE_CELLS:
    if "translate_one(MANDARIN" in source:
        settings = {}
        exec(compile(definitions_only(source), "example", "exec"), settings)
        EXAMPLES.append({"mandarin": settings["MANDARIN"], "speaker": settings["SPEAKER"],
                         "listener": settings["LISTENER"], "formal": "yes" if settings["FORMAL"] else "no"})


# ---------------------------------------------------------------------------
# 2. Run the notebook's code (in the background, so the page can show "Loading...")
# ---------------------------------------------------------------------------

NB = {"__name__": "model_notebook"}   # the notebook's settings and functions end up in here
READY = threading.Event()             # set once loading has finished (or failed)
LOAD_ERRORS = []


def load_notebook_code():
    try:
        chosen = [(*find_cell(marker), True) for marker in RUN_WHOLE_CELL]
        chosen += [(*find_cell(marker), False) for marker in DEFINITIONS_ONLY]
        chosen.sort()                 # run them in the notebook's own order
        # Section 6 starts with "del zh_en, en_sr" (it frees section 5's baseline models).
        # We skip section 5's loading, so give it two empty stand-ins to delete.
        NB["zh_en"] = NB["en_sr"] = None
        for number, source, whole in chosen:
            code = source if whole else definitions_only(source)
            exec(compile(code, f"model.ipynb cell {number}", "exec"), NB)
        print(f"\nModels ready (running on {NB['DEVICE']}).")
    except Exception as error:
        LOAD_ERRORS.append(f"{type(error).__name__}: {error}")
        raise
    finally:
        READY.set()


# ---------------------------------------------------------------------------
# 3. Translate one sentence with the notebook's translate_one()
# ---------------------------------------------------------------------------

ONE_AT_A_TIME = threading.Lock()   # one sentence at a time keeps memory low


def translate_and_record(mandarin, speaker, listener, formal):
    """Call the notebook's translate_one(). It prints its answers; to show them as cards we
    also need them as values. translate_one() looks up translate() and pick() by name each
    time it runs, so for this one call we put in versions that do exactly the same thing
    and also write down what they returned. Afterwards we put the real ones back."""
    real_translate, real_pick = NB["translate"], NB["pick"]
    translations, picks = [], []

    def translate_and_note(*args, **kwargs):
        result = real_translate(*args, **kwargs)
        translations.append(result)
        return result

    def pick_and_note(options, row):
        result = real_pick(options, row)
        picks.append((options, row, result))
        return result

    printed = io.StringIO()
    with ONE_AT_A_TIME:
        NB["translate"], NB["pick"] = translate_and_note, pick_and_note
        try:
            with contextlib.redirect_stdout(printed):
                NB["translate_one"](mandarin, speaker, listener, formal)
        finally:
            NB["translate"], NB["pick"] = real_translate, real_pick

    # translate_one() calls translate() three times: Mandarin -> English, English -> Serbian,
    # then NLLB's 32 options. Each call returns one list of answers per sentence.
    english = translations[0][0][0]
    baseline = NB["to_latin"](translations[1][0][0])
    options, row, (picked, note) = picks[0]     # options are already in Latin letters
    return {"english": english, "baseline": baseline, "options": options, "row": row,
            "picked": picked, "note": note, "printout": printed.getvalue()}


# ---------------------------------------------------------------------------
# 4. Turn the answers into the page's cards (HTML)
# ---------------------------------------------------------------------------

PROPERTY_NAMES = {"speaker_gender": "the speaker's gender", "listener_gender": "the listener's gender",
                  "formality": "formality"}


def esc(text):
    return html.escape(str(text))


def chips(serbian, row):
    """✓ / ✗ chips, from the notebook's endings_note(), e.g. 'speaker: woman ✓'."""
    note = NB["endings_note"](serbian, row)
    if note == "nothing to check":
        return '<div class="chips"><span class="chip none">nothing to check</span></div>'
    parts = []
    for part in note.split(", "):
        kind = "ok" if part.endswith("✓") else "bad"
        parts.append(f'<span class="chip {kind}">{esc(part)}</span>')
    return '<div class="chips">' + "".join(parts) + "</div>"


def card(title, how, serbian, row, extra="", ours=False):
    return (f'<div class="card{" ours" if ours else ""}">'
            f'<div class="card-head"><h3>{esc(title)}</h3><p class="how">{esc(how)}</p></div>'
            f'<div class="serbian">{esc(serbian)}</div>'
            f'{chips(serbian, row)}{extra}</div>')


def picker_badge(result):
    options, row, picked, note = result["options"], result["row"], result["picked"], result["note"]
    total = len(options)
    if not NB["tested"](row):
        return ('<div class="badge neutral">Nothing to check: no option shows a speaker, listener or '
                "formality, so this is NLLB's top answer.</div>")
    if note == "matched":
        rank = options.index(picked) + 1
        if rank == 1:
            return f"<div class=\"badge matched\">✓ NLLB's top answer already fits (option 1 of {total}).</div>"
        return (f'<div class="badge matched">✓ Picked option {rank} of {total}: '
                "the first one whose endings fit.</div>")
    if note == "repaired":
        source = next(option for option in options if NB["repair"](option, row) == picked)
        return (f'<div class="badge repaired"><b>⚠ Repaired.</b> None of the {total} options fit, so our '
                f"rules changed the endings of <i>{esc(source)}</i>. Please check it.</div>")
    return (f'<div class="badge guess"><b>⚠ Had to guess.</b> None of the {total} options fit and repair '
            "couldn't fix them, so this is NLLB's top answer. Its endings may be wrong.</div>")


def cards_html(result, mandarin, seconds):
    row = result["row"]
    checked = [PROPERTY_NAMES.get(p, p) for p in NB["tested"](row)]
    if checked:
        checked_line = "Checked: " + ", ".join(checked) + "."
    else:
        checked_line = "Nothing to check: none of NLLB's 32 options shows a speaker, listener or formality."
    in_test_set = mandarin in set(NB["df"]["mandarin"])
    test_note = ('<p class="test-note">Note: this sentence is in our test set, so it isn\'t a new '
                 "sentence.</p>" if in_test_set else "")
    english = f'<p class="middle">English in the middle: <i>{esc(result["english"])}</i></p>'
    return (f'<p class="checked-line">{esc(checked_line)}</p>{test_note}'
            '<div class="cards">'
            + card("Through English", "Baseline: Mandarin → English → Serbian", result["baseline"], row, english)
            + card("NLLB direct", "One model, Mandarin → Serbian, its top answer", result["options"][0], row)
            + card("Ours", f"NLLB's {len(result['options'])} options + our picker", result["picked"], row,
                   picker_badge(result), ours=True)
            + "</div>"
            '<p class="footnote">The picker checks word endings, not meaning: a wrong word can still get '
            f"through. Translated in {seconds:.1f} s on {esc(NB['DEVICE'].upper())}.</p>")


def options_html(result):
    """All of NLLB's options, best first, with the one the picker used marked."""
    options, row, picked, note = result["options"], result["row"], result["picked"], result["note"]
    checking = bool(NB["tested"](row))
    if note == "matched":
        used, label = options.index(picked), "← picked"
    elif note == "repaired":
        used = next(i for i, option in enumerate(options) if NB["repair"](option, row) == picked)
        label = "← repaired from this"
    else:
        used, label = 0, "← used (had to guess)"
    lines = []
    for i, option in enumerate(options):
        fits = ('<span class="yes">✓</span>' if NB["fits"](option, row) else '<span class="no">✗</span>'
                if checking else "–")
        mark = f'<span class="used">{label}</span>' if i == used else ""
        lines.append(f'<tr class="{"used-row" if i == used else ""}"><td>{i + 1}</td>'
                     f"<td>{esc(option)} {mark}</td><td class=\"fit\">{fits}</td></tr>")
    repaired_line = (f'<p class="repaired-line">After repair: <b>{esc(picked)}</b></p>'
                     if note == "repaired" else "")
    return (f"{repaired_line}<table class=\"options\"><thead><tr><th>#</th><th>NLLB's option "
            "(best first)</th><th>Endings fit?</th></tr></thead><tbody>" + "".join(lines) + "</tbody></table>")


def run(mandarin, speaker, listener, formal_choice):
    mandarin = (mandarin or "").strip()
    if not mandarin:
        return '<p class="checked-line">Type a Mandarin sentence first.</p>', "", ""
    start = time.time()
    result = translate_and_record(mandarin, speaker, listener, formal_choice == "yes")
    seconds = time.time() - start
    return (cards_html(result, mandarin, seconds), options_html(result),
            f'<pre class="printout">{esc(result["printout"])}</pre>')


def wait_for_models():
    """Runs when the page opens: wait for the models, then switch the buttons on."""
    READY.wait()
    if LOAD_ERRORS:
        message = f"**Loading failed:** {LOAD_ERRORS[0]}. See the terminal for details."
        return [message] + [gr.update(interactive=False)] * (1 + len(EXAMPLES))
    message = f"Models ready (running on {NB['DEVICE'].upper()}). Type a sentence or pick an example."
    return [message] + [gr.update(interactive=True)] * (1 + len(EXAMPLES))


# ---------------------------------------------------------------------------
# 5. The page
# ---------------------------------------------------------------------------

CSS = """
.gradio-container { max-width: 1480px !important; margin: 0 auto !important; }
#title h1 { font-size: 2.6rem; margin: 8px 0 0; letter-spacing: -0.01em; }
#subtitle p { font-size: 1.2rem; color: #4b5563; margin-top: 4px; }
#mandarin textarea { font-size: 1.9rem !important; line-height: 1.4 !important; }
#translate-btn { font-size: 1.25rem; min-height: 56px; }
.example-btn { font-size: 1.05rem !important; }
#status p { font-size: 1.05rem; color: #374151; }
.checked-line { font-size: 1.15rem; margin: 6px 0 14px; color: #1f2937; }
.test-note { color: #92400e; font-size: 1.05rem; }
.cards { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; }
.card { background: #ffffff; border: 1px solid #d6d9e0; border-radius: 14px; padding: 20px 22px;
        display: flex; flex-direction: column; gap: 14px; }
.card.ours { border: 2px solid #4338ca; box-shadow: 0 6px 20px rgba(67, 56, 202, 0.12); }
.card h3 { margin: 0; font-size: 1.35rem; color: #111827; }
.card.ours h3 { color: #3730a3; }
.card .how { margin: 2px 0 0; font-size: 0.98rem; color: #6b7280; }
.card .serbian { font-size: 1.8rem; font-weight: 600; line-height: 1.3; color: #111827; }
.card .middle { margin: 0; font-size: 1rem; color: #4b5563; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; }
.chip { padding: 5px 12px; border-radius: 999px; font-size: 1.02rem; font-weight: 600; }
.chip.ok { background: #dcf3e3; color: #14532d; }
.chip.bad { background: #fde2e2; color: #991b1b; }
.chip.none { background: #eef0f3; color: #4b5563; }
.badge { border-radius: 10px; padding: 10px 14px; font-size: 1.05rem; line-height: 1.4; }
.badge.matched { background: #e7f6ec; color: #14532d; border: 1px solid #a7d9b6; }
.badge.repaired { background: #fff4d6; color: #7a4b00; border: 1px solid #f0c75e; }
.badge.guess { background: #fde2e2; color: #991b1b; border: 1px solid #f3a5a5; }
.badge.neutral { background: #eef0f3; color: #374151; border: 1px solid #d6d9e0; }
.footnote { color: #6b7280; font-size: 1rem; margin-top: 14px; }
table.options { width: 100%; border-collapse: collapse; font-size: 1.05rem; }
table.options th, table.options td { text-align: left; padding: 6px 10px; border-bottom: 1px solid #e5e7eb; }
table.options td.fit { text-align: center; }
table.options .yes { color: #15803d; font-weight: 700; }
table.options .no { color: #b91c1c; }
table.options tr.used-row td { background: #eef2ff; font-weight: 600; }
.used { color: #3730a3; font-weight: 700; margin-left: 8px; }
.repaired-line { font-size: 1.1rem; }
.printout { font-size: 0.95rem; white-space: pre-wrap; background: #f6f7f9; padding: 12px; border-radius: 8px; }
footer { display: none !important; }   /* hide Gradio's page footer, for a cleaner video */
@media (max-width: 900px) { .cards { grid-template-columns: 1fr; } }
"""

# Always use the light colours, so every recording looks the same.
FORCE_LIGHT = """
() => {
  const url = new URL(window.location);
  if (url.searchParams.get('__theme') !== 'light') {
    url.searchParams.set('__theme', 'light');
    window.location.href = url.href;
  }
}
"""

LOADING_MESSAGE = ("⏳ **Loading the three models...** The first time, this downloads about 3 GB "
                   "and can take several minutes. After that it takes about half a minute.")

with gr.Blocks(title="Lost in Translation", css=CSS, js=FORCE_LIGHT,
               theme=gr.themes.Soft(primary_hue="indigo", text_size=gr.themes.sizes.text_lg)) as demo:
    gr.Markdown("# Lost in Translation", elem_id="title")
    gr.Markdown("Mandarin → Serbian that keeps who's talking: the speaker's gender, the listener's "
                "gender and formality. **A prototype**, built for a 48-hour contest.", elem_id="subtitle")

    with gr.Row(equal_height=False):
        with gr.Column(scale=3):
            mandarin_box = gr.Textbox(label="Mandarin sentence", lines=2, elem_id="mandarin",
                                      placeholder="Type or paste a Mandarin sentence")
            gr.Markdown("**Examples** (from section 8 of our notebook, not in our test set):")
            example_buttons = []
            for example in EXAMPLES:
                formality = "formal" if example["formal"] == "yes" else "casual"
                label = f'{example["mandarin"]}  ({example["speaker"]} → {example["listener"]}, {formality})'
                example_buttons.append(gr.Button(label, size="sm", interactive=False,
                                                 elem_classes="example-btn"))
        with gr.Column(scale=2):
            speaker_radio = gr.Radio(["man", "woman"], value="woman", label="Who is speaking?")
            listener_radio = gr.Radio(["man", "woman"], value="man", label="Who are they talking to?")
            formal_radio = gr.Radio([("Formal (您 / Vi)", "yes"), ("Casual (你 / ti)", "no")], value="no",
                                    label="Formal or casual?")
            translate_button = gr.Button("Translate", variant="primary", interactive=False,
                                         elem_id="translate-btn")

    status = gr.Markdown(LOADING_MESSAGE, elem_id="status")
    cards_box = gr.HTML('<p class="checked-line">The three translations appear here.</p>')
    with gr.Accordion("See all 32 options NLLB gave, and which one our picker used", open=False):
        options_box = gr.HTML()
    with gr.Accordion("What the notebook's translate_one() printed", open=False):
        printout_box = gr.HTML()

    inputs = [mandarin_box, speaker_radio, listener_radio, formal_radio]
    outputs = [cards_box, options_box, printout_box]
    translate_button.click(run, inputs, outputs)
    mandarin_box.submit(run, inputs, outputs)

    def fill_example(number):
        example = EXAMPLES[number]
        return example["mandarin"], example["speaker"], example["listener"], example["formal"]

    for number, button in enumerate(example_buttons):
        button.click(lambda number=number: fill_example(number), None, inputs).then(run, inputs, outputs)

    # show_progress="minimal": a small timer only, so the loading message isn't greyed out.
    demo.load(wait_for_models, None, [status, translate_button] + example_buttons, show_progress="minimal")


if __name__ == "__main__":
    print("Loading the notebook's code and the three models (the page opens meanwhile)...")
    threading.Thread(target=load_notebook_code, daemon=True).start()
    # On a laptop: no public link; the page is only at http://127.0.0.1:7860.
    # In Colab: the page runs on Google's computer, so your browser can't reach it directly.
    # share=True makes Gradio print a temporary public link (ending in .gradio.live, works for
    # about 72 hours) that you open in a new tab. Anyone with that link can use the page.
    in_colab = "google.colab" in sys.modules
    demo.queue().launch(share=in_colab, show_api=False)
