# Agent 基础概念实践项目构建计划

## 一、需求分析

根据 `基础.md` 文件内容，需要构建以下项目结构：

```
01_foundations/
├── .env
├── 01_prompt_basics.py
├── 02_function_calling.py
├── 03_react_loop.py
└── 04_memory_demo.py
```

## 二、依赖清单

| 依赖包 | 版本要求 | 用途 |
|--------|----------|------|
| python | >= 3.10 | 运行环境 |
| openai | latest | 兼容 longcat API（使用 OpenAI 格式） |
| python-dotenv | latest | 加载环境变量 |

## 三、文件创建清单

| 文件 | 内容说明 |
|------|----------|
| `.env` | API Key 和 Base URL 配置文件 |
| `01_prompt_basics.py` | Prompt 结构示例代码（适配 longcat API） |
| `02_function_calling.py` | Function Calling 实现（适配 longcat API） |
| `03_react_loop.py` | ReAct 循环实现（适配 longcat API） |
| `04_memory_demo.py` | 对话记忆实现（适配 longcat API） |

## 四、执行步骤

1. 安装 Python 依赖包
2. 创建 `01_foundations/` 目录
3. 创建 `.env` 文件（配置 longcat API）
4. 创建四个 Python 文件

## 五、longcat API 适配方案

longcat 作为 API 服务，假设支持 OpenAI 兼容格式：
- 使用 `openai` 库，配置自定义 base_url
- 支持标准的 chat completion 接口

## 六、风险提示

1. 需要用户手动在 `.env` 文件中填入有效的 longcat API Key 和 Base URL
2. 确保网络可访问 longcat API 服务

## 七、验证方式

运行 `python 01_prompt_basics.py` 验证基础功能是否正常
