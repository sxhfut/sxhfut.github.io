---
layout: page
title: Frontiers
title_zh: 前沿雷达
description: A living radar for affective computing, AI for psychology, embodied emotional intelligence, and industry applications.
description_zh: 自动聚合情感计算、人工智能+心理、具身情感智能与产业应用动态的前沿雷达。
permalink: /frontiers/
toggle: on
rank: 6
---

{% assign frontier = site.data.frontiers %}
{% assign items = frontier.items %}
{% assign community_items = items | where: "kind", "community" %}

<div class="summary-band">
  <div><strong>{{ items | size }}</strong><span><span class="lang-en">curated and automatically fetched items</span><span class="lang-zh">条前沿论文与产业动态</span></span></div>
  <div><strong>arXiv</strong><span><span class="lang-en">open paper metadata refreshed by script</span><span class="lang-zh">开放论文元数据自动抓取</span></span></div>
  <div><strong>{{ frontier.stats.rss_items | default: 0 }}</strong><span><span class="lang-en">RSS/open-feed research and industry signals</span><span class="lang-zh">条 RSS / 开放订阅源信号</span></span></div>
  <div><strong>{{ frontier.stats.recent_signal_items | default: frontier.stats.last30days_items | default: 0 }}</strong><span><span class="lang-en">recent community and open-source signals</span><span class="lang-zh">条近 30 天社区与开源信号</span></span></div>
  <div><strong>BJT</strong><span><span class="lang-en">last updated {{ frontier.generated_date_beijing | default: frontier.generated_at | slice: 0, 10 }}</span><span class="lang-zh">北京时间更新 {{ frontier.generated_date_beijing | default: frontier.generated_at | slice: 0, 10 }}</span></span></div>
</div>

<div class="media-note">
  <h2><span class="lang-en">How This Radar Updates</span><span class="lang-zh">本页如何自动更新</span></h2>
  <p><span class="lang-en">Scheduled and manual GitHub Actions refresh this page. Full refreshes fetch open arXiv metadata, scan selected RSS and Atom feeds from research labs, journals, AI media, and industry channels, merge usable Last30Days community or open-source signals, then add curated lab applications, media reports, and standards updates into static content. Curated-only refreshes update lab-selected items quickly.</span><span class="lang-zh">本页由 GitHub Actions 定时或手动刷新。全量刷新会抓取开放 arXiv 论文元数据，扫描研究机构、期刊、AI 媒体与产业渠道 RSS / Atom 订阅源，并在有可用信号时合并 Last30Days 社区与开源动态，再加入实验室精选应用、媒体报道与标准成果。精选刷新则用于快速更新人工选择条目。</span></p>
  <p><span class="lang-en">The radar is a discovery layer. Items are pointers to primary sources and should be read with the original links.</span><span class="lang-zh">前沿雷达承担发现与筛选功能。所有条目都是通往原始来源的线索，应结合原文继续阅读。</span></p>
</div>

<div class="frontier-lens-board">
  <div>
    <span><span class="lang-en">MAC-Lab Lens</span><span class="lang-zh">MAC-Lab 视角</span></span>
    <h2><span class="lang-en">A radar that turns external signals into lab capability.</span><span class="lang-zh">面向能力建设的研究雷达。</span></h2>
    <p><span class="lang-en">Each item is interpreted through MAC-Lab's long-term route: multimedia affective computing, ubiquitous psychological computing, embodied emotional intelligence, and AI for mind-body health.</span><span class="lang-zh">每条内容都放回 MAC-Lab 的长期路线中理解：多模态情感计算、普适心理计算、具身情感智能，以及 AI 身心健康平台。</span></p>
  </div>
  <div class="frontier-method">
    <article>
      <strong>01</strong>
      <span><span class="lang-en">Signal</span><span class="lang-zh">发现信号</span></span>
      <p><span class="lang-en">Capture new papers and selected application news around AI + psychology.</span><span class="lang-zh">捕捉 AI + 心理、情感计算与具身智能的新论文和应用动态。</span></p>
    </article>
    <article>
      <strong>02</strong>
      <span><span class="lang-en">Capability</span><span class="lang-zh">映射能力</span></span>
      <p><span class="lang-en">Map signals to affective LLMs, multimodal sensing, assessment, support, and embodied interaction.</span><span class="lang-zh">映射到情感大模型、多模态感知、心理评估、身心支持和具身交互能力。</span></p>
    </article>
    <article>
      <strong>03</strong>
      <span><span class="lang-en">Translation</span><span class="lang-zh">走向落地</span></span>
      <p><span class="lang-en">Keep the radar connected with platforms, student projects, standards, and deployment scenarios.</span><span class="lang-zh">把前沿判断连接到平台建设、学生项目、标准工作和真实场景落地。</span></p>
    </article>
  </div>
