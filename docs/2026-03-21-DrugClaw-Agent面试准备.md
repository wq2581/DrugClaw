# DrugClaw 项目面试准备手册

> 适用方向：大厂实习 / 校招 / 日常面试中的 Agent、RAG、多智能体、垂直领域 AI 系统岗位
>
> 使用方式：这不是 README 的重复版，而是一份“你怎么讲清楚这个项目”的备稿。建议先背熟前 3 节，再反复练后面的追问题。

---

## 1. 先用一句话讲清这个项目

**一句话版本：**

DrugClaw 是一个面向药物知识问答与证据综合的 Agentic RAG 系统，它不是简单“检索几段文本再让 LLM 总结”，而是通过 **任务规划、资源路由、代码型检索、证据结构化、图推理和反思补检索**，把药物相关问题拆开并用更合适的知识源回答。

**更面试化一点的说法：**

我做的是一个垂直领域的多智能体 RAG 系统，领域是药物智能。它的核心目标不是提高“对话流畅度”，而是提高 **答案的证据密度、可追溯性和专业性**。因为药物问题不像通用问答，很多时候需要跨数据库做交叉验证，比如靶点、适应症、不良反应、药物相互作用、说明书和药物基因组学信息，单纯做向量检索和摘要很容易答得浅、答得混。

---

## 2. 面试时怎么讲

### 2.1 30 秒版本

DrugClaw 是一个药物领域的 Agentic RAG 系统。它会先分析用户问题，选择合适的药物知识资源，再通过检索 Agent 和代码生成 Agent 去调用具体数据库，把结果结构化成 evidence 和 claim；如果问题复杂，还会走图构建、路径重排、答案生成和反思补检索这条链路。它的重点不是“像聊天机器人”，而是让药物答案更可靠、更有证据来源。

### 2.2 3 分钟版本

如果让我用一句话概括，我会说 DrugClaw 是一个 **垂直领域、多智能体、带图推理能力的药物问答系统**。

它解决的核心问题是：在药物领域，很多问题不能靠单一知识源或者普通 RAG 解决。比如一个药物的已知靶点、说明书信息、DDI 机制、不良反应和 PGx 限制，通常散落在不同数据库里，而且字段表达也不统一。普通 RAG 往往只是把几段文本拿回来总结，但药物问题更需要结构化证据和跨源验证。

所以 DrugClaw 的设计不是单一 Retriever，而是一个多阶段工作流。系统先做 **Planner**，把问题分类、识别实体、生成子问题、推荐技能；然后 **Retriever** 选择合适的资源；再交给 **Coder Agent** 针对具体资源写短代码去查询，这样每个数据库都能按自己的方式访问，而不是被硬塞进统一接口。检索结果会被标准化成 evidence item 和 claim。对于复杂问题，系统进一步用 **Graph Builder** 抽取实体关系三元组，构建证据子图，再通过 **Reranker** 找出高价值路径，由 **Responder** 生成回答，最后 **Reflector** 判断证据是否足够，不够的话会触发 Web search 做补充。

这套设计的关键价值在于三点：

1. 它是 **领域原生** 的，而不是在通用 RAG 上加一点 biomedical prompt。
2. 它支持 **按资源特性检索**，而不是把所有数据源强行抽象成同一种 API。
3. 它会显式处理 **证据充分性**，而不是检索完一次就盲目回答。

### 2.3 10 分钟版本

10 分钟版本建议按下面顺序讲：

1. 先讲业务问题：为什么药物问答比普通 QA 难。
2. 再讲系统目标：提高答案的准确性、证据性、可追溯性。
3. 然后讲架构分层：CLI / Orchestration / Agents / Skills / Evidence / Logging。
4. 再讲一次 query 的完整执行链路。
5. 重点讲 3 个关键设计：
   - 为什么要有 resource registry
   - 为什么要有 code agent
   - 为什么要有 reflector 和 web fallback
6. 最后讲 trade-off、局限和下一步优化。

如果时间很紧，最值得展开的是第 5 点。

---

## 3. 这个项目到底在解决什么问题

### 3.1 普通 RAG 在药物场景下的问题

你可以直接这样答：

> 药物领域的问题比通用问答更强依赖结构化证据。很多答案需要跨多个异构知识源验证，而且不同资源的粒度、接口、字段、可信度和更新频率差异都很大。如果只是“召回文本块 + LLM 总结”，很容易出现答案流畅但证据很薄，或者把机制、靶点、疾病、细胞系这些概念混在一起。

DrugClaw 的设计动机本质上来自 4 个痛点：

1. **资源异构**  
   有 REST API、CLI 工具、本地数据文件、数据集等多种访问模式。

2. **问题类型多样**  
   药物靶点、ADR、DDI、labeling、repurposing、PGx 等问题需要的资源和推理路径不同。

3. **答案不能只靠文本相似度**  
   药物问答很多时候需要明确关系类型，比如 `drug -> inhibits -> target`，而不是只有一段“看起来相关”的文本。

4. **不能默认一次检索就够**  
   某些问题需要先用结构化资源建立主结论，再用 web 或文献检索补缺口。

### 3.2 为什么不用“统一接口 + 单 Retriever”

这是一个很容易被追问的点。

你的回答可以是：

> 因为统一接口会牺牲资源表达力。药物数据库不是同质化数据源，有的强在结构化关系，有的强在说明书文本，有的强在机制路径，有的强在实验 bioactivity。如果强行把所有资源压成同一个 schema，短期上层代码会更整齐，但长期会丢失资源独有能力。DrugClaw 更强调“按资源原生方式检索，再在上层做证据统一”。

这就是为什么项目里有 `SkillRegistry` 和 `ResourceRegistry`，同时又保留了 Code Agent。

---

## 3.3 面试里怎么回答 Why DrugClaw

这是一个高频问题，而且很容易答得空。你不要回答成：

> 因为 Agent 很火，所以我做了一个 Agent 项目。

更好的回答方式是：

> 我做 DrugClaw 的原因，不是单纯想做一个“会搜资料的 AI”，而是我发现药物问题天然不适合被粗暴地当成通用 RAG 问答来处理。药物领域的问题，经常需要跨数据库验证、明确证据出处、区分结构化关系和自由文本、处理资源间冲突，还要能解释为什么会得出这个结论。普通助手很多时候能给出一个“看起来像对的答案”，但经不起继续追问。DrugClaw 想解决的就是这个 gap: 把药物问题从“文本检索 + 总结”升级成“面向证据和推理链的 agentic workflow”。

你也可以更工程一点地说：

> Why DrugClaw，本质上是 because generic AI assistants are too broad, and single databases are too narrow. 我们需要的是一个位于二者之间的系统：它既能像 agent 一样做任务拆解、资源路由和工具调用，又能像专业科研系统一样保留证据来源、资源差异和推理链。

