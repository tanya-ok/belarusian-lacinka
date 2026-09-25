# Audit corrections - edition 0.5

## Implemented

- B1: removed the Kołas quotation, transcription and translation. Page 30 remains a reading recommendation with original questions. No quotation-exception or worldwide public-domain claim is needed for a reproduced passage.
- B2: bundled unmodified Noto Sans and Noto Serif and their SIL OFL 1.1 licence. Removed all system-font dependencies. The external audit's proprietary-font concern was an unresolved licensing question, not evidence that embedding was unlawful. Microsoft's font FAQ distinguishes document embedding from redistributing font software: https://learn.microsoft.com/en-us/typography/fonts/font-faq . Its Windows-specific guidance does not settle the old macOS font licence.
- B3: used čytańnie in an explicitly labelled modern reading of Ciotka's title. The cited Wikisource transcription itself contains cytańnie, so the error was not independently invented by the book. The printed scan's exact typography remains unverified; the book no longer implies a diplomatic transcription.
- B4: numbered PDF references are actual HTTPS links. A generated public bibliography is in the publication allowlist, accessible from the homepage. No private-repository path is offered to readers.
- B5: edition 0.5 throughout current editorial content and website. Earlier entries in illustration-generation provenance are historical records, not the current edition label.
- B6: restored source em dashes in the opening poem and Maja malitva transcription. Blank-space stanza separation is explicitly documented as a layout choice.
- Replaced the obsolete Kaleta PDF URL with DOI 10.31338/2720-698Xaa.25.16; fixed the page-28 reference; removed unused scene fields.
- Added a rights notice without assigning a new licence to the user's work or claiming exclusive rights in AI images.
- Verified official action releases through GitHub API and pinned their commits. The workflow remains an inactive example, manual-only, with limited permissions.
- Added a release manifest and verification that fails on stale inputs/outputs. The workflow packages exactly seven named files; it does not publish the repository or rebuild unreviewed PDFs.

## Verified independently

- Source poem: https://knihi.com/Janka_Kupala/Viecier,_i_sokal,_i_ja.html . The original two em dashes are retained.
- Ciotka advertisement transcription: https://be.wikisource.org/wiki/Жалейка_(1908) . The source transcription contains c; the book labels its corrected modern reading.
- Noto licence: https://github.com/notofonts/noto-fonts/blob/main/LICENSE . The exact downloaded licence is included verbatim.
- GitHub Free does not support Pages from private repositories; the external audit's contrary sentence is incorrect. Official eligibility: https://docs.github.com/en/pages/getting-started-with-github-pages . No account-plan assumptions or visibility changes were made.

## Remaining limits

- This is not a legal opinion or certification of originality, worldwide rights clearance or perfect linguistic accuracy. A specialist review before public release remains sensible.
- Illustrations were not regenerated or upscaled. Six 512 px cells at 95 mm are approximately 137 ppi; the cover is approximately 235 ppi. A physical print proof is needed to judge softness. Do not label these 300 dpi artwork.
- No new open-content licence has been chosen by the owner. The notice makes this explicit and does not override third-party rights or statutory exceptions.
- Historical claims not implicated in the corrections were not exhaustively re-audited. No definitive conclusion about Belarusian transitional copyright provisions is needed for this conservative revision and none is asserted.
- GitHub Pages has not been enabled, deployed or tested live. A manifest proves consistency, not editorial approval; publication still requires the owner's separate approval.
