# Awesome AI 生产准备度资源清单

[English README](README.md)

本仓库收录 57 项公开资源，帮助团队判断 AI 原型进入真实业务流程前还缺什么。范围包括评估、可观测性、安全护栏、治理、文档、部署和运行责任。

它不是热门项目排行榜，也不代表维护者对所列项目作安全背书。资源是否适用，仍需结合你的业务流程、数据边界和风险等级判断。

## 从问题开始

| 当前问题 | 建议入口 |
|---|---|
| 不知道原型离受控试点还差什么 | [生产路径](docs/production_path.md) |
| 需要快速选择一组基础工具 | [推荐起步组合](docs/recommended_starting_set.md) |
| 已经知道缺口，准备查具体工具 | [英文主清单](README.md#quick-decision-map) |
| 想了解资源为什么被收录或移除 | [收录规则](docs/curation_policy.md) |
| 想复用机器可读数据 | [`data/resources.json`](data/resources.json) |

## 资源覆盖范围

- Prompt、RAG 和 Agent 评估；
- Trace、监控和线上可观测性；
- 输入输出校验与安全护栏；
- LLM 安全测试和红队工具；
- AI 治理、风险管理和系统文档；
- 公平性、可解释性和以人为本设计；
- 模型服务、MLOps 和部署基础设施；
- FDE、解决方案架构和运行交接。

## 三个仓库如何配合

```text
查找工具和标准
  → Awesome AI Production Readiness
判断原型是否具备进入受控流程的结构条件
  → AI Prototype-to-Production Toolkit
把评估结果变成可供负责人审议的决策包
  → Research-to-Decision Toolkit
```

- [AI Prototype-to-Production Toolkit](https://github.com/Anonymousyz/ai-prototype-to-production-toolkit)
- [Research-to-Decision Toolkit](https://github.com/Anonymousyz/research-to-decision-toolkit)

## 使用边界

1. 链接可以访问，不等于项目仍在维护；归档项目会单独标注。
2. 被收录不等于通过安全、合规或许可证审查。
3. 同一工具在不同架构、数据和行业中可能得出不同结论。
4. 本清单不能替代威胁建模、供应链审查、数据保护评估或人工审批。
5. 维护者自己的项目会明确披露，不按星标数量优先推荐。

## 本地验证

```bash
python scripts/export_resources.py --curated-at YYYY-MM-DD
python -m unittest discover -s tests -v
python scripts/check_links.py
```

导出脚本会把英文 README 中的资源条目转换为 `data/resources.json`。重复 URL 会直接报错。链接检查会区分正常响应、访问限制和明确失败；自动化检查不能代替人工判断资源质量。

## 贡献与许可

提交资源前请阅读 [`CONTRIBUTING.md`](CONTRIBUTING.md) 和 [`docs/curation_policy.md`](docs/curation_policy.md)，并披露你与项目的关系。

本清单采用 CC0-1.0。各项目仍受其自身许可证约束。
