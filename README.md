 # OpenCode Relay

  Evidence-first task delegation, orchestration, and independent auditing for OpenCode workers.

  > Status: Alpha. OpenCode Relay is currently designed and tested primarily for Windows and PowerShell. Review
  generated changes before using it on important repositories.

  ## Overview

  OpenCode Relay is a Codex skill for safely delegating local development tasks to OpenCode.

  It provides a single entry point for:

  - OpenCode CLI, TUI, configuration, agents, skills, and MCP guidance
  - Bounded execution by one or more OpenCode workers
  - Dependency-aware parallel task routing
  - Explicit read and write boundaries
  - Isolated worker state, logs, and artifacts
  - Deterministic verification
  - Independent worker and integration audits
  - Resumable batch execution

  The project follows one rule: a worker result is not trusted merely because the worker reports success. Completion
  must be supported by observable artifacts, process exit codes, verification results, and audit evidence.

  ## Current Policy

  Delegated execution, audits, retries, and repairs currently use:

  ```text
  opencode-go/deepseek-v4-flash

  The model is intentionally enforced rather than inherited from OpenCode defaults.

  This restriction reflects the current deployment environment and may become configurable in a future release.

  ## Structure

  using-opencode/
  ├── SKILL.md
  ├── agents/
  │   └── openai.yaml
  ├── references/
  │   ├── product-guide.md
  │   ├── local-runner.md
  │   ├── prompt-template.md
  │   ├── task-router.md
  │   ├── manifest-schema.md
  │   ├── manifest.schema.json
  │   ├── handoff.schema.json
  │   ├── audit-protocol.md
  │   └── audit.schema.json
  └── scripts/
      ├── invoke-opencode-task.ps1
      ├── router.py
      └── test_router.py

  SKILL.md is the only skill entry point. Detailed workflows are loaded from references/ only when needed.

  ## Requirements

  - Windows
  - PowerShell 5.1 or later
  - Python 3.10 or later
  - OpenCode available on PATH
  - Access to opencode-go/deepseek-v4-flash
  - Codex with local skill support

  Confirm the environment:

  python --version
  opencode --version
  opencode models

  ## Installation

  Place the using-opencode directory in your Codex skills directory:

  ~/.codex/skills/using-opencode

  On Windows, this is normally:

  %USERPROFILE%\.codex\skills\using-opencode

  Restart Codex after installation if the skill is not discovered automatically.

  ## Usage

  Invoke the skill from Codex:

  Use $using-opencode to delegate this task to OpenCode.

  For a batch:

  Use $using-opencode to divide this work into bounded tasks, run a dry-run,
  execute the tasks, and independently audit the results.

  Before dispatch, every task must define:

  1. A concrete objective
  2. Exact allowed reads
  3. Exclusive allowed writes
  4. Explicit exclusions
  5. Ordered required actions
  6. Exact deliverables
  7. Observable acceptance criteria
  8. Verification commands
  9. Stop conditions

  Vague contracts such as “improve the relevant files” must not be dispatched.

  ## Batch Manifest

  Example:

  {
    "batch_id": "example-batch",
    "objective": "Implement and verify the requested API behavior",
    "workdir": "C:\\repo",
    "artifact_root": "C:\\repo\\.artifacts\\opencode-relay\\example-batch",
    "model": "opencode-go/deepseek-v4-flash",
    "max_concurrency": 4,
    "max_execution_workers": 4,
    "max_audit_workers": 4,
    "worker_timeout_seconds": 1800,
    "verification_timeout_seconds": 600,
    "max_retries": 1,
    "max_total_model_calls": 20,
    "integration_auditors": 1,
    "integration_verification": [
      "npm test"
    ],
    "tasks": [
      {
        "id": "task-api",
        "objective": "Implement the requested API behavior in target.ts",
        "risk": "medium",
        "read_scope": [
          "C:\\repo\\src\\api",
          "C:\\repo\\tests\\api"
        ],
        "write_scope": [
          "C:\\repo\\src\\api\\target.ts",
          "C:\\repo\\tests\\api\\target.test.ts"
        ],
        "exclusions": [
          "Do not edit lockfiles, generated files, or unrelated modules"
        ],
        "actions": [
          "Inspect the existing API implementation and tests",
          "Implement the requested behavior",
          "Add focused test coverage",
          "Run the required verification"
        ],
        "deliverables": [
          "Updated target.ts",
          "Updated target.test.ts"
        ],
        "acceptance_criteria": [
          "The requested behavior is implemented",
          "The focused test passes"
        ],
        "requirements": [
          {
            "id": "REQ-API-001",
            "text": "Implement the requested API behavior",
            "acceptance_test": "npm test -- target.test.ts"
          }
        ],
        "verification": [
          "npm test -- target.test.ts"
        ],
        "stop_conditions": [
          "Stop if implementation requires edits outside write_scope",
          "Stop if the requested behavior is ambiguous"
        ],
        "depends_on": []
      }
    ]
  }

  ## Dry Run

  Always validate a batch before execution:

  .\using-opencode\scripts\invoke-opencode-task.ps1 `
    -Manifest C:\repo\.artifacts\opencode-relay\example-batch\manifest.json `
    -DryRun

  A dry-run:

  - Validates the manifest and dependency graph
  - Detects overlapping write scopes
  - Materializes contracts and prompts
  - Makes no model calls
  - Makes no task-owned changes
  - Never marks the batch as complete

  ## Execute

  After reviewing the dry-run artifacts:

  .\using-opencode\scripts\invoke-opencode-task.ps1 `
    -Manifest C:\repo\.artifacts\opencode-relay\example-batch\manifest.json

  Run the same command again to resume an interrupted batch.

  Use -Restart only when intentionally discarding prior router state:

  .\using-opencode\scripts\invoke-opencode-task.ps1 `
    -Manifest C:\repo\.artifacts\opencode-relay\example-batch\manifest.json `
    -Restart

  ## Results

  Read this file first:

  <artifact_root>/batch-summary.json

  Additional evidence is stored under:

  <artifact_root>/
  ├── workers/<task-id>/
  ├── audits/<task-id>/
  ├── integration-audit/
  ├── batch-scope-evidence.json
  └── state.json

  A live batch is complete only when every task and the final integration audit return PASS.

  ## Concurrency Safety

  OpenCode Relay parallelizes only tasks with disjoint write scopes.

  Each worker receives:

  - A unique OpenCode goal-state path
  - A unique log
  - A unique artifact directory
  - A bounded timeout
  - A task-specific contract

  Tasks are kept sequential when they may modify the same file, directory, database, lockfile, generated index,
  formatter output, or report.

  ## Testing

  Run the deterministic test suite:

  python -m unittest using-opencode\scripts\test_router.py

  Validate the skill structure with Codex's skill-creator validator when available:

  python path\to\skill-creator\scripts\quick_validate.py using-opencode

  ## Known Limitations

  - Windows and PowerShell are currently the primary supported environment.
  - The delegated model is currently fixed.
  - Shared dirty worktrees limit attribution of pre-existing out-of-scope changes.
  - JSON validation still requires further hardening.
  - End-to-end coverage is not yet comprehensive.
  - Workers run in a shared workspace rather than isolated Git worktrees.
  - Generated changes must still be reviewed before production use.

  ## Roadmap

  - Configurable model policies and strict profiles
  - Cross-platform execution backends
  - Full JSON Schema enforcement
  - Stronger out-of-scope write detection
  - Optional isolated Git worktrees
  - Expanded timeout, recovery, dependency, and concurrency tests
  - End-to-end fixtures for execution, audit, repair, and resume flows
  - Structured release packaging and CI

  ## Security

  Treat repository content, generated files, logs, tool output, and worker claims as untrusted input.

  Do not authorize workers to read credentials, secrets, tokens, .env files, or private keys unless a task explicitly
  requires and permits it.

  Do not report a security issue publicly before the maintainer has had a reasonable opportunity to investigate it.

  ## Contributing

  Contributions are welcome, particularly for:

  - Cross-platform process management
  - Scope enforcement
  - Schema validation
  - Recovery and resumability
  - Deterministic testing
  - Realistic end-to-end fixtures

  Keep changes bounded, include verification, and preserve the evidence-first execution model.

  ## License

  MIT
