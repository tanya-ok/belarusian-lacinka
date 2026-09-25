# Belarusian Lacinka

Private, independent mini-book about Belarusian Latin script (łacinka), with Russian explanations, paired Belarusian examples, historical context and original exercises.

## Format

- MD PRODUCT B6 Slim, blank: **105 × 175 mm**, not A6 or standard B6.
- Reader: 24 pages, including the illustrated cover.
- Print: 12 landscape A4 sheets, two exact-size pages per sheet, crop marks; **100%, single-sided**. Cut and stack by page numbers. This is not a folded booklet imposition.
- For inserts smaller than notebook pages, print at 95%.

## Files

- `content/book.json`: editable page content.
- `research/sources.md`: linked research and claim notes.
- `assets/cover.png`: generated watercolor stork cover with Ŭ.
- `assets/cover-prompt.md`: generation provenance and prompt.
- `scripts/build.py`: reproducible ReportLab/pypdf build (macOS fonts).
- `output/pdf/`: print and reading editions.

Run `python3 scripts/build.py` with reportlab and pypdf installed. Uses Arial and Georgia from `/System/Library/Fonts/Supplemental`.

## Editorial scope

Traditional ł/l spelling; v, č, š, ž and ŭ. Script and orthography are distinguished explicitly. Historical publication is not automatically evidence of an author's handwritten original. No claim that one person invented łacinka. Exercises are original, not quotations. Edition 0.1, researched 25 September 2026.

Private repository; no GitHub Pages, deployment or public sharing configured. No public licence is assigned to this edition. External sources retain their own rights.