</div>

<section class="frontier-latest" aria-labelledby="frontier-latest-title">
  <div class="frontier-latest__head">
    <span><span class="lang-en">Latest Updates</span><span class="lang-zh">最新抓取</span></span>
    <h2 id="frontier-latest-title"><span class="lang-en">Fresh signals from the latest radar refresh.</span><span class="lang-zh">让最近一次雷达更新先被看见。</span></h2>
    <p><span class="lang-en">This strip intentionally shows only the newest four signals. The full archive below contains {{ items | size }} items, with search, filters, and pagination.</span><span class="lang-zh">这里有意只展示最新 4 条信号；下方完整归档共 {{ items | size }} 条，支持搜索、筛选和分页。</span></p>
    <a class="frontier-latest__jump" href="#frontier-archive"><span class="lang-en">View the full archive</span><span class="lang-zh">查看全部 {{ items | size }} 条</span></a>
  </div>
  <div class="frontier-latest__grid">
    {% for item in items limit:4 %}
      <a class="frontier-latest__item" href="{{ item.url }}">
        <time>{{ item.published }}</time>
        <strong><span class="lang-en">{{ item.title }}</span><span class="lang-zh">{{ item.title_zh | default: item.title }}</span></strong>
        <span>{{ item.kind | upcase }} · {{ item.track }}</span>
      </a>
    {% endfor %}
  </div>
</section>

<div class="frontier-archive-heading" id="frontier-archive">
  <span><span class="lang-en">Full Archive</span><span class="lang-zh">完整归档</span></span>
  <h2><span class="lang-en">Search and page through every radar item.</span><span class="lang-zh">所有前沿条目都在这里分页浏览。</span></h2>
</div>

<div class="frontier-toolbar" aria-label="Frontier filters">
  <button type="button" data-frontier-filter="all"><span class="lang-en">All</span><span class="lang-zh">全部</span></button>
  <button type="button" data-frontier-filter="paper"><span class="lang-en">Papers</span><span class="lang-zh">论文</span></button>
  {% if community_items.size > 0 %}
    <button type="button" data-frontier-filter="community"><span class="lang-en">Signals</span><span class="lang-zh">信号</span></button>
  {% endif %}
  <button type="button" data-frontier-filter="industry"><span class="lang-en">Industry</span><span class="lang-zh">产业</span></button>
  <button type="button" data-frontier-filter="translation"><span class="lang-en">Applications</span><span class="lang-zh">应用</span></button>
  <button type="button" data-frontier-filter="standard"><span class="lang-en">Standards</span><span class="lang-zh">标准</span></button>
  <label>
    <span class="lang-en">Search</span><span class="lang-zh">搜索</span>
    <input type="search" data-frontier-search placeholder="affective computing, counseling, emotion...">
  </label>
</div>

<div class="frontier-results" aria-live="polite">
  <p data-frontier-count></p>
  <span><span class="lang-en">The archive is ordered by recency first, then MAC-Lab relevance. Use filters and search to narrow the radar as it grows.</span><span class="lang-zh">归档默认按时间优先、实验室相关度辅助排序。随着内容增长，可通过筛选与搜索快速收敛到具体方向。</span></span>
</div>

<nav class="frontier-pagination frontier-pagination--top" data-frontier-pagination hidden aria-label="Frontier pagination top">
  <button type="button" data-frontier-prev><span class="lang-en">Previous</span><span class="lang-zh">上一页</span></button>
  <div class="frontier-pagination__pages" data-frontier-pages></div>
  <button type="button" data-frontier-next><span class="lang-en">Next</span><span class="lang-zh">下一页</span></button>
