---
layout: page
title: Notes
title_zh: 深度札记
description: Field notes from MAC-Lab on affective AI, psychological computing, embodied emotional intelligence, student training, and research translation.
description_zh: MAC-Lab 关于情感智能、心理计算、具身情感智能、学生培养与科研转化的深度札记。
permalink: /notes/
toggle: on
rank: 6.5
---

<div class="media-note">
  <h2><span class="lang-en">Field Notes for People Who Want to Understand the Route</span><span class="lang-zh">给真正想理解这条路线的人看的札记</span></h2>
  <p><span class="lang-en">MAC-Lab works in a space where algorithms, psychology, interaction, hardware, field validation, and public communication meet. These notes explain the lab's judgment, not just its outputs.</span><span class="lang-zh">MAC-Lab 做的是算法、心理、交互、硬件、场景验证和公共表达交汇处的问题。这些札记解释的是团队的判断方式，而不仅是成果列表。</span></p>
</div>

<div class="summary-band">
  <div><strong><span class="lang-en">Question</span><span class="lang-zh">问题意识</span></strong><span><span class="lang-en">What is the real problem behind the label?</span><span class="lang-zh">标签背后的真问题是什么？</span></span></div>
  <div><strong><span class="lang-en">System</span><span class="lang-zh">系统意识</span></strong><span><span class="lang-en">How does a model become a usable capability?</span><span class="lang-zh">模型如何变成可用能力？</span></span></div>
  <div><strong><span class="lang-en">People</span><span class="lang-zh">人的状态</span></strong><span><span class="lang-en">How can AI support people without simplifying them?</span><span class="lang-zh">AI 如何支持人而不简化人？</span></span></div>
  <div><strong><span class="lang-en">Route</span><span class="lang-zh">长期路线</span></strong><span><span class="lang-en">Why does a stable research spine matter?</span><span class="lang-zh">为什么长期主线很重要？</span></span></div>
</div>

