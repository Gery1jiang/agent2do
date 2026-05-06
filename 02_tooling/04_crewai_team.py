from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, Process

load_dotenv()

LONGCAT_API_KEY = os.getenv("LONGCAT_API_KEY")
LONGCAT_API_BASE = os.getenv("LONGCAT_API_BASE")
LONGCAT_MODEL = os.getenv("LONGCAT_MODEL", "LongCat-Flash-Chat")

llm_config = {
    "model": LONGCAT_MODEL,
    "api_key": LONGCAT_API_KEY,
    "base_url": LONGCAT_API_BASE,
    "temperature": 0.2,
    "llm_type": "openai",
}


researcher = Agent(
    role="市场研究员",
    goal="深入研究指定主题，收集准确的市场数据和趋势",
    backstory="你是一名经验丰富的市场分析师，擅长从海量信息中提炼关键洞察。",
    verbose=True,
    llm=llm_config,
)


writer = Agent(
    role="内容撰写人",
    goal="基于研究结果撰写清晰、有说服力的报告",
    backstory="你是专业的商业写作专家，擅长将复杂数据转化为易读的报告。",
    verbose=True,
    llm=llm_config,
)


research_task = Task(
    description="研究 2024-2025 年 AI agent 市场的主要玩家、融资情况和技术趋势",
    expected_output="包含 5 个关键发现的结构化研究报告，每条发现附有数据支持",
    agent=researcher,
)


write_task = Task(
    description="基于研究报告，撰写一篇 500 字的市场摘要，面向非技术管理层",
    expected_output="500 字左右的市场摘要，使用非技术语言，包含结论和建议",
    agent=writer,
    context=[research_task],
)


crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff()
print("\n========== 最终报告 ==========")
print(result)
