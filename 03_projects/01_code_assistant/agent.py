
from dotenv import load_dotenv
import os
from typing import TypedDict, Annotated, List
import operator
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from sandbox import safe_execute

load_dotenv()

LONGCAT_API_KEY = os.getenv("LONGCAT_API_KEY")
LONGCAT_API_BASE = os.getenv("LONGCAT_API_BASE")
LONGCAT_MODEL = os.getenv("LONGCAT_MODEL", "LongCat-Flash-Chat")


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]


@tool
def execute_python(code):
    """
    执行 Python 代码并返回输出结果。
    适合：验证算法、测试函数、数学计算。
    代码应包含 print 语句输出结果。
    """
    result = safe_execute(code)
    if result["error"]:
        return "执行错误:\n" + result["error"]
    output = result["stdout"] or "(无输出)"
    if result["stderr"]:
        output += "\n警告: " + result["stderr"]
    return output


@tool
def write_file(filename, content):
    """将代码或内容写入文件"""
    try:
        # 确保 output 目录存在
        output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return "文件已写入：" + file_path
    except Exception as e:
        return "写入失败: " + str(e)


tools = [execute_python, write_file]
tool_node = ToolNode(tools)


llm = ChatOpenAI(
    model=LONGCAT_MODEL,
    temperature=0.1,
    api_key=LONGCAT_API_KEY,
    base_url=LONGCAT_API_BASE,
).bind_tools(tools)


SYSTEM = """你是一个代码助手。工作方式：
1. 理解用户的编程需求
2. 编写代码解决问题
3. 用 execute_python 工具测试代码
4. 如果测试失败，分析错误并修复
5. 确认正确后，向用户展示最终代码和解释

始终先测试代码再交付。"""


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


def code_assistant(request):
    print("\n用户: " + request + "\n" + "=" * 50)
    result = app.invoke({"messages": [HumanMessage(content=request)]})
    for msg in result["messages"]:
        if hasattr(msg, "content") and msg.content and not hasattr(msg, "tool_calls"):
            print("\n助手:\n" + msg.content)


if __name__ == "__main__":
    code_assistant("实现一个 LRU 缓存，容量为 3，并演示 get/put 操作")

