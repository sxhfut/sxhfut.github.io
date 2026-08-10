---
layout: page
title: Calls & Opportunities
title_zh: 征稿与学术机会
nav_title: Calls
nav_title_zh: 学术机会
description: A daily refreshed list of conferences, journals, workshops, challenges, and academic opportunities around MAC-Lab's research route.
description_zh: 围绕 MAC-Lab 长期研究方向整理的会议、期刊、Workshop、挑战赛与学术机会入口。
permalink: /opportunities/
toggle: on
rank: 6.2
faq:
  - question: "What academic opportunities does MAC-Lab track?"
    question_zh: "MAC-Lab 会跟踪哪些学术机会？"
    answer: "MAC-Lab tracks conferences, journal submission routes, workshops, challenges, and selected calls around affective computing, AI plus psychology, multimodal intelligence, HCI, intelligent user interfaces, embodied agents, ubiquitous sensing, digital health, education, social computing, computational social science, human factors, and smart cockpit."
    answer_zh: "MAC-Lab 重点跟踪情感计算、AI + 心理、多模态智能、人机交互、智能用户界面、具身智能体、普适感知、数字健康、教育、社会计算、计算社会科学、人因工程和智能座舱相关的会议、期刊投稿入口、Workshop、挑战赛和专题征稿。"
  - question: "How often is the opportunities page refreshed?"
    question_zh: "学术机会页面多久更新一次？"
    answer: "The opportunity data is refreshed once a day by a scheduled GitHub Actions workflow, with official and curated entries kept as the stable base."
    answer_zh: "机会数据通过 GitHub Actions 每天刷新一次，官方入口和人工精选条目作为稳定底座保留。"
  - question: "Who is this page useful for?"
    question_zh: "这个页面适合谁看？"
    answer: "It is useful for undergraduate students, graduate students, lab members, collaborators, and partners who want to understand where MAC-Lab's research route connects with active academic venues and student training opportunities."
    answer_zh: "本科生、研究生、实验室成员、合作导师和产业伙伴都可以通过这个入口了解 MAC-Lab 的长期方向如何连接到活跃学术场域和学生训练机会。"
---

{% assign opportunity = site.data.opportunities %}
{% assign items = opportunity.items %}

<div class="summary-band opportunity-summary">
  <div><strong>{{ items | size }}</strong><span><span class="lang-en">active and watchlisted opportunities</span><span class="lang-zh">条学术机会与关注入口</span></span></div>
  <div><strong>{{ opportunity.stats.official_items | default: 0 }}</strong><span><span class="lang-en">official or lab-curated entries</span><span class="lang-zh">条官方或人工精选入口</span></span></div>
  <div><strong>{{ opportunity.stats.open_items | default: 0 }}</strong><span><span class="lang-en">open or rolling opportunities</span><span class="lang-zh">条开放或滚动投稿机会</span></span></div>
  <div><strong>BJT</strong><span><span class="lang-en">updated {{ opportunity.generated_date_beijing | default: opportunity.generated_at | slice: 0, 10 }}</span><span class="lang-zh">北京时间更新 {{ opportunity.generated_date_beijing | default: opportunity.generated_at | slice: 0, 10 }}</span></span></div>
</div>

<div class="media-note opportunity-intro">
  <h2><span class="lang-en">Calls that help the lab plan research, training, and collaboration.</span><span class="lang-zh">把机会放回研究训练里看。</span></h2>
  <p><span class="lang-en">MAC-Lab follows calls that sit close to its long route: affective computing, AI + psychology, multimodal sensing, affective NLP, HCI, intelligent user interfaces, embodied agents, ubiquitous sensing, digital health, education, social and psychological computing, trustworthy AI, human factors, and smart cockpit. Some items are immediate deadlines; others are watchlist venues worth preparing for before the official call opens.</span><span class="lang-zh">这里关注的是与实验室长期方向相邻、并且值得学生提前准备的机会：情感计算、AI + 心理、多模态感知、情感 NLP、人机交互、智能用户界面、具身智能体、普适感知、数字健康、教育、社会与心理计算、可信 AI、人因工程和智能座舱。有些是近期截止，有些是值得提前布局的长期关注入口。</span></p>
  <p><span class="lang-en">Dates can change. Please use the original link as the final source before planning a submission, workshop proposal, challenge team, or student project.</span><span class="lang-zh">投稿和参会时间可能调整。正式准备论文、Workshop、挑战赛或学生项目之前，请以原始链接为准。</span></p>
</div>