</nav>

<div class="frontier-list">
  {% for item in items %}
    <article class="frontier-card" data-frontier-card data-kind="{{ item.kind | slugify }}" data-search="{{ item.title | append: ' ' | append: item.title_zh | append: ' ' | append: item.summary | append: ' ' | append: item.summary_zh | append: ' ' | append: item.track | downcase | escape }}">
      <div class="frontier-card__meta">
        <time>{{ item.published }}</time>
        <span>{{ item.kind | upcase }}</span>
        <strong>{{ item.track }}</strong>
        {% if item.relevance_score %}
          <div class="frontier-card__score">
            <b>{{ item.relevance_score }}</b>
            <small><span class="lang-en">MAC-Lab relevance</span><span class="lang-zh">相关度</span></small>
          </div>
        {% endif %}
      </div>
      <div class="frontier-card__body">
        <h2><span class="lang-en">{{ item.title }}</span><span class="lang-zh">{{ item.title_zh | default: item.title }}</span></h2>
        {% if item.authors and item.authors.size > 0 %}
          <p class="frontier-card__authors">{{ item.authors | join: ", " }}</p>
        {% endif %}
        <p><span class="lang-en">{{ item.summary }}</span><span class="lang-zh">{{ item.summary_zh | default: item.summary }}</span></p>
        {% if item.lens %}
          <div class="frontier-card__lens">
            <strong><span class="lang-en">MAC-Lab Lens</span><span class="lang-zh">实验室视角</span></strong>
            <p><span class="lang-en">{{ item.lens }}</span><span class="lang-zh">{{ item.lens_zh | default: item.lens }}</span></p>
          </div>
        {% endif %}
        {% if item.capability_tags and item.capability_tags.size > 0 %}
          <div class="frontier-tags frontier-tags--capability">
            {% for tag in item.capability_tags %}
              <span><span class="lang-en">{{ tag }}</span><span class="lang-zh">{{ item.capability_tags_zh[forloop.index0] | default: tag }}</span></span>
            {% endfor %}
          </div>
        {% endif %}
        {% if item.categories and item.categories.size > 0 %}
          <div class="frontier-tags">
            {% for category in item.categories %}
              <span>{{ category }}</span>
            {% endfor %}
          </div>
        {% endif %}
        <a href="{{ item.url }}"><span class="lang-en">Open Link</span><span class="lang-zh">查看原文</span></a>
      </div>
    </article>
  {% endfor %}
</div>

<div class="frontier-empty" data-frontier-empty hidden>
  <strong><span class="lang-en">No matching radar item yet.</span><span class="lang-zh">暂时没有匹配条目。</span></strong>
  <p><span class="lang-en">Try another keyword, switch filters, or check back after the next scheduled update.</span><span class="lang-zh">可以换一个关键词、切换筛选条件，或等待下一次定时更新。</span></p>
</div>

<nav class="frontier-pagination frontier-pagination--bottom" data-frontier-pagination hidden aria-label="Frontier pagination bottom">
  <button type="button" data-frontier-prev><span class="lang-en">Previous</span><span class="lang-zh">上一页</span></button>
  <div class="frontier-pagination__pages" data-frontier-pages></div>
  <button type="button" data-frontier-next><span class="lang-en">Next</span><span class="lang-zh">下一页</span></button>
</nav>

