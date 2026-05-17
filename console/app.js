(function () {
  const state = {
    supabase: null,
    session: null,
    profile: null,
    view: "overview"
  };

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
    if (view === "overview") hydrateOverview();
    if (view === "profile") hydrateProfile();
    if (view === "news") hydrateNews();
    if (view === "people") hydratePeople();
    if (view === "projects") hydrateProjects();
    if (view === "settings") hydrateSettings();
  }

  function hydrateOverview() {
    const roleNode = viewMount.querySelector("[data-profile-role]");
    if (roleNode) roleNode.textContent = state.profile?.role || "pending";
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
      const { error } = await client.from("student_pages").upsert(payload, { onConflict: "owner_id" });
      showStatus(error ? error.message : "个人页面已保存。", error ? "error" : "success");
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
      const { error } = await client.from("lab_news").insert(payload);
      showStatus(error ? error.message : "新闻素材已提交。", error ? "error" : "success");
      if (!error) {
        form.reset();
        loadNews();
      }
    });

    loadNews();
  }

  async function hydratePeople() {
    const list = $("#peopleList");
    const client = requireClient();
    const query = client
      .from("profiles")
      .select("full_name, email, role, status, github_username, updated_at")
      .order("updated_at", { ascending: false })
      .limit(30);
    const { data, error } = await query;
    renderRecords(list, data, error, isAdmin() ? "暂无成员记录。" : "成员列表仅对 owner/admin 开放。");
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
      const { error } = await client.from("lab_outputs").insert(payload);
      showStatus(error ? error.message : "材料已保存。", error ? "error" : "success");
      if (!error) {
        form.reset();
        loadProjects();
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
      const title = row.title || row.full_name || row.email || "Untitled";
      const meta = [row.category, row.type, row.role, row.status].filter(Boolean).join(" · ");
      node.innerHTML = `
        <strong>${escapeHtml(title)}</strong>
        <span>${escapeHtml(meta)}</span>
        <p>${escapeHtml(row.summary || row.github_username || row.created_at || "")}</p>
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