<section class="opportunity-featured" aria-labelledby="opportunity-featured-title">
  <div class="opportunity-featured__head">
    <span><span class="lang-en">Worth Watching</span><span class="lang-zh">近期值得看</span></span>
    <h2 id="opportunity-featured-title"><span class="lang-en">A few doors students can start planning around.</span><span class="lang-zh">几个可以提前安排的入口。</span></h2>
    <p><span class="lang-en">The full archive below shows {{ items | size }} entries with filters, search, and pagination.</span><span class="lang-zh">下方完整列表共 {{ items | size }} 条，支持筛选、搜索和分页。</span></p>
  </div>
  <div class="opportunity-featured__grid">
    {% for item in items limit:4 %}
      <a class="opportunity-featured__item" href="{{ item.url }}">
        <span>{{ item.deadline_label }} · {{ item.deadline }}</span>
        <strong><span class="lang-en">{{ item.title }}</span><span class="lang-zh">{{ item.title_zh | default: item.title }}</span></strong>
        <small>{{ item.track }} · {{ item.place }}</small>
      </a>
    {% endfor %}
  </div>
</section>

<div class="frontier-archive-heading" id="opportunity-archive">
  <span><span class="lang-en">Full Archive</span><span class="lang-zh">完整列表</span></span>
  <h2><span class="lang-en">Find calls by direction, format, and timing.</span><span class="lang-zh">按方向、类型和时间找机会。</span></h2>
</div>

<div class="frontier-toolbar opportunity-toolbar" aria-label="Opportunity filters">
  <button type="button" data-opportunity-filter="all"><span class="lang-en">All</span><span class="lang-zh">全部</span></button>
  <button type="button" data-opportunity-filter="conference"><span class="lang-en">Conferences</span><span class="lang-zh">会议</span></button>
  <button type="button" data-opportunity-filter="journal"><span class="lang-en">Journals</span><span class="lang-zh">期刊</span></button>
  <button type="button" data-opportunity-filter="workshop"><span class="lang-en">Workshops</span><span class="lang-zh">Workshop</span></button>
  <button type="button" data-opportunity-filter="challenge"><span class="lang-en">Challenges</span><span class="lang-zh">挑战赛</span></button>
  <button type="button" data-opportunity-filter="closing_soon"><span class="lang-en">Closing soon</span><span class="lang-zh">临近截止</span></button>
  <button type="button" data-opportunity-filter="rolling"><span class="lang-en">Rolling</span><span class="lang-zh">滚动投稿</span></button>
  <button type="button" data-opportunity-filter="watch"><span class="lang-en">Watchlist</span><span class="lang-zh">关注入口</span></button>
  <label>
    <span class="lang-en">Search</span><span class="lang-zh">搜索</span>
    <input type="search" data-opportunity-search placeholder="ACII, CHI, affective, mental health...">
  </label>
</div>

<div class="frontier-results opportunity-results" aria-live="polite">
  <p data-opportunity-count></p>
  <span><span class="lang-en">The list is ordered by urgency first, then MAC-Lab relevance. Official and lab-curated entries form the stable base; HCI, social-computing, AI, and CFP indexes add useful signals when available.</span><span class="lang-zh">列表默认先看时间，再看与实验室方向的贴合度。官方和人工精选入口构成稳定底座，HCI、社会计算、AI 与 CFP 索引会在可用时补充新信号。</span></span>
</div>

<nav class="frontier-pagination frontier-pagination--top opportunity-pagination" data-opportunity-pagination hidden aria-label="Opportunity pagination top">
  <button type="button" data-opportunity-prev><span class="lang-en">Previous</span><span class="lang-zh">上一页</span></button>
  <div class="frontier-pagination__pages" data-opportunity-pages></div>
  <button type="button" data-opportunity-next><span class="lang-en">Next</span><span class="lang-zh">下一页</span></button>
</nav>

