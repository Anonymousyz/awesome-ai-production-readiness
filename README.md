# Awesome AI Production Readiness

![Awesome](https://awesome.re/badge.svg)
![License: CC0](https://img.shields.io/badge/license-CC0-lightgrey.svg)

A curated list of tools, frameworks, guides, and templates for moving AI systems from prototype to production.

The focus is practical production readiness:

- evaluation;
- observability;
- guardrails;
- governance;
- model/system documentation;
- human-centered AI;
- risk management;
- deployment checklists;
- FDE / applied AI workflows.

> If an AI demo works, what must be true before it enters a real business workflow?

---

## Contents

- [Evaluation and testing](#evaluation-and-testing)
- [Observability and monitoring](#observability-and-monitoring)
- [Guardrails and safety](#guardrails-and-safety)
- [Responsible AI and governance](#responsible-ai-and-governance)
- [Model/system documentation](#modelsystem-documentation)
- [Human-centered AI](#human-centered-ai)
- [Security and risk frameworks](#security-and-risk-frameworks)
- [Production readiness checklists](#production-readiness-checklists)
- [FDE and deployment workflow](#fde-and-deployment-workflow)

---

## Evaluation and testing

- [OpenAI Evals](https://github.com/openai/evals) — Framework for evaluating LLMs and LLM systems; useful for custom evals and benchmark registries.
- [promptfoo](https://github.com/promptfoo/promptfoo) — Test prompts, agents and RAGs; supports red teaming, model comparison and CI/CD.
- [DeepEval](https://github.com/confident-ai/deepeval) — Pytest-like LLM evaluation framework with RAG, agentic, hallucination, toxicity and custom metrics.
- [RAGAS](https://github.com/vibrantlabsai/ragas) — Evaluation framework for retrieval-augmented generation applications.

## Observability and monitoring

- [Arize Phoenix](https://github.com/Arize-ai/phoenix) — Open-source AI observability and evaluation platform for tracing, datasets, experiments and prompt management.
- [Opik](https://github.com/comet-ml/opik) — Open-source platform for debugging, evaluating and monitoring LLM applications, RAG systems and agentic workflows.

## Guardrails and safety

- [NVIDIA NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) — Programmable guardrails for LLM conversational systems.
- [Guardrails AI](https://github.com/guardrails-ai/guardrails) — Input/output guards, validators and structured output validation for LLM applications.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — Security risks and guidance for LLM applications.

## Responsible AI and governance

- [Microsoft Responsible AI Toolbox](https://github.com/microsoft/responsible-ai-toolbox) — Model assessment dashboards for error analysis, fairness, interpretability and responsible AI workflows.
- [Fairlearn](https://github.com/fairlearn/fairlearn) — Python package for assessing and improving fairness of machine learning systems.
- [AIF360](https://github.com/Trusted-AI/AIF360) — IBM toolkit with fairness metrics and bias mitigation algorithms.
- [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit) — Agent governance, policy enforcement, zero-trust identity, sandboxing and reliability engineering.

## Model/system documentation

- [TensorFlow Model Card Toolkit](https://github.com/tensorflow/model-card-toolkit) — Toolkit for generating model cards and documenting model development/performance.
- [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993) — Foundational paper on model cards.

## Human-centered AI

- [Google People + AI Guidebook](https://pair.withgoogle.com/guidebook/) — Practical guidance for human-centered AI products, feedback, trust, autonomy and error handling.

## Security and risk frameworks

- [NIST AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/) — Suggested actions mapped to NIST AI RMF Govern, Map, Measure and Manage functions.
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — US government AI risk management framework.
- [OWASP GenAI Security Project](https://genai.owasp.org/) — Security and safety resources for generative AI systems.

## Production readiness checklists

- [AI Prototype-to-Production Toolkit](https://github.com/your-name/ai-prototype-to-production-toolkit) — Checklists, scorecards, prompts and risk templates for assessing AI prototype readiness. Replace with final public URL after launch.

## FDE and deployment workflow

- [OpenAI Cookbook](https://github.com/openai/openai-cookbook) — Practical examples and guides for working with the OpenAI API.
- [AI Prototype-to-Production Toolkit](https://github.com/your-name/ai-prototype-to-production-toolkit) — FDE discovery guide, pilot memo and readiness review templates. Replace with final public URL after launch.

---

## Contribution guidelines

Add resources that help teams move AI systems from demos into real workflows.

Good entries should be:

- practical;
- public;
- actively maintained or historically important;
- relevant to evaluation, observability, guardrails, governance, documentation, human oversight, or production readiness.

Please avoid vendor-only marketing pages without reusable technical or governance value.

---

## Related project

This list is maintained alongside the [AI Prototype-to-Production Toolkit](https://github.com/your-name/ai-prototype-to-production-toolkit), a practical readiness toolkit for enterprise and regulated AI deployment.

---

## License

CC0-1.0 for this curated list. Individual projects have their own licenses.
