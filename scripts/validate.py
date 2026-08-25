#!/usr/bin/env python3
"""Validate Tree Ring Memory Claude plugin packaging and safety guidance."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_WRAPPER_VERSION = "0.3.2"
UNSAFE_TOKEN_EXPORT = "export TREE_RING_COORDINATOR_TOKEN='<"
CANONICAL_ISSUES = "https://github.com/TerminallyLazy/Tree-Ring-Memory/issues"
CANONICAL_ADVISORY = "https://github.com/TerminallyLazy/Tree-Ring-Memory/security/advisories/new"


def read(relative: str) -> str:
    """Read a UTF-8 repository file."""
    return (ROOT / relative).read_text(encoding="utf-8")


def require_markers(relative: str, markers: list[str]) -> None:
    """Require every contract marker in a repository file."""
    text = " ".join(read(relative).split())
    missing = [marker for marker in markers if " ".join(marker.split()) not in text]
    if missing:
        raise SystemExit(f"{relative} is missing: {', '.join(missing)}")


def validate_manifests() -> None:
    """Validate package identity and synchronized wrapper versions."""
    plugin = json.loads(read(".claude-plugin/plugin.json"))
    marketplace = json.loads(read(".claude-plugin/marketplace.json"))

    if plugin.get("name") != "tree-ring-memory":
        raise SystemExit("plugin.json name must be tree-ring-memory")
    if plugin.get("version") != EXPECTED_WRAPPER_VERSION:
        raise SystemExit("plugin.json wrapper version is stale")
    if marketplace.get("version") != EXPECTED_WRAPPER_VERSION:
        raise SystemExit("marketplace wrapper version is stale")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        raise SystemExit("marketplace.json must contain exactly one plugin")
    if plugins[0].get("source") != "./":
        raise SystemExit("marketplace plugin source must be ./")
    if "version" in plugins[0]:
        raise SystemExit(
            "marketplace entry must defer to plugin.json as the version authority"
        )


def validate_skill() -> None:
    """Validate the bundled skill's v0.15 behavioral contract."""
    relative = "skills/tree-ring-memory/SKILL.md"
    text = read(relative)
    if not text.startswith("---\n"):
        raise SystemExit("SKILL.md must start with YAML frontmatter")
    require_markers(
        relative,
        [
            "0.15.0 or newer",
            "Runtime Bootstrap And Updates",
            "--project --init --release latest --no-animation",
            "tree-ring update --check",
            "DOX Contract Flow",
            "tree-ring dox sync --source-root <path> --dry-run",
            "Certification Boundary",
            "tree-ring integrations certify --source-root .",
            "tree-ring recall-quality --source-root .",
            "full framework release suite",
            "tree-ring integrations status",
            "configured-awaiting-proof",
            "active-isolated",
            "needs-plugin",
            "--agent-profile",
            "--workflow-id",
            "--session-id",
            "--operation-id",
            "--source-ref",
            "TREE_RING_COORDINATOR_TOKEN",
            "history-safe, no-echo",
            "same-host local-filesystem processes",
            "not a read ACL",
            "schema v3",
            "operation is unsupported",
        ],
    )


def validate_readme() -> None:
    """Validate public install, migration, and boundary guidance."""
    require_markers(
        "README.md",
        [
            "v0.15.0",
            "Receipt-Backed Harness Readiness",
            "configured-awaiting-proof",
            "needs-user-review",
            "schema v3",
            "mixed-version operation is unsupported",
            "one host",
            "local filesystem",
            "not read access-control boundaries",
            "TREE_RING_COORDINATOR_TOKEN",
        ],
    )


