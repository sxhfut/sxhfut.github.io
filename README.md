# MAC-Lab | Xiao Sun Academic Homepage

This repository hosts the English-first bilingual academic homepage for Professor Xiao Sun and MAC-Lab at Hefei University of Technology.

Built with Jekyll and GitHub Pages.

## Local Preview

```bash
BUNDLE_PATH=/tmp/sxhfut-github-pages-bundle bundle exec jekyll build
python3 -m http.server 4010 --bind 127.0.0.1 --directory _site
```

## Frontier Radar

```bash
python3 scripts/update_frontiers.py
```

The scheduled GitHub Actions workflow in `.github/workflows/update-frontiers.yml` refreshes `_data/frontiers.json` from arXiv metadata and curated manual signals.
