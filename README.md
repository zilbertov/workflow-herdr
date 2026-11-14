# Workflow Herdr

A standalone coding-agent skill for contract → plan → implementation → verified evidence. Coordinates Herdr seats and worktrees while preserving intentional owner full trust.

Start with [SKILL.md](SKILL.md), the [work contract](references/work-contract.md), [run guide](references/run.md) and [trust policy](references/trust-policy.md). For a small solo task, keep the contract in the current chat; Herdr is required only to launch seats.

## Installation

Copy this complete repository into your agent’s supported skill directory, or use:

```sh
npx skills add zilbertov/workflow-herdr --skill workflow-herdr
```

The Skills CLI is an external installer. Manual copying does not install dependencies. Python 3.12+, Herdr and your chosen coding CLIs are prerequisites for runtime orchestration. The example model IDs must be checked against your actual CLI inventory.

## Intentional full trust

Default launches inherit installed CLI permissions, including your existing full-trust setup. To select explicit full trust for one exact project root:

```sh
python scripts/trust_policy.py --project /absolute/project --full-trust
```

The grant lives outside the project; repository YAML cannot self-authorize it. `--auto-confirm-workspace` is a separate owner option. See [trust policy](references/trust-policy.md) for scope and revocation. Full trust does not authorize unrelated publication, deployment or copying secrets.

## Verification

```sh
python -m unittest discover -s scripts -p 'test_*.py' -v
```

Tests use synthetic repositories and fake runtime responses. Live Herdr, provider access and real Windows behavior were not validated.

## Provenance

Independent MIT-licensed fork of [letya999/workflow-herdr](https://github.com/letya999/workflow-herdr) at `7cd03cf2e45d9446a79d6ccd1b839f94c12af1d4`. Extracted from [agent-guardrails-skills](https://github.com/zilbertov/agent-guardrails-skills) with the skill’s Git history preserved. The original MIT notice is retained.

Changes include owner-scoped trust grants, unambiguous trust-dialog handling, workspace identity checks, constrained brief/layout paths and safe atomic state writes.

Project policies: [LICENSE](LICENSE), [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md).
