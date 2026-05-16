---
layout: page
title: Manage
title_zh: 后台管理
description: A practical content-management plan for MAC-Lab's GitHub Pages website, combining GitHub login, static CMS editing, issue forms, and scheduled automation.
description_zh: MAC-Lab GitHub Pages 网站的后台管理方案：结合 GitHub 登录、静态 CMS、Issue 表单与定时自动化。
permalink: /manage/
toggle: false
rank: 9.5
---

<div class="summary-band">
  <div><strong>GitHub</strong><span><span class="lang-en">versioned content and permissions</span><span class="lang-zh">版本化内容与权限</span></span></div>
  <div><strong>CMS</strong><span><span class="lang-en">browser editing for public pages</span><span class="lang-zh">浏览器编辑公开页面</span></span></div>
  <div><strong>Actions</strong><span><span class="lang-en">scheduled radar and data refresh</span><span class="lang-zh">定时采集与数据刷新</span></span></div>
  <div><strong>Forms</strong><span><span class="lang-en">structured submissions from lab members</span><span class="lang-zh">成员结构化提交</span></span></div>
</div>

<div class="research-lead">
  <h2><span class="lang-en">What GitHub Pages can and cannot do</span><span class="lang-zh">GitHub Pages 能做什么，不能做什么</span></h2>
  <p><span class="lang-en">GitHub Pages is excellent for a public academic website: fast static pages, strong version history, stable URLs, search-engine crawlability, scheduled GitHub Actions, and safe public documentation. It does not provide a private database or server-side user system by itself. For login-based editing, the best lightweight path is to use GitHub authentication and commit-based content management.</span><span class="lang-zh">GitHub Pages 非常适合公开学术网站：静态页面快、版本历史清楚、URL 稳定、搜索引擎容易抓取，并且可以配合 GitHub Actions 定时更新。它本身不提供私有数据库或服务器端用户系统。若要登录编辑，最稳妥的轻量路线是使用 GitHub 身份认证和基于提交的内容管理。</span></p>
</div>

<div class="media-note">
  <h2><span class="lang-en">Current Admin Status</span><span class="lang-zh">当前后台状态</span></h2>
  <p><span class="lang-en">Two admin layers are now prepared. `/admin/` is the public-content CMS for website pages. `/console/` is the internal lab console scaffold for members, student pages, news materials, outputs, and review workflow. Live login for `/console/` requires a Supabase project URL and anon key, plus the database schema in `docs/admin/supabase-schema.sql`.</span><span class="lang-zh">现在已经预留两层后台。`/admin/` 用于官网公开内容编辑；`/console/` 用于实验室内部管理，包括成员、学生个人页、新闻素材、成果材料和审核流程。`/console/` 正式登录需要配置 Supabase 项目的 URL 和 anon key，并部署 `docs/admin/supabase-schema.sql` 中的数据库权限模型。</span></p>
</div>

<div class="framework-grid framework-grid--page">
  <article class="framework-card framework-card--dark">
    <span class="framework-kicker">Internal Console</span>
    <h2><span class="lang-en">Private lab management is staged at `/console/`.</span><span class="lang-zh">内部管理控制台已放在 `/console/`。</span></h2>
    <p><span class="lang-en">Recommended roles are simple: Professor Sun as owner, a small group of trusted students as admins, and ordinary students as members who can maintain their own pages and submit materials.</span><span class="lang-zh">推荐权限保持清晰：孙晓教授为 owner，少数可信学生为 admin，普通学生为 student，可维护自己的页面并提交新闻、成果和项目材料。</span></p>
    <a class="text-link" href="/console/"><span class="lang-en">Open Console</span><span class="lang-zh">打开内部控制台</span></a>
  </article>
  <article class="framework-card">
    <span class="framework-kicker">Setup</span>
    <h2><span class="lang-en">Supabase provides login, database, and role control.</span><span class="lang-zh">Supabase 负责登录、数据库与权限。</span></h2>
    <p><span class="lang-en">GitHub Pages remains the public website host. Internal data should live in Supabase with Row Level Security, not in this public repository.</span><span class="lang-zh">GitHub Pages 继续承担公开官网托管；内部数据放入带行级权限的 Supabase，不进入公开仓库。</span></p>
    <a class="text-link" href="/docs/admin/backend-setup/"><span class="lang-en">Read Setup Notes</span><span class="lang-zh">查看部署说明</span></a>
  </article>
