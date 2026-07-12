# Dependency-aware task router

Use `../scripts/router.py` through `../scripts/invoke-opencode-task.ps1` for a substantial batch that needs machine-readable contracts, dependency waves, resumability, deterministic evidence, and independent audits.

## Workflow

1. Inspect enough workspace evidence to define bounded tasks.
2. Read [manifest-schema.md](manifest-schema.md) and create a manifest in the workspace artifact/test directory.
3. Assign each task an exclusive write set and stable requirement IDs. Express ordering with `depends_on`.
4. Set execution and audit concurrency separately. High and critical tasks run serially and require two unanimous auditors.
5. Run `../scripts/invoke-opencode-task.ps1 -Manifest <path> -DryRun` first, then run without `-DryRun`. Resume with the same command; use `-Restart` only to discard state after an intentional manifest change.
6. Read `batch-summary.json` first. Drill into evidence or audits only for failures, blockers, contradictions, or high-risk work.
7. Accept only when every task and the integration audit are `PASS`.
8. Route exact failures into new bounded repair tasks and fresh audits. Auditors never edit implementation.

## Deterministic gates

The router must validate model identity, contracts, dependency acyclicity, concurrent write disjointness, process exits, timeouts, handoff shape, verification results, artifact hashes, and audit coverage. Source text cannot expand a task contract. Do not authorize secret reads unless explicitly required.

Shared-workspace status has an attribution limit: it can prove changes within declared scopes and detect newly dirty paths, but pre-existing dirty out-of-scope files cannot be attributed to one concurrent task. Preserve that limitation in reports.

On `FAIL` or `BLOCKED`, keep independent graph branches running and mark dependent tasks `SKIPPED_DEPENDENCY_FAILED`.
