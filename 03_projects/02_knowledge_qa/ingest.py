
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
SILICONFLOW_API_BASE = os.getenv("SILICONFLOW_API_BASE")
SILICONFLOW_EMBEDDING_MODEL = os.getenv("SILICONFLOW_EMBEDDING_MODEL", "BAAI/bge-m3")


def ingest_documents(docs_dir: str = "./docs", db_dir: str = "./chroma_db"):
    """将目录中的 PDF 文档入库"""

    docs_dir = os.path.join(os.path.dirname(__file__), docs_dir)
    db_dir = os.path.join(os.path.dirname(__file__), db_dir)

    # 1. 加载文档
    loader = DirectoryLoader(docs_dir, glob="**/*.pdf", loader_cls=PyPDFLoader)
    raw_docs = loader.load()
    print("加载了", len(raw_docs), "个文档页面")

    # 2. 分块：chunk_size 和 overlap 影响检索质量
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", "。", ".", " ", ""],
    )
    chunks = splitter.split_documents(raw_docs)
    print("分割为", len(chunks), "个 chunks")

    # 3. 嵌入 + 存储（分批处理，每批 64 个）
    embeddings = OpenAIEmbeddings(
        model=SILICONFLOW_EMBEDDING_MODEL,
        api_key=SILICONFLOW_API_KEY,
        base_url=SILICONFLOW_API_BASE,
    )
    batch_size = 64
    db = None
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        if db is None:
            db = Chroma.from_documents(batch, embeddings, persist_directory=db_dir)
        else:
            db.add_documents(batch)
        print(f"处理第 {i//batch_size + 1} 批，共 {len(chunks)} 个 chunks")
    print("向量数据库已保存到", db_dir)
    return db


if __name__ == "__main__":
    docs_dir = os.path.join(os.path.dirname(__file__), "docs")
    os.makedirs(docs_dir, exist_ok=True)
    # 在 docs 目录放入 PDF 文件后运行
    ingest_documents()
