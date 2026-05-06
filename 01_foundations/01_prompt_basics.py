from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"

class MockClient:
    def __init__(self):
        self.chat = type('obj', (object,), {'completions': type('obj', (object,), {'create': self._create})()})()
    
    def _create(self, model=None, messages=None, temperature=None, **kwargs):
        last_message = messages[-1]["content"] if messages else ""
        if "排序" in last_message or "sort" in last_message.lower():
            code = '''def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr'''
            return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': code})()})]})
        elif "fibonacci" in last_message.lower() or "斐波那契" in last_message:
            code = '''def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    result = [0, 1]
    for i in range(2, n):
        result.append(result[i-1] + result[i-2])
    return result'''
            return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': code})()})]})
        else:
            return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': '我是一个代码助手，擅长帮助编写 Python 代码。\n\n你可以问我：\n- 数据结构与算法实现\n- Python 语法问题\n- 代码优化建议\n- 设计模式\n\n请问有什么代码需要我帮忙编写？'})()})]})

if USE_MOCK:
    client = MockClient()
else:
    client = OpenAI(
        api_key=os.getenv("LONGCAT_API_KEY"),
        base_url=os.getenv("LONGCAT_API_BASE"),
    )

def chat_with_agent():
    print("=" * 60)
    print("          代码助手 - LongCat API 交互模式")
    print("=" * 60)
    print("输入 'exit' 或 'quit' 退出对话")
    print("输入 'clear' 清空对话历史")
    print("-" * 60)
    
    system_prompt = """你是一个专业的 Python 代码助手，严格遵守以下规则：

【角色定义】
- 你的唯一任务是帮助用户编写 Python 代码
- 只回答与代码相关的问题，非代码问题请拒绝回答

【回答约束】
- 必须直接给出代码和简要说明
- 代码要简洁、规范、可运行
- 非代码问题回答："抱歉，我是代码助手，只回答代码相关问题。"

【示例】
用户：写一个冒泡排序
助手：
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

用户：解释什么是装饰器
助手：
装饰器是 Python 中用于修改函数行为的语法糖：
def decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

用户：今天天气怎么样？
助手：
抱歉，我是代码助手，只回答代码相关问题。"""
    
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    while True:
        user_input = input("\n你: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("代码助手: 再见！")
            break
        
        if user_input.lower() == 'clear':
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            print("代码助手: 对话历史已清空")
            continue
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = client.chat.completions.create(
                model=os.getenv("LONGCAT_MODEL", "LongCat-Flash-Chat"),
                messages=messages,
                temperature=0.2,
            )
            reply = response.choices[0].message.content
            print(f"\n代码助手:\n{reply}")
            messages.append({"role": "assistant", "content": reply})
            
        except Exception as e:
            print(f"代码助手: 出错了 - {str(e)}")

if __name__ == "__main__":
    chat_with_agent()