这句话很好用，因为它直接把项目放在了一个明确的位置上：

- 不是通用聊天助手
- 不是单一数据库前端
- 不是纯文献综述工具
- 而是一个 **面向复杂药物问题的 agentic evidence system**

### 3.4 为什么“药物问题”特别适合做这种 Agent 系统

这是你可以主动拔高的地方。

药物问题相比很多普通问答场景，有几个天然特点：

1. **问题不是单跳的**

比如“一个药的已知靶点是什么”看起来简单，但真正要答好，常常要区分：

- primary target 还是 off-target
- 结构化数据库证据还是文献叙述
- 实验活性还是临床意义
- 单一来源结论还是多源交叉验证

2. **知识源非常异构**

药物领域里常见的信息源包括：

- 药物知识库
- 靶点和 bioactivity 数据库
- label / prescribing 信息
- ADR / pharmacovigilance 资源
- DDI 资源
- 文献和临床试验

这些源的访问方式、字段结构、证据粒度都不同，所以你很难用一个统一 schema 干净地包住全部能力。

3. **错误容忍度更低**

在药物领域，“大致差不多”往往不够。一个回答如果没说清来源、证据强度和局限，表面看起来很流畅，实际并不适合研究或高要求分析场景。

4. **问题经常需要“检索 + 组织 + 判断是否足够”**

这正好对应了 Agent 系统最适合发挥价值的三个地方：

- 先规划任务
- 再选择和调用工具
- 最后做自我评估和必要补检索

所以你可以说：

> 我认为药物问答不是简单的信息查找问题，而更像一个需要 evidence workflow 的复杂任务。这也是它很适合用 agentic system，而不是只用一个大模型 prompt 解决的原因。

### 3.5 DrugClaw 面向哪些用户群体

这一节不要答成“所有人都能用”。越泛，越显得没想清楚。

更合理的说法是：DrugClaw 面向的是 **对药物问题有结构化追问需求的人**，而不是普通泛用户。

可以分成 4 类：

#### 3.5.1 药物研发 / 生物医药研究人员

典型需求：

- 查 drug-target evidence
- 看机制、重定位、路径和多源证据
- 快速缩小检索面，而不是手工翻多个数据库

他们最看重的是：

- 是否能跨资源
- 是否有明确 evidence source
- 是否能保留结构化关系

#### 3.5.2 医学信息学 / 生信 / 药学方向学生和研究生

典型需求：

- 作为科研辅助工具
- 快速理解某个药物相关问题的证据图景
- 把分散资源组织成更容易讲述和复盘的答案

他们最看重的是：

- 学习曲线不要太高
- 能快速拿到较完整的 reasoning chain
- 输出可以继续加工成报告或分析笔记

#### 3.5.3 需要做药物情报分析的工程型用户

比如：

- 做 biomedical AI / agent 的工程师
- 做药物知识系统、检索系统、RAG 平台的人

这类用户不一定把 DrugClaw 当最终产品，而可能把它当：

- 架构参考
- 能力底座
- 或可复用的 domain-specific agent framework

他们最看重的是：

- 系统设计是否清晰
- 模块是否可替换
- 资源注册和执行链路是否工程化

#### 3.5.4 高要求的信息核验用户

比如临床研究支持、医学情报整理、药物分析等场景中的专业用户。

他们最看重的是：

- 能不能交代来源
- 能不能解释资源之间的差异
- 能不能知道系统什么时候“不够确定”

### 3.6 它不主要面向谁

这个反而很加分，因为说明你知道边界。

DrugClaw **不主要面向**：

1. 普通日常问答用户  
   他们更适合用通用助手。

2. 只想查单一药品说明书的人  
   这种场景直接用单一高质量数据库可能更高效。

3. 需要直接临床决策支持的最终场景  
   DrugClaw 更像 research / analysis / evidence synthesis 系统，不应该被表述成已可直接替代正式临床决策系统。

一句话说就是：

> 它更适合“需要跨源证据和推理链的人”，而不是“只想快问快答的人”。

### 3.7 竞品怎么看：不要硬找单一对标

这一点非常关键。

DrugClaw 不太像一个能被单独拿去和某个现成产品完全一一对应的项目。更准确的说法是：

> DrugClaw 的竞品不是单一产品，而是三类替代方案。

#### 第一类：通用 AI 搜索 / 通用 AI 助手

典型例子：

- ChatGPT / Deep Research
- Perplexity

这类产品的优势是：

- 交互自然
- 覆盖面广
- 对开放问题和时效性问题友好

但它们的局限也很明显：

- 不是药物原生设计
- 对异构药物资源的结构差异感知不强
- 很难稳定表达“这个结论到底来自哪些资源、是否可交叉验证”
- 对结构化药物关系和专业 evidence workflow 支持不够强

面试里的讲法：

> 通用 AI 助手的强项是 broad coverage，不是 domain-native evidence orchestration。

#### 第二类：科研 / 文献综述型 AI 工具

典型例子：

- Elicit
- 其他 literature review / scientific copilot 工具

这类产品的优势是：

- 对论文发现、文献综述和研究问题梳理更友好
- 很适合“这个方向有哪些研究”之类的问题

局限是：

- 更偏 literature-centric
- 不一定擅长调动药物数据库、标签库、知识库、DDI/ADR 资源
- 不一定强调 structured drug relation 和 multi-resource validation

面试讲法：

> 这类工具更像“研究文献副驾驶”，而 DrugClaw 更强调“围绕药物问题调用多类证据源并综合推理”。

#### 第三类：专业数据库 / 专业情报平台

典型例子：

- DrugBank
- Open Targets Platform
- BenchSci ASCEND
- 以及单独的 ChEMBL、DGIdb、DailyMed、openFDA 等资源

这类系统或数据库的优势是：

- 单点能力强
- 某个子任务上数据质量很高
- 在自己的领域内往往更权威、更深入

它们的局限是：

- 往往只覆盖问题的一部分
- 用户需要自己跨系统切换和整合
- 不一定把“问答、检索、证据组织、反思补检索”串成统一工作流

面试讲法：

> 单一数据库的强项是深，不是横向协调；DrugClaw 的价值不是替代这些资源，而是把它们编排起来。

### 3.8 如果面试官提到 ToolUniverse 和 Biomni，该怎么比

这两个名字很值得准备，因为它们都更接近“Agent for Science / Biomedicine”的前沿系统，不是普通聊天产品。

但你不能把它们和 DrugClaw 说成简单的同类竞品。更准确的看法是：

