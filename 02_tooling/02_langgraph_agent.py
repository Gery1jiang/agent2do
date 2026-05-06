from dotenv import load_dotenv
import os
from typing import TypedDict, Annotated, List
import operator
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

LONGCAT_API_KEY = os.getenv("LONGCAT_API_KEY")
LONGCAT_API_BASE = os.getenv("LONGCAT_API_BASE")
LONGCAT_MODEL = os.getenv("LONGCAT_MODEL", "LongCat-Flash-Chat")


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]


@tool
def search(query: str) -> str:
    """搜索互联网获取信息"""
    return f"搜索 '{query}' 的结果：这是模拟的搜索结果内容。"


@tool
def calculator(expression: str) -> str:
    """计算数学表达式"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"错误: {e}"


tools = [search, calculator]
tool_node = ToolNode(tools)


llm = ChatOpenAI(
    model=LONGCAT_MODEL,
    temperature=0,
    api_key=LONGCAT_API_KEY,
    base_url=LONGCAT_API_BASE,
).bind_tools(tools)


def call_model(state: AgentState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END


graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("tools", tool_node)

graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")

app = graph.compile()


result = app.invoke({
    "messages": [HumanMessage(content="2024 年世界人口大约是多少？再帮我算一下 1234 × 5678")]
})

for msg in result["messages"]:
    if hasattr(msg, "content") and msg.content:
        print(f"[{type(msg).__name__}] {msg.content}\n")
