# 知识库问答项目 - Product Requirement Document

## Overview
- **Summary**: 实现一个基于 RAG Pipeline 的知识库问答系统，支持 PDF 文档入库、向量检索、来源标注。
- **Purpose**: 让用户可以基于自己的文档提问，系统返回准确的、带来源标注的回答。
- **Target Users**: 需要从文档中快速获取信息的学习者、研究人员、知识工作者。

## Goals
- 实现文档入库功能（支持 PDF 格式）
- 实现基于向量检索的 RAG 问答系统
- 返回带来源标注的准确回答
- 复用现有环境配置（LongCat 和 SiliconFlow）

## Non-Goals (Out of Scope)
- 暂不实现其他文档格式（Word、PPT 等）
- 暂不实现重排（Rerank）功能
- 暂不实现网页搜索等外部数据源集成

## Background & Context
- 已有项目：01_foundations（基础）、02_tooling（框架）、01_code_assistant（代码助手）
- 可用 API：LongCat（LLM）、SiliconFlow（Embedding）
- 参考实现：实战.md 中的项目 2

## Functional Requirements
- **FR-1**: 文档入库功能（ingest.py）
- **FR-2**: PDF 文档加载和分块
- **FR-3**: 向量存储和检索（Chroma）
- **FR-4**: 知识库问答 Agent（agent.py）
- **FR-5**: 答案来源标注（文档名和页码）

## Non-Functional Requirements
- **NFR-1**: 代码风格与现有项目保持一致
- **NFR-2**: 兼容 Windows 环境
- **NFR-3**: 支持环境变量配置

## Constraints
- **Technical**: Python >= 3.10、LangChain、ChromaDB
- **Business**: 使用已有的 API Key，不引入额外成本
- **Dependencies**: langchain-community、pypdf、unstructured

## Assumptions
- SiliconFlow 的 Embedding API 兼容 OpenAI 接口
- PDF 文档在 docs 目录下
- 用户已有可测试的 PDF 文档

## Acceptance Criteria

### AC-1: 文档入库功能完整
- **Given**: docs 目录下有 PDF 文件
- **When**: 运行 ingest.py
- **Then**: 文档被加载、分块、嵌入并保存到 chroma_db 目录
- **Verification**: `programmatic`
- **Notes**: 需要看到加载和分块的日志输出

### AC-2: 知识库问答正常工作
- **Given**: 文档已入库
- **When**: 运行 agent.py 提问关于文档的问题
- **Then**: Agent 调用 search_knowledge_base 工具，返回带来源标注的回答
- **Verification**: `programmatic`

### AC-3: 配置正确加载
- **Given**: .env 文件中有正确的 API Key
- **When**: 导入项目代码
- **Then**: API 配置正确加载，可正常调用
- **Verification**: `programmatic`

## Open Questions
- 暂无