- `ToolUniverse` 更像 **科学工具生态和 AI scientist 基础设施**
- `Biomni` 更像 **通用生物医学 AI agent**
- `DrugClaw` 更像 **聚焦药物问题的垂直 agentic evidence workflow**

也就是说，这三者的抽象层级并不完全一样。

#### 3.8.1 ToolUniverse 怎么看

你可以把 ToolUniverse 理解成：

> 一个把大量科学工具统一注册、统一调用、统一协议化的生态底座，目标是把任意 LLM 变成能调用科学工具的 AI scientist。

它的关键词是：

- 统一协议
- 大量科学工具
- 通用科学工作流
- ecosystem / infrastructure

从这个角度看，它更像：

- tool layer
- platform layer
- AI scientist construction kit

而不是一个专门围绕“药物问题怎么回答”优化的系统。

所以和 DrugClaw 的区别在于：

1. **抽象层级不同**  
   ToolUniverse 更偏“给 agent 接工具的生态底座”；DrugClaw 更偏“围绕药物问题已经设计好的 agent workflow”。

2. **领域范围不同**  
   ToolUniverse 面向的是更广义的科学任务；DrugClaw 明显更聚焦药物 intelligence。

3. **优化目标不同**  
   ToolUniverse 更强调 interoperability、tool discovery 和 composability；DrugClaw 更强调 query planning、drug-native resource routing、evidence structuring 和 answer synthesis。

4. **系统边界不同**  
   ToolUniverse 更像“把工具世界接起来”；DrugClaw 更像“在药物场景下把问答链路跑完整”。

一句话总结：

> 如果说 ToolUniverse 解决的是“AI scientist 如何拥有一个统一可调用的科学工具宇宙”，那 DrugClaw 解决的是“在药物这个高密度专业问题上，如何把检索、证据和回答组织成稳定工作流”。

#### 3.8.2 Biomni 怎么看

Biomni 更接近一个你真正应该认真对比的对象，因为它不是单纯工具平台，而是一个明确的 **general-purpose biomedical AI agent**。

你可以这样理解：

> Biomni 的目标是覆盖广泛的生物医学研究任务，包括生信分析、数据库查询、代码执行、实验设计和多种生物医学任务场景，它更像一个“通用 biomedical research agent”。

和 DrugClaw 相比，它的差异主要有：

1. **任务范围更广**  
   Biomni 不只关心药物，还覆盖更宽的 biomedical action space。

2. **环境更重**  
   从公开资料看，Biomni 集成了大量工具、软件和数据库，更像一个大而全的 biomedical agent environment。

3. **目标更像 AI biologist / biomedical copilot**  
   它强调的是 general-purpose biomedical autonomy，而不是只围绕药物问答和证据综合。

这意味着 DrugClaw 和 Biomni 的关系更像：

- Biomni 追求 **广谱 biomedical agent**
- DrugClaw 追求 **高聚焦 drug-native agent**

所以 DrugClaw 的优势不是“覆盖更大”，而是“焦点更准”。

你可以在面试里这样说：

> 如果把 Biomni 看作一个通用生物医学 AI agent，那么 DrugClaw 更像它在药物 intelligence 方向上的垂直化特化版本。前者强调覆盖广、动作空间大、任务类型多；后者强调针对药物问题把资源组织、证据表达和推理链打磨得更细。

#### 3.8.3 DrugClaw 相对 ToolUniverse 的优势和短板

优势：

- 对药物问题的 task design 更聚焦
- 不只是工具接入，还包含完整的问答链路
- 更强调 evidence、claim、final answer 这些面向回答质量的中间层
- 对药物资源的 task-specific routing 更明确

短板：

- 工具生态规模和通用性不如 ToolUniverse
- 更像垂直解法，不是通用科学工具平台
- 可扩展到其他科学场景的能力不如 ToolUniverse 自然

#### 3.8.4 DrugClaw 相对 Biomni 的优势和短板

优势：

- 问题边界更清晰，系统目标更集中
- 更适合把 drug-target、ADR、DDI、labeling、PGx 等药物任务讲成一个 coherent workflow
- 对“答案为什么成立”的表达更适合做药物问答型 demo 和面试讲解

短板：

- 覆盖的 biomedical action space 明显更小
- 不像 Biomni 那样天然面向更广的研究任务和复杂分析环境
- 如果面试官更重视“通用 biomedical AI scientist”，Biomni 的叙事会更大

#### 3.8.5 一个很好用的总括回答

你可以直接背这一段：

> 我会把 ToolUniverse、Biomni 和 DrugClaw 放在三个不同层级看。ToolUniverse 更像科学 Agent 的工具生态底座，它解决的是海量科学工具怎么被统一接入和调用；Biomni 更像通用生物医学 AI agent，它追求的是更广泛的 biomedical action space；DrugClaw 则更聚焦药物 intelligence，强调围绕药物问题做资源路由、证据结构化、图推理和反思补检索。也就是说，DrugClaw 不一定比它们“更大”，但它更像一个在药物问题上打磨得更尖、更清楚、更适合讲清楚设计取舍的系统。

#### 3.8.6 如果面试官进一步问：那 DrugClaw 还有什么成立空间？

你可以答：

> 我觉得成立空间主要来自 specialization。通用平台和通用 biomedical agent 一定很重要，但它们未必会把药物问题里最细的证据组织和回答质量当成一等公民。DrugClaw 的价值就在于把这个垂直问题做深：不只是能调用工具，而是能围绕 drug-native query 把 planning、retrieval、evidence、claim、response 和 reflection 串成更稳定的闭环。

### 3.9 如果面试官说：DrugClaw 不就是小号 Biomni / ToolUniverse？

这是一个很典型、也很有攻击性的追问。重点不是硬顶回去，而是把“规模更大”与“问题定义更清楚”区分开。

你不要回答成：

> 不是不是，我们也很厉害。

更好的回答方式是：

> 我觉得它们不是简单的大号和小号关系，而是抽象层级和优化目标不同。ToolUniverse 解决的是科学工具如何被统一接入和组合，Biomni 解决的是更广谱的 biomedical agent 问题，而 DrugClaw 解决的是药物 intelligence 这个更窄但更深的子问题。也就是说，它不是在所有维度上和它们正面竞争，而是在 specialization 上做取舍。

### 3.9.1 一个最稳的回答框架

你可以按这 4 句来答：

1. **先承认对方更“大”**

> 如果看工具规模、任务范围和系统野心，ToolUniverse 和 Biomni 的叙事肯定更大。

2. **再指出“大”不等于“解决了我的问题”**

> 但我的问题定义并不是“做一个最通用的科学 agent”，而是“把药物问题的检索、证据和回答组织成一个更稳定的工作流”。

3. **强调 specialization 的价值**

