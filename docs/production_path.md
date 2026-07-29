# A practical production path

Teams usually move from a demo toward a production decision through a sequence of questions.

| Step | Question | Start with | Companion artifact |
|---|---|---|---|
| 1. Frame | Which workflow changes, and who owns the decision? | [AI Prototype-to-Production Toolkit](https://github.com/Anonymousyz/ai-prototype-to-production-toolkit) | discovery guide, readiness checklist |
| 2. Test | What counts as acceptable output, and how will failure appear? | Evaluation and testing | evaluation plan, test set, threshold |
| 3. Control | Which data, permissions, guardrails, logs, and overrides are required? | Guardrails, security, governance, and documentation | risk register, system card, control design |
| 4. Operate | Who monitors cost, incidents, adoption, and rollback? | Observability, deployment, and MLOps | operating owner, runbook, rollback condition |
| 5. Decide | Which alternative should responsible people choose? | [Research-to-Decision Toolkit](https://github.com/Anonymousyz/research-to-decision-toolkit) | decision packet, alternatives, pre-mortem, stop condition |

Readers often arrive with a concrete gap, so the catalog is organized by tool category. This page explains the order in which those categories support one operating workflow.

A listed project may address one part of the path. Teams still need to examine evidence, permission, and responsibility before a person approves a deployment.