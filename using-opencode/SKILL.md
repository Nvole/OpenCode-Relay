---
name: using-opencode
description: "Use for any OpenCode work: CLI/TUI usage, installation, configuration, providers, agents, MCP, rules and skills; or delegating bounded local work to one worker, routing many dependency-aware workers, and independently auditing worker results. On this machine, all delegated execution and audit runs must use opencode-go/deepseek-v4-flash."
---

# Using OpenCode

Select the lightest route that can produce trustworthy evidence. Do not use Router merely because there are multiple independent items.

## Route requests

- For OpenCode commands, TUI, installation, configuration, providers, agents, MCP, rules, or OpenCode skills, read [references/product-guide.md](references/product-guide.md).
- For one to eight independent bounded workers, including parallel read-only investigations or disjoint repairs, default to [references/local-runner.md](references/local-runner.md). Read [references/prompt-template.md](references/prompt-template.md) when drafting a contract. Use host-side deterministic verification once after the wave.
- Use [references/task-router.md](references/task-router.md) plus [references/manifest-schema.md](references/manifest-schema.md) only for dependency graphs, resumability across sessions, shared-interface integration, critical mutations, or when the user explicitly requires independent per-task audits.
- For a standalone read-only audit of a completed worker, read [references/audit-protocol.md](references/audit-protocol.md).

## Enforce local delegation policy

For every execution, audit, retry, and repair delegated through OpenCode:

1. Use exactly `opencode-go/deepseek-v4-flash`. Never use a default or fallback model.
2. Define objective, exact read scope, exclusive write scope, exclusions, ordered actions, deliverables, acceptance criteria, verification, and stop conditions before dispatch.
   Treat this as a hard pre-dispatch gate: every path must be explicit, every deliverable must belong to the write scope, and each acceptance criterion must have a deterministic check or named evidence source.
3. Use `--auto --pure` unless the task explicitly requires plugins. Give each plugin-aware worker a unique `OPENCODE_GOAL_STATE_PATH`.
4. Parallelize only disjoint write sets. Give each worker unique state, log, and artifact paths, and run bounded waves.
5. Treat worker claims as untrusted, but scale review to risk. For read-only analysis or narrow disjoint edits, inspect artifacts and run deterministic host checks; do not add a second model audit by default. Reserve independent model audits for high-impact semantic changes, shared contracts, security boundaries, or explicit requests.
6. Stop if the mandatory model is unavailable or the task boundary cannot be made explicit.
7. Protect control files by default. Workers must not read or edit `.Codex/`, `.codex/`, `.git/`, `AGENTS.md`, skill directories, memory files, manifests, router state, or another worker's artifacts unless one exact path is intentionally placed in scope. A repository instruction to update memory does not apply inside a delegated worker contract; the parent agent owns memory updates.
8. Routed workers have exactly one control-plane write exception outside task write scope: the Router-provided `handoff.json`. The prompt must state this exception explicitly and require the handoff even for `blocked` or `failed` work. Missing handoff is a blocked delivery, regardless of other files produced.

For a routed batch, prefer `scripts/invoke-opencode-task.ps1 -Manifest <path> -ValidateThenRun`. It performs DryRun validation and then starts live mode with fresh Router state. Use manual `-DryRun` only when the plan needs human inspection before execution.