> 对药物问题来说，很多难点来自资源异构、证据表达和推理链，而不是单纯多接几个工具就自然解决。

4. **最后落回 DrugClaw 的成立点**

> 所以 DrugClaw 的成立空间不来自规模，而来自对药物问题的垂直打磨和更清晰的系统边界。

### 3.9.2 如果对方说：那不就是 scope 更小而已？

你可以这么接：

> 对，scope 确实更小，但这不是弱点本身。很多时候 scope 收窄是为了把关键问题真正做深。DrugClaw 的目标不是证明我能覆盖最多任务，而是证明在药物问题上，agent system 应该如何设计 planning、resource routing、evidence structuring 和 reflection。这种垂直化本身就是一种研究和工程选择。

### 3.9.3 如果对方说：那直接在 Biomni 上加几个药物工具不就行了？

你可以答：

> 表面上看像是“多接几个药物工具”，但真正难的地方不只是工具接入，而是围绕药物任务建立合适的 query taxonomy、skill routing、evidence model、claim cleaning 和 answer policy。也就是说，问题不只是有没有这些工具，而是系统是否把 drug-native reasoning 当成核心设计对象。

这句里的几个词很重要：

- query taxonomy
- skill routing
- evidence model
- claim cleaning
- answer policy

它们能把你的回答从“泛泛争论”拉回到系统设计。

### 3.9.4 如果对方说：ToolUniverse 已经是统一工具协议了，你这不就是重复造轮子？

你可以答：

> 如果目标是做通用科学工具基础设施，那 ToolUniverse 的路线当然更合理。但 DrugClaw 的目标不是只做统一协议层，而是做一个面向药物问题的 end-to-end workflow。统一协议解决的是工具怎么接，DrugClaw 还想解决的是：药物问题怎么分类、资源怎么选、证据怎么表达、什么时候该继续补检索。这些不完全是同一层的问题。

### 3.9.5 如果对方说：那 Biomni 看起来更像真正的前沿系统，DrugClaw 会不会太像垂直 demo？

这是很难的问题，但答好了很加分。

你可以这样说：

> 这是一个合理质疑。我会承认 Biomni 的叙事更大，也更像通用 biomedical AI scientist 的方向。但我不觉得垂直就等于 demo。相反，很多系统价值恰恰来自把一个高密度问题做透。DrugClaw 如果能清楚回答“药物问题为什么和普通 RAG 不一样、为什么要有 planner/coder/reflector、为什么要有 evidence 和 claim 这些中间层”，那它就不是一个随便堆工具的 demo，而是一个有明确问题定义和设计取舍的垂直系统。

这段话很重要，因为它把“垂直”从短板转成了方法论。

### 3.9.6 一个简短但杀伤力比较强的版本

你可以直接背这一段：

> 我同意 Biomni 和 ToolUniverse 在规模和通用性上都更大，但 DrugClaw 的目标本来就不是做更大的系统，而是做更清楚的系统。它聚焦药物问题，把最关键的设计点放在 query planning、resource routing、evidence modeling 和 reflection 上。换句话说，它不是大一统平台，而是一个用垂直问题去验证 agent workflow 设计是否成立的系统。

### 3.10 可以直接背的竞品分层回答

你可以直接背下面这段：

> 我不会把 DrugClaw 的竞品只理解成某一个产品。更准确地说，它面对的是三类替代方案：第一类是 ChatGPT、Perplexity 这类通用 AI 助手，它们很强，但不够 drug-native；第二类是 Elicit 这类科研综述工具，它们偏文献工作流，不一定擅长调用结构化药物资源；第三类是 DrugBank、Open Targets 甚至 BenchSci 这类专业平台，它们在单点上很深，但不一定负责跨资源的 agentic orchestration。DrugClaw 的定位恰好卡在三者之间：它想保留 agent 的灵活性、专业资源的深度，以及 evidence synthesis 的可追溯性。

### 3.11 DrugClaw 相对竞品的核心优势

这部分建议你不要说太多花哨词，抓住 5 点就够了。

#### 优势 1：drug-native，而不是通用问题硬套专业 prompt

它从问题类型、资源组织、证据表达上都假设“这是药物问题”，而不是把药物问答当成通用问答的一个子集。

这意味着它在设计上会天然考虑：

- target lookup
- ADR
- DDI
- labeling
- pharmacogenomics
- repurposing

而不是事后再补丁式适配。

#### 优势 2：不是单一知识源，而是多资源编排

相对单一数据库前端，DrugClaw 的优势不在于某个数据库更全，而在于：

- 能同时动用多个资源
- 能处理资源状态和依赖
- 能把多源结果转成统一 evidence 视图

#### 优势 3：不是纯文本总结，而是 evidence-aware workflow

很多系统的最终输出只有一段话。

DrugClaw 的中间层更明确：

- retrieval result
- evidence item
- claim
- final answer

这使得它更适合被 debug、评估和复盘。

#### 优势 4：保留资源原生能力，而不是强行统一接口

Code Agent + fallback retrieve 这套设计，让它既能灵活调用不同资源，又不会因为过度抽象而丢掉资源特异性。

#### 优势 5：有 reflection / fallback，而不是一轮检索就结束

这是它相对很多普通 RAG demo 最明显的进步点之一：

- 先回答
- 再判断证据够不够
- 不够再继续补

这种机制更接近你希望真实 Agent 系统具备的行为。

### 3.12 但它的优势不是“全面碾压”

这是成熟表达。

你可以这样说：

> DrugClaw 的优势不在于它在每个单点上都胜过所有竞品，而在于它把多资源药物问答里最难的那部分，也就是资源路由、证据组织、推理链和反思补检索，放到了系统中心。相应地，它也会承担更多复杂度，比如链路更长、调试更难、时延更高。

这句话非常适合面试，因为它既强调了优势，也承认了代价。

### 3.13 如果面试官问：为什么不是直接用 DrugBank 或 Open Targets？

你可以直接答：

> 因为真实药物问题经常不是某一个数据库能单独讲完的。DrugBank 或 Open Targets 本身都很强，但一个偏结构化药物知识和 target 信息，一个偏 target-disease association 和优先级分析。DrugClaw 不是想取代它们，而是把这类资源编排到同一个 query workflow 里，让用户不用自己在多个工具之间来回切换，再手工整合证据。

### 3.14 如果面试官问：为什么不是直接用 Perplexity / ChatGPT？

你可以这样答：

> 因为通用 AI 助手的强项是广覆盖和自然交互，但药物问题更在乎 evidence provenance、resource specificity 和 reasoning trace。DrugClaw 的设计重点恰好是这三个维度。它不一定比通用助手更适合所有问题，但对复杂药物问题，它更强调答案为什么成立，而不只是答案是什么。