</div>

<h2><span class="lang-en">Recommended Admin Architecture</span><span class="lang-zh">推荐后台架构</span></h2>

<div class="card-grid card-grid--four">
  <article class="feature-card">
    <span><span class="lang-en">1. Public CMS</span><span class="lang-zh">1. 公开内容 CMS</span></span>
    <h3><span class="lang-en">Use `/admin/` for page and data editing</span><span class="lang-zh">用 `/admin/` 编辑页面与数据</span></h3>
    <p><span class="lang-en">The repository includes a Decap CMS scaffold. After GitHub OAuth is configured, authorized users can edit selected pages and data files in the browser and publish changes through commits.</span><span class="lang-zh">仓库已预留 Decap CMS 后台。配置 GitHub OAuth 后，授权用户可以在浏览器中编辑指定页面和数据文件，并通过提交发布。</span></p>
  </article>
  <article class="feature-card">
    <span><span class="lang-en">2. Issue Forms</span><span class="lang-zh">2. 表单收集</span></span>
    <h3><span class="lang-en">Use GitHub Issue Forms for structured updates</span><span class="lang-zh">用 GitHub 表单收集结构化更新</span></h3>
    <p><span class="lang-en">Students and lab members can submit news, publications, cases, and frontier items through controlled forms, then a maintainer reviews and converts them into public content.</span><span class="lang-zh">学生和实验室成员可以通过受控表单提交新闻、论文、案例和前沿条目，再由维护者审核后转成公开内容。</span></p>
  </article>
  <article class="feature-card">
    <span><span class="lang-en">3. Automation</span><span class="lang-zh">3. 自动化</span></span>
    <h3><span class="lang-en">Use GitHub Actions for scheduled refreshes</span><span class="lang-zh">用 GitHub Actions 定时刷新</span></h3>
    <p><span class="lang-en">The frontier radar already uses a scheduled workflow. The same pattern can support monthly summaries, publication refreshes, sitemap updates, and content-health checks.</span><span class="lang-zh">前沿雷达已经使用定时工作流。相同模式可扩展到月度观察、论文刷新、站点地图更新和内容健康检查。</span></p>
  </article>
  <article class="feature-card">
    <span><span class="lang-en">4. Private Work</span><span class="lang-zh">4. 私有工作</span></span>
    <h3><span class="lang-en">Keep sensitive management outside the public site</span><span class="lang-zh">敏感管理不要放在公开站点</span></h3>
    <p><span class="lang-en">Internal student records, partner contracts, raw data, and unpublished technical details should stay in private systems, not in a public GitHub Pages repository.</span><span class="lang-zh">学生内部记录、合作合同、原始数据和未公开技术细节，应放在私有系统中，不应进入公开 GitHub Pages 仓库。</span></p>
  </article>
</div>

<h2><span class="lang-en">Seven Optimizations and GitHub Support</span><span class="lang-zh">七类优化与 GitHub 支持情况</span></h2>

