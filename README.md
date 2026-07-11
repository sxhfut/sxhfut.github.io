# MAC-Lab | Multimedia Affective Computing and Psychological AI

English-first bilingual website for **MAC-Lab, the Multimedia Affective Computing Lab led by Professor Xiao Sun at Hefei University of Technology**.

Website: [https://sxhfut.github.io](https://sxhfut.github.io)

## About

MAC-Lab is Professor Xiao Sun's HFUT-based public research platform for multimedia affective computing, psychological computing, and embodied emotional intelligence. The public record connects Professor Sun's HFUT work since 2011 with the HFUT Affective Computing Institute, the Anhui affective-computing key-lab route, Ubiquitous Psychological Computing, and later embodied emotional-intelligence systems. The lab now presents two connected research frameworks:

- **Ubiquitous Psychological Computing**: sensing, profiling, assessing, and supporting mental states in real-world environments.
- **Embodied Emotional Intelligence**: emotional perception, understanding, expression, and interaction for robots, digital humans, smart cockpits, companion agents, and active-health systems.

The site presents MAC-Lab as a research platform that connects high-level publications, national research programs, technology transfer, student training, industry collaboration, public communication, and real-world AI systems for mind-body health.

## Source-Backed Identity

High-trust public sources used by the site:

- HFUT official faculty page for Professor Xiao Sun: [https://faculty.hfut.edu.cn/sunxiao/zh_CN/index.htm](https://faculty.hfut.edu.cn/sunxiao/zh_CN/index.htm)
- Anhui Artificial Intelligence Society affective-computing committee page: [https://aaai.net.cn/list/qgjszwh](https://aaai.net.cn/list/qgjszwh)
- External academic report on Professor Xiao Sun's multimodal affective computing in pervasive scenarios: [https://jdxy.cjlu.edu.cn/info/1052/20338.htm](https://jdxy.cjlu.edu.cn/info/1052/20338.htm)
- Earlier affective-computing paper connecting Xiao Sun, Fuji Ren, HFUT, and the Anhui affective-computing key-lab affiliation: [https://jeit.ac.cn/cn/article/doi/10.11999/JEIT160975](https://jeit.ac.cn/cn/article/doi/10.11999/JEIT160975)
- CCF YOCSEF Hefei report mentioning HFUT Affective Computing Institute research achievements: [https://www.ccf.org.cn/YOCSEF/Branches/Hefei/News/bgh/2016-09-23/607278.shtml](https://www.ccf.org.cn/YOCSEF/Branches/Hefei/News/bgh/2016-09-23/607278.shtml)
- HFUT affective-computing development record: [https://sxhfut.github.io/lineage/](https://sxhfut.github.io/lineage/)
- Concept pages for AI-search extraction: [Ubiquitous Psychological Computing](https://sxhfut.github.io/concepts/ubiquitous-psychological-computing/), [Embodied Emotional Intelligence](https://sxhfut.github.io/concepts/embodied-emotional-intelligence/), and [HFUT Affective Computing Institute](https://sxhfut.github.io/concepts/hfut-affective-computing-institute/)

## Site Sections

- `Research`: core directions, long-term research route, Ubiquitous Psychological Computing, and Embodied Emotional Intelligence.
- `Development record`: public-source HFUT affective-computing route and citable concept entry points.
- `Projects`: national and major projects, applied platforms, MindOS, Mindmirror, MindScore, MindCare, smart cockpit, and child-development support.
- `Solutions`: scenario-oriented solution routes for affective computing, human factors, psychological computing, cognitive computing, and deployable software-hardware platforms.
- `Cases`: public-safe capability cases around Mindmirror, MindScore, MindOS, MindTalk, MindPet, MemOS-Mind, and related platform lines.
- `Impact`: representative publications, international challenges, patents, software, awards, standards, and real-world impact.
- `People`: student training, competition outcomes, team culture, and public student information.
- `News`: MAC-Lab newsroom for lab updates, public releases, media coverage, and HFUT faculty-blog synchronization.
- `Frontiers`: automatically refreshed AI + psychology and affective-computing frontier radar.
- `Media`: curated public coverage of Professor Xiao Sun and MAC-Lab.
- `Join`: admissions and collaboration information for undergraduates, graduate students, academic PhD students, engineering doctoral students, and partners.
- `Manage`: explanation of the public CMS and private console architecture.
- `Console`: private lab-management scaffold for members, student pages, news materials, and output review.

## Content Workflow

The current site is a static Jekyll website deployed through GitHub Pages. Public-facing content is edited in Markdown, HTML, and structured data files, then published through Git commits.

Search and AI discovery files:

- `_includes/structured-data.html`: JSON-LD identity graph for MAC-Lab, Professor Xiao Sun, the website, and each page.
- FAQ Schema is emitted automatically when a page defines `faq` in front matter.
- `robots.txt`: crawler access and sitemap discovery.
- `llms.txt`: concise Markdown summary for LLM-oriented retrieval and answer engines.
- `_data/staged_updates.yml`: homepage update stream for staged research, media, platform, and frontier-refresh signals.
- `_data/lab_sources.json`: scheduled public-source synchronization data from the HFUT faculty blog, ORCID, and DBLP when available.
- `images/hero/mac-lab-real-workshop-xiao-sun.jpg`: realistic lab-scene hero image for public sharing and structured previews.

Editing model:

- Public page updates can be edited through Markdown/HTML files or the `/admin/` Decap CMS scaffold after GitHub OAuth is configured.
- Public news, cases, and frontier suggestions can be collected through GitHub Issue Forms and reviewed before publication.
- The `Frontiers` page is designed to combine curated lab/media/application items with automatically fetched open paper metadata.
- The `Update Lab Source Signals` GitHub Action refreshes `_data/lab_sources.json` twice daily from public sources and feeds the Newsroom/RSS surfaces.
- The 2026-05-29 HFUT faculty-blog updates have been synchronized into the News and Frontiers data, including the MAC-Lab website release, two IEEE Transactions on Affective Computing papers, and one IEEE Transactions on Artificial Intelligence paper.
- The 2026-06-22 newsroom refresh adds ORCID/DOI/DBLP publication signals for recent works in IEEE/ACM TASLP, IEEE Transactions on Artificial Intelligence, IEEE Transactions on Fuzzy Systems, IEEE Transactions on Affective Computing, IEEE Transactions on Computational Social Systems, EMNLP, ICASSP, and IPMLP.
- Sensitive internal information, unpublished technical details, raw data, partner contracts, student records, and private management work should not be stored in this public GitHub Pages repository.

## Content Admin

The repository includes two admin layers:

1. Public website CMS for outward-facing content.
2. Internal lab console for members and operational materials.

### Public CMS

The lightweight static-CMS scaffold lives in:

```text
admin/index.html
admin/config.yml
```

The public admin entry is:

```text
https://sxhfut.github.io/admin/
```

Important notes:

- The admin UI is public, but editing requires GitHub authentication and repository permission once OAuth is configured.
- Decap CMS with the GitHub backend needs a GitHub OAuth provider or compatible auth proxy before live editing works on GitHub Pages.
- Local CMS testing can be enabled temporarily with Decap's local backend server, but the committed config is oriented toward GitHub-authenticated editing.
- The CMS is limited to public-facing pages. Private lab-management records should remain in the internal console and Supabase layer.

GitHub Issue Forms are also available for structured content intake:

- Lab news updates
- Capability case updates
- Frontier radar item suggestions

This keeps submissions reviewable, versioned, and public-safe before they become website content.

### Internal Console

The internal management scaffold lives in:

```text
console/index.html
console/app.js
console/styles.css
docs/admin/supabase-schema.sql
docs/admin/backend-setup.md
```

The console entry is:

```text
https://sxhfut.github.io/console/
```

Recommended backend:

- Supabase Auth for GitHub/email login.
- Supabase Postgres for member records, student pages, news materials, output materials, review tasks, analytics snapshots, and backup manifests.
- Partner CRM for scenario requirements, contact context, priority, next step, and follow-up status.
- Browser-side JSON export for owner/admin handoff backups under Row Level Security.
- Row Level Security for owner/admin/student permissions.

Recommended roles:

- `owner`: Professor Sun, final authority for permissions and publishing.
- `admin`: a small number of trusted student maintainers.
- `student`: ordinary lab members who can maintain their own page and submit materials.

To activate the console, create a Supabase project, run `docs/admin/supabase-schema.sql`, then configure:

```text
console/config.js
```

with the public Supabase URL and anon key. The anon key is browser-safe when RLS is enabled. Never commit a Supabase service-role key.

If the console shows missing analytics or backup tables, rerun the latest `docs/admin/supabase-schema.sql` in the Supabase SQL Editor. The schema is written to be rerunnable after console upgrades.

## Website Analytics

The site includes an optional analytics module for aggregate visitor statistics. It is disabled by default and only loads third-party analytics scripts after an ID or token is configured in `_config.yml`.

Recommended options:

- **GoatCounter**: the simplest privacy-friendly option for a GitHub Pages academic site. It gives page views, referrers, browser/device information, country-level trends, and a small public or private dashboard without cookies.
- **Cloudflare Web Analytics**: privacy-friendly aggregate analytics for page views, referrers, browsers, performance, and approximate country or regional traffic trends.
- **Plausible**: a polished paid/open-source analytics option if a more product-like dashboard is preferred.

Supported configuration keys:

```yml
analytics:
  cloudflare_token: ""
  goatcounter_code: ""
  goatcounter_domain: ""
  goatcounter_show_counter: false
  goatcounter_counter_path: "TOTAL"
  goatcounter_display_offset: 0
  google_measurement_id: ""
  plausible_domain: ""
  plausible_script_url: "https://plausible.io/js/script.js"
```

Fastest path with GoatCounter:

1. Create a GoatCounter site for `sxhfut.github.io`.
2. Copy the site code, for example `maclab` from `https://maclab.goatcounter.com`.
3. Put that code into `_config.yml` under `analytics.goatcounter_code`.
4. To show a small public footer counter, set `analytics.goatcounter_show_counter` to `true` and enable "Allow adding visitor counts on your website" in GoatCounter site settings.
5. If the site had meaningful traffic before analytics was added, set `analytics.goatcounter_display_offset` as the historical baseline added to the visible public count.
6. Commit and push. GitHub Pages will rebuild and start collecting aggregate trend data.

Cloudflare Web Analytics is also suitable:

1. Create a Web Analytics site in the Cloudflare dashboard for `sxhfut.github.io`.
2. Copy the site token from Cloudflare's JavaScript snippet.
3. Paste only the token into `_config.yml` under `analytics.cloudflare_token`.
4. Commit and push. GitHub Pages will rebuild the site and begin collecting aggregate traffic data.

The internal `/console/` analytics page can store monthly snapshots copied from GoatCounter, Cloudflare, Plausible, or Google Analytics. This keeps long-term page-trend history in Supabase even if the external analytics dashboard only keeps a limited window.

The public site should use analytics for content improvement, international visibility, collaboration reach, and admissions interest. It should not be used to identify individual visitors. If a future internal lab system needs login-based audit records, that should be implemented separately from the public website analytics layer.

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

Fast-sync only curated manual items without crawling remote sources:

```bash
python3 scripts/sync_frontiers_manual.py
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
- Fast manual-sync workflow: `.github/workflows/sync-frontiers-manual.yml`
- Schedule: every day at 08:25 and 20:25 Beijing time
- Manual full run: GitHub repository → Actions → Update Frontier Radar → Run workflow
- Manual curated-only run: GitHub repository → Actions → Sync Curated Frontier Items → Run workflow
- Output: `_data/frontiers.json`
- Deployment path: the workflow commits changed data, then GitHub Pages rebuilds the static site
- Last30Days enrichment: the workflow clones `mvanhorn/last30days-skill` and uses it as an optional recent-signal source for Reddit, Hacker News, Polymarket, and GitHub activity from the latest 30-day window
- MAC-Lab Lens: each item is enriched with relevance score, capability tags, and a short lab-perspective note
- Resilience: if one arXiv query fails or is rate-limited, the script reuses existing items for that track instead of dropping the direction
- Resilience: if Last30Days is unavailable or one topic fails, the radar skips that enrichment and still publishes arXiv plus curated items

Current automatic queries focus on:

- AI + psychology and mental health
- AI for mind-body health and digital mental-health systems
- affective computing and emotion understanding
- multimodal affective computing, speech, voice, and sensing
- empathetic dialogue and counseling dialogue
- embodied emotional intelligence
- ubiquitous psychological computing and psychological assessment

Optional Last30Days controls:

```bash
LAST30DAYS_SKILL_ROOT=/path/to/last30days-skill/skills/last30days
LAST30DAYS_MAX_TOPICS=4
LAST30DAYS_ITEMS_PER_TOPIC=2
LAST30DAYS_SOURCES=reddit,hn,polymarket,github
LAST30DAYS_TOPICS="Affective Computing::affective computing emotion AI;Embodied Emotional Intelligence::embodied emotional intelligence robot emotion"
LAST30DAYS_DISABLE=1
```

The Last30Days layer is meant to surface fresh public discourse, open-source activity, and industry-adjacent signals. It complements the arXiv paper stream rather than replacing it.

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