<div class="opportunity-list">
  {% for item in items %}
    <article class="opportunity-card" data-opportunity-card data-kind="{{ item.kind | slugify }}" data-status="{{ item.status | slugify }}" data-rolling="{% if item.deadline == 'Rolling' %}true{% else %}false{% endif %}" data-search="{{ item.title | append: ' ' | append: item.title_zh | append: ' ' | append: item.summary | append: ' ' | append: item.summary_zh | append: ' ' | append: item.track | append: ' ' | append: item.fit | downcase | escape }}">
      <div class="opportunity-card__date">
        <span>{{ item.deadline_label }}</span>
        <strong>{{ item.deadline }}</strong>
        {% if item.deadline_tz %}
          <small>{{ item.deadline_tz }}</small>
        {% endif %}
      </div>
      <div class="opportunity-card__body">
        <div class="opportunity-card__topline">
          <span>{{ item.kind | upcase }}</span>
          <span>{{ item.track }}</span>
          {% if item.source_type == "official" %}
            <span>Official</span>
          {% endif %}
          {% if item.status == "closing_soon" %}
            <span class="is-hot"><span class="lang-en">Closing soon</span><span class="lang-zh">临近截止</span></span>
          {% elsif item.status == "watch" %}
            <span><span class="lang-en">Watchlist</span><span class="lang-zh">关注入口</span></span>
          {% endif %}
        </div>
        <h2><span class="lang-en">{{ item.title }}</span><span class="lang-zh">{{ item.title_zh | default: item.title }}</span></h2>
        <p class="opportunity-card__venue">{{ item.venue }}</p>
        <p><span class="lang-en">{{ item.summary }}</span><span class="lang-zh">{{ item.summary_zh | default: item.summary }}</span></p>
        <div class="opportunity-card__details">
          <span><b><span class="lang-en">When</span><span class="lang-zh">时间</span></b>{{ item.date | default: "TBD" }}</span>
          <span><b><span class="lang-en">Where</span><span class="lang-zh">地点</span></b>{{ item.place | default: "TBD" }}</span>
          <span><b><span class="lang-en">Source</span><span class="lang-zh">来源</span></b>{{ item.source }}</span>
        </div>
        {% if item.fit and item.fit.size > 0 %}
          <div class="frontier-tags opportunity-tags">
            {% for tag in item.fit %}
              <span><span class="lang-en">{{ tag }}</span><span class="lang-zh">{{ item.fit_zh[forloop.index0] | default: tag }}</span></span>
            {% endfor %}
          </div>
        {% endif %}
        <a href="{{ item.url }}"><span class="lang-en">Open original link</span><span class="lang-zh">打开原始链接</span></a>
      </div>
    </article>
  {% endfor %}
</div>

<div class="frontier-empty opportunity-empty" data-opportunity-empty hidden>
  <strong><span class="lang-en">No matching opportunity yet.</span><span class="lang-zh">暂时没有匹配机会。</span></strong>
  <p><span class="lang-en">Try another keyword or switch filters.</span><span class="lang-zh">可以换一个关键词，或切换筛选条件。</span></p>
</div>

<nav class="frontier-pagination frontier-pagination--bottom opportunity-pagination" data-opportunity-pagination hidden aria-label="Opportunity pagination bottom">
  <button type="button" data-opportunity-prev><span class="lang-en">Previous</span><span class="lang-zh">上一页</span></button>
  <div class="frontier-pagination__pages" data-opportunity-pages></div>
  <button type="button" data-opportunity-next><span class="lang-en">Next</span><span class="lang-zh">下一页</span></button>
</nav>

<script>
  (function () {
    var buttons = Array.prototype.slice.call(document.querySelectorAll("[data-opportunity-filter]"));
    var cards = Array.prototype.slice.call(document.querySelectorAll("[data-opportunity-card]"));
    var search = document.querySelector("[data-opportunity-search]");
    var count = document.querySelector("[data-opportunity-count]");
    var empty = document.querySelector("[data-opportunity-empty]");
    var paginations = Array.prototype.slice.call(document.querySelectorAll("[data-opportunity-pagination]"));
    var prevButtons = Array.prototype.slice.call(document.querySelectorAll("[data-opportunity-prev]"));
    var nextButtons = Array.prototype.slice.call(document.querySelectorAll("[data-opportunity-next]"));
    var pageContainers = Array.prototype.slice.call(document.querySelectorAll("[data-opportunity-pages]"));
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

    function filterMatches(card) {
      if (activeFilter === "all") return true;
      if (activeFilter === "closing_soon") return card.dataset.status === "closing_soon";
      if (activeFilter === "rolling") return card.dataset.rolling === "true";
      if (activeFilter === "watch") return card.dataset.status === "watch";
      return card.dataset.kind === activeFilter;
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
          button.setAttribute("aria-label", "Go to opportunity page " + page);
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
        var typeMatches = filterMatches(card);
        var textMatches = !query || (card.dataset.search || "").indexOf(query) !== -1;
        return typeMatches && textMatches;
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
        button.classList.toggle("is-active", button.dataset.opportunityFilter === activeFilter);
      });

      if (count) {
        var visibleStart = matches.length === 0 ? 0 : start + 1;
        var visibleEnd = Math.min(matches.length, end);
        count.innerHTML = '<span class="lang-en">Showing ' + visibleStart + '-' + visibleEnd + ' of ' + matches.length + ' opportunities · Page ' + currentPage + ' of ' + pageCount + '</span><span class="lang-zh">显示第 ' + visibleStart + '-' + visibleEnd + ' 条，共 ' + matches.length + ' 条机会 · 第 ' + currentPage + ' / ' + pageCount + ' 页</span>';
      }
      if (empty) {
        empty.hidden = matches.length !== 0;
      }
      renderPagination(pageCount);

      if (shouldScroll) {
        var target = document.querySelector(".opportunity-results");
        if (target) {
          target.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      }
    }

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        activeFilter = button.dataset.opportunityFilter;
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