<script>
  (function () {
    var buttons = Array.prototype.slice.call(document.querySelectorAll("[data-frontier-filter]"));
    var cards = Array.prototype.slice.call(document.querySelectorAll("[data-frontier-card]"));
    var search = document.querySelector("[data-frontier-search]");
    var count = document.querySelector("[data-frontier-count]");
    var empty = document.querySelector("[data-frontier-empty]");
    var paginations = Array.prototype.slice.call(document.querySelectorAll("[data-frontier-pagination]"));
    var prevButtons = Array.prototype.slice.call(document.querySelectorAll("[data-frontier-prev]"));
    var nextButtons = Array.prototype.slice.call(document.querySelectorAll("[data-frontier-next]"));
    var pageContainers = Array.prototype.slice.call(document.querySelectorAll("[data-frontier-pages]"));
    var activeFilter = "all";
    var pageSize = 10;
    var currentPage = 1;

    function pageNumbers(pageCount) {
      var numbers = [];
      var start = Math.max(1, currentPage - 2);
      var end = Math.min(pageCount, currentPage + 2);

      if (start > 1) {
        numbers.push(1);
        if (start > 2) numbers.push("ellipsis-start");
      }

      for (var page = start; page <= end; page += 1) {
        numbers.push(page);
      }

      if (end < pageCount) {
        if (end < pageCount - 1) numbers.push("ellipsis-end");
        numbers.push(pageCount);
      }

      return numbers;
    }

    function renderPagination(pageCount) {
      if (!paginations.length || !pageContainers.length) return;

      paginations.forEach(function (pagination) {
        pagination.hidden = pageCount <= 1;
      });

      pageContainers.forEach(function (pages) {
        pages.innerHTML = "";

        pageNumbers(pageCount).forEach(function (page) {
          if (typeof page === "string") {
            var ellipsis = document.createElement("span");
            ellipsis.textContent = "...";
            ellipsis.setAttribute("aria-hidden", "true");
            pages.appendChild(ellipsis);
            return;
          }

          var button = document.createElement("button");
          button.type = "button";
          button.textContent = page;
          button.className = page === currentPage ? "is-active" : "";
          button.setAttribute("aria-label", "Go to page " + page);
          button.setAttribute("aria-current", page === currentPage ? "page" : "false");
          button.addEventListener("click", function () {
            currentPage = page;
            update(true);
          });
          pages.appendChild(button);
        });
      });

      prevButtons.forEach(function (prev) {
        prev.disabled = currentPage <= 1;
      });
      nextButtons.forEach(function (next) {
        next.disabled = currentPage >= pageCount;
      });
    }

    function update(shouldScroll) {
      var query = search ? search.value.trim().toLowerCase() : "";
      var matches = cards.filter(function (card) {
        var kindMatches = activeFilter === "all" || card.dataset.kind === activeFilter;
        var textMatches = !query || (card.dataset.search || "").indexOf(query) !== -1;
        return kindMatches && textMatches;
      });
      var pageCount = Math.max(1, Math.ceil(matches.length / pageSize));
      currentPage = Math.min(currentPage, pageCount);
      var start = (currentPage - 1) * pageSize;
      var end = start + pageSize;

      cards.forEach(function (card) {
        card.hidden = true;
      });

      matches.slice(start, end).forEach(function (card) {
        card.hidden = false;
      });

      buttons.forEach(function (button) {
        button.classList.toggle("is-active", button.dataset.frontierFilter === activeFilter);
      });

      if (count) {
        var visibleStart = matches.length === 0 ? 0 : start + 1;
        var visibleEnd = Math.min(matches.length, end);
        count.innerHTML = '<span class="lang-en">Showing ' + visibleStart + '-' + visibleEnd + ' of ' + matches.length + ' matched items · Page ' + currentPage + ' of ' + pageCount + '</span><span class="lang-zh">显示第 ' + visibleStart + '-' + visibleEnd + ' 条，共 ' + matches.length + ' 条匹配内容 · 第 ' + currentPage + ' / ' + pageCount + ' 页</span>';
      }
      if (empty) {
        empty.hidden = matches.length !== 0;
      }
      renderPagination(pageCount);

      if (shouldScroll) {
        var target = document.querySelector(".frontier-results");
        if (target) {
          target.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      }
    }

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        activeFilter = button.dataset.frontierFilter;
        currentPage = 1;
        update();
      });
    });

    if (search) {
      search.addEventListener("input", function () {
        currentPage = 1;
        update();
      });
    }

    prevButtons.forEach(function (prev) {
      prev.addEventListener("click", function () {
        if (currentPage > 1) {
          currentPage -= 1;
          update(true);
        }
      });
    });

    nextButtons.forEach(function (next) {
      next.addEventListener("click", function () {
        currentPage += 1;
        update(true);
      });
    });

    update();
  })();
</script>
