# Agent 实战项目规划 - The Implementation Plan

## [ ] Task 1: 搭建项目目录结构
- **Priority**: P0
- **Depends On**: None
- **Description**: 
  - 创建 03_projects/ 根目录
  - 创建四个子目录：01_code_assistant/、02_knowledge_qa/、03_browser_agent/、04_research_assistant/
- **Acceptance Criteria Addressed**: [AC-1]
- **Test Requirements**:
  - `programmatic` TR-1.1: 检查 03_projects/ 下是否包含四个子目录
- **Notes**: 使用 Windows 兼容命令

## [ ] Task 2: 配置统一 .env 文件
- **Priority**: P0
- **Depends On**: Task 1
- **Description**: 
  - 从 01_foundations/.env 和 02_tooling/.env 提取可用配置
  - 生成 03_projects/.env，包含 LongCat 和 SiliconFlow 配置
- **Acceptance Criteria Addressed**: [AC-2]
- **Test Requirements**:
  - `programmatic` TR-2.1: 检查 .env 文件包含所有必需配置项
- **Notes**: 注意 API_BASE 路径正确

## [ ] Task 3: 实现代码沙箱 (sandbox.py)
- **Priority**: P0
- **Depends On**: Task 2
- **Description**: 
  - 在 01_code_assistant/ 下创建 sandbox.py
  - 实现 safe_execute() 函数：带重定向 stdout/stderr、受限全局变量、超时限制
- **Acceptance Criteria Addressed**: [AC-3]
- **Test Requirements**:
  - `programmatic` TR-3.1: 测试执行简单打印代码能返回正确输出
  - `programmatic` TR-3.2: 测试危险操作（如 open()）被限制
- **Notes**: 参考实战.md 中的代码

## [ ] Task 4: 实现代码助手 Agent (agent.py)
- **Priority**: P0
- **Depends On**: Task 3
- **Description**: 
  - 在 01_code_assistant/ 下创建 agent.py
  - 使用 LangGraph 构建 ReAct Agent
  - 定义工具：execute_python、write_file
  - 使用 LongCat API
- **Acceptance Criteria Addressed**: [AC-4]
- **Test Requirements**:
  - `programmatic` TR-4.1: 测试 agent 能启动并响应简单代码请求
  - `human-judgement` TR-4.2: 检查代码风格与现有项目一致
- **Notes**: 适配 LongCat 的 model 名称

## [ ] Task 5: 创建 requirements.txt 和 README
- **Priority**: P1
- **Depends On**: Task 4
- **Description**: 
  - 在 03_projects/ 下创建 requirements.txt，列出所需依赖
  - 创建简易 README 说明如何运行
- **Acceptance Criteria Addressed**: [NFR-2]
- **Test Requirements**:
  - `programmatic` TR-5.1: 检查 requirements.txt 包含所有必需依赖
- **Notes**: 依赖列表参考实战.md
