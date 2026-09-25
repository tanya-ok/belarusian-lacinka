# Publication preparation - not enabled

The repository remains private. Nothing here enables Pages or publishes content.

`index.html` is the English download-page template, with the educational and research disclaimer. `pages.yml.example` is an inactive, manual-only GitHub Actions template. The public artifact is allowlisted: index, generated sources page, rights notice, font licence, cover and two approved PDFs. No other repository files are packaged. SHA-256 verification rejects changed inputs or stale outputs. Actions are pinned to verified commit hashes; dependencies are pinned and fonts bundled. This checks consistency, not legal clearance or originality.

When the owner approves publication:

1. Review all book pages, the Latin transcription, attribution and permissions for public distribution.
2. Confirm the GitHub plan supports Pages from a private repository. GitHub Free does not support a private repository as a Pages source; Pro or another eligible plan is needed. Do not change repository visibility automatically. A private source repository does not imply the Pages website is private.
3. Move the workflow template to `.github/workflows/pages.yml`, enable Pages using GitHub Actions in repository settings, then run the workflow manually.
4. Verify the published site, both PDF links, mobile layout, disclaimer and print dimensions. The expected project URL is `https://tanya-ok.github.io/belarusian-lacinka/`; it is not a live-site claim.

Reference: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages (checked 25 September 2026).
