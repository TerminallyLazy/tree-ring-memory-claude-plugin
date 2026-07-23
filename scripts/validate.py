#!/usr/bin/env python3
"""Validate Tree Ring Memory Claude plugin packaging and safety guidance."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_WRAPPER_VERSION = "0.2.0"


def read(relative: str) -> str:
    """Read a UTF-8 repository file."""
    return (ROOT / relative).read_text(encoding="utf-8")


def require_markers(relative: str, markers: list[str]) -> None:
    """Require every contract marker in a repository file."""
    text = read(relative)
    missing = [marker for marker in markers if marker not in text]
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
    if plugins[0].get("version") != EXPECTED_WRAPPER_VERSION:
        raise SystemExit("marketplace plugin version is stale")


def validate_skill() -> None:
    """Validate the bundled skill's v0.13 behavioral contract."""
    relative = "skills/tree-ring-memory/SKILL.md"
    text = read(relative)
    if not text.startswith("---\n"):
        raise SystemExit("SKILL.md must start with YAML frontmatter")
    require_markers(
        relative,
        [
            "tree-ring 0.13.0",
            "--agent-profile",
            "--workflow-id",
            "--session-id",
            "--operation-id",
            "--source-ref",
            "TREE_RING_COORDINATOR_TOKEN",
            "one host",
            "local filesystem",
            "not a read ACL",
            "schema v3",
            "Mixed-version operation is unsupported",
        ],
    )


def validate_readme() -> None:
    """Validate public install, migration, and boundary guidance."""
    require_markers(
        "README.md",
        [
            "v0.13.0",
            "schema v3",
            "Mixed v0.12/v0.13 operation is unsupported",
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
            "Mixed-version operation is unsupported",
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
        ],
    )


def validate_workflow() -> None:
    """Validate that CI executes a checksum-pinned v0.13 runtime smoke."""
    require_markers(
        ".github/workflows/validate.yml",
        [
            'TREE_RING_VERSION: "0.13.0"',
            "cbe4c108c8881b2df1b72a26bfc86396dcdccba66fc8b976f340012e8c095e7d",
            "sha256sum --check --status",
            "bash scripts/smoke_v013.sh",
        ],
    )
    require_markers(
        "scripts/smoke_v013.sh",
        [
            "tree-ring 0.13.0",
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