<div class="project-list project-list--page">
  <article class="note-article">
    <div class="note-title">
      <h2><span class="lang-en">AI psychology is not emotion labeling</span><span class="lang-zh">AI 心理计算不是给情绪贴标签</span></h2>
      <p><span class="lang-en">The task is not to name a feeling. The task is to understand a changing person in a changing situation.</span><span class="lang-zh">这件事的核心不是给情绪命名，而是在变化的情境中理解一个正在变化的人。</span></p>
    </div>
    <div class="note-body">
      <p><span class="lang-en">Emotion labels are useful starting points, but they are too thin for real psychological computing. A person's state is shaped by time, context, personality, language, body signals, social relationships, task pressure, and the person's willingness to be understood.</span><span class="lang-zh">情绪标签有用，但不足以支撑真实的心理计算。人的状态由时间、环境、个性、语言、生理行为信号、社会关系、任务压力以及“是否愿意被理解”共同塑造。</span></p>
      <p><span class="lang-en">MAC-Lab treats Ubiquitous Psychological Computing as a full pipeline: sensing, temporal evidence, psychological profiling, risk assessment, early warning, and supportive feedback. The point is not to make the model sound certain. The point is to make uncertainty visible enough for responsible human-machine collaboration.</span><span class="lang-zh">MAC-Lab 把普适心理计算理解为一条完整链路：感知、时间证据、心理画像、风险评估、早期预警和支持性反馈。关键不是让模型显得很确定，而是让不确定性被看见，从而支持负责任的人机协同。</span></p>
      <figure class="note-visual note-visual--flow">
        <figcaption><span class="lang-en">From affect labels to psychological computing</span><span class="lang-zh">从情绪标签到心理计算</span></figcaption>
        <div class="note-flow">
          <span><b><span class="lang-en">Signals</span><span class="lang-zh">信号</span></b><small><span class="lang-en">speech · image · behavior · physiology</span><span class="lang-zh">语音 · 图像 · 行为 · 生理</span></small></span>
          <span><b><span class="lang-en">Context</span><span class="lang-zh">情境</span></b><small><span class="lang-en">time · task · relationship · environment</span><span class="lang-zh">时间 · 任务 · 关系 · 环境</span></small></span>
          <span><b><span class="lang-en">Judgment</span><span class="lang-zh">判断</span></b><small><span class="lang-en">profile · risk · uncertainty</span><span class="lang-zh">画像 · 风险 · 不确定性</span></small></span>
          <span><b><span class="lang-en">Support</span><span class="lang-zh">支持</span></b><small><span class="lang-en">warning · care · referral · feedback</span><span class="lang-zh">预警 · 关护 · 转介 · 反馈</span></small></span>
        </div>
      </figure>
      <div class="note-insights">
        <div><strong><span class="lang-en">What we refuse</span><span class="lang-zh">我们避免什么</span></strong><p><span class="lang-en">Overconfident diagnosis, shallow affect labels, and one-size-fits-all intervention.</span><span class="lang-zh">避免过度诊断、浅层情绪标签和一刀切干预。</span></p></div>
        <div><strong><span class="lang-en">What we build</span><span class="lang-zh">我们建设什么</span></strong><p><span class="lang-en">Systems that combine multimodal evidence, temporal modeling, human feedback, and deployable care scenarios.</span><span class="lang-zh">建设融合多模态证据、时间建模、人类反馈和可落地关护场景的系统。</span></p></div>
      </div>
    </div>
  </article>

  <article class="note-article">
    <div class="note-title">
      <h2><span class="lang-en">The difficult middle between a paper and a deployed system</span><span class="lang-zh">论文到系统之间，最难的是中间地带</span></h2>
      <p><span class="lang-en">The hard part begins after a model looks promising.</span><span class="lang-zh">模型看起来有效之后，真正困难的部分才开始。</span></p>
    </div>
    <div class="note-body">
      <p><span class="lang-en">A model can work in a benchmark and still fail in a classroom, hospital, cockpit, counseling room, or home environment. Deployment exposes sensor noise, missing data, user trust, privacy boundaries, device constraints, and maintenance cost.</span><span class="lang-zh">模型可以在基准数据上有效，却未必能在学校、医院、座舱、咨询场景或家庭环境中稳定运行。真实部署会暴露传感噪声、数据缺失、用户信任、隐私边界、设备约束和长期维护成本。</span></p>
      <p><span class="lang-en">This is where MAC-Lab's experience becomes distinctive. Research translation is treated as a design discipline: define the task, the data boundary, the user's role, the evaluation protocol, the feedback loop, and the handoff mechanism before chasing model complexity.</span><span class="lang-zh">这正是 MAC-Lab 的经验价值所在。科研转化本身是一种设计能力：先定义任务、数据边界、用户角色、评测流程、反馈闭环和交付机制，再谈模型复杂度。</span></p>
      <figure class="note-visual note-visual--bridge">
        <figcaption><span class="lang-en">The middle ground MAC-Lab works through</span><span class="lang-zh">MAC-Lab 反复穿越的中间地带</span></figcaption>
        <div class="note-bridge">
          <span><b><span class="lang-en">Paper</span><span class="lang-zh">论文</span></b><small><span class="lang-en">method, metric, novelty</span><span class="lang-zh">方法、指标、创新点</span></small></span>
          <span><b><span class="lang-en">Prototype</span><span class="lang-zh">样机</span></b><small><span class="lang-en">data flow, interface, scenario</span><span class="lang-zh">数据流、界面、场景</span></small></span>
          <span><b><span class="lang-en">Pilot</span><span class="lang-zh">试点</span></b><small><span class="lang-en">users, noise, trust, governance</span><span class="lang-zh">用户、噪声、信任、治理</span></small></span>
          <span><b><span class="lang-en">System</span><span class="lang-zh">系统</span></b><small><span class="lang-en">operation, maintenance, iteration</span><span class="lang-zh">运行、维护、迭代</span></small></span>
        </div>
      </figure>
      <div class="note-insights note-insights--three">
        <div><strong><span class="lang-en">Scientific discipline</span><span class="lang-zh">科学纪律</span></strong><p><span class="lang-en">Keep evidence, uncertainty, and evaluation visible.</span><span class="lang-zh">让证据、不确定性和评测机制保持可见。</span></p></div>
        <div><strong><span class="lang-en">Engineering judgment</span><span class="lang-zh">工程判断</span></strong><p><span class="lang-en">Make sensing, latency, devices, and data governance part of the design.</span><span class="lang-zh">把感知、延迟、设备和数据治理纳入设计。</span></p></div>
        <div><strong><span class="lang-en">Partner value</span><span class="lang-zh">合作价值</span></strong><p><span class="lang-en">Move beyond demos toward systems partners can trust and iterate.</span><span class="lang-zh">从演示样机走向合作方能够信任和持续迭代的系统。</span></p></div>
      </div>
    </div>
  </article>

  <article class="note-article">
    <div class="note-title">
      <h2><span class="lang-en">A good student competition should keep growing after the final</span><span class="lang-zh">好的竞赛项目，应该在比赛之后继续生长</span></h2>
      <p><span class="lang-en">A medal is a checkpoint. The better question is what the project becomes next.</span><span class="lang-zh">奖项是一个节点，更重要的是项目之后还能长成什么。</span></p>
    </div>
    <div class="note-body">
      <p><span class="lang-en">Competition is a powerful entry point for undergraduate and master's students because it compresses problem definition, coding, presentation, teamwork, and scenario thinking into one cycle. But the medal is not the end of the research value.</span><span class="lang-zh">竞赛对本科生和硕士生很有价值，因为它把问题定义、代码实现、表达汇报、团队协作和场景思维压缩到一个周期里。但奖项不是科研价值的终点。</span></p>
      <p><span class="lang-en">MAC-Lab tries to keep strong student work alive after the final: sharpen the research question, clean the system architecture, build reusable modules, write papers, protect intellectual property, and connect the work with a longer platform route.</span><span class="lang-zh">MAC-Lab 更看重竞赛之后的继续生长：把研究问题打磨清楚，把系统架构整理干净，把模块沉淀出来，把论文、专利、软著和长期平台路线连接起来。</span></p>
      <figure class="note-visual">
        <figcaption><span class="lang-en">How a student project compounds</span><span class="lang-zh">学生项目如何继续增值</span></figcaption>
        <div class="note-ladder">
          <span><b><span class="lang-en">Contest</span><span class="lang-zh">竞赛</span></b><small><span class="lang-en">problem, demo, teamwork</span><span class="lang-zh">问题、样机、团队</span></small></span>
          <span><b><span class="lang-en">Research</span><span class="lang-zh">科研</span></b><small><span class="lang-en">paper, dataset, method</span><span class="lang-zh">论文、数据、方法</span></small></span>
          <span><b><span class="lang-en">System</span><span class="lang-zh">系统</span></b><small><span class="lang-en">software, patent, module</span><span class="lang-zh">软著、专利、模块</span></small></span>
          <span><b><span class="lang-en">Platform</span><span class="lang-zh">平台</span></b><small><span class="lang-en">scenario, partner, career</span><span class="lang-zh">场景、合作、成长</span></small></span>
        </div>
      </figure>
      <div class="note-insights">
        <div><strong><span class="lang-en">For undergraduates</span><span class="lang-zh">对本科生</span></strong><p><span class="lang-en">Enter through projects, competitions, and real systems; learn to turn an idea into something that can be tested.</span><span class="lang-zh">从项目、竞赛和真实系统进入，学习把想法变成可验证的东西。</span></p></div>
        <div><strong><span class="lang-en">For graduate students</span><span class="lang-zh">对研究生</span></strong><p><span class="lang-en">Turn engineering momentum into sharper problems, stronger evidence, and publishable work.</span><span class="lang-zh">把工程冲劲转化为更清楚的问题、更扎实的证据和可发表成果。</span></p></div>
      </div>
    </div>
  </article>

  <article class="note-article">
    <div class="note-title">
      <h2><span class="lang-en">Embodied emotional intelligence is about situated response</span><span class="lang-zh">具身情感智能，核心是场景化回应能力</span></h2>
      <p><span class="lang-en">A good answer is not always a good response.</span><span class="lang-zh">回答正确，不等于回应合适。</span></p>
    </div>
    <div class="note-body">
      <p><span class="lang-en">The next step for AI is not only to answer correctly, but to respond appropriately in context. Robots, digital humans, smart cockpits, and companion agents must read multimodal signals, understand social timing, and express support with restraint.</span><span class="lang-zh">AI 的下一步，不只是回答正确，而是在具体情境中回应得合适。机器人、数字人、智能座舱和陪伴智能体，需要读取多模态信号，理解社会时机，并以克制、可信的方式表达支持。</span></p>
      <p><span class="lang-en">Embodied Emotional Intelligence connects perception, understanding, expression, action, safety, and long-term interaction memory. It is where affective computing meets physical presence, voice, gaze, motion, and responsibility.</span><span class="lang-zh">具身情感智能连接感知、理解、表达、行动、安全和长期交互记忆。它是情感计算与身体在场、语音、视线、动作和责任边界相遇的地方。</span></p>
      <figure class="note-visual note-visual--orbit">
        <figcaption><span class="lang-en">Capabilities that must move together</span><span class="lang-zh">必须协同演进的能力</span></figcaption>
        <div class="note-orbit" aria-hidden="true">
          <span class="note-orbit__core"><span class="lang-en">Situated<br>Response</span><span class="lang-zh">场景化<br>回应</span></span>
          <span><span class="lang-en">Perceive</span><span class="lang-zh">感知</span></span>
          <span><span class="lang-en">Understand</span><span class="lang-zh">理解</span></span>
          <span><span class="lang-en">Express</span><span class="lang-zh">表达</span></span>
          <span><span class="lang-en">Act</span><span class="lang-zh">行动</span></span>
          <span><span class="lang-en">Remember</span><span class="lang-zh">记忆</span></span>
          <span><span class="lang-en">Stay Safe</span><span class="lang-zh">安全</span></span>
        </div>
      </figure>
      <div class="note-insights">
        <div><strong><span class="lang-en">Typical carriers</span><span class="lang-zh">典型载体</span></strong><p><span class="lang-en">Robots, digital humans, smart cockpits, companion agents, and mind-body health terminals.</span><span class="lang-zh">机器人、数字人、智能座舱、陪伴智能体和身心健康终端。</span></p></div>
        <div><strong><span class="lang-en">Technical reliability</span><span class="lang-zh">技术可靠性</span></strong><p><span class="lang-en">In care, education, mobility, and health, emotional appropriateness becomes part of system reliability.</span><span class="lang-zh">在照护、教育、交通和健康场景中，情感合适性本身就是系统可靠性的一部分。</span></p></div>
      </div>
    </div>
  </article>

  <article class="note-article">
    <div class="note-title">
      <h2><span class="lang-en">Why a stable research spine beats short-lived topic chasing</span><span class="lang-zh">为什么长期主线比短期追题更有力量</span></h2>
      <p><span class="lang-en">The carriers change. The central question keeps accumulating.</span><span class="lang-zh">载体会变，但核心问题会不断积累。</span></p>
    </div>
    <div class="note-body">
      <p><span class="lang-en">MAC-Lab's route has moved from natural language processing to dialogue, affective computing, multimodal affective computing, ubiquitous psychological computing, and embodied emotional intelligence. The carriers changed; the core question stayed steady: how can AI understand and support human state?</span><span class="lang-zh">MAC-Lab 的路线从自然语言处理、人机对话、情感计算、多模态情感计算，延伸到普适心理计算和具身情感智能。载体在变化，核心问题一直稳定：AI 如何理解并支持人的状态？</span></p>
      <p><span class="lang-en">A stable spine lets students, systems, papers, patents, platforms, and partners accumulate around one expanding problem space. That accumulation is why the lab can speak to both frontier research and real industry needs without becoming either a paper factory or a pure outsourcing workshop.</span><span class="lang-zh">稳定主线让学生、系统、论文、专利、平台和合作伙伴围绕同一个不断扩展的问题空间持续积累。正因为有这种积累，实验室才能同时面向前沿科研和真实产业需求，而不是变成单一产出形态。</span></p>
      <figure class="note-visual note-visual--timeline">
        <figcaption><span class="lang-en">One route, expanding carriers</span><span class="lang-zh">一条主线，不断扩展的载体</span></figcaption>
        <div class="note-timeline">
          <span><b>2002</b><small><span class="lang-en">NLP</span><span class="lang-zh">自然语言处理</span></small></span>
          <span><b>2011</b><small><span class="lang-en">Dialogue + affective computing</span><span class="lang-zh">人机对话与情感计算</span></small></span>
          <span><b>2015</b><small><span class="lang-en">Multimodal + industrialization</span><span class="lang-zh">多模态与产业化</span></small></span>
          <span><b>2018</b><small><span class="lang-en">Mind-body guardian system</span><span class="lang-zh">智能心身守护系统</span></small></span>
          <span><b>Now</b><small><span class="lang-en">Ubiquitous psychological computing + embodied emotional intelligence</span><span class="lang-zh">普适心理计算与具身情感智能</span></small></span>
        </div>
      </figure>
      <div class="note-insights">
        <div><strong><span class="lang-en">Laboratory identity</span><span class="lang-zh">实验室身份</span></strong><p><span class="lang-en">The route makes the lab recognizable: NLP, HCI, affective computing, AI psychology, embodied interaction, and mind-body health are not scattered keywords.</span><span class="lang-zh">这条路线让实验室有辨识度：NLP、人机交互、情感计算、AI 心理、具身交互和身心健康不是散乱关键词。</span></p></div>
        <div><strong><span class="lang-en">Why it matters</span><span class="lang-zh">为什么重要</span></strong><p><span class="lang-en">Long-term focus makes collaboration easier because partners can see where the lab has depth, systems, students, and field experience.</span><span class="lang-zh">长期聚焦让合作更容易建立信任，因为合作方能看到实验室的深度、系统、学生梯队和场景经验。</span></p></div>
      </div>
    </div>
  </article>
