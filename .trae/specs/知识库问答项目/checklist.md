# 知识库问答项目 - Verification Checklist

## 目录结构
- [ ] 02_knowledge_qa/ 目录存在
- [ ] 02_knowledge_qa/ 下有 ingest.py 和 agent.py
- [ ] 02_knowledge_qa/docs/ 目录存在
- [ ] 02_knowledge_qa/chroma_db/ 目录存在（运行后）

## 文档入库
- [ ] 运行 ingest.py 能成功加载 PDF 文档
- [ ] 运行后能看到加载和分块的日志
- [ ] 向量数据库保存到 chroma_db 目录

## 知识库问答
- [ ] 运行 agent.py 能正常启动
- [ ] 提问关于文档的问题时，Agent 会调用 search_knowledge_base 工具
- [ ] 返回的回答包含来源标注（文档名和页码）

## 配置
- [ ] API 配置正确加载（LongCat 和 SiliconFlow）
- [ ] requirements.txt 包含所有必需依赖
- [ ] 代码风格与现有项目保持一致
