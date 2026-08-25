# Tree Ring Memory Claude Code Plugin

Tree Ring Memory is a local-first memory lifecycle practice for Claude Code
agents.

This plugin packages one Claude Code skill plus a few explicit slash commands
that teach agents when to recall, write, audit, consolidate, and forget project
memory using the open-source
[Tree Ring Memory](https://github.com/TerminallyLazy/Tree-Ring-Memory) CLI.

It does not run a background service, scrape chats, capture transcripts, install
hooks, or ship a networked MCP server. The active agent chooses when a memory
action is useful, source-linked, and privacy-safe.

## What It Adds

- Recall before context-dependent project work.
- Concise memory writes for validated decisions, lessons, warnings, and user
  preferences.
- Evidence-backed outcomes through `tree-ring evidence`.
- Explicit forgetting, redaction, and supersession guidance.
- DOX and Revolve adapter usage with dry-run-first guardrails.
- Same-host multi-agent identity, idempotency, filtered fan-in, and optional
  coordinator write-policy guidance.
- Receipt-backed harness readiness that distinguishes configured bridges from
  observed use in a fresh Claude Code session.
- Verified project-local CLI bootstrap and scope-preserving update guidance.

## Install Tree Ring Memory

From the actual project root, after the user has authorized Tree Ring setup:

Download the official version-pinned `v0.15.0/install.sh` to a temporary file,
verify its SHA-256 is
`ef0d5eb8f09cbe2e4c3abe80ee9a98a56759c89ad4ddd103d6c68314cd653ade`, inspect
it, then run these commands from the project root:

```bash
sh <verified-installer-path> --project --init --release latest --no-animation
.tree-ring/bin/tree-ring --root .tree-ring integrations status --verbose
```

Do not pipe a network response directly to a shell.

The plugin requires Tree Ring Memory v0.15.0 or
newer:

```bash
tree-ring --version
tree-ring integrations status --help
```

Before a current binary upgrades a pre-v0.13 store to schema v3, stop every
Tree Ring process, checkpoint and back up the complete store, and upgrade every
CLI, plugin, and bundled worker. Do not use a v0.12 writer against schema v3;
all mixed-version operation is unsupported.

If the CLI is missing or older, the plugin may bootstrap or update it when the
user's request already authorizes Tree Ring setup. Otherwise it explains the
exact operation and asks before downloading or changing software. Use
`tree-ring update --check` for a read-only release check and, with update
authorization, `tree-ring update` to preserve the active install scope. It does
not edit shell configuration, change global scope, or claim that a memory
action ran without the required authorization and observed command output.

For other install paths, use the canonical project README:
<https://github.com/TerminallyLazy/Tree-Ring-Memory#install>

## Install The Plugin

Add this repository as a Claude Code plugin marketplace:

```text
/plugin marketplace add TerminallyLazy/tree-ring-memory-claude-plugin
/plugin install tree-ring-memory@tree-ring-memory
```

After installation, Claude Code can use:

```text
/tree-ring-memory:tree-ring-memory
/tree-ring-memory:tree-ring-recall
/tree-ring-memory:tree-ring-capture
/tree-ring-memory:tree-ring-audit
/tree-ring-memory:tree-ring-status
/tree-ring-memory:tree-ring-dox-sync
/tree-ring-memory:tree-ring-certify
/tree-ring-memory:tree-ring-update
```

## Use

Ask Claude Code:

```text
Use Tree Ring Memory to recall durable project context before editing.
Use Tree Ring Memory to capture this validated lesson without storing a transcript.
Use Tree Ring Memory to audit stale or sensitive memory before closeout.
Preview DOX contract summaries and sync only concise, source-linked guidance.
Generate harness certification evidence without claiming full release certification.
```

The skill looks for project-local `.tree-ring/SKILL.md` and `.tree-ring/CLI.md`
first. If they are absent, it falls back to the public CLI commands documented
in the main framework repository.

For DOX projects, the plugin reads the applicable `AGENTS.md` chain before
edits and keeps those live contracts authoritative. `/tree-ring-memory:tree-ring-dox-sync`
previews the local adapter output before any persistence and never rewrites the
source contracts.

`/tree-ring-memory:tree-ring-certify` uses the installed CLI for harness or
recall-quality evidence. The larger `scripts/certify-tree-ring.sh` suite remains
exclusive to a complete Tree Ring framework source checkout; it is not bundled
with this plugin.

## Receipt-Backed Harness Readiness

For a new project, start with:

```bash
tree-ring init
tree-ring integrations status
```

Configuration is not activation proof. A harness is `active` only after a
fresh, matching receipt shows scoped recall and safe context injection from a
new session. States such as `configured-awaiting-proof`, `needs-trust`,
`needs-plugin`, `needs-project-mount`, `needs-user-review`, and `unsupported`
remain explicitly non-active. The `/tree-ring-memory:tree-ring-status` command
reports the exact state without modifying trust, bridges, or receipts.

For fan-out/fan-in, the supported shared-root boundary is cooperative Tree Ring
processes on one host and a local filesystem. Identity and scope route memory;
they are not read access-control boundaries. Cross-host and network-filesystem
workflows need per-host stores plus explicit, source-preserving fan-in.

## Canonical Project

- Framework repo: <https://github.com/TerminallyLazy/Tree-Ring-Memory>
- Launch page: <https://terminallylazy.github.io/Tree-Ring-Memory/>
- Homebrew tap: <https://github.com/TerminallyLazy/homebrew-tree-ring>
- v0.15 release: <https://github.com/TerminallyLazy/Tree-Ring-Memory/releases/tag/v0.15.1>

## Security

This plugin ships instructions only. It does not include remote MCP servers,
webhooks, analytics, credentials, or networked runtime code.

Coordinated mode uses a one-time capability only through
`TREE_RING_COORDINATOR_TOKEN`. Keep it out of prompts, command arguments,
memory, logs, source references, and ordinary worker environments.

See [PRIVACY.md](PRIVACY.md), [TERMS.md](TERMS.md), and
[SECURITY.md](SECURITY.md) for data handling, use terms, and disclosures.
