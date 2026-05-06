# 浏览器Agent项目 - 产品需求文档

## Overview
- **Summary**: 实现一个基于Playwright的浏览器自动化Agent，能够通过自然语言指令完成网页浏览、信息提取、表单填写等任务
- **Purpose**: 提供一个可以自动化完成网页操作任务的AI助手，支持导航、点击、文本提取、表单填写和截图等功能
- **Target Users**: 需要自动化完成重复性网页操作任务的用户，如信息收集、数据抓取、表单填写等场景

## Goals
- 实现浏览器自动化的核心功能：导航、点击、文本提取、表单填写、截图
- 集成LLM实现工具调用能力，支持多步骤任务规划和执行
- 提供清晰的错误处理和状态反馈机制

## Non-Goals (Out of Scope)
- 不实现高级浏览器操作如文件上传/download
- 不支持多页面并行操作
- 不实现复杂的页面交互如拖拽、滚动

## Background & Context
- 当前项目已使用LongCat API作为LLM后端
- 参考代码助手项目的架构模式（langgraph + tool calling）
- 需要安装playwright依赖并配置浏览器

## Functional Requirements
- **FR-1**: 支持URL导航功能，能够打开指定网页
- **FR-2**: 支持页面文本提取，获取当前页面的主要文字内容
- **FR-3**: 支持CSS选择器点击，能够点击页面元素
- **FR-4**: 支持表单填写，能够在输入框中填写文字
- **FR-5**: 支持页面截图，能够保存当前页面截图
- **FR-6**: 集成LLM工具调用，自动规划和执行多步骤任务

## Non-Functional Requirements
- **NFR-1**: 操作超时处理，每个操作最多等待10秒
- **NFR-2**: 错误处理完善，捕获并报告操作失败原因
- **NFR-3**: 输出结果清晰，包含执行步骤和结果摘要

## Constraints
- **Technical**: 使用Python 3.x，依赖playwright、langchain、langgraph
- **Business**: 需要配置LongCat API密钥
- **Dependencies**: 需要安装playwright并下载chromium浏览器

## Assumptions
- 用户已安装Python环境和pip包管理器
- 用户已配置.env文件中的API密钥
- 用户能够访问目标网站

## Acceptance Criteria

### AC-1: 浏览器导航功能
- **Given**: 有效的URL
- **When**: 调用navigate工具
- **Then**: 浏览器成功导航到指定URL并返回成功消息
- **Verification**: `programmatic`

### AC-2: 文本提取功能
- **Given**: 页面已加载完成
- **When**: 调用get_text工具
- **Then**: 返回页面主要文本内容（最多3000字符）
- **Verification**: `programmatic`

### AC-3: 元素点击功能
- **Given**: 有效的CSS选择器
- **When**: 调用click工具
- **Then**: 成功点击指定元素或返回错误信息
- **Verification**: `programmatic`

### AC-4: 表单填写功能
- **Given**: 有效的CSS选择器和文本内容
- **When**: 调用fill_input工具
- **Then**: 成功填写输入框或返回错误信息
- **Verification**: `programmatic`

### AC-5: 截图功能
- **Given**: 页面已加载
- **When**: 调用screenshot工具
- **Then**: 成功保存截图文件
- **Verification**: `programmatic`

### AC-6: 多步骤任务执行
- **Given**: 完整的任务描述
- **When**: 调用browser_agent执行任务
- **Then**: 自动规划并执行多个工具调用完成任务
- **Verification**: `human-judgment`

## Open Questions
- [ ] 是否需要支持其他浏览器（Firefox, WebKit）？
- [ ] 是否需要支持无头模式配置？