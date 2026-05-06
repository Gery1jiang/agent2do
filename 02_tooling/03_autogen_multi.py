from dotenv import load_dotenv
import os
import autogen

load_dotenv()

LONGCAT_API_KEY = os.getenv("LONGCAT_API_KEY")
LONGCAT_API_BASE = os.getenv("LONGCAT_API_BASE")
LONGCAT_MODEL = os.getenv("LONGCAT_MODEL", "LongCat-Flash-Chat")

config_list = [{
    "model": LONGCAT_MODEL,
    "api_key": LONGCAT_API_KEY,
    "base_url": LONGCAT_API_BASE,
}]
llm_config = {"config_list": config_list, "temperature": 0.2}


assistant = autogen.AssistantAgent(
    name="代码助手",
    llm_config=llm_config,
    system_message="你是一个 Python 专家，编写高质量代码并解释实现思路。",
)


reviewer = autogen.AssistantAgent(
    name="代码审查员",
    llm_config=llm_config,
    system_message="你是严格的代码审查员，检查代码的正确性、可读性和潜在 bug，给出改进建议。",
)


user_proxy = autogen.UserProxyAgent(
    name="用户",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    code_execution_config={"work_dir": "coding", "use_docker": False},
)


groupchat = autogen.GroupChat(
    agents=[user_proxy, assistant, reviewer],
    messages=[],
    max_round=6,
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message="请编写一个 Python 函数，实现归并排序，并包含单元测试。",
)
