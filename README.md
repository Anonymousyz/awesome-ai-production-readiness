# Awesome AI Production Readiness

![Awesome](https://awesome.re/badge.svg)
![License: CC0](https://img.shields.io/badge/license-CC0-lightgrey.svg)
![Focus: Production AI](https://img.shields.io/badge/focus-production%20AI-blue)
![Topics: evals guardrails governance](https://img.shields.io/badge/topics-evals%20%7C%20guardrails%20%7C%20governance-green)

A curated list of tools, frameworks, guides, and templates for moving AI systems from prototype to production.

The focus is practical production readiness:

- evaluation and testing;
- observability and monitoring;
- guardrails and safety;
- responsible AI and governance;
- model/system documentation;
- human-centered AI;
- security and risk frameworks;
- deployment infrastructure;
- FDE / applied AI workflows.

> If an AI demo works, what must be true before it enters a real business workflow?

---

## Production readiness lens

This list is curated through one lens:

> **Production-ready AI = workflow + evidence + governance + accountability.**

The related manifesto is here: [AI Production Readiness Manifesto](https://github.com/Anonymousyz/ai-prototype-to-production-toolkit/blob/main/MANIFESTO.md).

This means the list prioritizes resources that help teams answer production questions, not only model capability questions.

---

## Contents

- [Quick decision map](#quick-decision-map)
- [Evaluation and testing](#evaluation-and-testing)
- [Observability and monitoring](#observability-and-monitoring)
- [Guardrails and safety](#guardrails-and-safety)
- [Responsible AI and governance](#responsible-ai-and-governance)
- [Model/system documentation](#modelsystem-documentation)
- [Human-centered AI](#human-centered-ai)
- [Security and risk frameworks](#security-and-risk-frameworks)
- [RAG and agent production patterns](#rag-and-agent-production-patterns)
- [Deployment and MLOps infrastructure](#deployment-and-mlops-infrastructure)
- [Production readiness checklists](#production-readiness-checklists)
- [FDE and deployment workflow](#fde-and-deployment-workflow)
- [Chinese intro](#chinese-intro)

---

## Quick decision map

| If you need to... | Start with |
|---|---|
| Test prompts, RAG outputs or agents before shipping | promptfoo, DeepEval, OpenAI Evals, RAGAS |
| Monitor LLM traces and production behavior | Phoenix, Opik, Langfuse, Helicone |
| Add input/output validation and guardrails | Guardrails AI, NeMo Guardrails, LLM Guard |
| Identify LLM security risks | OWASP LLM Top 10, garak, PyRIT |
| Create governance or risk documentation | NIST AI RMF, Model Card Toolkit, AI Prototype-to-Production Toolkit |
| Assess fairness and model risk | Fairlearn, AIF360, Responsible AI Toolbox |
| Build production RAG or agent apps | LlamaIndex, LangChain, LangGraph, Haystack, DSPy |
| Deploy models and services | BentoML, KServe, Seldon Core, Ray Serve, MLflow |

See also [`docs/decision_map.md`](docs/decision_map.md).

---

## Evaluation and testing

- [OpenAI Evals](https://github.com/openai/evals) — Framework for evaluating LLMs and LLM systems; useful for custom evals and benchmark registries.
- [promptfoo](https://github.com/promptfoo/promptfoo) — Test prompts, agents and RAGs; supports red teaming, model comparison and CI/CD.
- [DeepEval](https://github.com/confident-ai/deepeval) — Pytest-like LLM evaluation framework with RAG, agentic, hallucination, toxicity and custom metrics.
- [RAGAS](https://github.com/explodinggradients/ragas) — Evaluation framework for retrieval-augmented generation applications.
- [Giskard](https://github.com/Giskard-AI/giskard) — Testing framework for ML and LLM systems with vulnerability detection.
- [Evidently](https://github.com/evidentlyai/evidently) — ML and LLM evaluation, monitoring and drift reports.
- [TruLens](https://github.com/truera/trulens) — Evaluation and tracking for LLM applications.
- [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) — Language model evaluation harness used across many benchmarks.

## Observability and monitoring

- [Arize Phoenix](https://github.com/Arize-ai/phoenix) — Open-source AI observability and evaluation platform for tracing, datasets, experiments and prompt management.
- [Opik](https://github.com/comet-ml/opik) — Open-source platform for debugging, evaluating and monitoring LLM applications, RAG systems and agentic workflows.
- [Langfuse](https://github.com/langfuse/langfuse) — Open-source LLM engineering platform for traces, evaluations, prompt management and metrics.
- [Helicone](https://github.com/Helicone/helicone) — Open-source LLM observability platform and gateway.
- [OpenTelemetry](https://github.com/open-telemetry/opentelemetry-collector) — Observability collector; useful foundation for production telemetry.
- [WhyLabs](https://github.com/whylabs/whylogs) — Data and ML logging/profiling for monitoring pipelines.

## Guardrails and safety

- [NVIDIA NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) — Programmable guardrails for LLM conversational systems.
- [Guardrails AI](https://github.com/guardrails-ai/guardrails) — Input/output guards, validators and structured output validation for LLM applications.
- [LLM Guard](https://github.com/protectai/llm-guard) — Security toolkit for sanitizing prompts and outputs in LLM applications.
- [Rebuff](https://github.com/protectai/rebuff) — Prompt injection detection and prevention toolkit.
- [Llama Guard](https://github.com/meta-llama/PurpleLlama) — Meta Purple Llama safety tools including Llama Guard resources.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — Security risks and guidance for LLM applications.

## Responsible AI and governance

- [Microsoft Responsible AI Toolbox](https://github.com/microsoft/responsible-ai-toolbox) — Model assessment dashboards for error analysis, fairness, interpretability and responsible AI workflows.
- [Fairlearn](https://github.com/fairlearn/fairlearn) — Python package for assessing and improving fairness of machine learning systems.
- [AIF360](https://github.com/Trusted-AI/AIF360) — IBM toolkit with fairness metrics and bias mitigation algorithms.
- [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit) — Agent governance, policy enforcement, zero-trust identity, sandboxing and reliability engineering.
- [AI Verify](https://github.com/aiverify-foundation/aiverify) — AI governance testing framework and software toolkit.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — AI Risk Management Framework.
- [OECD AI Principles](https://oecd.ai/en/ai-principles) — International AI policy principles.

## Model/system documentation

- [TensorFlow Model Card Toolkit](https://github.com/tensorflow/model-card-toolkit) — Toolkit for generating model cards and documenting model development/performance.
- [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993) — Foundational paper on model cards.
- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) — Foundational documentation pattern for datasets.
- [Hugging Face Model Cards](https://huggingface.co/docs/hub/model-cards) — Practical model card documentation pattern used by the HF ecosystem.

## Human-centered AI

- [Google People + AI Guidebook](https://pair.withgoogle.com/guidebook/) — Practical guidance for human-centered AI products, feedback, trust, autonomy and error handling.
- [Microsoft HAX Toolkit](https://www.microsoft.com/en-us/haxtoolkit/) — Human-AI interaction guidelines and workbook.
- [PAIR Guidebook: User Needs + Defining Success](https://pair.withgoogle.com/guidebook/chapters/user-needs/) — Useful for defining human-centered success criteria.

## Security and risk frameworks

- [NIST AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/) — Suggested actions mapped to NIST AI RMF Govern, Map, Measure and Manage functions.
- [OWASP GenAI Security Project](https://genai.owasp.org/) — Security and safety resources for generative AI systems.
- [garak](https://github.com/NVIDIA/garak) — LLM vulnerability scanner.
- [PyRIT](https://github.com/Azure/PyRIT) — Python Risk Identification Tool for generative AI red teaming.
- [Microsoft Counterfit](https://github.com/Azure/counterfit) — Automation for assessing security of AI systems.
- [Presidio](https://github.com/microsoft/presidio) — Data protection and PII detection/anonymization toolkit.

## RAG and agent production patterns

- [LangChain](https://github.com/langchain-ai/langchain) — Framework for LLM applications and integrations.
- [LangGraph](https://github.com/langchain-ai/langgraph) — Framework for controllable agent workflows.
- [LlamaIndex](https://github.com/run-llama/llama_index) — Data framework for LLM and RAG applications.
- [Haystack](https://github.com/deepset-ai/haystack) — Framework for production NLP and RAG pipelines.
- [DSPy](https://github.com/stanfordnlp/dspy) — Programming model for optimizing LM pipelines.
- [Microsoft AutoGen](https://github.com/microsoft/autogen) — Multi-agent AI application framework.
- [CrewAI](https://github.com/crewAIInc/crewAI) — Multi-agent automation framework.

## Deployment and MLOps infrastructure

- [MLflow](https://github.com/mlflow/mlflow) — ML lifecycle platform for tracking, packaging and model registry.
- [BentoML](https://github.com/bentoml/BentoML) — Model serving and AI application deployment framework.
- [KServe](https://github.com/kserve/kserve) — Kubernetes model inference platform.
- [Seldon Core](https://github.com/SeldonIO/seldon-core) — Model deployment and monitoring on Kubernetes.
- [Ray Serve](https://github.com/ray-project/ray) — Scalable model serving framework in Ray.
- [DVC](https://github.com/iterative/dvc) — Data and model versioning.
- [lakeFS](https://github.com/treeverse/lakeFS) — Data version control for object storage.

## Production readiness checklists

- [AI Prototype-to-Production Toolkit](https://github.com/Anonymousyz/ai-prototype-to-production-toolkit) — Checklists, scorecards, prompts and risk templates for assessing AI prototype readiness.
- [NIST AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/) — Use Govern/Map/Measure/Manage to structure readiness review.
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — Use as a security checklist for LLM applications.

## FDE and deployment workflow

- [OpenAI Cookbook](https://github.com/openai/openai-cookbook) — Practical examples and guides for working with the OpenAI API.
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) — Practical Claude examples and recipes.
- [AI Prototype-to-Production Toolkit](https://github.com/Anonymousyz/ai-prototype-to-production-toolkit) — FDE discovery guide, pilot memo and readiness review templates.

---

## Chinese intro

这个仓库不是泛泛的 AI 资料清单，而是聚焦一个问题：

> 一个 AI demo 如果要进入真实业务流程，还差哪些生产化条件？

适合关注：AI 落地、FDE、LLMOps、AI 治理、模型评估、RAG/Agent 生产化、受监管行业 AI 部署的人收藏。

---

## Contribution guidelines

Add resources that help teams move AI systems from demos into real workflows.

Good entries should be:

- practical;
- public;
- actively maintained or historically important;
- relevant to evaluation, observability, guardrails, governance, documentation, human oversight, security, deployment, or production readiness.

Please avoid vendor-only marketing pages without reusable technical or governance value.

---

## Related project

This list is maintained alongside the [AI Prototype-to-Production Toolkit](https://github.com/Anonymousyz/ai-prototype-to-production-toolkit), a practical readiness toolkit for enterprise and regulated AI deployment.

---

## License

CC0-1.0 for this curated list. Individual projects have their own licenses.
