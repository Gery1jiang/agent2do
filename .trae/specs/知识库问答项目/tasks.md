# 知识库问答项目 - The Implementation Plan

## [ ] Task 1: 实现文档入库（ingest.py）
- **Priority**: P0
- **Depends On**: None
- **Description**: 
  - 在 02_knowledge_qa/ 目录下创建 ingest.py
  - 实现 PDF 文档加载（DirectoryLoader + PyPDFLoader）
  - 实现分块（RecursiveCharacterTextSplitter）
  - 使用 SiliconFlow 进行嵌入
  - 保存到 Chroma 向量数据库
- **Acceptance Criteria Addressed**: [AC-1, AC-3]
- **Test Requirements**:
  - `programmatic` TR-1.1: 运行 ingesting 能成功加载文档并保存向量数据库
- **Notes**: 使用实战.md 中的代码作为参考

## [ ] Task 2: 实现知识库问答 Agent（agent.py）
- **Priority**: P0
- **Depends On**: Task 1
- **Description**: 
  - 在 02_knowledge_qa/ 目录下创建 agent.py
  - 加载向量数据库
  - 定义 search_knowledge_base 和 general_knowledge 工具
  - 使用 LangGraph 构建 ReAct Agent
  - 使用 LongCat API
- **Acceptance Criteria Addressed**: [AC-2, AC-3]
- **Test Requirements**:
  - `programmatic` TR-2.1: 运行 agent.py 能正常回答问题并带来源标注
- **Notes**: 需要正确配置向量数据库路径

## [ ] Task 3: 创建 docs 目录和示例文档
- **Priority**: P1
- **Depends On**: None
- **Description**: 
  - 在 02_knowledge_qa/ 下创建 docs 目录
  - 创建一个简单的测试文档（或使用项目中的某个文档）
- **Acceptance Criteria Addressed**: [AC-1]
- **Test Requirements**:
  - `human-judgement` TR-3.1: 检查 docs 目录是否存在且有文档

## [ ] Task 4: 更新 requirements.txt
- **Priority**: P1
- **Depends On**: None
- **Description**: 
  - 在 03_projects/requirements.txt 中添加知识库问答项目的依赖
- **Acceptance Criteria Addressed**: [NFR-1]
- **Test Requirements**:
  - `programmatic` TR-4.1: 检查 requirements.txt 包含 langchain-community、pypdf 等依赖
