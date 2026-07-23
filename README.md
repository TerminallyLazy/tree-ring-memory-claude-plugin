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

## Install Tree Ring Memory

macOS ARM64 with Homebrew:

```bash
brew tap TerminallyLazy/tree-ring
brew install tree-ring
```

The multi-agent and coordinator guidance requires Tree Ring Memory v0.13.0 or
newer:

```bash
tree-ring --version
tree-ring policy --help
```

Before a v0.13 binary upgrades an existing store to schema v3, stop every
Tree Ring process, checkpoint and back up the complete store, and upgrade every
CLI, plugin, and bundled worker. Mixed v0.12/v0.13 operation is unsupported.

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
```

## Use

Ask Claude Code:

```text
Use Tree Ring Memory to recall durable project context before editing.
Use Tree Ring Memory to capture this validated lesson without storing a transcript.
Use Tree Ring Memory to audit stale or sensitive memory before closeout.
```

The skill looks for project-local `.tree-ring/SKILL.md` and `.tree-ring/CLI.md`
first. If they are absent, it falls back to the public CLI commands documented
in the main framework repository.

For fan-out/fan-in, the supported shared-root boundary is cooperative Tree Ring
processes on one host and a local filesystem. Identity and scope route memory;
they are not read access-control boundaries. Cross-host and network-filesystem
workflows need per-host stores plus explicit, source-preserving fan-in.

## Canonical Project

- Framework repo: <https://github.com/TerminallyLazy/Tree-Ring-Memory>
- Launch page: <https://terminallylazy.github.io/Tree-Ring-Memory/>
- Homebrew tap: <https://github.com/TerminallyLazy/homebrew-tree-ring>

## Security

This plugin ships instructions only. It does not include remote MCP servers,
webhooks, analytics, credentials, or networked runtime code.

Coordinated mode uses a one-time capability only through
`TREE_RING_COORDINATOR_TOKEN`. Keep it out of prompts, command arguments,
memory, logs, source references, and ordinary worker environments.

See [SECURITY.md](SECURITY.md) for disclosure and privacy guidance.
