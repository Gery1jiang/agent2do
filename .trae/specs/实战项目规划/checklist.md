# Agent 实战项目规划 - Verification Checklist

## 目录结构
- [ ] 03_projects/ 目录存在
- [ ] 03_projects/ 下包含 01_code_assistant/、02_knowledge_qa/、03_browser_agent/、04_research_assistant/ 四个子目录

## 环境配置
- [ ] 03_projects/.env 存在
- [ ] .env 包含 LONGCAT_API_KEY、LONGCAT_API_BASE、LONGCAT_MODEL、SILICONFLOW_API_KEY、SILICONFLOW_API_BASE、SILICONFLOW_EMBEDDING_MODEL

## 代码沙箱
- [ ] sandbox.py 文件存在
- [ ] safe_execute() 函数能执行简单代码并返回 stdout
- [ ] 危险操作（如文件写入）被限制

## 代码助手
- [ ] agent.py 文件存在
- [ ] Agent 能正常启动
- [ ] Agent 能调用 execute_python 工具
- [ ] 代码风格与现有项目一致

## 依赖文档
- [ ] requirements.txt 存在
- [ ] requirements.txt 包含 langchain、langchain-openai、langgraph 等必需依赖
