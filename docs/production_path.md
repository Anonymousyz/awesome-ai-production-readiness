# A production path, not a shopping list

A team does not move from a demo to production by picking one more framework. The work usually follows a path:

| Step | Question | Start with | Companion artifact |
|---|---|---|---|
| 1. Frame | Which workflow is changing and who owns the decision? | [AI Prototype-to-Production Toolkit](https://github.com/Anonymousyz/ai-prototype-to-production-toolkit) | discovery guide, readiness checklist |
| 2. Test | What does acceptable output look like, and how will failure appear? | Evaluation and testing | evaluation plan, test set, threshold |
| 3. Control | What data, permissions, guardrails, logs, and overrides are required? | Guardrails, security, governance, and documentation | risk register, system card, control design |
| 4. Operate | Who monitors cost, incidents, adoption, and rollback? | Observability, deployment, and MLOps | operating owner, runbook, rollback condition |
| 5. Decide | Which alternative should accountable humans choose? | [Research-to-Decision Toolkit](https://github.com/Anonymousyz/research-to-decision-toolkit) | decision packet, alternatives, pre-mortem, stop condition |

The list is organized by tool category because readers often arrive with a concrete gap. This page shows the order in which those categories become useful in an operating workflow.

A listed project may solve part of one step. No entry, including the two companion repositories, replaces evidence, permission, or accountable human judgment.
