(function () {
  const state = {
    supabase: null,
    session: null,
    profile: null,
    view: "overview"
  };

  const REVIEW_STATUSES = ["submitted", "review", "approved", "public_ready", "archived"];
  const STATUS_LABELS = {
    draft: "草稿",
    submitted: "已提交",
    review: "审核中",
    approved: "已通过",
    public_ready: "可公开",
    private: "内部保存",
    archived: "已归档"
  };
  const TASK_TYPE_LABELS = {
    news: "新闻发布",
    case: "能力案例",
    frontier: "前沿精选",
    student_page: "学生页面",
    solution: "行业方案",
    publication: "论文成果",
    output: "成果材料",
    public_update: "公开更新"
  };
  const SOURCE_TABLES = new Set(["lab_news", "lab_outputs", "partner_requests", "frontier_curations", "student_pages"]);

  const $ = (selector) => document.querySelector(selector);
  const viewMount = $("#viewMount");
  const setupPanel = $("#setupPanel");
  const authPanel = $("#authPanel");
  const appPanel = $("#appPanel");
  const statusBanner = $("#statusBanner");
  const userRole = $("#userRole");
  const signOutButton = $("#signOutButton");

  function getConfig() {
    const runtimeConfig = window.MACLAB_CONSOLE_CONFIG || {};
    const localConfig = JSON.parse(localStorage.getItem("maclab_console_config") || "{}");
    const config = {
      supabaseUrl: runtimeConfig.supabaseUrl || localConfig.supabaseUrl,
      supabaseAnonKey: runtimeConfig.supabaseAnonKey || localConfig.supabaseAnonKey
    };
    if (!config.supabaseUrl || !config.supabaseAnonKey || config.supabaseUrl.includes("YOUR-PROJECT")) {
      return null;
    }
    return config;
  }

  function getPartialConfig() {
    const runtimeConfig = window.MACLAB_CONSOLE_CONFIG || {};
    const localConfig = JSON.parse(localStorage.getItem("maclab_console_config") || "{}");
    return {
      supabaseUrl: runtimeConfig.supabaseUrl || localConfig.supabaseUrl || "",
      supabaseAnonKey: runtimeConfig.supabaseAnonKey || localConfig.supabaseAnonKey || ""
    };
  }

  function showStatus(message, type) {
    statusBanner.hidden = false;
    statusBanner.textContent = message;
    statusBanner.classList.toggle("is-error", type === "error");
  }

  function hideStatus() {
    statusBanner.hidden = true;
    statusBanner.textContent = "";
  }

  function requireClient() {
    if (!state.supabase) {
      throw new Error("Supabase is not configured.");
    }
    return state.supabase;
  }

  function isAdmin() {
    return ["owner", "admin"].includes(state.profile?.role);
  }

  function labelStatus(status) {
    return STATUS_LABELS[status] || status || "未设置";
  }

  function labelTaskType(type) {
    return TASK_TYPE_LABELS[type] || type || "公开更新";
  }

  function safeUrl(value) {
    const url = String(value || "").trim();
    if (!url) return "";
    try {
      const parsed = new URL(url, window.location.origin);
      return parsed.protocol === "http:" || parsed.protocol === "https:" ? parsed.href : "";
    } catch (_error) {
      return "";
    }
  }

  function normalizePath(value, fallback) {
    const path = String(value || "").trim() || fallback;
    return path.startsWith("/") ? path : `/${path}`;
  }

  function taskTargetFor(type) {
    return {
      news: "/news/",
      case: "/cases/",
      frontier: "/frontiers/",
      student_page: "/team/",
      solution: "/solutions/",
      publication: "/publications/",
      output: "/projects/"
    }[type] || "/";
  }

  function taskTypeForOutput(type) {
    return {
      project: "output",
      paper: "publication",
      competition: "news",
      platform: "case",
      partner: "case"
    }[type] || "output";
  }

  async function createWorkflowTask(options) {
    const client = requireClient();
    const taskType = options.taskType || "public_update";
    const payload = {
      task_type: taskType,
      title: options.title,
      summary: options.summary || "",
      source_url: options.sourceUrl || null,
      target_url: options.targetUrl || taskTargetFor(taskType),
      priority: options.priority || 3,
      status: "submitted",
      submitted_by: state.session.user.id,
      metadata: {
        source_table: options.sourceTable || null,
        source_id: options.sourceId || null,
        origin_label: options.originLabel || "",
        publish_hint: options.publishHint || "",
        created_by_console: true
      }
    };
    const { error } = await client.from("content_tasks").insert(payload);
    return error;
  }

  async function createWorkflowTaskFromInsert(result, fallback) {
    const row = result?.data;
    return createWorkflowTask({
      ...fallback,
      sourceId: row?.id || null,
      title: fallback.title || row?.title || row?.organization || "待整理素材",
      summary: fallback.summary || row?.summary || row?.need_summary || "",
      sourceUrl: fallback.sourceUrl || row?.source_url || ""
    });
  }

  async function syncLinkedSourceStatus(row, status) {
    const metadata = row?.metadata || {};
    const table = metadata.source_table;
    const id = metadata.source_id;
    if (!table || !id || !SOURCE_TABLES.has(table)) return null;
    const client = requireClient();
    if (table === "student_pages") {
      const payload = {
        visibility: status === "public_ready" ? "published" : status === "archived" ? "hidden" : "draft",
        ...(isAdmin() ? { reviewed_by: state.session.user.id } : {}),
        ...(status === "public_ready" ? { published_at: new Date().toISOString() } : {})
      };
      const { error } = await client.from(table).update(payload).eq("id", id);
      return error;
    }
    const payload = { status };
    if (["lab_news", "frontier_curations", "student_pages"].includes(table) && isAdmin()) {
      payload.reviewed_by = state.session.user.id;
    }
    if (["frontier_curations", "student_pages"].includes(table) && status === "public_ready") {
      payload.published_at = new Date().toISOString();
    }
    const { error } = await client.from(table).update(payload).eq("id", id);
    return error;
  }

  async function init() {
    const config = getConfig();
    if (!config) {
      setupPanel.hidden = false;
      const partial = getPartialConfig();
      const form = $("#setupForm");
      if (form) {
        form.url.value = partial.supabaseUrl;
        form.anonKey.value = partial.supabaseAnonKey;
      }
      authPanel.hidden = true;
      appPanel.hidden = true;
      return;
    }

    state.supabase = window.supabase.createClient(config.supabaseUrl, config.supabaseAnonKey);
    const { data } = await state.supabase.auth.getSession();
    state.session = data.session;

    state.supabase.auth.onAuthStateChange((_event, session) => {
      state.session = session;
      renderShell();
    });

    renderShell();
  }

  async function renderShell() {
    setupPanel.hidden = true;
    if (!state.session) {
      authPanel.hidden = false;
      appPanel.hidden = true;
      userRole.textContent = "未登录";
      signOutButton.hidden = true;
      return;
    }

    authPanel.hidden = true;
    appPanel.hidden = false;
    signOutButton.hidden = false;
    await loadProfile();
    renderView(state.view);
  }

  async function loadProfile() {
    const client = requireClient();
    const user = state.session.user;
    const { data, error } = await client
      .from("profiles")
      .select("*")
      .eq("id", user.id)
      .maybeSingle();

    if (error) {
      state.profile = { id: user.id, email: user.email, role: "pending", status: "pending" };
      userRole.textContent = "pending";
      showStatus("已登录，但尚未读取到权限表。请确认 Supabase SQL 已部署，或等待 owner 审核账号。", "error");
      return;
    }

    state.profile = data || { id: user.id, email: user.email, role: "pending", status: "pending" };
    userRole.textContent = `${state.profile.role || "pending"} · ${user.email || ""}`;
    hideStatus();
  }

  function renderView(view) {
    state.view = view;
    document.querySelectorAll(".console-nav button").forEach((button) => {
      button.classList.toggle("is-active", button.dataset.view === view);
    });

    const template = $(`#${view}Template`);
    viewMount.replaceChildren(template.content.cloneNode(true));
    hydrateViewLinks();
    if (view === "overview") hydrateOverview();
    if (view === "profile") hydrateProfile();
    if (view === "news") hydrateNews();
    if (view === "partners") hydratePartners();
    if (view === "review") hydrateReviewQueue();
    if (view === "frontiers") hydrateFrontierCurations();
    if (view === "people") hydratePeople();
    if (view === "projects") hydrateProjects();
    if (view === "audit") hydrateAudit();
    if (view === "settings") hydrateSettings();
  }

  function hydrateOverview() {
    const roleNode = viewMount.querySelector("[data-profile-role]");
    if (roleNode) roleNode.textContent = state.profile?.role || "pending";
    loadDashboardCounts();
  }

  function hydrateViewLinks() {
    viewMount.querySelectorAll("[data-console-view]").forEach((node) => {
      node.addEventListener("click", () => renderView(node.dataset.consoleView));
    });
  }

  async function loadDashboardCounts() {
    const client = requireClient();
    const specs = [
      { key: "content_tasks", table: "content_tasks", statuses: ["submitted", "review"] },
      { key: "lab_news", table: "lab_news", statuses: ["submitted", "review", "public_ready"] },
      { key: "partner_requests", table: "partner_requests", statuses: ["submitted", "review"] },
      { key: "frontier_curations", table: "frontier_curations", statuses: ["submitted", "review", "public_ready"] }
    ];
    await Promise.all(specs.map(async (spec) => {
      const node = viewMount.querySelector(`[data-count="${spec.key}"]`);
      if (!node) return;
      let query = client.from(spec.table).select("id", { count: "exact", head: true });
      if (spec.statuses) query = query.in("status", spec.statuses);
      const { count, error } = await query;
      node.textContent = error ? "—" : String(count || 0);
    }));
  }

  async function hydrateProfile() {
    const form = $("#studentPageForm");
    const client = requireClient();
    const { data } = await client
      .from("student_pages")
      .select("*")
      .eq("owner_id", state.session.user.id)
      .maybeSingle();

    if (data) {
      form.title_zh.value = data.title_zh || "";
      form.title_en.value = data.title_en || "";
      form.slug.value = data.slug || "";
      form.research_tags.value = (data.research_tags || []).join(", ");
      form.body_zh.value = data.body_zh || "";
      form.body_en.value = data.body_en || "";
      form.visibility.value = data.visibility || "draft";
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const payload = {
        owner_id: state.session.user.id,
        title_zh: form.title_zh.value.trim(),
        title_en: form.title_en.value.trim(),
        slug: form.slug.value.trim() || null,
        research_tags: form.research_tags.value.split(",").map((item) => item.trim()).filter(Boolean),
        body_zh: form.body_zh.value.trim(),
        body_en: form.body_en.value.trim(),
        visibility: form.visibility.value,
        updated_at: new Date().toISOString()
      };
      const { data: savedPage, error } = await client
        .from("student_pages")
        .upsert(payload, { onConflict: "owner_id" })
        .select("id, title_zh, title_en, slug, body_zh, visibility")
        .single();
      if (!error && payload.visibility === "published") {
        await createWorkflowTaskFromInsert({ data: savedPage }, {
          sourceTable: "student_pages",
          taskType: "student_page",
          targetUrl: "/team/",
          title: `学生页面审核：${payload.title_zh}`,
          summary: payload.body_zh,
          publishHint: "审核学生个人页，确认研究方向、成果、竞赛经历和公开表述后再进入官网团队页面。"
        });
      }
      showStatus(error ? error.message : "个人页面已保存。申请发布时会自动进入审核队列。", error ? "error" : "success");
    });
  }

  async function hydrateNews() {
    const form = $("#newsForm");
    const list = $("#newsList");
    const client = requireClient();

    async function loadNews() {
      const { data, error } = await client
        .from("lab_news")
        .select("title, category, summary, status, created_at")
        .order("created_at", { ascending: false })
        .limit(10);
      renderRecords(list, data, error, "暂无新闻素材。");
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const payload = {
        title: form.title.value.trim(),
        category: form.category.value,
        summary: form.summary.value.trim(),
        source_url: form.source_url.value.trim() || null,
        submitted_by: state.session.user.id,
        status: isAdmin() ? "approved" : "submitted"
      };
      const { data: savedNews, error } = await client
        .from("lab_news")
        .insert(payload)
        .select("id, title, summary, source_url, category")
        .single();
      let taskError = null;
      if (!error) {
        taskError = await createWorkflowTaskFromInsert({ data: savedNews }, {
          sourceTable: "lab_news",
          taskType: "news",
          targetUrl: "/news/",
          title: `新闻发布：${payload.title}`,
          summary: payload.summary,
          sourceUrl: payload.source_url,
          publishHint: "核对事实、时间、参与人、公开链接和英文摘要后，可转入实验室新闻页。"
        });
      }
      showStatus(error ? error.message : taskError ? `新闻已保存，但审核任务创建失败：${taskError.message}` : "新闻素材已提交，并已进入审核队列。", error || taskError ? "error" : "success");
      if (!error) {
        form.reset();
        loadNews();
        loadDashboardCounts();
      }
    });

    loadNews();
  }

  async function hydratePeople() {
    const list = $("#peopleList");
    const client = requireClient();
    const query = client
      .from("profiles")
      .select("id, full_name, email, role, status, github_username, updated_at")
      .order("updated_at", { ascending: false })
      .limit(30);
    const { data, error } = await query;
    renderPeople(list, data, error);
  }

  async function hydratePartners() {
    const form = $("#partnerForm");
    const list = $("#partnerList");
    const client = requireClient();

    async function loadPartners() {
      const { data, error } = await client
        .from("partner_requests")
        .select("organization, contact_name, scenario, need_summary, status, created_at")
        .order("created_at", { ascending: false })
        .limit(12);
      renderRecords(list, data, error, isAdmin() ? "暂无合作线索。" : "合作线索仅对 owner/admin 开放。");
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const payload = {
        organization: form.organization.value.trim(),
        contact_name: form.contact_name.value.trim() || null,
        contact_email: form.contact_email.value.trim() || null,
        scenario: form.scenario.value,
        need_summary: form.need_summary.value.trim(),
        status: "submitted",
        owner_id: isAdmin() ? state.session.user.id : null
      };
      const { error } = await client.from("partner_requests").insert(payload);
      let taskError = null;
      if (!error) {
        taskError = await createWorkflowTask({
          sourceTable: "partner_requests",
          sourceId: null,
          taskType: "solution",
          title: `合作线索梳理：${payload.organization}`,
          summary: payload.need_summary,
          targetUrl: "/solutions/",
          priority: 4,
          publishHint: "先做场景诊断和合作路径判断，适合公开时再转为行业方案、能力案例或联合申报材料。"
        });
      }
      showStatus(error ? error.message : taskError ? `线索已保存，但审核任务创建失败：${taskError.message}` : "合作线索已保存，并已进入方案审核队列。", error || taskError ? "error" : "success");
      if (!error) {
        form.reset();
        loadPartners();
        loadDashboardCounts();
      }
    });

    loadPartners();
  }

  async function hydrateReviewQueue() {
    const form = $("#taskForm");
    const list = $("#taskList");
    const client = requireClient();

    async function loadTasks() {
      const { data, error } = await client
        .from("content_tasks")
        .select("id, title, task_type, summary, priority, status, source_url, target_url, metadata, created_at")
        .order("created_at", { ascending: false })
        .limit(20);
      renderReviewTasks(list, data, error, "暂无审核任务。");
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const payload = {
        title: form.title.value.trim(),
        task_type: form.task_type.value,
        priority: Number(form.priority.value),
        source_url: form.source_url.value.trim() || null,
        target_url: form.target_url.value.trim() || null,
        summary: form.summary.value.trim(),
        status: "submitted",
        submitted_by: state.session.user.id
      };
      const { error } = await client.from("content_tasks").insert(payload);
      showStatus(error ? error.message : "审核任务已提交。", error ? "error" : "success");
      if (!error) {
        form.reset();
        loadTasks();
        loadDashboardCounts();
      }
    });

    loadTasks();
  }

  async function hydrateFrontierCurations() {
    const form = $("#frontierCurationForm");
    const list = $("#frontierCurationList");
    const client = requireClient();

    async function loadCurations() {
      const { data, error } = await client
        .from("frontier_curations")
        .select("id, title, source_url, track, summary, takeaway_zh, relevance, status, created_at")
        .order("created_at", { ascending: false })
        .limit(20);
      renderReviewTasks(list, data, error, "暂无人工精选条目。");
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const payload = {
        title: form.title.value.trim(),
        source_url: form.source_url.value.trim(),
        track: form.track.value,
        summary: form.summary.value.trim(),
        takeaway_zh: form.takeaway_zh.value.trim(),
        takeaway_en: form.takeaway_en.value.trim(),
        relevance: Number(form.relevance.value),
        status: "submitted",
        submitted_by: state.session.user.id
      };
      const { data: savedCuration, error } = await client
        .from("frontier_curations")
        .upsert(payload, { onConflict: "source_url" })
        .select("id, title, source_url, track, summary, takeaway_zh, relevance")
        .single();
      let taskError = null;
      if (!error) {
        taskError = await createWorkflowTaskFromInsert({ data: savedCuration }, {
          sourceTable: "frontier_curations",
          taskType: "frontier",
          targetUrl: "/frontiers/",
          title: `前沿精选：${payload.title}`,
          summary: payload.takeaway_zh || payload.summary,
          sourceUrl: payload.source_url,
          publishHint: "判断是否适合进入前沿雷达人工精选、月度观察或实验室方向笔记。"
        });
      }
      showStatus(error ? error.message : taskError ? `前沿条目已保存，但审核任务创建失败：${taskError.message}` : "前沿精选已保存，并已进入审核队列。", error || taskError ? "error" : "success");
      if (!error) {
        form.reset();
        loadCurations();
        loadDashboardCounts();
      }
    });

    loadCurations();
  }

  async function hydrateProjects() {
    const form = $("#projectForm");
    const list = $("#projectList");
    const client = requireClient();

    async function loadProjects() {
      const { data, error } = await client
        .from("lab_outputs")
        .select("title, type, summary, status, created_at")
        .order("created_at", { ascending: false })
        .limit(12);
      renderRecords(list, data, error, "暂无项目或成果材料。");
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const payload = {
        title: form.title.value.trim(),
        type: form.type.value,
        summary: form.summary.value.trim(),
        status: form.status.value,
        submitted_by: state.session.user.id
      };
      const { data: savedOutput, error } = await client
        .from("lab_outputs")
        .insert(payload)
        .select("id, title, type, summary, status")
        .single();
      let taskError = null;
      if (!error && payload.status !== "private") {
        const taskType = taskTypeForOutput(payload.type);
        taskError = await createWorkflowTaskFromInsert({ data: savedOutput }, {
          sourceTable: "lab_outputs",
          taskType,
          targetUrl: taskTargetFor(taskType),
          title: `成果材料审核：${payload.title}`,
          summary: payload.summary,
          publishHint: "核对项目级别、论文出处、学生贡献、可公开边界和对外包装角度。"
        });
      }
      showStatus(error ? error.message : taskError ? `材料已保存，但审核任务创建失败：${taskError.message}` : "材料已保存，并按状态进入审核流。", error || taskError ? "error" : "success");
      if (!error) {
        form.reset();
        loadProjects();
        loadDashboardCounts();
      }
    });

    loadProjects();
  }

  function hydrateSettings() {
    $("#resetConfigButton")?.addEventListener("click", () => {
      localStorage.removeItem("maclab_console_config");
      window.location.reload();
    });
  }

  async function hydrateAudit() {
    const list = $("#auditList");
    const client = requireClient();
    const { data, error } = await client
      .from("content_audit_logs")
      .select("table_name, row_id, action, old_status, new_status, changed_at")
      .order("changed_at", { ascending: false })
      .limit(30);
    renderAuditLogs(list, data, error);
  }

  function renderRecords(container, rows, error, emptyText) {
    container.replaceChildren();
    if (error) {
      const node = document.createElement("div");
      node.className = "record-item";
      node.innerHTML = `<strong>无法读取</strong><p>${escapeHtml(error.message)}</p>`;
      container.appendChild(node);
      return;
    }
    if (!rows || rows.length === 0) {
      const node = document.createElement("div");
      node.className = "record-item";
      node.textContent = emptyText;
      container.appendChild(node);
      return;
    }
    rows.forEach((row) => {
      const node = document.createElement("article");
      node.className = "record-item";
      const title = row.title || row.organization || row.full_name || row.email || "Untitled";
      const meta = [row.category, row.type, row.scenario, row.role].filter(Boolean).join(" · ");
      node.innerHTML = `
        <strong>${escapeHtml(title)}</strong>
        ${row.status ? `<span class="record-status">${escapeHtml(labelStatus(row.status))}</span>` : ""}
        <span>${escapeHtml(meta)}</span>
        <p>${escapeHtml(row.summary || row.need_summary || row.github_username || row.created_at || "")}</p>
      `;
      container.appendChild(node);
    });
  }

  function renderPeople(container, rows, error) {
    container.replaceChildren();
    if (error) {
      const node = document.createElement("div");
      node.className = "record-item";
      node.innerHTML = `<strong>无法读取成员</strong><p>${escapeHtml(error.message)}</p>`;
      container.appendChild(node);
      return;
    }
    if (!rows || rows.length === 0) {
      const node = document.createElement("div");
      node.className = "record-item";
      node.textContent = isAdmin() ? "暂无成员记录。" : "成员列表仅对 owner/admin 开放。";
      container.appendChild(node);
      return;
    }

    rows.forEach((row) => {
      const node = document.createElement("article");
      node.className = "record-item record-item--person";
      const title = row.full_name || row.email || "Pending user";
      const actions = state.profile?.role === "owner"
        ? `
          <div class="person-actions" data-user-id="${escapeHtml(row.id)}">
            <select data-role>
              ${["student", "admin", "owner"].map((role) => `<option value="${role}" ${row.role === role ? "selected" : ""}>${role}</option>`).join("")}
            </select>
            <select data-status>
              ${["pending", "active", "suspended"].map((status) => `<option value="${status}" ${row.status === status ? "selected" : ""}>${status}</option>`).join("")}
            </select>
            <button type="button" data-save-person>更新</button>
          </div>
        `
        : "";
      node.innerHTML = `
        <strong>${escapeHtml(title)}</strong>
        <span>${escapeHtml([row.role, row.status, row.github_username].filter(Boolean).join(" · "))}</span>
        <p>${escapeHtml(row.updated_at || "")}</p>
        ${actions}
      `;
      container.appendChild(node);
    });

    container.querySelectorAll("[data-save-person]").forEach((button) => {
      button.addEventListener("click", async () => {
        const wrapper = button.closest("[data-user-id]");
        const userId = wrapper?.dataset.userId;
        const role = wrapper?.querySelector("[data-role]")?.value;
        const status = wrapper?.querySelector("[data-status]")?.value;
        if (!userId || !role || !status) return;
        const client = requireClient();
        const { error } = await client.from("profiles").update({ role, status }).eq("id", userId);
        showStatus(error ? error.message : "成员权限已更新。", error ? "error" : "success");
        if (!error) hydratePeople();
      });
    });
  }

  function renderReviewTasks(container, rows, error, emptyText) {
    container.replaceChildren();
    if (error) {
      const node = document.createElement("div");
      node.className = "record-item";
      node.innerHTML = `<strong>无法读取</strong><p>${escapeHtml(error.message)}</p>`;
      container.appendChild(node);
      return;
    }
    if (!rows || rows.length === 0) {
      const node = document.createElement("div");
      node.className = "record-item";
      node.textContent = emptyText;
      container.appendChild(node);
      return;
    }

    rows.forEach((row, index) => {
      const node = document.createElement("article");
      node.className = "record-item record-item--review";
      const meta = [
        labelTaskType(row.task_type) || row.track,
        labelStatus(row.status),
        row.priority ? `P${row.priority}` : null,
        row.relevance ? `R${row.relevance}` : null,
        row.metadata?.origin_label || null,
        row.created_at
      ].filter(Boolean).join(" · ");
      const detail = row.summary || row.takeaway_zh || row.target_url || row.source_url || "";
      const actions = isAdmin()
        ? `
          <div class="review-actions" data-record-id="${escapeHtml(row.id)}" data-row-index="${index}" data-table="${row.track ? "frontier_curations" : "content_tasks"}">
            <select data-status>
              ${REVIEW_STATUSES.map((status) => `<option value="${status}" ${row.status === status ? "selected" : ""}>${labelStatus(status)}</option>`).join("")}
            </select>
            <button type="button" data-save-review>更新状态</button>
            <button class="review-action-button" type="button" data-generate-draft>生成公开草稿</button>
          </div>
        `
        : "";
      node.innerHTML = `
        <strong>${escapeHtml(row.title)}</strong>
        <span>${escapeHtml(meta)}</span>
        <p>${escapeHtml(detail)}</p>
        ${safeUrl(row.source_url) ? `<a href="${escapeHtml(safeUrl(row.source_url))}" target="_blank" rel="noreferrer">打开来源</a>` : ""}
        ${actions}
      `;
      container.appendChild(node);
    });

    container.querySelectorAll("[data-save-review]").forEach((button) => {
      button.addEventListener("click", async () => {
        const wrapper = button.closest("[data-record-id]");
        const id = wrapper?.dataset.recordId;
        const table = wrapper?.dataset.table;
        const status = wrapper?.querySelector("[data-status]")?.value;
        const row = rows[Number(wrapper?.dataset.rowIndex)];
        if (!id || !table || !status) return;
        const client = requireClient();
        const { error } = await client.from(table).update({
          status,
          reviewed_by: state.session.user.id,
          ...(status === "public_ready" ? { published_at: new Date().toISOString() } : {})
        }).eq("id", id);
        const syncError = !error && table === "content_tasks" ? await syncLinkedSourceStatus(row, status) : null;
        showStatus(error ? error.message : syncError ? `任务已更新，但源记录同步失败：${syncError.message}` : "状态已更新，关联素材也已同步。", error || syncError ? "error" : "success");
        if (!error) renderView(state.view);
      });
    });

    container.querySelectorAll("[data-generate-draft]").forEach((button) => {
      button.addEventListener("click", async () => {
        const wrapper = button.closest("[data-row-index]");
        const row = rows[Number(wrapper?.dataset.rowIndex)];
        if (!row) return;
        const draft = await buildPublicDraft(row);
        showDraft(draft);
      });
    });
  }

  async function fetchLinkedSource(row) {
    const metadata = row?.metadata || {};
    const table = metadata.source_table;
    const id = metadata.source_id;
    if (!table || !id || !SOURCE_TABLES.has(table)) return {};
    const client = requireClient();
    const { data, error } = await client.from(table).select("*").eq("id", id).maybeSingle();
    if (error) {
      showStatus(`关联素材读取失败：${error.message}`, "error");
      return {};
    }
    return data || {};
  }

  async function buildPublicDraft(row) {
    const source = await fetchLinkedSource(row);
    const taskType = row.task_type || (row.track ? "frontier" : "public_update");
    const title = source.title || row.title || source.organization || "待发布内容";
    const summary = source.summary || source.need_summary || row.summary || row.takeaway_zh || "";
    const sourceUrl = source.source_url || row.source_url || "";
    const targetUrl = normalizePath(row.target_url, taskTargetFor(taskType));
    const today = new Date().toISOString().slice(0, 10);
    const label = labelTaskType(taskType);
    const origin = row.metadata?.origin_label || source.category || source.type || source.scenario || "";
    const publishHint = row.metadata?.publish_hint || "发布前请核对事实、署名、公开链接、敏感边界和中英文表达。";

    if (taskType === "news") {
      return [
        "# 官网新闻草稿",
        "",
        `目标页面：${targetUrl}`,
        `素材状态：${labelStatus(row.status)}`,
        `来源类型：${origin || "实验室动态"}`,
        "",
        "## 建议加入 `_data/staged_updates.yml` 的摘要",
        "",
        `- date: \"${today}\"`,
        "  label: \"Lab News\"",
        "  label_zh: \"实验室动态\"",
        `  title: \"${yamlText(title)}\"`,
        `  title_zh: \"${yamlText(title)}\"`,
        `  summary: \"${yamlText(summary)}\"`,
        `  summary_zh: \"${yamlText(summary)}\"`,
        `  url: \"${targetUrl}\"`,
        "",
        "## 新闻正文初稿",
        "",
        `### ${title}`,
        "",
        summary || "请补充新闻事实、参与人员、成果价值、合作单位和可公开链接。",
        "",
        sourceUrl ? `原始来源：${sourceUrl}` : "",
        "",
        `发布提示：${publishHint}`
      ].filter(Boolean).join("\n");
    }

    if (taskType === "frontier") {
      return [
        "# 前沿雷达精选草稿",
        "",
        `目标页面：${targetUrl}`,
        `方向：${source.track || row.track || "AI + Psychology"}`,
        `相关度：${source.relevance || row.relevance || "待评估"}`,
        "",
        `## ${title}`,
        "",
        summary || "请补充论文、产业动态或开源项目的核心贡献。",
        "",
        source.takeaway_zh || row.takeaway_zh ? `实验室观点：${source.takeaway_zh || row.takeaway_zh}` : "实验室观点：请说明它与普适心理计算、具身情感智能、多模态情感计算或行业场景的关系。",
        "",
        sourceUrl ? `原始来源：${sourceUrl}` : "",
        "",
        `发布提示：${publishHint}`
      ].filter(Boolean).join("\n");
    }

    if (taskType === "solution" || taskType === "case") {
      return [
        taskType === "solution" ? "# 行业方案草稿" : "# 能力案例草稿",
        "",
        `目标页面：${targetUrl}`,
        `素材状态：${labelStatus(row.status)}`,
        "",
        `## ${title}`,
        "",
        "### 场景问题",
        summary || "请补充合作方真实场景、用户角色、可用信号、现有痛点和预期价值。",
        "",
        "### MAC-Lab 可提供的能力",
        "- 多模态情感与身心状态感知",
        "- 人因与心智画像建模",
        "- 场景化评价、预警、反馈与干预流程",
        "- 软硬件一体化平台、试点验证和阶段性报告",
        "",
        "### 下一步合作路径",
        "先进行场景诊断和数据条件确认，再形成技术路线、试点方案、交付边界与联合成果规划。",
        "",
        `发布提示：${publishHint}`
      ].join("\n");
    }

    return [
      "# 公开内容草稿",
      "",
      `目标页面：${targetUrl}`,
      `任务类型：${label}`,
      `素材状态：${labelStatus(row.status)}`,
      "",
      `## ${title}`,
      "",
      summary || "请补充可公开摘要。",
      "",
      sourceUrl ? `原始来源：${sourceUrl}` : "",
      "",
      `发布提示：${publishHint}`
    ].filter(Boolean).join("\n");
  }

  function yamlText(value) {
    return String(value || "").replaceAll("\\", "\\\\").replaceAll('"', '\\"').replace(/\s+/g, " ").trim();
  }

  function showDraft(draft) {
    const panel = $("#publicDraftPanel");
    const output = $("#publicDraftOutput");
    const copyButton = $("#copyDraftButton");
    if (!panel || !output) return;
    output.value = draft;
    panel.hidden = false;
    panel.scrollIntoView({ behavior: "smooth", block: "start" });
    copyButton?.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(output.value);
        showStatus("公开草稿已复制，可以粘贴到公开 CMS 或 GitHub 内容文件中。", "success");
      } catch (_error) {
        output.select();
        showStatus("浏览器未允许自动复制，已选中草稿文本。", "error");
      }
    }, { once: true });
  }

  function renderAuditLogs(container, rows, error) {
    container.replaceChildren();
    if (error) {
      const node = document.createElement("div");
      node.className = "record-item";
      node.innerHTML = `<strong>无法读取日志</strong><p>${escapeHtml(error.message)}</p>`;
      container.appendChild(node);
      return;
    }
    if (!rows || rows.length === 0) {
      const node = document.createElement("div");
      node.className = "record-item";
      node.textContent = isAdmin() ? "暂无操作日志。" : "操作日志仅对 owner/admin 开放。";
      container.appendChild(node);
      return;
    }
    rows.forEach((row) => {
      const node = document.createElement("article");
      node.className = "record-item";
      node.innerHTML = `
        <strong>${escapeHtml(row.table_name)} · ${escapeHtml(row.action)}</strong>
        <span>${escapeHtml([row.old_status, row.new_status].filter(Boolean).join(" → "))}</span>
        <p>${escapeHtml(row.changed_at)} · ${escapeHtml(row.row_id || "")}</p>
      `;
      container.appendChild(node);
    });
  }

  function escapeHtml(value) {
    return String(value || "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  $("#setupForm")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    localStorage.setItem("maclab_console_config", JSON.stringify({
      supabaseUrl: form.url.value.trim(),
      supabaseAnonKey: form.anonKey.value.trim()
    }));
    window.location.reload();
  });

  $("#githubLoginButton")?.addEventListener("click", async () => {
    const client = requireClient();
    await client.auth.signInWithOAuth({
      provider: "github",
      options: { redirectTo: `${window.location.origin}/console/` }
    });
  });

  $("#emailLoginForm")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const client = requireClient();
    const email = event.currentTarget.email.value.trim();
    const { error } = await client.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: `${window.location.origin}/console/` }
    });
    alert(error ? error.message : "登录邮件已发送，请到邮箱点击 Magic Link。");
  });

  signOutButton?.addEventListener("click", async () => {
    if (state.supabase) await state.supabase.auth.signOut();
  });

  document.querySelectorAll(".console-nav button").forEach((button) => {
    button.addEventListener("click", () => renderView(button.dataset.view));
  });

  init().catch((error) => {
    setupPanel.hidden = false;
    authPanel.hidden = true;
    appPanel.hidden = true;
    console.error(error);
  });
})();
