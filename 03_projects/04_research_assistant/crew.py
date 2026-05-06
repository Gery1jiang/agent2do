import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("LONGCAT_MODEL", "LongCat-Flash-Chat"),
    api_key=os.getenv("LONGCAT_API_KEY"),
    base_url=os.getenv("LONGCAT_API_BASE"),
    temperature=0.3
)

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def tavily_search(query: str) -> str:
    """从互联网搜索最新、准确的信息，适用于获取当前事件、趋势数据和专业知识"""
    try:
        result = tavily_client.search(query=query, max_results=5)
        results = []
        for i, item in enumerate(result.get('results', []), 1):
            results.append(f"[{i}] {item.get('title', '')}\nURL: {item.get('url', '')}\n摘要: {item.get('content', '')}")
        return "\n\n---\n\n".join(results) if results else "未找到相关信息"
    except Exception as e:
        return f"搜索失败: {str(e)}"

searcher = Agent(
    role="信息检索专家",
    goal="从互联网高效检索准确、权威的信息",
    backstory="你是一名信息检索专家，擅长制定精准搜索策略，识别可信信息源。",
    tools=[tavily_search],
    llm=llm,
    verbose=True,
    max_iter=5,
)

analyst = Agent(
    role="数据分析师",
    goal="对收集到的信息进行批判性分析，识别模式和关键洞察",
    backstory="你是一名资深分析师，能从海量数据中提炼核心结论，善于发现数据背后的故事。",
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="报告撰写人",
    goal="将分析结论整理为结构清晰、可读性强的研究报告",
    backstory="你是一名专业作家，擅长将复杂的分析转化为清晰的书面报告。",
    llm=llm,
    verbose=True,
)

def create_research_crew(topic: str) -> Crew:
    search_task = Task(
        description=f"""对主题「{topic}」进行全面的信息检索：
        1. 搜索最新的相关数据和趋势
        2. 找到至少 5 个可信信息来源
        3. 记录每个来源的 URL 和关键数据点""",
        expected_output="包含来源 URL、关键数据和引用的结构化信息汇总",
        agent=searcher,
    )

    analysis_task = Task(
        description=f"""分析关于「{topic}」的收集信息：
        4. 识别 3-5 个核心趋势或模式
        5. 对比不同来源的观点
        6. 指出数据的局限性或不确定性""",
        expected_output="3-5 个核心发现，每个附有证据和置信度评估",
        agent=analyst,
        context=[search_task],
    )

    write_task = Task(
        description=f"""基于分析结果，撰写关于「{topic}」的专业研究报告：
        结构要求：
        - 执行摘要（150字）
        - 主要发现（3-5条，每条含数据支撑）
        - 趋势分析
        - 结论与建议
        - 参考来源""",
        expected_output="格式规范、数据充分的 Markdown 格式研究报告",
        agent=writer,
        context=[search_task, analysis_task],
        output_file="research_report.md",
    )

    return Crew(
        agents=[searcher, analyst, writer],
        tasks=[search_task, analysis_task, write_task],
        process=Process.sequential,
        verbose=True,
    )

if __name__ == "__main__":
    topic = "2025 年 AI Agent 在企业软件中的应用现状与趋势"
    crew = create_research_crew(topic)
    result = crew.kickoff()
    print("\n" + "="*60)
    print("研究报告已生成：research_report.md")
    print("="*60)
    print(result)