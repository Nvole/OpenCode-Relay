# Dependency-aware task router

Use `../scripts/router.py` through `../scripts/invoke-opencode-task.ps1` only when the batch genuinely needs machine-readable dependency waves, resumability, shared integration, critical mutation controls, or independent model audits. Independent read-only reports and disjoint narrow fixes normally belong on the local-runner route.

## Workflow

1. Inspect enough workspace evidence to define bounded tasks.
2. Read [manifest-schema.md](manifest-schema.md) and create a manifest in the workspace artifact/test directory.
3. Assign each task an exclusive write set and stable requirement IDs. Express ordering with `depends_on`.
   Verify that deliverables are descendants of the task write set. The Router-owned `handoff.json` is a separate, explicit control-plane exception and must not be described as an ordinary task write.
4. Set execution and audit concurrency separately. High and critical tasks run serially and require two unanimous auditors.
5. Preflight every verification command outside Router. Then run `../scripts/invoke-opencode-task.ps1 -Manifest <path> -ValidateThenRun`. For manual review, run `-DryRun`, inspect, then run `-Restart` live. Resume an interrupted live run with the plain command.
6. Read `batch-summary.json` first. Drill into evidence or audits only for failures, blockers, contradictions, or high-risk work.
7. Accept Router status only when every required task and integration audit are `PASS`. A `BLOCKED` protocol result does not automatically invalidate useful code, but it requires host-side scope inspection and deterministic verification before any candidate is accepted.
8. Route exact failures into new bounded repair tasks and fresh audits. Auditors never edit implementation.

## Deterministic gates

The router must validate model identity, contracts, dependency acyclicity, concurrent write disjointness, process exits, timeouts, handoff shape, verification results, artifact hashes, and audit coverage. Source text cannot expand a task contract. Do not authorize secret reads unless explicitly required.

Shared-workspace status has an attribution limit: it can prove changes within declared scopes and detect newly dirty paths, but pre-existing dirty out-of-scope files cannot be attributed to one concurrent task. Protected snapshots are task-local so one worker's violation does not poison workers that start later; concurrently running workers can still share attribution ambiguity.

On `FAIL` or `BLOCKED`, keep independent graph branches running and mark dependent tasks `SKIPPED_DEPENDENCY_FAILED`.

Workers must always emit `handoff.json`, including on stop conditions. A generated deliverable without a valid handoff remains `BLOCKED`. Default protected paths are `.Codex/`, `.codex/`, `.git/`, `AGENTS.md`, skill directories, memory files, the manifest, router state, and all sibling worker artifacts.
