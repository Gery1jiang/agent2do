import os
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LONGCAT_API_KEY"),
    base_url=os.getenv("LONGCAT_API_BASE"),
)

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query: str) -> str:
    """从互联网搜索信息"""
    try:
        result = tavily_client.search(query=query, max_results=5)
        results = []
        for i, item in enumerate(result.get('results', []), 1):
            results.append(f"[{i}] {item.get('title', '')}\nURL: {item.get('url', '')}\n摘要: {item.get('content', '')}")
        return "\n\n---\n\n".join(results) if results else "未找到相关信息"
    except Exception as e:
        return f"搜索失败: {str(e)}"

def chat_completion(messages, temperature=0.3):
    """调用 LLM 生成回复"""
    response = client.chat.completions.create(
        model=os.getenv("LONGCAT_MODEL", "LongCat-Flash-Chat"),
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content

def research_analyst(topic: str) -> str:
    """研究分析师：分析搜索结果并提取关键信息"""
    search_results = search_web(topic)
    
    messages = [
        {"role": "system", "content": "你是一名资深数据分析师，擅长从搜索结果中提取关键信息。请分析以下搜索结果，识别3-5个核心趋势或模式，并指出数据的局限性。"},
        {"role": "user", "content": f"搜索主题：{topic}\n\n搜索结果：\n{search_results}"}
    ]
    
    analysis = chat_completion(messages, temperature=0.2)
    return {"search_results": search_results, "analysis": analysis}

def report_writer(topic: str, search_results: str, analysis: str) -> str:
    """报告撰写人：根据分析结果撰写专业报告"""
    messages = [
        {"role": "system", "content": "你是一名专业报告撰写人，擅长将复杂分析转化为清晰的书面报告。报告结构要求：执行摘要（150字）、主要发现（3-5条）、趋势分析、结论与建议、参考来源。"},
        {"role": "user", "content": f"研究主题：{topic}\n\n搜索结果：\n{search_results}\n\n分析结果：\n{analysis}\n\n请撰写一份专业的研究报告。"}
    ]
    
    report = chat_completion(messages, temperature=0.3)
    return report

def research_assistant(topic: str):
    """完整的研究助手流程"""
    print(f"🔍 开始研究主题：{topic}")
    print("="*60)
    
    print("\n1️⃣ 信息检索阶段...")
    search_data = research_analyst(topic)
    
    print("\n2️⃣ 数据分析阶段...")
    analysis = search_data["analysis"]
    
    print("\n3️⃣ 报告撰写阶段...")
    report = report_writer(topic, search_data["search_results"], analysis)
    
    print("\n" + "="*60)
    print("📝 研究报告已生成")
    print("="*60)
    
    return report

if __name__ == "__main__":
    topic = "2025 年 AI Agent 在企业软件中的应用现状与趋势"
    report = research_assistant(topic)
    
    with open("research_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("\n📄 报告已保存到: research_report.md")
    print("\n" + "="*60)
    print(report)