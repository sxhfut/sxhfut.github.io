---
layout: page
title: MAC-Lab Backend Setup
title_zh: MAC-Lab 后台部署说明
description: Supabase and GitHub setup notes for MAC-Lab public CMS and private lab console.
description_zh: MAC-Lab 公开内容 CMS 与内部管理控制台的 Supabase / GitHub 配置说明。
permalink: /docs/admin/backend-setup/
toggle: false
---

# MAC-Lab Backend Setup

This website has two admin layers:

- `/admin/`: public website CMS for pages that are safe to publish.
- `/console/`: private lab console for members, student pages, news materials, outputs, and review workflow.

## Recommended Stack

- Public website: GitHub Pages + Jekyll.
- Public content editing: Decap CMS + GitHub OAuth.
- Internal management: Supabase Auth + Postgres + Row Level Security.

This keeps the public site fast and crawlable while placing private records in a real database.

## Supabase Setup

1. Create a Supabase project.
2. In Supabase SQL Editor, run `docs/admin/supabase-schema.sql`.
3. Enable Auth providers:
   - GitHub OAuth for Professor Sun and technical admins.
   - Email magic link for students if needed.
4. Add the site URL in Supabase Auth URL settings:
   - Site URL: `https://sxhfut.github.io`
   - Redirect URL: `https://sxhfut.github.io/console/`
5. Sign in once at `https://sxhfut.github.io/console/`.
6. In Supabase SQL Editor, activate the owner account:

```sql
update public.profiles
set role = 'owner', status = 'active'
where email = 'YOUR_EMAIL@hfut.edu.cn';
```

## Console Configuration

Copy the example config:

```text
console/config.example.js -> console/config.js
```

Then fill in the public Supabase values:

```js
window.MACLAB_CONSOLE_CONFIG = {
  supabaseUrl: "https://YOUR-PROJECT.supabase.co",
  supabaseAnonKey: "YOUR_PUBLIC_ANON_KEY"
};
```

The anon key is designed to be public. Never place the Supabase `service_role` key in this repository or in browser code.

## Roles

- `owner`: Professor Sun. Full review and permission control.
- `admin`: trusted student/admin maintainers. Can maintain records and review materials.
- `student`: lab member. Can maintain their own page and submit news/output materials.

New users are created as `student + pending`. The owner can activate them and promote selected users.

## What Goes Where

Use `/admin/` for:

- Homepage sections.
- Research directions.
- Solutions and capability cases.
- Public news and media pages.
- Recruitment pages.

Use `/console/` for:

- Student profile drafts.
- Lab news source materials.
- Project and output materials.
- Partner and scenario leads.
- Review tasks for public publishing.
- Manually selected frontier radar items.
- Access analytics snapshots from GoatCounter, Cloudflare, Plausible, Google Analytics, or manual monthly summaries.
- Lightweight JSON backups of console tables for owner/admin handoff.
- Audit logs for important content changes.
- Member permissions.
- Internal review states.

Keep contracts, budgets, raw datasets, unpublished technical details, sensitive student records, and partner confidential files outside this public repository.

## Content Workflow

The internal console now uses `content_tasks` as the bridge from private records to public website updates:

1. A student or admin submits a student page, lab news item, project/output material, partner lead, or frontier curation.
2. The console creates a linked review task with source metadata, target page, priority, and publishing hint.
3. The owner/admin moves the task through submitted, review, approved, public-ready, or archived.
4. When a linked task changes status, the source record is updated where the table supports review status.
5. The review queue can generate a public Markdown/YAML draft for the GitHub/Decap CMS layer.

This keeps raw working material in Supabase while making the final public site explicit, versioned, and searchable.

## Lab Operations Workflow

The console is now organized as an operating workspace rather than only a set of forms:

- **Operations overview**: live counts, recent review focus, and audit activity.
- **Partner CRM**: partner requests move through new lead, requirement clarification, proposal-ready, public-case, and archived stages.
- **Output library**: papers, projects, competitions, platforms, and partner cases keep public evidence links, venue/level, year, and contributor notes.
- **Frontier review**: automatic radar items can be refined into lab-curated viewpoints before public release.
- **Analytics snapshots**: aggregate traffic data can be recorded periodically to observe which pages, topics, and entry sources are working.
- **Backup export**: owner/admin can download a JSON package of the tables they can access under RLS.

If the console shows that analytics or backup snapshot tables are missing, rerun the latest `docs/admin/supabase-schema.sql` in Supabase SQL Editor. The file is idempotent and can be rerun after upgrades.

## Website Analytics Setup

The public site has a lightweight analytics include at `_includes/analytics.html`.
It stays disabled until one of the following `_config.yml` fields is filled:

```yml
analytics:
  goatcounter_code: ""
  goatcounter_show_counter: false
  goatcounter_counter_path: "TOTAL"
  cloudflare_token: ""
  plausible_domain: ""
```

Recommended path:

1. Use GoatCounter for the fastest setup, or Cloudflare Web Analytics if a Cloudflare account is already being used.
2. If a public total counter is wanted, enable `goatcounter_show_counter` and turn on visitor counters in GoatCounter site settings.
3. Keep the public site analytics aggregate-only: page views, referrers, popular pages, browser/device category, and approximate geography.
4. Every month, copy the key dashboard numbers into `/console/` → Analytics as a `site_metric_snapshots` record.
5. Use the trend to improve homepage sections, research pages, industry solutions, frontiers, media pages, and recruitment text.

This separates public visibility analytics from internal user activity logs. Public analytics should not be used to identify individual visitors.

## Next Backend Milestones

1. Add Supabase Storage buckets for approved public images and private attachments.
2. Add scheduled export from GoatCounter, Cloudflare, or Plausible API into `site_metric_snapshots`.
3. Add GitHub issue or pull-request creation for public-ready content.
4. Add file attachments and owner-only notes for partner CRM records.
5. Add periodic database export to private storage for disaster recovery.

## Backend Features Already Modeled

The SQL schema now includes:

- `profiles`: member identity, role, and account status.
- `student_pages`: student-maintained profile drafts.
- `lab_news`: news source materials and review states.
- `lab_outputs`: papers, projects, competitions, platforms, and partner-facing evidence.
- `partner_requests`: collaboration leads and scenario requirements.
- `content_tasks`: public-publishing review queue.
- `frontier_curations`: manually selected frontier radar items and lab takeaways.
- `content_audit_logs`: append-only audit trail for content changes.
- `partner_touchpoints`: follow-up records for partner CRM interactions.
- `site_metric_snapshots`: aggregate website traffic snapshots.
- `content_backup_snapshots`: records of console export manifests.

The console is designed so public communication and internal operations stay separate: public pages are published through GitHub/Decap CMS, while private review state, partner leads, member permissions, and logs stay in Supabase with Row Level Security.
