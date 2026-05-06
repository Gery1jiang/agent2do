import re
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"

class MockClient:
    def __init__(self):
        self.chat = type('obj', (object,), {'completions': type('obj', (object,), {'create': self._create})()})()
    
    def _create(self, model=None, messages=None, stop=None, temperature=None, **kwargs):
        last_message = messages[-1]["content"] if messages else ""
        if "Observation:" in last_message:
            if "搜索" in last_message:
                return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': 'Thought: 已获取搜索结果，现在总结答案。\nFinal Answer: 根据搜索结果，你查询的内容已找到相关信息。'})()})]})
            elif "计算" in last_message:
                return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': 'Thought: 计算完成，现在给出最终答案。\nFinal Answer: 计算结果已得出。'})()})]})
            else:
                return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': 'Thought: 已获取信息，现在总结答案。\nFinal Answer: 任务已完成。'})()})]})
        else:
            if any(op in last_message for op in ['+', '-', '*', '/', '计算', '等于', '多少']):
                return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': 'Thought: 需要进行数学计算。\nAction: calculator[' + last_message + ']'})()})]})
            else:
                return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': 'Thought: 需要搜索相关信息来回答问题。\nAction: search[' + last_message + ']'})()})]})

if USE_MOCK:
    client = MockClient()
else:
    client = OpenAI(
        api_key=os.getenv("LONGCAT_API_KEY"),
        base_url=os.getenv("LONGCAT_API_BASE"),
    )

def search_web(query: str) -> str:
    search_results = {
        "2024年诺贝尔物理学奖": "2024年诺贝尔物理学奖授予John J. Hopfield和Geoffrey E. Hinton，以表彰他们在人工智能和机器学习领域的基础贡献。",
        "Python学习": "Python是一种高级编程语言，广泛应用于数据科学、人工智能、Web开发等领域。",
        "北京天气": "北京今天天气晴朗，温度22度，适合户外活动。",
    }
    return search_results.get(query, f"关于 '{query}' 的搜索结果：这是示例搜索结果内容。")

def calculator(expression: str) -> str:
    clean_expr = ''.join([c for c in expression if c in '0123456789+-*/(). '])
    try:
        return str(eval(clean_expr))
    except Exception as e:
        return f"计算错误: {e}"

TOOLS = {"search": search_web, "calculator": calculator}

SYSTEM_PROMPT = """你是一个 ReAct agent，按以下格式思考和行动：

Thought: 分析当前情况，决定下一步
Action: search[查询内容] 或 calculator[数学表达式]
Observation: （工具返回结果，由系统填写）
... 重复以上步骤 ...
Final Answer: 最终回答

只输出 Thought 和 Action，不要伪造 Observation。"""

def parse_action(text: str):
    match = re.search(r"Action:\s*(\w+)\[(.+?)\]", text)
    if match:
        return match.group(1), match.group(2)
    return None, None

def react_agent(question: str, max_steps: int = 5):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": question},
    ]

    for step in range(max_steps):
        response = client.chat.completions.create(
            model=os.getenv("LONGCAT_MODEL", "LongCat-Flash-Chat"),
            messages=messages,
            stop=["Observation:"],
            temperature=0.1,
        )
        output = response.choices[0].message.content
        print(f"\n[Step {step+1}]\n{output}")

        if "Final Answer:" in output:
            final = output.split("Final Answer:")[-1].strip()
            print(f"\n✅ 最终答案: {final}")
            return final

        tool_name, tool_input = parse_action(output)
        if tool_name and tool_name in TOOLS:
            observation = TOOLS[tool_name](tool_input)
            print(f"Observation: {observation}")

            messages.append({"role": "assistant", "content": output})
            messages.append({"role": "user", "content": f"Observation: {observation}"})
        else:
            print("未检测到有效 Action，退出")
            break

    return "达到最大步数限制"

def chat_with_react_agent():
    print("=" * 60)
    print("          ReAct Agent - LongCat API 交互模式")
    print("=" * 60)
    print("ReAct 模式：思考 → 行动 → 观察 → 总结")
    print("可用工具:")
    print("  - search[查询内容]: 搜索网络信息")
    print("  - calculator[表达式]: 数学计算")
    print("输入 'exit' 或 'quit' 退出对话")
    print("输入 'clear' 清空对话历史")
    print("-" * 60)
    
    while True:
        user_input = input("\n你: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("ReAct Agent: 再见！")
            break
        
        if user_input.lower() == 'clear':
            print("ReAct Agent: 对话历史已清空")
            continue
        
        print(f"\n🎯 问题: {user_input}")
        print("-" * 40)
        
        try:
            react_agent(user_input)
            
        except Exception as e:
            print(f"ReAct Agent: 出错了 - {str(e)}")

if __name__ == "__main__":
    chat_with_react_agent()