import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"

class MockClient:
    def __init__(self):
        self.chat = type('obj', (object,), {'completions': type('obj', (object,), {'create': self._create})()})()
    
    def _create(self, model=None, messages=None, tools=None, tool_choice=None, **kwargs):
        last_message = messages[-1]["content"] if messages else ""
        if tools:
            for tool in tools:
                tool_name = tool["function"]["name"]
                if tool_name == "get_weather" and "天气" in last_message:
                    city = "北京"
                    if "上海" in last_message:
                        city = "上海"
                    elif "广州" in last_message:
                        city = "广州"
                    elif "深圳" in last_message:
                        city = "深圳"
                    tool_func = type('obj', (object,), {'name': 'get_weather', 'arguments': json.dumps({"city": city, "unit": "celsius"})})()
                    tool_call = type('obj', (object,), {'id': 'call_123', 'function': tool_func})()
                    return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'tool_calls': [tool_call], 'content': None})()})]})
                elif tool_name == "calculate" and ("计算" in last_message or "+" in last_message or "-" in last_message or "*" in last_message or "/" in last_message):
                    tool_func = type('obj', (object,), {'name': 'calculate', 'arguments': json.dumps({"expression": last_message})})()
                    tool_call = type('obj', (object,), {'id': 'call_123', 'function': tool_func})()
                    return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'tool_calls': [tool_call], 'content': None})()})]})
        return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': '我是一个工具助手，可以帮你查询天气和进行计算。', 'tool_calls': None})()})]})

if USE_MOCK:
    client = MockClient()
else:
    client = OpenAI(
        api_key=os.getenv("LONGCAT_API_KEY"),
        base_url=os.getenv("LONGCAT_API_BASE"),
    )

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名，如：北京"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "进行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式，如：2+3*4"},
                },
                "required": ["expression"],
            },
        },
    }
]

def get_weather(city: str, unit: str = "celsius") -> dict:
    weather_data = {
        "北京": {"temperature": 22, "condition": "晴天"},
        "上海": {"temperature": 25, "condition": "多云"},
        "广州": {"temperature": 28, "condition": "阴天"},
        "深圳": {"temperature": 27, "condition": "小雨"},
    }
    data = weather_data.get(city, {"temperature": 20, "condition": "晴"})
    return {"city": city, "temperature": data["temperature"], "condition": data["condition"], "unit": unit}

def calculate(expression: str) -> dict:
    try:
        result = eval(expression)
        return {"expression": expression, "result": result, "success": True}
    except Exception as e:
        return {"expression": expression, "error": str(e), "success": False}

def call_tool(tool_name, args):
    if tool_name == "get_weather":
        return get_weather(**args)
    elif tool_name == "calculate":
        return calculate(**args)
    else:
        return {"error": f"未知工具: {tool_name}"}

def run_with_tools(messages):
    response = client.chat.completions.create(
        model=os.getenv("LONGCAT_MODEL", "LongCat-Flash-Chat"),
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    msg = response.choices[0].message

    if msg.tool_calls:
        messages.append({"role": "assistant", "content": msg.content})
        
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"\n[调用工具] {func_name}({args})")

            result = call_tool(func_name, args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, ensure_ascii=False),
            })

        final = client.chat.completions.create(
            model=os.getenv("LONGCAT_MODEL", "LongCat-Flash-Chat"),
            messages=messages,
        )
        return final.choices[0].message.content
    else:
        return msg.content

def chat_with_agent():
    print("=" * 60)
    print("          工具助手 - LongCat API 交互模式")
    print("=" * 60)
    print("可用工具:")
    print("  - get_weather: 获取天气 (如: 北京天气怎么样?)")
    print("  - calculate: 数学计算 (如: 计算 2+3*4)")
    print("输入 'exit' 或 'quit' 退出对话")
    print("输入 'clear' 清空对话历史")
    print("-" * 60)
    
    messages = [
        {"role": "system", "content": """你是一个工具调用助手，根据用户需求选择合适的工具。

可用工具：
1. get_weather(city, unit): 获取指定城市的天气
2. calculate(expression): 进行数学计算

如果需要调用工具，输出 tool_calls；如果不需要工具，可以直接回答。"""}
    ]
    
    while True:
        user_input = input("\n你: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("工具助手: 再见！")
            break
        
        if user_input.lower() == 'clear':
            messages = [
                {"role": "system", "content": """你是一个工具调用助手，根据用户需求选择合适的工具。

可用工具：
1. get_weather(city, unit): 获取指定城市的天气
2. calculate(expression): 进行数学计算

如果需要调用工具，输出 tool_calls；如果不需要工具，可以直接回答。"""}
            ]
            print("工具助手: 对话历史已清空")
            continue
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            reply = run_with_tools(messages)
            print(f"\n工具助手:\n{reply}")
            messages.append({"role": "assistant", "content": reply})
            
        except Exception as e:
            print(f"工具助手: 出错了 - {str(e)}")

if __name__ == "__main__":
    chat_with_agent()