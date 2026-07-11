---
layout: page
title: News
title_zh: 实验室新闻
description: First-hand MAC-Lab updates, public news releases, and media coverage on Professor Xiao Sun's team.
description_zh: MAC-Lab 一手动态、公开新闻发布与孙晓教授团队相关媒体报道。
permalink: /news/
toggle: on
rank: 5
---

{% assign lab_sources = site.data.lab_sources %}

<div class="summary-band">
  <div><strong>Newsroom</strong><span><span class="lang-en">first-hand MAC-Lab announcements</span><span class="lang-zh">实验室一手动态发布</span></span></div>
  <div><strong>{{ lab_sources.generated_date_beijing | default: "2026-07-12" }}</strong><span><span class="lang-en">latest public-source refresh</span><span class="lang-zh">最新公开来源同步</span></span></div>
  <div><strong>{{ lab_sources.stats.hfut_faculty_blog_total | default: 56 }}</strong><span><span class="lang-en">public faculty-blog entries tracked</span><span class="lang-zh">教师博客公开动态条目</span></span></div>
  <div><strong>ORCID</strong><span><span class="lang-en">{{ lab_sources.stats.orcid_high_signal_items | default: 0 }} high-signal publication records in the source pool</span><span class="lang-zh">{{ lab_sources.stats.orcid_high_signal_items | default: 0 }} 条高信号成果进入来源池</span></span></div>
</div>

<div class="media-note">
  <h2><span class="lang-en">MAC-Lab Newsroom</span><span class="lang-zh">MAC-Lab 实验室新闻中心</span></h2>
  <p><span class="lang-en">MAC-Lab Newsroom publishes research progress, platform releases, student achievements, competitions, collaborations, and public communication. It brings together first-hand lab releases and media-radar coverage about MAC-Lab and Professor Xiao Sun.</span><span class="lang-zh">MAC-Lab 新闻中心发布科研进展、平台发布、学生成果、竞赛获奖、合作交流与社会传播动态，汇集实验室一手发布和媒体雷达发现的公开报道。</span></p>
  <p><a href="{{ '/frontiers/' | prepend: site.baseurl }}"><span class="lang-en">AI + Psychology Frontier Radar</span><span class="lang-zh">查看 AI + 心理前沿雷达</span></a></p>
</div>

<h2><span class="lang-en">Source-Synced Updates</span><span class="lang-zh">公开来源同步动态</span></h2>
<p class="muted"><span class="lang-en">This stream is refreshed by scheduled GitHub Actions from the HFUT faculty blog and public publication records. It is intentionally selective: official lab posts and high-signal publication venues are surfaced first.</span><span class="lang-zh">这一栏由 GitHub Actions 定时从合工大教师博客和公开论文记录同步。它会有选择地展示：优先呈现实验室官方动态和高信号发表来源。</span></p>

<div class="news-list news-list--compact">
  {% for item in lab_sources.publication_news_items limit:8 %}
    <article>
      <time>{{ item.published }}</time>
      <div>
        <h2><a href="{{ item.url }}"><span class="lang-en">{{ item.title }}</span><span class="lang-zh">{{ item.title_zh | default: item.title }}</span></a></h2>
        <p><span class="lang-en">{{ item.source }}{% if item.venue %} · {{ item.venue }}{% endif %} · {{ item.track }}</span><span class="lang-zh">{{ item.source }}{% if item.venue %} · {{ item.venue }}{% endif %} · {{ item.track_zh | default: item.track }}</span></p>
      </div>
    </article>
  {% endfor %}
</div>

<h2><span class="lang-en">Recent Media Coverage</span><span class="lang-zh">近期媒体报道</span></h2>

