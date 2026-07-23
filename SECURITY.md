# Security Policy

Tree Ring Memory Claude Code Plugin is an instructions-only wrapper around the
open-source Tree Ring Memory CLI.

## What This Plugin Does Not Do

- It does not run background services.
- It does not define Claude Code hooks.
- It does not ship a networked MCP server.
- It does not collect analytics.
- It does not ask for credentials, tokens, or API keys.
- It does not store raw chat transcripts.

## Privacy Guidance

Only store concise, useful memory. Do not store secrets, credentials, tokens,
private keys, raw chain-of-thought, temporary scratchpad notes, unverified claims
as durable truth, or private health, financial, legal, or personal identifier
details without explicit user instruction.

Use `tree-ring audit`, `tree-ring forget`, redaction, and supersession when
memory is wrong, sensitive, stale, or replaced by newer evidence.

## Coordinated Mode

Tree Ring Memory v0.13 Coordinated mode uses a one-time capability supplied
only through `TREE_RING_COORDINATOR_TOKEN`. Never place its value in a prompt,
CLI argument, memory event, log, source reference, committed file, or ordinary
worker environment. Tree Ring stores only a hash of the capability.

The policy is operational write authorization in official Rust and CLI paths.
It is not a read ACL, an operating-system security boundary, or protection
against an adversary who controls the database files or process environment.
The supported shared-root boundary is cooperative processes on one host using a
local filesystem; it does not establish cross-host or network-filesystem safety.

## Reporting A Vulnerability

Open a private vulnerability report on the canonical framework repository:

<https://github.com/TerminallyLazy/Tree-Ring-Memory/security/advisories/new>

If GitHub advisories are unavailable, open a minimal public issue without
including exploit details or sensitive data.
