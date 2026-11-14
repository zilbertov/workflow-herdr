# Owner trust policy

The default is CLI-policy inheritance. To explicitly use broad process permissions on a trusted root, run `python <skill>/scripts/trust_policy.py --project <absolute-root> --full-trust`. This is a deliberate one-time owner decision; do not ask it again during unchanged authorized work.

Add `--auto-confirm-workspace` only when acceptance of the Codex workspace prompt is also intended. The helper requires a recognized trust screen, visibly selected Yes, a single Enter and a recognized composer afterwards. Otherwise it reports a specific blocked state without submitting a prompt. A bare Yes/No list is ambiguous and is not clicked.

Use `--revoke` to remove a root grant. Grants match resolved roots exactly; they do not authorize descendants, sibling repos or all future worktrees. A worktree may inherit the normal CLI policy, but explicit owner trust must be recorded for its own root. Project `.herdr/workflow.yaml` cannot self-authorize these flags.

The registry defaults to `~/.config/agent-guardrails/workflow-trust.json` (owner-controlled `WORKFLOW_HERDR_TRUST_FILE` override). New registry files use private permissions and atomic replacement; concurrent manual edits should be serialized. No credentials are stored. Do not put a trust registry under attacker-controlled project content.

Project-controlled launch mappings, harness definitions and legacy native argv overrides require an owner grant. Without it, bundled mappings are used; project `mappings/` cannot override them implicitly. Role briefs and expanded layout paths must stay in their allowed roots, including resolved symlinks, regardless of full trust.
