# Contract and acceptance

Before implementation identify the requested outcome, existing contract/source of truth, allowed files/services, prohibited side effects and observable acceptance. Resolve only ambiguities that materially change these facts; reuse the user's existing answers and permissions.

Plan at the risk level of the task. A tiny fix can use one sentence; multiple workstreams need file ownership, dependencies, a checkpoint and a rollback for external writes. Prefer existing tools and architecture. Do not fabricate a product rule from current buggy code.

Implementation stays within the contract. When a new fact changes scope, record it and continue independent work; escalate only the dependent decision. Full trust changes execution permissions, not the requested objective.

Acceptance records source/diff, commands with exit status, observed behavior, remaining uncertainty, and the receipt author. A green unit suite does not prove deployment. An idle worker is not done. A timeout does not establish that an external action failed: inspect correlated evidence before retrying it. Never call a waived check a passed check.
