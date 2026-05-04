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

<div class="summary-band">
  <div><strong>{{ items | size }}</strong><span><span class="lang-en">curated and automatically fetched items</span><span class="lang-zh">条前沿论文与产业动态</span></span></div>
  <div><strong>arXiv</strong><span><span class="lang-en">open paper metadata refreshed by script</span><span class="lang-zh">开放论文元数据自动抓取</span></span></div>
  <div><strong>Manual</strong><span><span class="lang-en">curated application, media, and standards updates</span><span class="lang-zh">人工精选应用、媒体与标准成果</span></span></div>
  <div><strong>UTC</strong><span><span class="lang-en">last updated {{ frontier.generated_at | slice: 0, 10 }}</span><span class="lang-zh">最近更新 {{ frontier.generated_at | slice: 0, 10 }}</span></span></div>
</div>

<div class="media-note">
  <h2><span class="lang-en">How This Radar Updates</span><span class="lang-zh">本页如何自动更新</span></h2>
  <p><span class="lang-en">This page is refreshed by a scheduled GitHub Actions workflow. It fetches open arXiv metadata for selected queries, merges curated industry applications, media reports, and standards updates, then regenerates the page as static content.</span><span class="lang-zh">本页由 GitHub Actions 定时更新：自动抓取开放 arXiv 论文元数据，合并人工精选的产业应用、媒体报道与标准成果，再生成静态页面。</span></p>
  <p><span class="lang-en">The radar is a discovery layer, not a clinical recommendation system. Items should be read as pointers to primary sources.</span><span class="lang-zh">本页是前沿发现层，不是临床或心理咨询建议系统。所有条目都应回到原始来源进一步阅读。</span></p>
</div>

<div class="frontier-toolbar" aria-label="Frontier filters">
  <button type="button" data-frontier-filter="all"><span class="lang-en">All</span><span class="lang-zh">全部</span></button>
  <button type="button" data-frontier-filter="paper"><span class="lang-en">Papers</span><span class="lang-zh">论文</span></button>
  <button type="button" data-frontier-filter="industry"><span class="lang-en">Industry</span><span class="lang-zh">产业</span></button>
  <button type="button" data-frontier-filter="translation"><span class="lang-en">Applications</span><span class="lang-zh">应用</span></button>
  <button type="button" data-frontier-filter="standard"><span class="lang-en">Standards</span><span class="lang-zh">标准</span></button>
  <label>
    <span class="lang-en">Search</span><span class="lang-zh">搜索</span>
    <input type="search" data-frontier-search placeholder="affective computing, counseling, emotion...">
  </label>
</div>

<div class="frontier-list">
  {% for item in items %}
    <article class="frontier-card" data-frontier-card data-kind="{{ item.kind | slugify }}" data-search="{{ item.title | append: ' ' | append: item.title_zh | append: ' ' | append: item.summary | append: ' ' | append: item.summary_zh | append: ' ' | append: item.track | downcase | escape }}">
      <div class="frontier-card__meta">
        <time>{{ item.published }}</time>
        <span>{{ item.kind | upcase }}</span>
        <strong>{{ item.track }}</strong>
      </div>
      <div class="frontier-card__body">
        <h2><span class="lang-en">{{ item.title }}</span><span class="lang-zh">{{ item.title_zh | default: item.title }}</span></h2>
        {% if item.authors and item.authors.size > 0 %}
          <p class="frontier-card__authors">{{ item.authors | join: ", " }}</p>
        {% endif %}
        <p><span class="lang-en">{{ item.summary }}</span><span class="lang-zh">{{ item.summary_zh | default: item.summary }}</span></p>
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

<script>
  (function () {
    var buttons = Array.prototype.slice.call(document.querySelectorAll("[data-frontier-filter]"));
    var cards = Array.prototype.slice.call(document.querySelectorAll("[data-frontier-card]"));
    var search = document.querySelector("[data-frontier-search]");
    var activeFilter = "all";

    function update() {
      var query = search ? search.value.trim().toLowerCase() : "";
      cards.forEach(function (card) {
        var kindMatches = activeFilter === "all" || card.dataset.kind === activeFilter;
        var textMatches = !query || (card.dataset.search || "").indexOf(query) !== -1;
        card.hidden = !(kindMatches && textMatches);
      });
      buttons.forEach(function (button) {
        button.classList.toggle("is-active", button.dataset.frontierFilter === activeFilter);
      });
    }

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        activeFilter = button.dataset.frontierFilter;
        update();
      });
    });

    if (search) {
      search.addEventListener("input", update);
    }

    update();
  })();
</script>
