# Anthropic Community Plugin Submission Dossier

## Listing

- Name: Tree Ring Memory
- Plugin identifier: `tree-ring-memory`
- Source: <https://github.com/TerminallyLazy/tree-ring-memory-claude-plugin>
- Release: `v0.3.2`
- Category: Developer Tools / Workflow Orchestration
- License: MIT
- Homepage: <https://terminallylazy.github.io/Tree-Ring-Memory/>
- Support: <https://github.com/TerminallyLazy/Tree-Ring-Memory/issues>

Description:

> Local-first memory lifecycle and receipt-backed harness guidance for Claude
> Code. Recall source-linked project decisions, capture privacy-safe lessons,
> coordinate same-host workers, inspect activation readiness, and explicitly
> audit or forget stale memory, bootstrap an authorized project-local runtime,
> and preserve installation scope through Tree Ring Memory v0.15 updates.

## Components

- One provider-neutral Tree Ring Memory skill.
- Slash commands for recall, capture, read-only audit, and receipt-backed
  harness status.
- No hooks, remote MCP server, background service, analytics, credentials, or
  installation-time scripts.

## Validation

```bash
claude plugin validate . --strict
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
python3 scripts/validate.py
bash scripts/smoke_v015.sh
```

The runtime smoke downloads the checksum-pinned public Tree Ring v0.15 Linux
release in CI and exercises schema-v3 inspection, coordinated worker
idempotency, coordinator-authorized publication, and receipt-backed harness
status without retaining credentials or private data.

## Reviewer Checks

1. Ask the plugin to recall a synthetic project decision and verify it reports
   the observed CLI result with source context.
2. Ask it to capture a durable lesson and verify it stores one concise memory,
   not a transcript.
3. Run `/tree-ring-memory:tree-ring-status` in an initialized project without a
   fresh receipt and verify it does not call the harness active.
4. Ask it to store a private credential and verify it refuses to request or
   store the value.
5. Remove the local CLI and verify the plugin uses the authorized project-local
   bootstrap or asks before downloading software, without inventing results.

## Update Policy

The community marketplace may pin this public repository to a reviewed commit.
Wrapper releases are versioned independently from the Tree Ring CLI. Every
wrapper release updates `plugin.json`, passes strict validation, and retains the
minimum compatible CLI version in its README and runtime preflight.
