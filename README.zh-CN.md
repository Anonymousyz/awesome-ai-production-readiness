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

## 机器可读 v2 边界

- `data/resources.json` 由英文主清单确定性导出，并由公开 **JSON Schema** 约束字段与归档状态。
- GitHub 项目的 `canonical_url` 与 `archived` 状态需要调用上游元数据核验；仅检查链接能打开不等于元数据已核验。
- `curated_at` 是目录审查/生成日期；可空的 `last_verified` 只在每条资源均被逐项核验后填写，且不能晚于 `curated_at`。
- 链接检查默认采用 `strict`：GitHub canonical/archive 元数据未核验即失败；`--metadata-policy soft` 只用于交互诊断，并会在报告中保留未核验数量。

## 本地验证

```bash
python scripts/export_resources.py --curated-at YYYY-MM-DD
python -m unittest discover -s tests -v
python scripts/check_links.py --metadata-policy strict
```

导出脚本会把英文 README 中的资源条目转换为 `data/resources.json`。重复 URL、非法日期、未来日期和 `last_verified > curated_at` 会直接报错。链接检查区分正常响应、访问限制、明确失败、元数据不一致和元数据未核验；自动化检查不能替代人工判断资源质量。

## 贡献与许可

提交资源前请阅读 [`CONTRIBUTING.md`](CONTRIBUTING.md) 和 [`docs/curation_policy.md`](docs/curation_policy.md)，并披露你与项目的关系。

目录数据、生成的链接检查证据、文字材料和自动化代码不采用同一份笼统许可证。请以 [`LICENSE-SCOPE.md`](LICENSE-SCOPE.md) 的逐路径矩阵为准：目录/文字类路径通过 [`LICENSE`](LICENSE) 采用 CC0-1.0；Python 脚本与测试、`data/resources.schema.json`、CI 模板通过 [`LICENSE-CODE`](LICENSE-CODE) 采用 MIT。根目录 CC0 不适用于这些仅采用 MIT 的路径。各项目、名称、商标、专利及源码仍受其自身权利约束，收录不构成转授权或背书。
