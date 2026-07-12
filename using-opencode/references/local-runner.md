# Bounded local runner

Use this route for one or a few local workers. For many tasks, dependency waves, resumability, or independent auditors, switch to [task-router.md](task-router.md).

## Contract gate

Do not invoke OpenCode until every item is concrete:

1. One observable objective and end state.
2. Exact allowed reads.
3. Exact allowed writes.
4. Explicit exclusions and required non-actions.
5. Ordered required actions.
6. Exact deliverables and paths.
7. Testable acceptance criteria.
8. Verification commands and expected results.
9. Stop conditions that prevent guessing or scope expansion.

Reject placeholders such as `relevant files`, `as needed`, or `improve everything`. Use [prompt-template.md](prompt-template.md) for a reusable contract.

## Invoke

Confirm `Get-Command opencode` and verify the exact model appears in `opencode models`. Then run from the actual task directory:

```powershell
opencode run --model opencode-go/deepseek-v4-flash --auto --pure $prompt
```

Do not use `--continue` for independent workers. Do not fall back when the model is unavailable.

## Parallel Windows runs

- Default to at most 8 workers; use 16 only with measured host and provider capacity. Treat 128 as an orchestration ceiling, never a launch target.
- Use bounded waves and wait for every process in a wave before starting the next.
- Prefer `Start-Job` on Windows PowerShell 5.1. Use `Start-ThreadJob` on PowerShell 7 only when already available.
- Set `OPENCODE_GOAL_STATE_PATH` inside each child, never repeatedly in the parent shell.
- Give every worker a unique state directory, log, title, and artifact path. Stream verbose output directly to its log and return only a small status object.
- Set a per-worker timeout. Terminate only the exact process tree created for that worker and retain its logs for diagnosis.
- Keep work sequential when writes touch the same file, directory ancestor, database, lockfile, generated index, formatter output, or report.

## Verify and report

Inspect changed files and requested artifacts, run targeted checks, confirm all process exit states, and verify writes stayed within scope. Report what was delegated, what it produced, what was independently verified, and what remains uncertain.
