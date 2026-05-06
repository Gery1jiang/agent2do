from dotenv import load_dotenv
import os
import chromadb
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

load_dotenv()

LONGCAT_API_KEY = os.getenv("LONGCAT_API_KEY")
LONGCAT_API_BASE = os.getenv("LONGCAT_API_BASE")
LONGCAT_MODEL = os.getenv("LONGCAT_MODEL", "LongCat-Flash-Chat")

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
SILICONFLOW_API_BASE = os.getenv("SILICONFLOW_API_BASE", "https://api.siliconflow.cn/v1")
SILICONFLOW_EMBEDDING_MODEL = os.getenv("SILICONFLOW_EMBEDDING_MODEL", "BAAI/bge-m3")


embeddings = OpenAIEmbeddings(
    model=SILICONFLOW_EMBEDDING_MODEL,
    api_key=SILICONFLOW_API_KEY,
    base_url=SILICONFLOW_API_BASE,
)


chroma_client = chromadb.PersistentClient(path="./chroma_db")


def get_embeddings(texts: list[str]) -> list[list[float]]:
    return embeddings.embed_documents(texts)


collection = chroma_client.get_or_create_collection(
    name="knowledge_base_bge_m3",
)

# 检查是否已有数据
if collection.count() == 0:
    documents = [
        "LangGraph 是 LangChain 的扩展，用于构建有状态的多 actor 应用程序。",
        "RAG（检索增强生成）通过检索外部知识来增强 LLM 的回答准确性。",
        "向量数据库通过余弦相似度或欧氏距离进行语义检索。",
        "AutoGen 由微软开发，支持多个 AI agent 之间的对话协作。",
        "Function calling 允许模型以结构化 JSON 格式请求执行外部函数。",
    ]

    doc_embeddings = get_embeddings(documents)
    collection.add(
        documents=documents,
        embeddings=doc_embeddings,
        ids=[f"doc_{i}" for i in range(len(documents))],
    )
    print(f"已添加 {len(documents)} 条文档（使用 {SILICONFLOW_EMBEDDING_MODEL} 嵌入）\n")
else:
    print(f"知识库已有 {collection.count()} 条文档\n")


def retrieve(query: str, n_results: int = 2) -> list[str]:
    query_embedding = embeddings.embed_query(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
    return results["documents"][0]


llm = ChatOpenAI(
    model=LONGCAT_MODEL,
    temperature=0,
    api_key=LONGCAT_API_KEY,
    base_url=LONGCAT_API_BASE,
)


def rag_answer(question: str) -> str:
    context_docs = retrieve(question)
    context = "\n".join(f"- {doc}" for doc in context_docs)

    response = llm.invoke([
        {"role": "system", "content": f"基于以下上下文回答问题：\n\n{context}"},
        {"role": "user",   "content": question},
    ])
    return response.content


questions = [
    "LangGraph 是什么？",
    "如何提高 LLM 回答的准确性？",
    "微软有没有开发什么 agent 框架？",
]

for q in questions:
    print(f"Q: {q}")
    print(f"A: {rag_answer(q)}\n")