### 3.15 你可以直接背的一段“定位总结”

> 我对 DrugClaw 的定位理解是：它不是通用 AI 助手，也不是单一数据库门户，而是一个面向复杂药物问题的 agentic evidence system。它试图解决的核心问题，不是“让 AI 更会说”，而是“让药物问题的答案更有来源、更能交叉验证、更能说明推理链”。这也是它和通用 research assistant、文献综述工具、单点数据库工具之间最大的差别。

---

## 4. 系统架构总览

你可以把 DrugClaw 理解成 6 层：

### 4.1 入口层

- `drugclaw/cli.py`
- `drugclaw/__main__.py`

作用：

- 提供 `drugclaw run/demo/doctor/list`
- 决定默认体验入口
- 管理 `--mode`、`--resource-filter`、`--show-plan`、`--debug-agents` 等开关

设计动机：

- 面试里可以强调，项目不是只有研究原型，也考虑了 **可体验性** 和 **可运维性**
- `doctor` 命令很像真实工程里的环境健康检查，而不是只给一段 notebook

### 4.2 编排层

- `drugclaw/main_system.py`

作用：

- 这里是整个系统的总调度器
- 用 LangGraph 组织节点和条件路由
- 支持 `GRAPH`、`SIMPLE`、`WEB_ONLY` 三种模式

设计动机：

- 把“一个 query 怎么流经多个 agent”显式化
- 避免把多智能体流程写成一大段 if-else
- 让系统既能支持完整图推理链路，也能支持轻量直达链路

### 4.3 Agent 层

- `agent_planner.py`
- `agent_retriever.py`
- `agent_coder.py`
- `agent_graph_builder.py`
- `agent_reranker.py`
- `agent_responder.py`
- `agent_reflector.py`
- `agent_websearch.py`

作用：

- 每个 agent 职责相对单一
- 通过状态对象串联，不让一个 agent 承担过多逻辑

设计动机：

- 这是一种 **分工明确的 agent pipeline**，不是为了“堆 agent 数量”，而是为了把复杂问题拆成更容易约束和评估的步骤
- 面试时可以强调：多 agent 的价值不在于“看起来高级”，而在于 **职责隔离、可观察性和可替换性**

### 4.4 资源与技能层

- `drugclaw/skills/...`
- `drugclaw/resource_registry.py`

作用：

- 封装底层药物知识资源
- 记录每种资源的可用性、依赖、访问模式和状态

设计动机：

- 现实里的外部资源经常不稳定，可能缺依赖、缺 metadata、接口挂掉
- 所以系统不能假设“资源都永远可用”，必须在运行时知道哪些资源当前 ready，哪些 degraded，哪些 disabled

### 4.5 证据与答案层

- `drugclaw/evidence.py`
- `drugclaw/claim_assessment.py`
- `drugclaw/response_formatter.py`

作用：

- 把原始检索结果整理成标准化 evidence item
- 对 claim 做聚合和置信度估计
- 输出最终 answer card

设计动机：

- 从“检索到了什么”过渡到“最终能对用户说什么”
- 避免直接把原始 record 堆给 LLM，导致输出噪声过大

### 4.6 记录与复盘层

- `drugclaw/query_logger.py`
- `query_logs/...`

作用：

- 每次 query 都保存 answer、report、metadata、evidence、reasoning trace

设计动机：

- 对 agent 系统来说，可复盘性非常重要
- 你在面试里可以强调：这是为了 **debug、评估、回归分析和错误定位**

---

## 5. 一次 query 是怎么跑完的

这部分一定要会讲，因为这是最典型的系统设计题。

### 5.1 三种模式

DrugClaw 当前有三种 thinking mode：

1. `SIMPLE`
2. `GRAPH`
3. `WEB_ONLY`

注意一个容易讲错的细节：

- 从系统设计上看，`GRAPH` 是“最完整能力”的默认思路
- 但从 CLI 首次体验看，`drugclaw run` 的默认模式是 `SIMPLE`

这个细节能体现你是真的看过代码，而不是只看 README。

### 5.2 SIMPLE 模式

链路大概是：

`plan -> retrieve -> normalize_evidence -> assess_claims -> simple_respond -> finalize`

适用场景：

- 结构化直查问题
- 用户已经知道要查哪些资源
- 希望快速得到稳定回答

设计动机：

- 不是所有问题都值得走重型图推理
- 对一些标准化问题，比如“imatinib 的已知靶点”，轻量链路能显著降低延迟和复杂度

### 5.3 GRAPH 模式

链路大概是：

`plan -> retrieve -> normalize_evidence -> optional_graph -> graph_build -> rerank -> assess_claims -> respond -> reflect -> [web_search] -> finalize`

适用场景：

- 需要多跳关联
- 需要把多源证据组织成图
- 需要判断当前证据是否足够，不够时再继续

设计动机：

- 图模式本质上是在追求更深的 **证据组织能力**
- 检索结果不是直接喂给回答器，而是先抽取实体和关系，再重排路径，最后综合回答

### 5.4 WEB_ONLY 模式

链路大概是：

`web_search_direct -> finalize`

适用场景：

- 非常新、非常时效性的内容
- 本地技能库不一定覆盖的问题

设计动机：

- 在医疗/药物场景里，最新信息可能来自文献或在线来源
- 因此系统保留了 web fallback，而不是死守结构化资源

### 5.5 一次完整 query 的执行逻辑

建议你按这个顺序讲：

1. 用户从 CLI 输入 query
2. `DrugClawSystem` 初始化全局状态和工作流
3. `PlannerAgent` 先做问题分类和资源偏好规划
4. `RetrieverAgent` 决定要用哪些 skill
5. `CoderAgent` 针对每个 skill 生成受限查询代码并执行，失败则 fallback 到 `skill.retrieve()`
6. 检索结果被整理成 `EvidenceItem`
7. 如果是 GRAPH 模式，则由 `GraphBuilderAgent` 从文本和 evidence 中提取三元组构图
8. `RerankerAgent` 对证据路径排序
9. `ResponderAgent` 生成结构化回答
10. `ReflectorAgent` 判断证据是否足够，不够则触发 `WebSearchAgent`
11. `finalize` 输出最终结果，并可由 `QueryLogger` 落盘

这就是一个典型的 **计划 -> 检索 -> 结构化 -> 推理 -> 回答 -> 反思** 的 agent 闭环。

---

## 6. 每个核心模块怎么讲

这一节是面试最重要的技术细节区。

### 6.1 PlannerAgent

对应文件：

- `drugclaw/agent_planner.py`
- `drugclaw/query_plan.py`

它做什么：