</div>

<h2><span class="lang-en">Reading Pathways</span><span class="lang-zh">推荐阅读路径</span></h2>

<div class="card-grid card-grid--four">
  <article class="feature-card">
    <span>Students</span>
    <h3><span class="lang-en">Start from training</span><span class="lang-zh">从学生培养看起</span></h3>
    <p><span class="lang-en">Read the competition and student-growth note, then visit People and Join.</span><span class="lang-zh">先读竞赛与学生成长札记，再看团队培养和加入我们。</span></p>
  </article>
  <article class="feature-card">
    <span>Partners</span>
    <h3><span class="lang-en">Start from translation</span><span class="lang-zh">从转化逻辑看起</span></h3>
    <p><span class="lang-en">Read the paper-to-deployment note, then visit Projects and Contact.</span><span class="lang-zh">先读论文到系统之间的中间地带，再看科研项目和合作入口。</span></p>
  </article>
  <article class="feature-card">
    <span>Researchers</span>
    <h3><span class="lang-en">Start from frameworks</span><span class="lang-zh">从框架问题看起</span></h3>
    <p><span class="lang-en">Read the AI psychology and embodied intelligence notes, then visit Research and Frontiers.</span><span class="lang-zh">先读 AI 心理计算和具身情感智能札记，再看研究方向和前沿雷达。</span></p>
  </article>
  <article class="feature-card">
    <span>Media</span>
    <h3><span class="lang-en">Start from public value</span><span class="lang-zh">从公共价值看起</span></h3>
    <p><span class="lang-en">Read the stable-route note, then visit Media and the Media Kit.</span><span class="lang-zh">先读长期主线札记，再看媒体关注和传播资料。</span></p>
  </article>
</div>
