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
- Member permissions.
- Internal review states.

Keep contracts, budgets, raw datasets, unpublished technical details, sensitive student records, and partner confidential files outside this public repository.

## Next Backend Milestones

1. Connect Supabase and verify GitHub/email login.
2. Add owner-only role editing controls in `/console/`.
3. Add export buttons that generate reviewed Markdown snippets for `/admin/`.
4. Add storage buckets for approved public images and private attachments.
5. Add audit logs for important admin actions.
