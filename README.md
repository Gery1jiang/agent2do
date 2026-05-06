# AI Agent 实战项目

> 🚀 从基础到实战的完整 AI Agent 学习路径，包含 Prompt Engineering、Function Calling、ReAct、RAG、多 Agent 协作等核心技术。

## 🌟 项目亮点

- **系统化学习路径**：从基础概念到实战项目，循序渐进
- **多框架覆盖**：LangChain、LangGraph、CrewAI、AutoGen
- **实战驱动**：四个完整项目，可直接运行使用
- **安全沙箱**：代码执行在受限环境中运行

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | LangChain, LangGraph, CrewAI, AutoGen |
| LLM |  OpenAI, Anthropic ，deepseek等|
| 向量数据库 | ChromaDB |
| 浏览器自动化 | Playwright |
| 搜索 API | Tavily |

## 📚 学习路径

```
阶段一：基础概念 ──→ 阶段二：工具框架 ──→ 阶段三：实战项目
```

### 阶段一：基础概念 (`01_foundations/`)

| 文件 | 主题 | 核心知识点 |
|------|------|------------|
| `01_prompt_basics.py` | Prompt 工程 | 指令设计、上下文管理、角色设定 |
| `02_function_calling.py` | 函数调用 | 工具定义、参数传递、响应解析 |
| `03_react_loop.py` | ReAct 模式 | 思考推理、工具调用循环 |
| `04_memory_demo.py` | 记忆机制 | 对话历史、长期记忆、摘要记忆 |

### 阶段二：工具框架 (`02_tooling/`)

| 文件 | 框架 | 核心能力 |
|------|------|----------|
| `01_langchain_basics.py` | LangChain | 链式调用、文档处理、模板引擎 |
| `02_langgraph_agent.py` | LangGraph | 状态管理、条件分支、工作流编排 |
| `03_autogen_multi.py` | AutoGen | 多 Agent 对话、角色扮演 |
| `04_crewai_team.py` | CrewAI | 任务分工、角色协作、流程管理 |
| `05_vectordb_rag.py` | ChromaDB | 文档嵌入、向量检索、RAG 流程 |

### 阶段三：实战项目 (`03_projects/`)

| 项目 | 核心技术 | 难度 | 功能 |
|------|----------|------|------|
| `01_code_assistant` | ReAct + 沙箱执行 | ⭐⭐ | 代码编写、测试、调试 |
| `02_knowledge_qa` | RAG Pipeline | ⭐⭐⭐ | PDF 问答、来源标注 |
| `03_browser_agent` | Playwright 自动化 | ⭐⭐⭐⭐ | 网页浏览、信息提取 |
| `04_research_assistant` | 多 Agent 协作 | ⭐⭐⭐⭐ | 信息检索、分析报告 |

## 🚀 快速开始

### 环境要求

- Python 3.10+
- API 密钥（deepseek/OpenAI/Anthropic）

### 安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd agent2do

# 安装核心依赖
pip install langchain langchain-openai langgraph chromadb python-dotenv

# 安装额外依赖
pip install openai anthropic
pip install playwright && playwright install chromium
pip install crewai tavily-python
pip install langchain-community pypdf unstructured
```

### 配置环境变量

创建 `.env` 文件：

```env
# LongCat API
LONGCAT_API_KEY=your_key
LONGCAT_API_BASE=https://api.longcat.chat/openai/v1
LONGCAT_MODEL=LongCat-Flash-Lite

# OpenAI API（可选）
OPENAI_API_KEY=your_key

# SiliconFlow Embedding
SILICONFLOW_API_KEY=your_key
SILICONFLOW_API_BASE=https://api.siliconflow.cn/v1
SILICONFLOW_EMBEDDING_MODEL=BAAI/bge-m3

# Tavily Search（研究助手用）
TAVILY_API_KEY=your_key
```

### 运行示例

```bash
# 基础概念
cd 01_foundations
python 03_react_loop.py

# 工具框架
cd 02_tooling
python 02_langgraph_agent.py

# 实战项目
cd 03_projects/01_code_assistant
python agent.py

cd 03_projects/02_knowledge_qa
python ingest.py  # 先导入文档
python agent.py

cd 03_projects/03_browser_agent
python agent.py

cd 03_projects/04_research_assistant
python crew.py
```

## 📁 项目结构

```
agent2do/
├── 01_foundations/          # 基础概念示例
│   ├── 01_prompt_basics.py
│   ├── 02_function_calling.py
│   ├── 03_react_loop.py
│   └── 04_memory_demo.py
├── 02_tooling/              # 工具框架示例
│   ├── 01_langchain_basics.py
│   ├── 02_langgraph_agent.py
│   ├── 03_autogen_multi.py
│   ├── 04_crewai_team.py
│   └── 05_vectordb_rag.py
├── 03_projects/             # 实战项目
│   ├── 01_code_assistant/   # 代码助手
│   ├── 02_knowledge_qa/     # 知识库问答
│   ├── 03_browser_agent/    # 浏览器Agent
│   └── 04_research_assistant/ # 研究助手
├── 基础.md                   # 基础概念学习文档
├── 框架.md                   # 工具框架学习文档
├── 生产.md                   # 生产部署学习文档
├── 实战.md                   # 实战项目学习文档
├── agentmap.md               # Agent 能力图谱
└── README.md                 # 项目说明
```

## 🔍 实战项目详解

### 1. 代码助手 (`01_code_assistant`)

**功能**：理解编程需求 → 编写代码 → 沙箱测试 → 修复错误 → 交付

**核心文件**：
- `agent.py` - Agent 主程序
- `sandbox.py` - 代码安全执行沙箱

**安全特性**：
- 受限的全局变量
- 禁止网络访问
- 执行超时控制

### 2. 知识库问答 (`02_knowledge_qa`)

**功能**：PDF 文档导入 → 向量检索 → 语义问答 → 来源标注

**核心文件**：
- `ingest.py` - 文档入库脚本
- `agent.py` - 问答 Agent

**RAG 流程**：
```
文档 → 分块 → 嵌入 → 存储 → 检索 → 重排 → 生成
```

### 3. 浏览器 Agent (`03_browser_agent`)

**功能**：自然语言指令 → 任务规划 → 浏览器操作 → 结果提取

**支持操作**：
- `navigate` - 页面导航
- `get_text` - 文本提取
- `click` - 元素点击
- `fill_input` - 表单填写
- `screenshot` - 页面截图

### 4. 研究助手 (`04_research_assistant`)

**功能**：主题分析 → 信息检索 → 数据分析 → 报告撰写

**Agent 团队**：
- **搜索专家**：从互联网检索信息
- **数据分析师**：分析收集的数据
- **报告撰写人**：生成结构化报告

## ⚠️ 安全说明

1. **代码沙箱**：代码助手使用受限环境执行，禁止危险操作
2. **API 密钥**：敏感信息存储在 `.env` 文件中，请勿提交到版本控制
3. **网络访问**：浏览器 Agent 仅访问用户指定网站
4. **文件权限**：限制文件系统访问范围

## 📖 学习文档

- [基础.md](基础.md) - Prompt、Function Calling、ReAct 基础
- [框架.md](框架.md) - LangChain、LangGraph、CrewAI 框架详解
- [生产.md](生产.md) - 部署、监控、优化指南
- [实战.md](实战.md) - 四个实战项目详细教程

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

⭐ 如果这个项目对你有帮助，请给个 Star！
