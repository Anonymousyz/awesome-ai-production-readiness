# Awesome AI 生产准备度

这是一个聚焦 AI 从 demo / prototype 走向 production 的资源清单。

核心问题：

> 一个 AI 原型看起来能跑，是否真的可以进入真实业务流程？

本清单关注：

- eval / 测试；
- observability / 监控；
- guardrails / 安全护栏；
- AI governance / 负责任 AI；
- model card / system card；
- human-centered AI；
- LLM 安全；
- RAG / Agent 生产化；
- FDE / AI 落地工作流。

建议先看英文 README，再按 `docs/decision_map.md` 选择工具。

## 核心判断

本清单采用一个生产化判断框架：

> 生产级 AI = 业务流程 + 评估证据 + 治理机制 + 责任链。

也就是说，AI demo 能跑，不等于可以进入真实业务流程。生产化还需要回答数据边界、质量评估、人工复核、审计日志、成本归属、事故责任和回滚机制等问题。

相关思想宣言：

https://github.com/Anonymousyz/ai-prototype-to-production-toolkit/blob/main/MANIFESTO.md
