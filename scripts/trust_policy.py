"""Owner-controlled trust decisions, separate from repository YAML."""
from __future__ import annotations
import argparse, json, os, tempfile
from pathlib import Path

def registry_path() -> Path:
    override = os.environ.get("WORKFLOW_HERDR_TRUST_FILE")
    return Path(override).expanduser() if override else Path.home()/".config"/"agent-guardrails"/"workflow-trust.json"

def policy_for(project: Path | None) -> dict:
    default = {"full_trust": False, "auto_confirm_workspace": False}
    if project is None:
        return default
    p = registry_path()
    if not p.exists():
        return default
    if p.is_symlink():
        raise ValueError("trust registry must not be a symlink")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        entry = data.get("projects", {}).get(str(project.resolve()), {})
    except (ValueError, TypeError, AttributeError) as exc:
        raise ValueError("invalid trust registry; refusing to guess permissions") from exc
    if not isinstance(entry, dict):
        raise ValueError("invalid project trust entry")
    for k in default:
        if k in entry and type(entry[k]) is not bool:
            raise ValueError(f"trust setting {k} must be a boolean")
    return {k: entry.get(k, v) for k,v in default.items()}

def apply_policy(config: dict, project: Path | None) -> dict:
    policy = policy_for(project)
    # Repository overlays cannot self-authorize an OS-level permission bypass.
    config["security"] = policy
    if policy["full_trust"]:
        for name, harness in config.get("harnesses", {}).items():
            prefix = (["--dangerously-bypass-approvals-and-sandbox"] if name == "codex" else ["--permission-mode", "dangerous"] if name == "devin" else [])
            if prefix:
                harness["args"] = prefix + list(harness.get("args") or [])
                harness["_model_args"] = {k: prefix + list(v) for k,v in harness.get("_model_args", {}).items()}
    return config

def set_project(project: Path, *, full_trust: bool, auto_confirm: bool, revoke: bool=False) -> Path:
    project = project.resolve()
    if not project.is_dir():
        raise ValueError("project directory does not exist")
    p = registry_path()
    if p.is_symlink():
        raise ValueError("trust registry must not be a symlink")
    data = json.loads(p.read_text()) if p.exists() else {"projects": {}}
    entries = data.setdefault("projects", {})
    if revoke:
        entries.pop(str(project), None)
    else:
        entries[str(project)] = {"full_trust":full_trust, "auto_confirm_workspace":auto_confirm}
    p.parent.mkdir(parents=True,exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".workflow-trust-", dir=p.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as f:
            json.dump(data,f,indent=2);f.write("\n")
        os.replace(tmp,p)
    finally:
        Path(tmp).unlink(missing_ok=True)
    return p

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="Record an intentional trust decision for one exact project root; does not launch agents")
    parser.add_argument("--project",required=True,type=Path)
    parser.add_argument("--full-trust",action="store_true")
    parser.add_argument("--auto-confirm-workspace",action="store_true")
    parser.add_argument("--revoke",action="store_true")
    args=parser.parse_args()
    print(set_project(args.project,full_trust=args.full_trust,auto_confirm=args.auto_confirm_workspace,revoke=args.revoke))
