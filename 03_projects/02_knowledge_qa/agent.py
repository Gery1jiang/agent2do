
from dotenv import load_dotenv
import os
from typing import TypedDict, Annotated, List
import operator
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

LONGCAT_API_KEY = os.getenv("LONGCAT_API_KEY")
LONGCAT_API_BASE = os.getenv("LONGCAT_API_BASE")
LONGCAT_MODEL = os.getenv("LONGCAT_MODEL", "LongCat-Flash-Chat")

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
SILICONFLOW_API_BASE = os.getenv("SILICONFLOW_API_BASE")
SILICONFLOW_EMBEDDING_MODEL = os.getenv("SILICONFLOW_EMBEDDING_MODEL", "BAAI/bge-m3")


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]


db_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
embeddings = OpenAIEmbeddings(
    model=SILICONFLOW_EMBEDDING_MODEL,
    api_key=SILICONFLOW_API_KEY,
    base_url=SILICONFLOW_API_BASE,
)
db = Chroma(persist_directory=db_dir, embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 4})


@tool
def search_knowledge_base(query):
    """
    从知识库中检索与查询最相关的内容。
    当需要回答特定文档相关的问题时使用。
    """
    docs = retriever.invoke(query)
    if not docs:
        return "知识库中未找到相关内容。"
    results = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "未知来源")
        page = doc.metadata.get("page", "?")
        results.append("[来源 " + str(i) + "] " + source + " 第" + str(page) + "页:\n" + doc.page_content)
    return "\n\n---\n\n".join(results)


@tool
def general_knowledge(question):
    """当问题不需要查知识库、而是常识性问题时使用此工具"""
    return "这是一个一般知识问题：" + question


tools = [search_knowledge_base, general_knowledge]
tool_node = ToolNode(tools)


llm = ChatOpenAI(
    model=LONGCAT_MODEL,
    temperature=0,
    api_key=LONGCAT_API_KEY,
    base_url=LONGCAT_API_BASE,
).bind_tools(tools)


SYSTEM = """你是一个基于知识库的问答助手。
- 涉及具体文档内容时，必须先调用 search_knowledge_base 工具
- 回答时注明信息来源（文档名和页码）
- 如果知识库中没有相关内容，如实告知用户
- 不要凭空捏造文档中的信息"""


def agent_node(state):
    messages = [SystemMessage(content=SYSTEM)] + state["messages"]
    return {"messages": [llm.invoke(messages)]}


def router(state):
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END


graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", router)
graph.add_edge("tools", "agent")
app = graph.compile()


def qa(question):
    result = app.invoke({"messages": [HumanMessage(content=question)]})
    last = result["messages"][-1]
    print("A: " + last.content + "\n")


if __name__ == "__main__":
    print("=" * 60)
    print("知识库问答助手 - 基于文档的智能问答系统")
    print("=" * 60)
    print("提示：输入问题进行问答，输入 'exit' 或 'quit' 退出\n")
    
    while True:
        try:
            question = input("请输入您的问题: ")
            if question.lower() in ["exit", "quit", "退出"]:
                print("感谢使用知识库问答助手！")
                break
            if not question.strip():
                print("请输入有效的问题\n")
                continue
            print("\n思考中...\n")
            qa(question)
        except KeyboardInterrupt:
            print("\n感谢使用知识库问答助手！")
            break