<div class="media-grid media-grid--page">
  <article>
    <span>2026-03-12 · China.com / People's Representative Daily</span>
    <h2><span class="lang-en">Decoding Emotion, Empowering Mind-Body Health</span><span class="lang-zh">解码情感，智惠身心</span></h2>
    <p><span class="lang-en">The feature presents Professor Xiao Sun's team as a long-term builder of embodied emotional interaction models and affective AI systems. It links the lab's trajectory from Chinese emotional corpora and affective robots to Ubiquitous Psychological Computing, EmoAda, PsyCoLLM, and embodied emotional intelligence.</span><span class="lang-zh">报道以“具身情感交互大模型突破之路”为主线，梳理团队从中文情感语料库、情感机器人，到普适心理计算、EmoAda、PsyCoLLM 和具身情感智能的长期建设路径。</span></p>
    <a href="https://digi.china.com/articles/20260312/202603121823261.html"><span class="lang-en">Read Story</span><span class="lang-zh">阅读全文</span></a>
  </article>
</div>

<h2><span class="lang-en">Lab Updates</span><span class="lang-zh">实验室动态</span></h2>
<p class="muted"><span class="lang-en">A curated stream of MAC-Lab progress across research platforms, publications, student training, competitions, standards, media visibility, and real-world applications.</span><span class="lang-zh">这里汇集 MAC-Lab 在科研平台、论文成果、学生培养、竞赛获奖、标准建设、媒体传播和成果转化方面的阶段性进展。</span></p>

