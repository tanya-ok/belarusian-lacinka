# Belarusian Lacinka

Private, independent mini-book about Belarusian Latin script (łacinka), with English explanations, paired Belarusian examples, historical context, poetry extracts and original exercises. Six dedicated watercolor pages follow storks from arrival and flight to nest-building and family life. Text pages have no stork vignettes.

## Format

- MD PRODUCT B6 Slim, blank: **105 × 175 mm**, not A6 or standard B6.
- Reader: 34 pages, including the illustrated cover and six standalone illustration pages.
- Print: 17 landscape A4 sheets, two exact-size pages per sheet, crop marks; **100%, single-sided**. Cut and stack by page numbers. This is not a folded booklet imposition.
- For inserts smaller than notebook pages, print at 95%.

## Files

- `content/book.json`: editable page content.
- `research/sources.md`: linked research and claim notes.
- `assets/cover.png`: generated watercolor stork cover with Ŭ.
- `assets/cover-prompt.md`: generation provenance and prompt.
- `scripts/build.py`: portable ReportLab/pypdf build using bundled OFL fonts.
- `output/pdf/`: print and reading editions.

Install `requirements.txt`, then run `python3 scripts/build.py`. Bundled Noto Sans and Noto Serif are licensed under SIL OFL 1.1; see `assets/fonts/OFL.txt`. Run `python3 scripts/verify_release.py` to reject stale outputs before publication. The build also generates the public bibliography and a SHA-256 release manifest.

## Editorial scope

Traditional ł/l spelling; v, č, š, ž and ŭ. Script and orthography are distinguished explicitly. Historical publication is not automatically evidence of an author's handwritten original. No claim that one person invented łacinka. Exercises are original, not quotations. Kupała's poetry is accompanied by new Latin-script transcriptions and original English meaning glosses, not claims of historical Latin editions. Kołas is recommended but not quoted. Edition 0.5, researched 25 September 2026.

Private repository; publication is not enabled. `publishing/` contains an English download-page template and an inactive manual GitHub Pages workflow for later owner-approved publication. No public licence is assigned to this edition. External sources retain their own rights.

Edition 0.5 opens with the complete “Viecier, i sokał, i ja…” on the first interior page, in a modern łacinka transcription. The colophon and website template state that the information is provided solely for educational and research purposes. See `research/audit-resolution.md` for corrections and remaining review limits. Illustration resolution is about 137 ppi at the current print size; a physical proof is still recommended.