- 识别问题类型
- 提取实体
- 生成子问题
- 推荐优先 skill
- 标记是否需要 graph reasoning / web fallback

为什么要单独做 Planner：

1. **降低后续 agent 的搜索空间**  
   如果一上来就让 Retriever 在所有资源里乱选，容易噪声大、成本高。

2. **让系统先显式理解问题结构**  
   比如 `target_lookup`、`labeling`、`ddi` 是完全不同的任务类型。

3. **把“意图识别”和“执行检索”解耦**  
   这样后续你可以单独优化 planner，而不需要改 retrieval 逻辑。

代码里值得提的点：

- `QueryPlan` 不是只存 skill 名字，还存问题类型、实体、证据偏好、图推理需求等字段
- `is_direct_target_lookup()` 和 `prioritize_target_lookup_skills()` 体现了对药物问题类型的显式建模，而不是完全靠黑盒 LLM

面试可总结为：

> Planner 的核心价值是先把 query 结构化，减少后面检索链路的盲目性。

### 6.2 RetrieverAgent

对应文件：

- `drugclaw/agent_retriever.py`

它做什么：

- 根据 query plan 或用户的 resource filter 决定查询哪些 skill
- 做实体归一化和扩展
- 选择执行策略，再把实际查询交给 Coder Agent

为什么 Retriever 不直接自己查：

因为“选资源”和“如何调用资源”是两件事。

设计动机：

1. **资源选择和资源调用分层**
2. **便于替换底层执行方式**
3. **让 retrieval 过程更容易调试**

值得讲的细节：

- 如果用户给了 `resource_filter`，系统会优先尊重用户指定资源
- 说明系统既支持智能路由，也支持人工约束

### 6.3 CoderAgent

对应文件：

- `drugclaw/agent_coder.py`

这是面试中最容易出彩的点之一。

它做什么：

- 针对每个 skill 先生成一个紧凑 query plan
- 再生成短 Python 代码
- 在受限 sandbox 里执行
- 如果失败，则自动 fallback 到 `skill.retrieve()`

为什么要有 Coder Agent：

这是 DrugClaw 和很多普通 RAG 项目的重要差异。

核心原因是：

1. **每个资源的最优查询方式不同**  
   不是所有资源都适合用一个统一的 `retrieve(query_text)`。

2. **代码是一种比纯 prompt 更强的中间表示**  
   它可以显式做过滤、排序、字段选择、格式化。

3. **把“使用工具”变成可约束行为**  
   不是让模型随意调用外部系统，而是在 allowlist 限制下写短程序。

4. **失败可兜底**  
   自动 fallback 到 `skill.retrieve()`，保证系统鲁棒性。

为什么说这是工程设计而不是噱头：

- 它有 AST 限制
- 有 allowlisted imports 和 builtins
- 屏蔽文件系统、网络、subprocess 等危险能力
- 有输出预算和节点预算

所以这个模块本质上是在做一个 **窄能力、安全受限、可回退的代码执行器**。

面试时你可以这样讲：

> 我们不是为了“让 LLM 写代码而写代码”，而是因为药物资源是异构的，代码生成能保留资源特异性，同时通过 sandbox 和 fallback 把风险压住。

### 6.4 GraphBuilderAgent

对应文件：

- `drugclaw/agent_graph_builder.py`

它做什么：

- 从 retrieved text 和 structured evidence 里抽取实体关系三元组
- 构建 evidence subgraph

为什么需要它：

1. **原始检索结果经常是文本块或半结构化记录**
2. **用户问题很多时候问的是“关系”而不是“文本内容”**
3. **图结构更适合表达药物问题里的多跳证据**

设计动机：

- 如果直接把所有检索文本送去回答，系统只能做“文本摘要”
- 加入图构建后，系统就能显式表示 `drug -> target -> pathway -> disease`

这里的 trade-off 也要会讲：

- 好处是表达更强
- 代价是 LLM 抽三元组可能有误差，且增加一次模型调用成本

### 6.5 RerankerAgent

对应文件：

- `drugclaw/agent_reranker.py`

你不一定要讲源码细节，但要会讲角色。

它做什么：

- 对证据路径打分和筛选
- 把“可能相关”变成“优先用于回答的高价值路径”

设计动机：

- 图构建后通常会有不少边和路径
- 如果不重排，Responder 还是会吃到很多噪声

一句话总结：

> Reranker 负责把图里的证据从“存在”变成“可用于回答”。

### 6.6 ResponderAgent

对应文件：

- `drugclaw/agent_responder.py`

它做什么：

- 基于 ranked paths 或 structured evidence 生成最终 Markdown 回答

为什么不是最开始就直接让它生成：

因为在这个项目里，回答生成应该是末端能力，而不是前面所有环节都不可靠时的补锅层。

设计动机：

1. 让回答建立在结构化证据之上
2. 让格式更稳定
3. 把“证据不足”显式暴露出来，而不是硬凑答案

你可以强调：

> DrugClaw 的回答生成不是“开放式闲聊”，而是带证据约束的答案综合。

### 6.7 ReflectorAgent

对应文件：

- `drugclaw/agent_reflector.py`

它做什么：

- 评估当前证据是否足够
- 计算 reward 和 marginal gain
- 决定要不要继续检索

为什么它重要：

这体现了 Agent 系统和一次性 pipeline 的核心差异。

设计动机：

1. **不是所有 query 都能一次检索到位**
2. **多轮补检索要有停止条件**
3. **系统需要知道自己什么时候“不够确定”**

这是面试里很加分的一点，因为它说明系统具备一定的 **self-evaluation** 能力。

### 6.8 WebSearchAgent

对应文件：

- `drugclaw/agent_websearch.py`

它做什么：

- 在结构化资源不足时，补充 PubMed / ClinicalTrials / web 信息

为什么不一开始就用 web：

1. web 噪声更大
2. 药物问题优先应该查高质量结构化资源
3. web 更适合作为补充而不是主证据

这就是一个很典型的“**高质量结构化资源优先，开放世界资源补缺口**”设计。

---

## 7. 关键数据结构怎么讲

### 7.1 AgentState

对应文件：

- `drugclaw/models.py`

作用：

- 是整个 LangGraph 工作流的共享状态
- 保存输入 query、thinking mode、reasoning history、retrieved text、evidence items、claim assessments、当前答案、web results 等

设计动机：

- 多 agent 系统最怕状态散落
- 用统一状态对象能让每个节点之间的数据边界更清楚

你可以这样答：

> AgentState 相当于工作流里的上下文总线，所有 agent 都围绕这个状态做读写。

### 7.2 QueryPlan

对应文件：

- `drugclaw/query_plan.py`

作用：

- 保存问题类型、实体、子问题、偏好 skill、风险等级等信息

