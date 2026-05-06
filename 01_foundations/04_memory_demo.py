from openai import OpenAI
from dotenv import load_dotenv
from collections import deque
import os

load_dotenv()

USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"

class MockClient:
    def __init__(self):
        self.chat = type('obj', (object,), {'completions': type('obj', (object,), {'create': self._create})()})()
    
    def _create(self, model=None, messages=None, temperature=None, **kwargs):
        history = [m["content"] for m in messages if m["role"] != "system"]
        if not history:
            return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': '你好！我是有记忆的助手，请告诉我一些关于你的信息。'})()})]})
        
        user_history = [h for i, h in enumerate(history) if i % 2 == 0]
        assistant_history = [h for i, h in enumerate(history) if i % 2 == 1]
        
        remembered_info = []
        for h in user_history:
            if "叫" in h or "名字" in h:
                if "叫" in h:
                    name = h.split("叫")[1].strip().split("，")[0].split("。")[0].split("我是")[0].strip()
                    remembered_info.append(f"名字：{name}")
            if "职业" in h or "工作" in h or "做什么" in h:
                if "是" in h:
                    job = h.split("是")[1].strip().split("。")[0]
                    remembered_info.append(f"职业：{job}")
            if "学习" in h:
                remembered_info.append(f"正在学习：{h}")
        
        if "记得" in history[-1] or "记得我" in history[-1] or "你还记得" in history[-1]:
            if remembered_info:
                return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': '是的，我记得你告诉我的信息：\n' + '\n'.join(remembered_info)})()})]})
            else:
                return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': '我记得我们正在聊天，但还没有获取到关于你的具体信息。请告诉我更多关于你的事情吧！'})()})]})
        elif len(history) == 1:
            return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': '你好！我是有记忆的助手，我会记住你说的重要信息。'})()})]})
        else:
            return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': '我正在仔细听你说的话，并会记住重要的信息！'})()})]})

if USE_MOCK:
    client = MockClient()
else:
    client = OpenAI(
        api_key=os.getenv("LONGCAT_API_KEY"),
        base_url=os.getenv("LONGCAT_API_BASE"),
    )

class ConversationAgent:
    def __init__(self, max_history: int = 10):
        self.system = "你是一个有记忆的助手，记住用户说的重要信息，如姓名、职业、爱好等。"
        self.history = deque(maxlen=max_history)
        self.original_max_history = max_history

    def chat(self, user_input: str) -> str:
        self.history.append({"role": "user", "content": user_input})

        messages = [{"role": "system", "content": self.system}] + list(self.history)

        response = client.chat.completions.create(
            model=os.getenv("LONGCAT_MODEL", "LongCat-Flash-Chat"),
            messages=messages,
            temperature=0.3,
        )
        reply = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": reply})
        
        # 自动压缩记忆
        self.summarize_and_compress()
        
        return reply

    def summarize_and_compress(self):
        if len(self.history) < 8:
            return
        history_text = "\n".join(
            f"{m['role']}: {m['content']}" for m in list(self.history)[:8]
        )
        summary_response = client.chat.completions.create(
            model=os.getenv("LONGCAT_MODEL", "LongCat-Flash-Chat"),
            messages=[
                {"role": "system", "content": "将以下对话压缩为 2-3 句摘要，保留关键信息，如姓名、职业、重要事实等。"},
                {"role": "user",   "content": history_text},
            ],
        )
        summary = summary_response.choices[0].message.content
        new_history = deque([
            {"role": "system", "content": f"[历史摘要] {summary}"},
        ] + list(self.history)[8:], maxlen=self.original_max_history)
        self.history = new_history
        print("[记忆已压缩]")

    def get_memory_status(self):
        return f"当前记忆长度: {len(self.history)}/{self.original_max_history}"

def chat_with_memory_agent():
    print("=" * 60)
    print("          记忆助手 - LongCat API 交互模式")
    print("=" * 60)
    print("这个助手会记住你说的重要信息！")
    print("输入 'exit' 或 'quit' 退出对话")
    print("输入 'clear' 清空记忆")
    print("输入 'status' 查看记忆状态")
    print("-" * 60)
    
    agent = ConversationAgent(max_history=12)
    
    while True:
        user_input = input("\n你: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("记忆助手: 再见！希望能再和你聊天！")
            break
        
        if user_input.lower() == 'clear':
            agent = ConversationAgent(max_history=12)
            print("记忆助手: 记忆已清空，开始新的对话！")
            continue
        
        if user_input.lower() == 'status':
            print(f"记忆助手: {agent.get_memory_status()}")
            continue
        
        try:
            reply = agent.chat(user_input)
            print(f"\n记忆助手:\n{reply}")
            
        except Exception as e:
            print(f"记忆助手: 出错了 - {str(e)}")

if __name__ == "__main__":
    chat_with_memory_agent()