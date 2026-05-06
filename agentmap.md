四个阶段，建议顺序学习：

**一 → [[基础]]**：先把 LLM 能力边界摸清，理解 function calling，再看 ReAct / CoT 等 agent 思维模式，最后补 memory 和 planning。

**二 → [[框架]]**：选一个主线（推荐 LangGraph，更底层可控），手写一遍简单 agent，再研究 Tool use 和向量库。

**三 → [[实战]]**：按复杂度递进——代码助手 → RAG 问答 → 浏览器 agent → 多 agent 系统，每个都要跑通再推进。

**四 → [[生产]]**：eval 体系 + tracing 是最容易被跳过但最重要的，上线前必须补。

时间参考：有 Python 基础的话，阶段一二约 2 周，阶段三约 1 个月，阶段四持续迭代。