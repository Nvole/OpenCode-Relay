# Batch manifest schema

Use UTF-8 JSON. Paths may be absolute or relative to `batch.workdir`; prefer absolute paths when tasks use different working directories.

```json
{
  "batch_id": "unique-slug",
  "objective": "The complete user-visible batch outcome",
  "workdir": "C:\\repo",
  "artifact_root": "C:\\repo\\claude_test\\opencode-router\\unique-slug",
  "model": "opencode-go/deepseek-v4-flash",
  "max_concurrency": 8,
  "max_execution_workers": 8,
  "max_audit_workers": 8,
  "worker_timeout_seconds": 1800,
  "verification_timeout_seconds": 600,
  "max_retries": 1,
  "max_log_bytes": 5000000,
  "max_total_model_calls": 100,
  "integration_auditors": 2,
  "integration_verification": ["npm test"],
  "tasks": [
    {
      "id": "task-001",
      "objective": "One observable end state",
      "risk": "medium",
      "read_scope": ["C:\\repo\\src\\area-a"],
      "write_scope": ["C:\\repo\\src\\area-a\\target.ts"],
      "exclusions": ["Do not edit lockfiles or other modules"],
      "actions": ["Inspect the target", "Implement the change"],
      "deliverables": ["Updated target.ts"],
      "acceptance_criteria": ["Named behavior is observable"],
      "requirements": [
        {"id": "REQ-API-001", "text": "Named behavior", "acceptance_test": "npm test -- target.test.ts"}
      ],
      "verification": ["npm test -- target.test.ts"],
      "stop_conditions": ["Required edit falls outside write_scope"],
      "depends_on": []
    }
  ]
}
```

## Validation rules

- `batch_id`, `objective`, `workdir`, `artifact_root`, `model`, and `tasks` are required.
- `model` must equal `opencode-go/deepseek-v4-flash`.
- Unknown batch, task, and requirement fields are rejected so misspellings cannot silently weaken a contract.
- `max_concurrency` must be an integer from 1 through 128.
- Execution/audit worker limits, timeouts, retry count, and maximum log bytes are optional and receive conservative defaults.
- Task IDs must be unique and match `^[a-z0-9][a-z0-9-]*$`.
- Every task array except `depends_on` must be non-empty.
- Dependencies must name tasks in the same manifest and the graph must be acyclic.
- Tasks in the same wave must have disjoint write scopes. A directory scope overlaps every descendant path.
- Each task gets artifact paths under `<artifact_root>/workers/<id>/` and `<artifact_root>/audits/<id>/`.
- `risk` defaults to `low`; `high` and `critical` require two unanimous auditors.
- Requirement IDs must be unique per task and match `REQ-[A-Z0-9-]+`.
- Reusing an artifact root resumes only when the manifest hash matches. Use `-Restart` after an intentional manifest change.
- `-DryRun` validates and materializes the plan without model calls or task-owned writes; its summary is never marked complete.
- Every verification command must exit nonzero on failure. PowerShell predicates such as `Test-Path` must be wrapped, for example: `if (-not (Test-Path target)) { throw 'missing target' }`.
- Full machine-readable constraints are in [manifest.schema.json](manifest.schema.json).
