# 工具与框架实践项目生成计划（LongCat 版本）

## 一、需求分析

根据 `框架.md` 文档，需要创建以下项目结构，并使用美团 LongCat API：

```
02_tooling/
├── .env
├── 01_langchain_basics.py
├── 02_langgraph_agent.py
├── 03_autogen_multi.py
├── 04_crewai_team.py
└── 05_vectordb_rag.py
```

## 二、LongCat API 配置

**API Key**: `ak_2dk7dg0rT8VU21N6jo5Oh5zI6eL31`

LongCat 提供 OpenAI 兼容的 API，配置方式：
- API Base: `https://api.longcat.chat/v1`
- API Key: 用户提供的 ak_2dk7dg0rT8VU21N6jo5Oh5zI6eL31

## 三、文件清单

| 文件 | 内容 | 依赖 |
|---|---|---|
| `.env` | LongCat API 配置 | - |
| `01_langchain_basics.py` | LangChain LCEL 基础、工具调用 | langchain, langchain-openai |
| `02_langgraph_agent.py` | LangGraph 状态机 Agent | langchain-openai, langgraph |
| `03_autogen_multi.py` | AutoGen 多 Agent 协作 | autogen-agentchat |
| `04_crewai_team.py` | CrewAI 团队协作 | crewai |
| `05_vectordb_rag.py` | 向量数据库 + RAG | chromadb, sentence-transformers |

## 四、依赖安装命令

```bash
pip install langchain langchain-openai langgraph
pip install autogen-agentchat
pip install crewai
pip install chromadb
pip install sentence-transformers
pip install python-dotenv
```

## 五、修改内容

1. 创建 `02_tooling/` 目录
2. 创建 `.env` 配置文件（配置 LongCat API）
3. 创建 5 个 Python 示例文件，全部使用 LongCat API
4. 修改 API 调用方式为 OpenAI 兼容格式

## 六、执行步骤

1. 创建目录 `02_tooling/`
2. 创建 `.env` 文件
3. 创建 `01_langchain_basics.py`
4. 创建 `02_langgraph_agent.py`
5. 创建 `03_autogen_multi.py`
6. 创建 `04_crewai_team.py`
7. 创建 `05_vectordb_rag.py`
