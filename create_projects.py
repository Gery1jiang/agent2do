
import os

# 基础目录
base_dir = r"g:\My_memory\知识库\大模型\Agent\agent2do\03_projects"

# 子文件夹列表
sub_dirs = [
    "01_code_assistant",
    "02_knowledge_qa",
    "03_browser_agent",
    "04_research_assistant"
]

# 创建基础目录
os.makedirs(base_dir, exist_ok=True)
print(f"✅ 创建目录: {base_dir}")

# 创建子文件夹
for sub_dir in sub_dirs:
    full_path = os.path.join(base_dir, sub_dir)
    os.makedirs(full_path, exist_ok=True)
    print(f"✅ 创建子目录: {full_path}")

print("\n🎉 所有目录创建完成！")

