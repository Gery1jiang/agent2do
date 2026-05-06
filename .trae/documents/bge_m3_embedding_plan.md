# 硅基流动 BAAI/bge-m3 嵌入模型集成计划

## 1. 背景目标
将当前简单关键词匹配的 RAG 实现升级为使用硅基流动提供的 BAAI/bge-m3 嵌入模型进行真正的语义检索。

## 2. 核心能力
- 使用 chroma 向量数据库持久化存储
- 集成硅基流动的 BAAI/bge-m3 嵌入 API（OpenAI 兼容）
- 实现真正的语义相似度检索
- 保持与 LongCat LLM 的对话集成

## 3. 功能拆解
- 更新 `.env` 文件，添加硅基流动 API 配置
- 修改 `05_vectordb_rag.py`：
  - 使用 OpenAI 兼容方式调用硅基流动 embedding API
  - 使用 Chroma 进行存储和检索
  - BAAI/bge-m3 支持 8192 tokens 的长文档

## 4. 流程逻辑
1. 用户输入问题
2. 使用硅基流动 API 生成问题的 embedding
3. 在 Chroma 中进行相似度检索
4. 检索 Top-K 相关文档
5. 将相关文档作为上下文传给 LongCat LLM
6. 返回回答

## 5. 硅基流动 API 配置
- API 地址：`https://api.siliconflow.cn/v1/embeddings`
- 模型：`BAAI/bge-m3`
- API Key：`sk-ldaqstylsycukthhzjncqylqtnchwlmgurmvwtlazmsmfnah`（用户提供）

## 6. 实施文件
- 修改：`.env` - 添加 SILICONFLOW_API_KEY 等配置
- 重写：`05_vectordb_rag.py` - 使用新的 embedding 方案

## 7. 依赖检查
- `chromadb` - 已安装
- `requests` - 用于直接调用 API（或使用 langchain_openai）

## 8. 风险提示
- 硅基流动 API 的调用额度限制
- BAAI/bge-m3 的响应延迟