def validate_commands() -> None:
    """Validate safe capture, recall, audit, and lifecycle commands."""
    require_markers(
        "commands/tree-ring-capture.md",
        [
            "--scope agent",
            "--agent-profile",
            "--workflow-id",
            "--session-id",
            "--operation-id",
            "--source-ref",
            "TREE_RING_COORDINATOR_TOKEN",
            "0.15.0 or newer",
        ],
    )
    require_markers(
        "commands/tree-ring-recall.md",
        [
            "env -u TREE_RING_AGENT_PROFILE",
            "--workflow-id",
            "--session-id",
            "--scope agent",
            "not read ACLs",
        ],
    )
    require_markers(
        "commands/tree-ring-audit.md",
        [
            "tree-ring policy status",
            "tree-ring policy audit --limit 100",
            "The CLI forget modes are `redact` and `delete`",
            "`/supersede <old_id>`",
            "never create or migrate a store",
            "mixed-version operation is unsupported",
        ],
    )
    require_markers(
        "commands/tree-ring-certify.md",
        [
            "tree-ring integrations certify --source-root <project-root>",
            "tree-ring recall-quality --source-root <project-root>",
            "repository-only",
            "does not execute the suite",
        ],
    )
    require_markers(
        "commands/tree-ring-dox-sync.md",
        [
            "tree-ring dox sync --source-root",
            "--dry-run",
            "Current source contracts are authoritative",
            "must not rewrite root or child `AGENTS.md` files",
            "TREE_RING_COORDINATOR_TOKEN",
        ],
    )
    require_markers(
        "commands/tree-ring-status.md",
        [
            "tree-ring integrations status --json --verbose",
            "configured-awaiting-proof",
            "needs-project-mount",
            "needs-plugin",
            "needs-user-review",
            "Do not modify global trust",
        ],
    )
    require_markers(
        "commands/tree-ring-update.md",
        [
            "tree-ring update --check",
            "preserve the active",
            "CLIs older than 0.15.0",
            "--root .tree-ring init",
        ],
    )

    all_markdown = "\n".join(
        path.read_text(encoding="utf-8")
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts
    )
    if re.search(r"tree-ring\s+forget[^\n]*--mode\s+supersede", all_markdown):
        raise SystemExit("found unsupported `forget --mode supersede` guidance")
    if "--coordinator-token" in all_markdown:
        raise SystemExit("coordinator capability must never be described as a CLI flag")

    audit = read("commands/tree-ring-audit.md")
    inspection_section = audit.split(
        "After the verified schema-v3 upgrade, start with non-mutating inspection:",
        maxsplit=1,
    )[1].split("If the user names a focus", maxsplit=1)[0]
    for apply_flag in ("--repair-fts", "--apply-expired", "--apply-secret-redactions"):
        if apply_flag in inspection_section:
            raise SystemExit(
                f"non-mutating inspection contains mutating flag {apply_flag}"
            )


def validate_security_boundary() -> None:
    """Validate coordinator capability and supported-boundary warnings."""
    require_markers(
        "SECURITY.md",
        [
            "TREE_RING_COORDINATOR_TOKEN",
            "not a read ACL",
            "one host",
            "local filesystem",
            "network-filesystem safety",
            "Harness Readiness",
            "Configuration alone is not",
            CANONICAL_ADVISORY,
            CANONICAL_ISSUES,
        ],
    )

    require_markers(
        "PRIVACY.md",
        [
            "does not operate a hosted service",
            "local SQLite database",
            "does not receive that database",
            CANONICAL_ISSUES,
        ],
    )
    require_markers(
        "TERMS.md",
        [
            "MIT License",
            "provided without warranty",
            CANONICAL_ISSUES,
        ],
    )
    require_markers(
        "SUBMISSION.md",
        [
            "v0.3.2",
            "claude plugin validate . --strict",
            "smoke_v015.sh",
        ],
    )
    skill = read("skills/tree-ring-memory/SKILL.md")
    if UNSAFE_TOKEN_EXPORT in skill:
        raise SystemExit("token-bearing export example must not appear in the skill")
    public_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.resolve() != Path(__file__).resolve()
        and path.suffix.lower()
        in {".json", ".md", ".py", ".sh", ".toml", ".txt", ".yaml", ".yml"}
    )
    if "tree-ring-memory-claude-plugin/issues" in public_text:
        raise SystemExit("support and security links must use the canonical repository")


def validate_workflow() -> None:
    """Validate that CI executes a checksum-pinned v0.15 runtime smoke."""
    require_markers(
        ".github/workflows/validate.yml",
        [
            "actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd",
            'TREE_RING_VERSION: "0.15.0"',
            "9b47873268dbb94712a49b02bd785cc69507facee1e879e46e6922778b4afbe6",
            "sha256sum --check --status",
            "bash scripts/smoke_v015.sh",
        ],
    )
    require_markers(
        "scripts/smoke_v015.sh",
        [
            "tree-ring 0.15.0",
            "integrations status --json --verbose",
            "fresh configuration must not report active",
            "TREE_RING_COORDINATOR_TOKEN",
            "--operation-id",
            "policy status",
            "policy audit --limit 100",
            "legacy-v2",
        ],
    )


def main() -> None:
    """Run every package, documentation, security, and CI contract check."""
    validate_manifests()
    validate_skill()
    validate_readme()
    validate_commands()
    validate_security_boundary()
    validate_workflow()
    print("Tree Ring Memory Claude plugin validation passed")


if __name__ == "__main__":
    main()
