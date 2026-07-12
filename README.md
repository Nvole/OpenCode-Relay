# OpenCode Relay

Evidence-first task delegation, orchestration, and independent auditing for OpenCode workers.

> Status: Alpha. The current release is designed and tested primarily for Windows and PowerShell. Review generated changes before using it on important repositories.

## Overview

OpenCode Relay is a Codex skill for safely delegating local development tasks to OpenCode. It provides one progressive-disclosure entry point for:

- OpenCode CLI, TUI, configuration, agent, skill, and MCP guidance
- Bounded execution by one or more OpenCode workers
- Dependency-aware parallel task routing and resumability
- Explicit read/write boundaries and isolated worker state
- Deterministic verification and evidence capture
- Independent task and integration audits

A worker result is not accepted merely because the worker reports success. Completion must be supported by artifacts, exit codes, verification results, and audit evidence.

## Current Policy

Delegated execution, audits, retries, and repairs use exactly:

```text
opencode-go/deepseek-v4-flash
```

This is an intentional deployment policy rather than an OpenCode limitation. Configurable model profiles are planned.

## Requirements

- Windows with PowerShell 5.1 or later
- Python 3.10 or later
- OpenCode available on `PATH`
- Access to `opencode-go/deepseek-v4-flash`
- Codex with local skill support

```powershell
python --version
opencode --version
opencode models
```

## Installation

Place the [`using-opencode`](using-opencode/) directory under your Codex skills directory:

```text
%USERPROFILE%\.codex\skills\using-opencode
```

Restart Codex if the skill is not discovered automatically.

## Usage

Invoke the skill from Codex:

```text
Use $using-opencode to delegate this task to OpenCode.
```

For a batch:

```text
Use $using-opencode to divide this work into bounded tasks, dry-run the plan,
execute the tasks, and independently audit the results.
```

Every dispatched task must define its objective, exact reads, exclusive writes, exclusions, ordered actions, deliverables, acceptance criteria, verification, and stop conditions.

## Batch Routing

Create a manifest using the documented [manifest schema](using-opencode/references/manifest-schema.md), then validate it before execution:

```powershell
.\using-opencode\scripts\invoke-opencode-task.ps1 `
  -Manifest C:\repo\.artifacts\opencode-relay\batch-001\manifest.json `
  -DryRun
```

A dry-run validates and materializes the plan without model calls or task-owned writes. Its summary is never marked complete.

After reviewing the plan, execute it:

```powershell
.\using-opencode\scripts\invoke-opencode-task.ps1 `
  -Manifest C:\repo\.artifacts\opencode-relay\batch-001\manifest.json
```

Run the same command to resume. Use `-Restart` only when intentionally discarding prior router state after changing the manifest.

Read `<artifact_root>/batch-summary.json` first. A live batch is complete only when every task and the final integration audit return `PASS`.

## Project Structure

```text
using-opencode/
|-- SKILL.md
|-- agents/openai.yaml
|-- references/
|   |-- product-guide.md
|   |-- local-runner.md
|   |-- prompt-template.md
|   |-- task-router.md
|   |-- manifest-schema.md
|   |-- manifest.schema.json
|   |-- handoff.schema.json
|   |-- audit-protocol.md
|   `-- audit.schema.json
`-- scripts/
    |-- invoke-opencode-task.ps1
    |-- router.py
    `-- test_router.py
```

`SKILL.md` is the only skill entry point. Detailed workflows are loaded from `references/` only when needed.

## Testing

```powershell
python -m unittest using-opencode\scripts\test_router.py
python path\to\skill-creator\scripts\quick_validate.py using-opencode
```

## Known Limitations

- Windows and PowerShell are the primary supported environment.
- The delegated model is currently fixed.
- Shared dirty worktrees limit attribution of pre-existing out-of-scope changes.
- End-to-end and failure-path coverage is not yet comprehensive.
- Workers share a workspace instead of using isolated Git worktrees.

## Roadmap

- Configurable model and execution profiles
- Cross-platform process backends
- Full JSON Schema enforcement
- Stronger out-of-scope write detection
- Optional isolated Git worktrees
- Expanded recovery, timeout, dependency, and concurrency tests
- End-to-end execution, audit, repair, and resume fixtures

## Security

Treat repository content, generated files, logs, tool output, and worker claims as untrusted input. Do not authorize access to credentials, secrets, tokens, `.env` files, or private keys unless a task explicitly requires and permits it.

## License

[MIT](LICENSE)