<div class="news-list">
  <article>
    <time>2026-06-22</time>
    <div>
      <h2><span class="lang-en">Recent Publication Record Strengthens MAC-Lab's AI + Psychology Route</span><span class="lang-zh">近期论文成果继续夯实 AI + 心理与情感计算主线</span></h2>
      <p><span class="lang-en">Recent publication records add works in IEEE/ACM Transactions on Audio, Speech, and Language Processing, IEEE Transactions on Artificial Intelligence, IEEE Transactions on Fuzzy Systems, IEEE Transactions on Affective Computing, IEEE Transactions on Computational Social Systems, EMNLP, ICASSP, and IPMLP. These studies connect emotional support conversation, dialogue generation, facial expression recognition, empathy alignment, speech emotion recognition, psychological understanding with large language models, and health-behavior modeling.</span><span class="lang-zh">近期论文成果覆盖 IEEE/ACM Transactions on Audio, Speech, and Language Processing、IEEE Transactions on Artificial Intelligence、IEEE Transactions on Fuzzy Systems、IEEE Transactions on Affective Computing、IEEE Transactions on Computational Social Systems、EMNLP、ICASSP 和 IPMLP 等期刊会议，围绕情感支持对话、对话生成、表情识别、共情对齐、语音情绪识别、大模型心理理解与健康行为建模等方向展开，进一步强化实验室 AI + 心理与情感计算主线。</span></p>
      <a href="{{ '/publications/' | prepend: site.baseurl }}"><span class="lang-en">Selected Publications</span><span class="lang-zh">查看代表论文</span></a>
    </div>
  </article>
  <article>
    <time>2026-06-22</time>
    <div>
      <h2><span class="lang-en">Recent Conference Papers Extend Affective NLP and Multimodal Perception</span><span class="lang-zh">近期会议论文拓展情感 NLP、多模态感知与心理行为分析方向</span></h2>
      <p><span class="lang-en">Recent indexed conference papers include MultiAgentESC at EMNLP 2025 for LLM-based multi-agent emotional support conversation, Temporal-Frequency State Space Duality at ICASSP 2025 for efficient speech emotion recognition, DEFormer at ICASSP 2025 for low-light and dark-vision enhancement, and a social-psychological dual-dimensional clustering study at IPMLP 2025 for health-behavior analysis.</span><span class="lang-zh">近期可检索会议论文包括：EMNLP 2025 的 MultiAgentESC，面向大语言模型多智能体情感支持对话；ICASSP 2025 的 Temporal-Frequency State Space Duality，面向高效语音情绪识别；ICASSP 2025 的 DEFormer，面向低光图像与暗视觉增强；以及 IPMLP 2025 的社会-心理双维聚类建模研究，面向健康行为异质性分析。</span></p>
      <a href="{{ '/publications/' | prepend: site.baseurl }}"><span class="lang-en">Selected Publications</span><span class="lang-zh">查看代表论文</span></a>
    </div>
  </article>
  <article>
    <time>2026-05-29</time>
    <div>
      <h2><span class="lang-en">MAC-Lab Official Website Released</span><span class="lang-zh">实验室主页发布：sxhfut.github.io</span></h2>
      <p><span class="lang-en">The new MAC-Lab website presents research directions, industry solutions, academic impact, lab news, frontier sharing, media coverage, student training, and collaboration channels as a long-term bilingual window for the lab.</span><span class="lang-zh">实验室主页 sxhfut.github.io 正式发布，集中呈现研究方向、行业方案、学术影响、实验室新闻、前沿分享、媒体关注、团队培养与合作入口，作为 MAC-Lab 对外展示和持续更新的双语窗口。</span></p>
      <a href="https://faculty.hfut.edu.cn/sunxiao/zh_CN/article/198496/content/1774.htm#article"><span class="lang-en">Details</span><span class="lang-zh">查看详情</span></a>
    </div>
  </article>
  <article>
    <time>2026-05-29</time>
    <div>
      <h2><span class="lang-en">Joint HFUT-USTC Work Accepted by IEEE Transactions on Affective Computing</span><span class="lang-zh">与中国科学技术大学联合研究成果被 IEEE Transactions on Affective Computing 录用</span></h2>
      <p><span class="lang-en">The paper CausalSymptom studies causal disentangled representation learning for depression severity estimation from transcribed clinical interviews, strengthening the lab's research line in interpretable affective and psychological computing.</span><span class="lang-zh">论文 CausalSymptom: Learning Causal Disentangled Representation for Depression Severity Estimation on Transcribed Clinical Interviews 被 IEEE Transactions on Affective Computing 录用，面向临床访谈文本中的抑郁严重程度估计与因果解耦表示学习。</span></p>
      <a href="https://faculty.hfut.edu.cn/sunxiao/zh_CN/article/198496/content/1773.htm#article"><span class="lang-en">Details</span><span class="lang-zh">查看详情</span></a>
    </div>
  </article>
  <article>
    <time>2026-05-29</time>
    <div>
      <h2><span class="lang-en">Diffusion-Enhanced Dialogue Modeling Work Published in IEEE Transactions on Artificial Intelligence</span><span class="lang-zh">扩散增强多轮对话建模研究发表于 IEEE Transactions on Artificial Intelligence</span></h2>
      <p><span class="lang-en">Professor Xiao Sun's team published Modeling Latent Background Information in Multiturn Dialogues Using Diffusion Model in IEEE Transactions on Artificial Intelligence. The article appeared online as Early Access on 17 March 2026, studying how latent background information such as persona, scene, and conversational atmosphere can be modeled for more reasonable multi-turn dialogue generation.</span><span class="lang-zh">孙晓教授团队合作论文 Modeling Latent Background Information in Multiturn Dialogues Using Diffusion Model 发表在 IEEE Transactions on Artificial Intelligence，并于 2026 年 3 月 17 日以 Early Access 形式上线。论文围绕多轮对话中的人物、场景、氛围等潜在背景信息建模，利用扩散模型提升对话生成的合理性与丰富性。</span></p>
      <a href="https://faculty.hfut.edu.cn/sunxiao/zh_CN/article/198496/content/1772.htm#article"><span class="lang-en">Details</span><span class="lang-zh">查看详情</span></a>
    </div>
  </article>
  <article>
    <time>2026-05-29</time>
    <div>
      <h2><span class="lang-en">ERMoV Published in IEEE Transactions on Affective Computing</span><span class="lang-zh">ERMoV 情绪调节驱动对话情绪识别研究发表于 IEEE Transactions on Affective Computing</span></h2>
      <p><span class="lang-en">Xiao Sun, Xuxiong Liu, and Yueqi Jiang published ERMoV: Modeling Affective Mental States via Emotion Regulation for Dialogue Emotion Recognition in IEEE Transactions on Affective Computing, a leading journal in affective computing. The work models affective mental states through emotion-regulation mechanisms, moving dialogue emotion recognition from surface labels toward psychologically grounded state modeling.</span><span class="lang-zh">孙晓、刘旭雄、姜月琪合作论文 ERMoV: Modeling Affective Mental States via Emotion Regulation for Dialogue Emotion Recognition 发表在情感计算领域顶级期刊 IEEE Transactions on Affective Computing。论文通过情绪调节机制建模情感心理状态，使对话情绪识别从浅层标签识别进一步走向具有心理机制支撑的状态建模。</span></p>
      <a href="https://faculty.hfut.edu.cn/sunxiao/zh_CN/article/198496/content/1771.htm#article"><span class="lang-en">Details</span><span class="lang-zh">查看详情</span></a>
    </div>
  </article>
  <article>
    <time>2026-01-20</time>
    <div>
      <h2><span class="lang-en">Causal-ESC Published in IEEE/ACM Transactions on Audio, Speech, and Language Processing</span><span class="lang-zh">Causal-ESC 情感支持对话研究发表于 IEEE/ACM TASLP</span></h2>
      <p><span class="lang-en">Causal-ESC captures cause-and-effect dynamics in emotional support conversation. The work connects affective NLP, empathetic dialogue, and psychologically meaningful interaction modeling, and is closely aligned with the lab's MindTalk-style emotional support system direction.</span><span class="lang-zh">Causal-ESC 面向情感支持对话中的因果动态检测，连接情感 NLP、共情对话和具有心理意义的交互建模，与实验室 MindTalk 式情感支持系统方向高度一致。</span></p>
      <a href="https://doi.org/10.1109/TASLPRO.2025.3648885"><span class="lang-en">DOI</span><span class="lang-zh">论文链接</span></a>
    </div>
  </article>
  <article>
    <time>2025-08-28</time>
    <div>
      <h2><span class="lang-en">Multimodal Affective Computing and Intervention Technology Wins Silver Award at the 11th International Exhibition of Inventions</span><span class="lang-zh">普适场景多模态情感计算与干预技术获第十一届国际发明展览会银奖</span></h2>
      <p><span class="lang-en">MAC-Lab's technology for multimodal affective computing and intervention in ubiquitous scenarios was recognized with a silver award at the Belt and Road and BRICS skills-development and technology-innovation competition.</span><span class="lang-zh">实验室“普适场景中的多模态情感计算与干预技术”在 2025 年第十一届国际发明展览会·“一带一路”暨金砖国家技能发展与技术创新大赛中获得银奖。</span></p>
      <a href="https://faculty.hfut.edu.cn/sunxiao/zh_CN/article/198496/content/1691.htm#article"><span class="lang-en">Details</span><span class="lang-zh">查看详情</span></a>
    </div>
  </article>
  <article>
    <time>2025-08-28</time>
    <div>
      <h2><span class="lang-en">Paper Accepted by IEEE Transactions on Fuzzy Systems</span><span class="lang-zh">实验室论文被 IEEE Transactions on Fuzzy Systems 录用</span></h2>
      <p><span class="lang-en">The work studies uncertainty and complexity in human facial emotional expression, adding a new perspective for understanding facial affect in natural interaction.</span><span class="lang-zh">论文关注人类面部情感表达的不确定性与复杂性，从新的视角理解自然交互中的表情表达问题。</span></p>
      <a href="https://faculty.hfut.edu.cn/sunxiao/zh_CN/article/198496/content/1693.htm#article"><span class="lang-en">Details</span><span class="lang-zh">查看详情</span></a>
    </div>
  </article>
  <article>
    <time>2025-08-28</time>
    <div>
      <h2><span class="lang-en">Student-Guided Work Published in IEEE Transactions on Image Processing</span><span class="lang-zh">指导论文发表在 CCF A 类期刊 IEEE Transactions on Image Processing</span></h2>
      <p><span class="lang-en">UniEmoX, a cross-modal semantic-guided large-scale pretraining approach for universal scene emotion perception, was published in IEEE Transactions on Image Processing.</span><span class="lang-zh">指导论文 UniEmoX: Cross-modal Semantic-Guided Large-Scale Pretraining for Universal Scene Emotion Perception 发表在 IEEE Transactions on Image Processing，面向通用场景情绪感知与跨模态语义预训练。</span></p>
      <a href="https://faculty.hfut.edu.cn/sunxiao/zh_CN/article/198496/content/1692.htm#article"><span class="lang-en">Details</span><span class="lang-zh">查看详情</span></a>
    </div>
  </article>
  <article>
    <time>2025-08-28</time>
    <div>
      <h2><span class="lang-en">Lab Outcomes Covered by China Daily, China.com, Phoenix, and Other Media</span><span class="lang-zh">实验室成果被中国日报、中华网、中国网、凤凰网等媒体报道</span></h2>
      <p><span class="lang-en">The coverage strengthens public visibility for the lab's work on affective AI, psychological computing, and applied mind-body health systems.</span><span class="lang-zh">相关报道提升了实验室在情感智能、心理计算与身心健康转化系统方向的社会可见度。</span></p>
      <a href="https://faculty.hfut.edu.cn/sunxiao/zh_CN/article/198496/content/1695.htm#article"><span class="lang-en">Details</span><span class="lang-zh">查看详情</span></a>
    </div>
  </article>
  <article>
    <time>2025-08-28</time>
    <div>
      <h2><span class="lang-en">Lab Contributes to Group Standard for Healthy Residential Environments</span><span class="lang-zh">实验室代表学校参编健康住区环境相关团体标准</span></h2>
      <p><span class="lang-en">The lab's human-factor affective computing technology entered standardization work for intelligent systems supporting healthy residential environments.</span><span class="lang-zh">实验室普适场景人因情感计算技术应用于健康住区环境身心表征与保障，参与编写《健康住区环境保障智能系统设计技术导则》。</span></p>
      <a href="https://faculty.hfut.edu.cn/sunxiao/zh_CN/article/198496/content/1694.htm#article"><span class="lang-en">Details</span><span class="lang-zh">查看详情</span></a>
    </div>
  </article>
  <article>
    <time>2025-03-19</time>
    <div>
      <h2><span class="lang-en">Professional Service, Editorial Recognition, and High-Level Publications</span><span class="lang-zh">学会任职、编委任职与高水平论文持续推进</span></h2>
      <p><span class="lang-en">March 2025 updates highlighted Professor Sun's election as a CAAI council member, editorial-board recognition, and lab publications in PNAS Nexus, IEEE Transactions on Multimedia, and IEEE Transactions on Computational Social Systems.</span><span class="lang-zh">2025 年 3 月动态集中呈现孙晓教授当选中国人工智能学会理事、当选《智能系统学报》领域编委，以及实验室合作论文发表于 PNAS 子刊、IEEE Transactions on Multimedia 和 IEEE Transactions on Computational Social Systems 等进展。</span></p>
      <a href="https://faculty.hfut.edu.cn/sunxiao/zh_CN/article/198496/list/index.htm"><span class="lang-en">More Updates</span><span class="lang-zh">更多动态</span></a>
    </div>
  </article>
  <article>
    <time>2025-01-06</time>
    <div>
      <h2><span class="lang-en">Student Innovation Awards and CNKI Top 1% Recognition</span><span class="lang-zh">学生创新大赛奖项与知网高被引学者 TOP 1%</span></h2>
      <p><span class="lang-en">The lab reported multiple China International College Students' Innovation Competition awards and Professor Sun's selection as a 2024 CNKI Highly Cited Scholar in the top 1%.</span><span class="lang-zh">实验室获得多项中国国际大学生创新大赛奖项，孙晓教授入选 2024 中国知网高被引学者 TOP 1%。</span></p>
      <a href="https://faculty.hfut.edu.cn/sunxiao/zh_CN/article/198496/list/2.htm"><span class="lang-en">More Updates</span><span class="lang-zh">更多动态</span></a>
    </div>
  </article>
</div>