设计动机：

- 在 planner 和 retriever 之间建立一个明确接口
- 避免后续步骤重新猜测用户意图

### 7.3 EvidenceItem / FinalAnswer

对应文件：

- `drugclaw/evidence.py`

作用：

- `EvidenceItem`：统一表示一条证据
- `ClaimSummary`：把多条证据聚合成 claim
- `FinalAnswer`：答案文本 + 关键 claim + citations + limitations + warnings

设计动机：

- 明确区分“原始记录”“证据”“claim”“最终答案”
- 这样系统更适合做后续评估、展示和回放

这里的思想非常值得讲：

> 一个成熟的 Agent 系统不能只有最终文本输出，还要能表示支撑这个输出的中间层对象。

### 7.4 ResourceRegistry

对应文件：

- `drugclaw/resource_registry.py`

作用：

- 保存资源的名称、类别、访问方式、依赖、metadata 路径、是否支持代码生成、fallback 能力和当前状态

为什么这个设计很重要：

因为很多 demo 型 Agent 系统都默认“工具永远可用”，但真实世界不是这样。

DrugClaw 把资源状态建模成：

- `ready`
- `missing_metadata`
- `missing_dependency`
- `degraded`
- `disabled`

这很工程化，也很适合面试里讲“系统鲁棒性”。

---

## 8. 这个项目里最值得讲的设计动机

这一节适合你在面试里主动“拔高”。

### 8.1 为什么要做垂直领域 Agent，而不是通用 Agent

回答模板：

> 在垂直领域里，问题不是单纯靠更强模型就能解决，很多时候是知识源组织、检索策略和证据表达的问题。药物领域尤其明显，因为资源异构强、术语严格、错误代价高，所以更适合做 domain-native agentic workflow。

### 8.2 为什么要保留多条执行路径，而不是只有一条重型 pipeline

回答模板：

> 因为问题复杂度不同。简单问题走重型图推理会增加延迟和失败点；复杂问题如果只走轻量直答，又不够稳。所以我把系统拆成 SIMPLE、GRAPH、WEB_ONLY 三种模式，本质上是在做复杂度分层。

### 8.3 为什么用 registry 驱动资源，而不是把资源写死

回答模板：

> 因为资源集合、依赖和可用状态是动态变化的。registry 的价值在于把“当前系统有哪些能力”从代码逻辑里抽离出来，变成运行时可查询、可诊断、可排序的事实层。

### 8.4 为什么 code generation 比单一工具调用更适合这个项目

回答模板：

> 因为每个药物知识源的数据结构和最佳访问路径不同。代码生成给了系统一个可编程的中间层，使得模型可以在受限环境里完成过滤、排序、字段选择和输出组织，而不是只能调用一个统一但表达力不足的 retrieve 接口。

### 8.5 为什么要做 reflector

回答模板：

> 这是为了让系统不只是“会回答”，还知道什么时候“回答依据还不够”。这一点对高风险领域尤其重要。

---

## 9. 你可以主动强调的工程亮点

面试时不要只讲“用了 agent”，要讲工程价值。

### 9.1 工作流清晰

- LangGraph 明确建模节点和条件边
- 不同模式走不同链路
- 便于调试和扩展

### 9.2 资源管理工程化

- 有 runtime resource registry
- 有 `doctor` 做环境检查
- 有 ready / degraded / disabled 等状态

### 9.3 执行安全性考虑到位

- Coder Agent 有 AST 限制
- 有 import / builtin allowlist
- 屏蔽文件系统、环境变量、网络和 subprocess
- 失败可 fallback

### 9.4 结果可追踪

- 每次 query 都有 `query_logs/<query_id>/`
- 有 answer、metadata、evidence、reasoning trace、pickle dump

### 9.5 输出不是纯文本，而是证据驱动

- 有 evidence item
- 有 claim assessment
- 有 answer confidence
- 有 limitations / warnings

---

## 10. 这个项目的不足和你该怎么承认

这一节很关键。好的候选人不会把项目说得“完美无缺”。

### 10.1 Code Agent 仍然可能增加时延

你可以这么说：

> Code Agent 提高了灵活性，但代价是额外的 planning、code generation 和 execution 成本。对于简单结构化查询，未来我会更积极地走 direct retrieve，减少无意义的代码生成。

### 10.2 LLM 抽图存在误差

> Graph Builder 的表达能力比固定 schema 更强，但 LLM 抽三元组本身有 hallucination 风险，所以需要更多 grounded evidence、关系过滤和图后处理。

### 10.3 资源质量不完全一致

> 不同数据库的数据更新频率和字段规范差异较大，所以最终答案的一致性仍然依赖后续 claim cleaning 和 source weighting。

### 10.4 默认输出还可以更产品化

> 当前系统虽然已经支持 answer card 和 report，但部分模式下仍有工程态痕迹，比如调试信息、claim 去噪和 evidence summarization 还可以继续优化。

### 10.5 评估体系还可以更完整

> 目前已经有 query logging 和一些测试，但如果面向更正式的生产级场景，我会进一步建立任务分类型 benchmark、source-grounded evaluation 和 answer quality metrics。

---

## 11. 面试高频追问与参考回答

### 11.1 你为什么觉得这个项目算 Agent，而不是普通 RAG？

参考回答：

> 我觉得关键不在于有没有多个 prompt，而在于系统是否具备显式的任务分解、状态传递、工具调用、结果反思和条件路由。DrugClaw 里有 Planner、Retriever、Coder、Graph Builder、Responder、Reflector 等不同角色，而且它们不是线性拼接，而是通过共享状态和条件分支形成闭环，所以它更接近一个 agentic workflow，而不是单轮 RAG。

### 11.2 多 Agent 一定比单 Agent 好吗？

参考回答：

> 不一定。多 Agent 的价值在于把复杂任务拆开、提高可解释性和可控性；但如果问题很简单，多 Agent 会增加延迟和失败点。所以 DrugClaw 才保留 SIMPLE 模式，本质上是按任务复杂度选择链路，而不是盲目多 Agent。

### 11.3 你怎么控制 Agent 的不稳定性？

参考回答：

> 我主要从三个层面控制：第一是工作流层面做职责隔离，比如 planner 不回答、responder 不选资源；第二是工具层面做约束，比如 coder agent 的 allowlist 和 sandbox；第三是输出层面做结构化证据和 claim assessment，而不是只看最终自然语言答案。

### 11.4 为什么不直接 fine-tune 一个模型来回答药物问题？

参考回答：

> 因为这类问题的难点不只是模型参数知识，而是外部知识源调用、证据组织和可追溯性。即使 fine-tune 过，模型也未必知道最新资源状态或具体数据库细节；而 agentic RAG 能把外部知识和模型推理结合起来。