<div class="project-list project-list--page">
  <article>
    <h2><span class="lang-en">Solutions Page</span><span class="lang-zh">行业解决方案页</span></h2>
    <p><span class="lang-en">Supported directly by GitHub Pages. The new Solutions page can grow by scenario, partner type, and application domain, keeping public communication focused on value, maturity, and collaboration entry points.</span><span class="lang-zh">GitHub Pages 直接支持。新的行业方案页可以按场景、合作对象和应用领域持续扩展，让公开表达聚焦价值、成熟度和合作入口。</span></p>
  </article>
  <article>
    <h2><span class="lang-en">Cases Page</span><span class="lang-zh">代表性案例页</span></h2>
    <p><span class="lang-en">Supported directly by GitHub Pages. Capability cases can present scenario value, research depth, delivery routes, and representative outcomes in a form suitable for public reading.</span><span class="lang-zh">GitHub Pages 直接支持。能力案例可以用适合公开阅读的方式呈现场景价值、研究深度、交付路线和代表性成果。</span></p>
  </article>
  <article>
    <h2><span class="lang-en">Collaboration Flow</span><span class="lang-zh">合作流程</span></h2>
    <p><span class="lang-en">Supported as static content and issue forms. The public site can explain the process; GitHub Issues can collect structured partner or lab-member updates.</span><span class="lang-zh">可通过静态内容和 Issue 表单支持。公开站点解释流程，GitHub Issues 收集结构化更新。</span></p>
  </article>
  <article>
    <h2><span class="lang-en">Visual Evidence</span><span class="lang-zh">视觉证据</span></h2>
    <p><span class="lang-en">Supported through static images and diagrams. The site can add architecture diagrams, scenario maps, transformation routes, and visual case narratives to make complex capabilities easier to read.</span><span class="lang-zh">可通过静态图片和图文模块支持。可以增加架构图、场景图、转化路径图和案例视觉叙事，让复杂能力更容易被理解。</span></p>
  </article>
  <article>
    <h2><span class="lang-en">SEO and AI Search</span><span class="lang-zh">SEO 与大模型抓取</span></h2>
    <p><span class="lang-en">Supported through metadata, sitemap, robots.txt, llms.txt, structured data, FAQ sections, and stable URLs.</span><span class="lang-zh">可通过元数据、站点地图、robots.txt、llms.txt、结构化数据、FAQ 和稳定 URL 支持。</span></p>
  </article>
  <article>
    <h2><span class="lang-en">Frontier Radar as Knowledge Asset</span><span class="lang-zh">前沿雷达知识资产化</span></h2>
    <p><span class="lang-en">Supported through GitHub Actions and data files. The radar can grow into topic clusters, monthly lab observations, and capability-linked trend summaries.</span><span class="lang-zh">可通过 GitHub Actions 和数据文件支持。雷达可继续扩展为方向聚类、月度观察和能力关联趋势总结。</span></p>
  </article>
  <article>
    <h2><span class="lang-en">Backend Management</span><span class="lang-zh">后台管理</span></h2>
    <p><span class="lang-en">Partially supported by GitHub alone. Public content editing can use GitHub login and static CMS. Private databases, fine-grained internal permissions, and operational dashboards require external services.</span><span class="lang-zh">GitHub 单独可部分支持。公开内容编辑可用 GitHub 登录和静态 CMS；私有数据库、精细权限和运营管理看板需要外接服务。</span></p>
  </article>
</div>

<div class="framework-grid framework-grid--page">
  <article class="framework-card framework-card--dark">
    <span class="framework-kicker">CMS Entry</span>
    <h2><span class="lang-en">Admin scaffold is available at `/admin/`.</span><span class="lang-zh">后台入口已预留在 `/admin/`。</span></h2>
    <p><span class="lang-en">The scaffold is intentionally limited to public content. Before live use, configure a GitHub OAuth provider for Decap CMS and add only trusted maintainers to the repository.</span><span class="lang-zh">该后台仅面向公开内容。正式使用前，需要为 Decap CMS 配置 GitHub OAuth，并只给可信维护者仓库权限。</span></p>
  </article>
  <article class="framework-card">
    <span class="framework-kicker">Safe Rule</span>
    <h2><span class="lang-en">Public website content is not the same as internal lab management.</span><span class="lang-zh">公开官网内容不等于实验室内部管理系统。</span></h2>
    <p><span class="lang-en">Use this website to publish public news, cases, recruitment, papers, media, and frontier summaries. Use private tools for student records, partner files, budgets, raw data, and sensitive technical documents.</span><span class="lang-zh">官网用于发布公开新闻、案例、招生、论文、媒体和前沿总结。学生记录、合作文件、经费、原始数据和敏感技术文档应放在私有工具中。</span></p>
  </article>
</div>
