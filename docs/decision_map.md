# Decision map: what to use when

| Situation | Useful tools/frameworks | Why |
|---|---|---|
| You have a demo and need to decide pilot vs production | AI Prototype-to-Production Toolkit, NIST AI RMF | Turn vague readiness into scored evidence and risk actions |
| You need prompt/RAG/agent regression tests | promptfoo, DeepEval, OpenAI Evals, RAGAS | Convert model behavior into repeatable tests |
| You need production tracing | Phoenix, Opik, Langfuse, Helicone | Trace prompts, responses, latency, cost, failures and feedback |
| You need to reduce prompt injection and unsafe outputs | Guardrails AI, NeMo Guardrails, garak, PyRIT | Test and constrain input/output behavior |
| You need governance evidence | NIST AI RMF, AI Verify, Responsible AI Toolbox | Document system purpose, risk, fairness and controls |
| You need human-centered product review | Google People + AI Guidebook, Microsoft HAX Toolkit | Design for trust, feedback, autonomy and error recovery |
| You need serving and deployment | BentoML, KServe, Ray Serve, Seldon Core, MLflow | Package, serve and monitor models in production environments |
