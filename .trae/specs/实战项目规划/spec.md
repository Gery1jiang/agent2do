# Agent 实战项目规划 - Product Requirement Document

## Overview
- **Summary**: 基于 `实战.md` 搭建 Agent 实战项目目录结构，先实现第一个项目「代码助手」，后三个项目（RAG、浏览器 Agent、研究助手）预留目录。复用现有 `.env` 中的 LongCat API 配置。
- **Purpose**: 将学习到的 Agent 基础和框架知识落地到可运行的实战项目，重点实现带沙箱代码执行的 ReAct 代码助手。
- **Target Users**: AI Agent 学习者、Python 开发者。

## Goals
- 搭建完整的项目目录结构（03_projects）
- 配置可复用的 API 环境（基于 LongCat）
- 实现第一个项目：代码助手（ReAct + 沙箱执行）
- 预留后三个项目的目录结构

## Non-Goals (Out of Scope)
- 暂不实现后三个项目（RAG、浏览器 Agent、研究助手）的核心代码
- 暂不添加额外的 API（Tavily、Anthropic 等）

## Background & Context
- 已有基础：01_foundations（基础概念）、02_tooling（框架实践）
- 可用 API：LongCat API（ak_2dk7dg0rT8VU21N6jo5Oh5zI6eL31，模型 LongCat-Flash-Chat）、SiliconFlow Embedding（BAAI/bge-m3）
- 项目参考：实战.md 中的代码示例

## Functional Requirements
- **FR-1**: 项目目录结构按实战.md 要求搭建
- **FR-2**: 配置统一的 .env 文件，复用现有 API
- **FR-3**: 实现 sandbox.py：带受限环境的 Python 代码沙箱执行器
- **FR-4**: 实现 agent.py：基于 LangGraph 的 ReAct 代码助手

## Non-Functional Requirements
- **NFR-1**: 代码风格与现有项目保持一致
- **NFR-2**: 依赖安装脚本提供 Windows 兼容命令
- **NFR-3**: 沙箱执行超时限制（30秒）

## Constraints
- **Technical**: Python >= 3.10，兼容 Windows，使用现有 API
- **Business**: 优先使用免费/已有的 API Key，不引入额外成本
- **Dependencies**: LangChain, LangGraph, OpenAI SDK

## Assumptions
- LongCat API 兼容 OpenAI 接口格式
- SiliconFlow Embedding 可用于后续 RAG 项目

## Acceptance Criteria

### AC-1: 项目目录结构完整
- **Given**: 当前项目根目录
- **When**: 执行目录搭建
- **Then**: 03_projects/ 目录包含 01_code_assistant/、02_knowledge_qa/、03_browser_agent/、04_research_assistant/ 四个子目录
- **Verification**: `programmatic`

### AC-2: .env 文件配置正确
- **Given**: 现有两个 .env 文件
- **When**: 生成 03_projects/.env
- **Then**: 包含 LONGCAT_API_KEY、LONGCAT_API_BASE、LONGCAT_MODEL、SILICONFLOW_API_KEY、SILICONFLOW_API_BASE、SILICONFLOW_EMBEDDING_MODEL
- **Verification**: `programmatic`

### AC-3: 沙箱执行器能安全运行代码
- **Given**: sandbox.py 已实现
- **When**: 执行带 print 的 Python 代码
- **Then**: 正确捕获输出并返回；执行危险操作（如文件写入）被限制
- **Verification**: `programmatic`

### AC-4: 代码助手 Agent 能正常工作
- **Given**: agent.py 已实现，依赖已安装
- **When**: 运行 agent.py，输入代码需求（如实现 LRU 缓存）
- **Then**: Agent 思考 -> 写代码 -> 沙箱执行 -> 输出结果
- **Verification**: `programmatic`

## Open Questions
- 暂无