### 11.5 这个项目最难的地方是什么？

参考回答：

> 我觉得最难的是在灵活性和稳定性之间找平衡。药物资源异构度很高，所以需要 code-driven retrieval 和 graph reasoning；但这又会带来时延、噪声和鲁棒性问题。所以系统里才会有 resource registry、fallback retrieve、reflector 和多种 thinking mode 这些平衡设计。

### 11.6 如果让你继续优化，你会先做什么？

参考回答：

> 我会先做三件事：第一，进一步收紧 direct retrieval 的路由，让简单结构化问题少走 code generation；第二，增强 claim cleaning 和 target/disease/cell line 区分，减少最终答案噪声；第三，建立分任务类型的离线评测集，用来系统比较 SIMPLE 和 GRAPH 的收益。

### 11.7 你觉得这个项目最有“研究味”和最有“工程味”的部分分别是什么？

参考回答：

> 最有研究味的是 graph reasoning、reflective retrieval 和 evidence sufficiency 这套思路；最有工程味的是 registry、doctor、sandbox、query logging 和 answer/evidence 的结构化落盘。

---

## 12. 如何讲“我自己的贡献”

如果面试官问“你具体做了什么”，你一定不要回答成泛泛的“我参与了这个项目”。

你可以按这个模板说：

### 12.1 贡献表达模板

> 我主要负责的是系统中和 [你真实负责的模块] 相关的部分，核心工作包括：
>
> 1. 把 [某个问题] 从原来的 [旧方案] 改成 [新方案]
> 2. 增加了 [某种能力]，解决了 [某类痛点]
> 3. 为了保证稳定性，我又补了 [测试 / fallback / logging / filtering / docs]

### 12.2 如果你主要是理解和二次开发

你也可以诚实但不减分地说：

> 这个项目我不是从 0 到 1 独立原创所有模块，但我做了比较深入的代码阅读、环境搭建、链路理解和定向修改。我的价值主要在于把系统的关键设计吃透，并能明确指出哪些模块解决了什么问题、哪里还存在 trade-off、下一步应该怎么优化。

这类表达比硬吹“全是我做的”更可信。

### 12.3 如果被追问你有没有真正看过代码

你可以拿这些细节点证明：

- CLI 默认 `run` 模式是 `SIMPLE`
- `DrugClawSystem` 里通过 LangGraph 路由不同 mode
- `QueryPlan` 会显式区分问题类型和 skill 偏好
- `CoderAgent` 不只是调工具，还会先生成 query plan 再生成代码
- 代码执行有 allowlist 和 fallback retrieve
- `ReflectorAgent` 会结合 evidence sufficiency 和 marginal gain 决定是否继续
- 每次 query 会在 `query_logs/` 下落 answer、metadata、reasoning trace、evidence 和完整结果

这些都不是只看 README 能说出来的。

---

## 13. 你可以直接背的“项目亮点总结”

下面这段可以直接背：

> 我觉得 DrugClaw 这个项目最有价值的地方，是它把药物问答从“普通 RAG 文本摘要”升级成了“面向垂直任务的 agentic evidence workflow”。它先规划问题，再选择资源，再用受限代码去做资源原生检索，把结果结构化成 evidence 和 claim；复杂问题还能走图构建、路径重排和反思补检索。这种设计让我真正学到了多智能体系统不只是多写几个 prompt，而是要解决职责边界、状态传递、工具约束、证据表达和停止条件这些问题。

---

## 14. 你可以直接背的“项目不足总结”

下面这段也建议准备：

> 这个项目还不是完美的。它的主要挑战在于灵活性和稳定性的平衡：一方面要支持很多异构药物资源，所以引入了 code agent 和 graph reasoning；另一方面这也带来了更高延迟和更复杂的错误面。我认为后续优化重点会放在 direct retrieval 路由、claim 去噪、图抽取的 groundedness 和更系统的 benchmark 上。

---

## 15. 如果面试官让你画图，你就画这个

```text
User Query
   |
   v
CLI / API Entry
   |
   v
DrugClawSystem (LangGraph Orchestrator)
   |
   +--> PlannerAgent ---------> QueryPlan
   |
   +--> RetrieverAgent -------> selected skills / entities
   |
   +--> CoderAgent -----------> resource-native retrieval
   |
   +--> Evidence normalization -> EvidenceItem / Claim
   |
   +--> [GRAPH mode only]
   |      GraphBuilder -> Reranker -> Responder -> Reflector
   |                                      |
   |                                      +--> WebSearch fallback
   |
   +--> [SIMPLE mode]
   |      direct respond
   |
   +--> Final Answer + QueryLogger
```

这张图重点不是画得好看，而是把 3 个层次画出来：

1. 编排层
2. agent 层
3. evidence / output 层

---

## 16. 最后给你的面试建议

### 16.1 不要一上来就讲“用了哪些模型”

先讲：

- 业务问题是什么
- 为什么普通 RAG 不够
- 为什么要这样拆系统

模型只是其中一个部件，不是项目的全部。

### 16.2 不要只讲流程，要讲设计动机

面试官更关心：

- 你为什么这么拆
- 你为什么觉得这个 trade-off 合理
- 你知道哪里还不够好吗

### 16.3 不要背 README，要背“问题-设计-收益-代价”

推荐你所有回答都按这个四段式：

1. 问题是什么
2. 设计是什么
3. 收益是什么
4. 代价和不足是什么

这是最像成熟工程师的表达方式。

### 16.4 把“Agent”讲成系统能力，而不是 buzzword

你要尽量避免说：

> 我这个项目用了好多 agent，所以很高级。

而要说：

> 我把任务拆成 planner、retriever、coder、responder、reflector，是因为它们分别解决意图理解、资源路由、工具调用、答案综合和证据自评估问题。

---

## 17. 临场速记版

如果面试前只剩 1 分钟，就记住下面这些关键词：

- 药物领域垂直 Agentic RAG
- 不只是文本检索，而是证据综合
- 多智能体分工：plan / retrieve / code / graph / respond / reflect
- 三种模式：SIMPLE / GRAPH / WEB_ONLY
- resource registry + skill registry
- code agent + sandbox + fallback
- evidence item + claim + final answer
- query logging + reasoning trace
- 核心 trade-off：灵活性 vs 稳定性

---

## 18. 你下一步该怎么用这份文档

建议你这样练：

1. 先把第 2 节和第 13 节背熟
2. 再把第 6 节每个模块用自己的话复述一遍
3. 对着第 11 节模拟追问
4. 最后把第 12 节改成你的真实贡献版本

如果你能把这四步做完，DrugClaw 这个项目基本就能讲得比较像样了。
