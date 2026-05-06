from dotenv import load_dotenv
import os
import re
from langchain_openai import ChatOpenAI

load_dotenv()

LONGCAT_API_KEY = os.getenv("LONGCAT_API_KEY")
LONGCAT_API_BASE = os.getenv("LONGCAT_API_BASE")
LONGCAT_MODEL = os.getenv("LONGCAT_MODEL", "LongCat-Flash-Chat")

llm = ChatOpenAI(
    model=LONGCAT_MODEL,
    temperature=0.2,
    api_key=LONGCAT_API_KEY,
    base_url=LONGCAT_API_BASE,
)


def multiply(a: int, b: int) -> int:
    """将两个整数相乘"""
    return a * b


def get_stock_price(symbol: str) -> str:
    """获取股票价格（模拟）"""
    prices = {
        "AAPL": 182.5, 
        "GOOGL": 141.3, 
        "TSLA": 248.0,
        "MSFT": 378.9,
        "NVDA": 875.3,
        "BABA": 85.2,
        "JD": 45.8,
    }
    return str(prices.get(symbol.upper(), "未找到该股票"))


def extract_numbers(text: str) -> list[int]:
    """从文本中提取数字"""
    pattern = r'(\d+)'
    matches = re.findall(pattern, text)
    return [int(m) for m in matches]


def extract_stock_symbol(text: str) -> str:
    """从文本中提取股票代码"""
    stock_patterns = [
        r'(苹果|AAPL|Apple)',
        r'(谷歌|GOOGL|Google)',
        r'(特斯拉|TSLA|Tesla)',
        r'(微软|MSFT|Microsoft)',
        r'(英伟达|NVDA|NVIDIA)',
        r'(阿里巴巴|BABA|Alibaba)',
        r'(京东|JD|Jingdong)',
    ]
    stock_mapping = {
        '苹果': 'AAPL', 'AAPL': 'AAPL', 'Apple': 'AAPL',
        '谷歌': 'GOOGL', 'GOOGL': 'GOOGL', 'Google': 'GOOGL',
        '特斯拉': 'TSLA', 'TSLA': 'TSLA', 'Tesla': 'TSLA',
        '微软': 'MSFT', 'MSFT': 'MSFT', 'Microsoft': 'MSFT',
        '英伟达': 'NVDA', 'NVDA': 'NVDA', 'NVIDIA': 'NVDA',
        '阿里巴巴': 'BABA', 'BABA': 'BABA', 'Alibaba': 'BABA',
        '京东': 'JD', 'JD': 'JD', 'Jingdong': 'JD',
    }
    for pattern in stock_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return stock_mapping.get(match.group(1).capitalize(), match.group(1).upper())
    return ""


def process_query(user_input: str) -> str:
    """处理用户查询，判断是否需要调用工具"""
    numbers = extract_numbers(user_input)
    stock_symbol = extract_stock_symbol(user_input)
    
    if len(numbers) >= 2 and ('乘' in user_input or '×' in user_input or '*' in user_input or '乘以' in user_input):
        result = multiply(numbers[0], numbers[1])
        return f"计算结果：{numbers[0]} × {numbers[1]} = {result}"
    
    if stock_symbol:
        price = get_stock_price(stock_symbol)
        return f"{stock_symbol} 的股价：{price}"
    
    return ""


def main():
    print("欢迎使用 LangChain 工具调用助手！")
    print("输入 'exit' 或 'quit' 退出程序")
    print("支持功能：乘法计算、股票查询（支持 AAPL、GOOGL、TSLA、MSFT、NVDA、BABA、JD）")
    print("-" * 60)
    
    while True:
        user_input = input("\n请输入您的问题：")
        
        if user_input.lower() in ["exit", "quit", "退出"]:
            print("感谢使用，再见！")
            break
        
        if not user_input.strip():
            print("请输入有效的问题")
            continue
        
        try:
            tool_result = process_query(user_input)
            
            if tool_result:
                print("\n回答:", tool_result)
            else:
                response = llm.invoke(user_input)
                print("\n回答:", response.content)
                
        except Exception as e:
            print(f"发生错误: {e}")


if __name__ == "__main__":
    main()
