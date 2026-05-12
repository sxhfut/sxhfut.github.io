# MAC-Lab | Multimedia Affective Computing and Psychological AI

English-first bilingual website for **MAC-Lab, the Multimedia Affective Computing Lab led by Professor Xiao Sun at Hefei University of Technology**.

Website: [https://sxhfut.github.io](https://sxhfut.github.io)

## About

MAC-Lab began from long-term work in natural language processing, human-computer interaction, and multimodal affective computing. The lab now extends this foundation toward two connected research frameworks:

- **Ubiquitous Psychological Computing**: sensing, profiling, assessing, and supporting mental states in real-world environments.
- **Embodied Emotional Intelligence**: emotional perception, understanding, expression, and interaction for robots, digital humans, smart cockpits, companion agents, and active-health systems.

The site presents MAC-Lab as a research platform that connects high-level publications, national research programs, technology transfer, student training, industry collaboration, public communication, and real-world AI systems for mind-body health.

## Site Sections

- `Research`: core directions, long-term research route, Ubiquitous Psychological Computing, and Embodied Emotional Intelligence.
- `Projects`: national and major projects, applied platforms, MindOS, MindMirror, MindCare, smart cockpit, and child-development support.
- `Impact`: representative publications, international challenges, patents, software, awards, standards, and real-world impact.
- `People`: student training, competition outcomes, team culture, and public student information.
- `News`: MAC-Lab newsroom for lab updates, public releases, and media coverage.
- `Frontiers`: automatically refreshed AI + psychology and affective-computing frontier radar.
- `Media`: curated public coverage of Professor Xiao Sun and MAC-Lab.
- `Join`: admissions and collaboration information for undergraduates, graduate students, academic PhD students, engineering doctoral students, and partners.

## Content Workflow

The current site is a static Jekyll website deployed through GitHub Pages. Public-facing content is edited in Markdown, HTML, and structured data files, then published through Git commits.

Search and AI discovery files:

- `_includes/structured-data.html`: JSON-LD identity graph for MAC-Lab, Professor Xiao Sun, the website, and each page.
- `robots.txt`: crawler access and sitemap discovery.
- `llms.txt`: concise Markdown summary for LLM-oriented retrieval and answer engines.
- `_data/staged_updates.yml`: homepage update stream for staged research, media, platform, and frontier-refresh signals.

Planned editing model:

- Public news and lab updates can be moved into structured data or Markdown collections for CMS-style editing.
- The `Frontiers` page is designed to combine curated lab/media/application items with automatically fetched open paper metadata.
- A future `/admin/` workflow can support easier content entry while keeping the public site fast and stable.

## Local Preview

```bash
BUNDLE_PATH=/tmp/sxhfut-github-pages-bundle bundle exec jekyll build
python3 -m http.server 4010 --bind 127.0.0.1 --directory _site
```

Then open:

```text
http://127.0.0.1:4010/
```

## Frontier Radar

Refresh the frontier dataset locally:

```bash
python3 scripts/update_frontiers.py
```

The generated data lives in:

```text
_data/frontiers.json
```

Curated manual items live in:

```text
_data/frontiers_manual.json
```

The intended scheduled workflow refreshes `_data/frontiers.json` from open arXiv metadata and curated application, media, and standards updates.

The production site refreshes the radar through GitHub Actions:

- Workflow: `.github/workflows/update-frontiers.yml`
- Schedule: every day at 06:25 Beijing time
- Manual run: GitHub repository → Actions → Update Frontier Radar → Run workflow
- Output: `_data/frontiers.json`
- Deployment path: the workflow commits changed data, then GitHub Pages rebuilds the static site

Current automatic queries focus on:

- AI + psychology and mental health
- affective computing and emotion understanding
- empathetic dialogue and counseling dialogue
- embodied emotional intelligence
- ubiquitous psychological computing and psychological assessment

## Repository Metadata

Repository description:

```text
MAC-Lab official bilingual website: multimedia affective computing, ubiquitous psychological computing, and embodied emotional intelligence.
```

Website:

```text
https://sxhfut.github.io
```

Topics:

```text
mac-lab
affective-computing
psychological-computing
embodied-ai
embodied-emotional-intelligence
multimodal-ai
natural-language-processing
human-computer-interaction
digital-health
github-pages
jekyll
```
