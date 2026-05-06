import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os
import json
import sys

load_dotenv()

LONGCAT_API_KEY = os.getenv("LONGCAT_API_KEY")
LONGCAT_API_BASE = os.getenv("LONGCAT_API_BASE")
LONGCAT_MODEL = os.getenv("LONGCAT_MODEL", "LongCat-Flash-Lite")

async def navigate(page, url: str) -> str:
    """打开指定 URL"""
    try:
        await page.goto(url)
        return f"已导航至: {page.url}"
    except Exception as e:
        return f"导航失败: {str(e)}"

async def get_text(page) -> str:
    """获取当前页面的文字内容"""
    try:
        text = await page.evaluate("""() => {
            const body = document.body.cloneNode(true);
            ['script','style','nav','footer','header'].forEach(tag => {
                body.querySelectorAll(tag).forEach(el => el.remove());
            });
            return body.innerText.slice(0, 3000);
        }""")
        return text if text else "页面无内容"
    except Exception as e:
        return f"获取文本失败: {str(e)}"

async def click(page, selector: str) -> str:
    """点击页面元素，使用 CSS 选择器"""
    try:
        await page.click(selector, timeout=5000)
        await page.wait_for_load_state("networkidle", timeout=10000)
        return f"已点击: {selector}"
    except Exception as e:
        return f"点击失败: {str(e)}"

async def fill_input(page, selector: str, text: str) -> str:
    """在输入框中填写文字"""
    try:
        await page.fill(selector, text)
        return f"已填写: {selector}"
    except Exception as e:
        return f"填写失败: {str(e)}"

async def screenshot(page, path: str = "screenshot.png") -> str:
    """截取当前页面截图"""
    try:
        await page.screenshot(path=path)
        return f"截图已保存: {path}"
    except Exception as e:
        return f"截图失败: {str(e)}"

TOOLS = [
    {"type": "function", "function": {
        "name": "navigate",
        "description": "打开指定 URL",
        "parameters": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]},
    }},
    {"type": "function", "function": {
        "name": "get_text",
        "description": "获取当前页面的文字内容",
        "parameters": {"type": "object", "properties": {}},
    }},
    {"type": "function", "function": {
        "name": "click",
        "description": "点击页面元素，使用 CSS 选择器",
        "parameters": {"type": "object", "properties": {"selector": {"type": "string"}}, "required": ["selector"]},
    }},
    {"type": "function", "function": {
        "name": "fill_input",
        "description": "在输入框中填写文字",
        "parameters": {"type": "object", "properties": {
            "selector": {"type": "string"}, "text": {"type": "string"},
        }, "required": ["selector", "text"]},
    }},
    {"type": "function", "function": {
        "name": "screenshot",
        "description": "截取当前页面截图",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}}},
    }},
]

async def execute_task(page, messages, llm):
    for step in range(10):
        response = llm.invoke(messages)
        
        print(f"[DEBUG] 响应类型: {type(response)}")
        print(f"[DEBUG] 响应内容: {response.content[:200] if response.content else '无'}")
        print(f"[DEBUG] 附加参数: {response.additional_kwargs}")
        
        tool_calls = response.additional_kwargs.get("tool_calls", [])
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            tool_calls = response.tool_calls
            print(f"[DEBUG] 工具调用(hasattr): {tool_calls}")
        
        if not tool_calls:
            return response.content, messages

        messages.append({"role": "assistant", "content": response.content or "", "tool_calls": tool_calls})

        for tc in tool_calls:
            if hasattr(tc, 'function'):
                func_name = tc.function.name
                args = json.loads(tc.function.arguments)
                tc_id = tc.id
            elif "function" in tc:
                func_name = tc["function"]["name"]
                args = json.loads(tc["function"]["arguments"])
                tc_id = tc.get("id")
            else:
                func_name = tc.get("name")
                args = tc.get("args", {})
                tc_id = tc.get("id")
            
            print(f"[执行] {func_name}({args})")

            if func_name == "navigate":
                result = await navigate(page, args["url"])
            elif func_name == "get_text":
                result = await get_text(page)
            elif func_name == "click":
                result = await click(page, args["selector"])
            elif func_name == "fill_input":
                result = await fill_input(page, args["selector"], args["text"])
            elif func_name == "screenshot":
                result = await screenshot(page, args.get("path", "screenshot.png"))
            else:
                result = f"未知工具: {func_name}"

            print(f"[结果] {result[:200]}")
            messages.append({"role": "tool", "tool_call_id": tc_id, "content": result})

    return "任务执行超时", messages

async def browser_agent():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, channel="chrome")
        page = await browser.new_page()

        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(
            model=LONGCAT_MODEL,
            temperature=0.1,
            api_key=LONGCAT_API_KEY,
            base_url=LONGCAT_API_BASE,
        ).bind_tools(TOOLS)

        messages = [
            {"role": "system", "content": "你是一个浏览器自动化 agent。使用提供的工具完成用户的网络任务。每次只执行一个步骤，观察结果后再决定下一步。"},
        ]

        print("🚀 浏览器Agent已启动！")
        print("输入 'exit' 或 'quit' 退出程序")
        print("=" * 50)

        while True:
            user_input = input("\n请输入您的指令: ").strip()
            
            if user_input.lower() in ["exit", "quit"]:
                print("👋 再见！")
                break
            
            if not user_input:
                print("请输入有效的指令")
                continue

            print(f"\n您的指令: {user_input}")
            print("-" * 50)

            messages.append({"role": "user", "content": user_input})
            result, messages = await execute_task(page, messages, llm)
            
            print(f"\n✅ 任务完成:\n{result}")
            print("=" * 50)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(browser_agent())