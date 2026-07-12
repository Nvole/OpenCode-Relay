# Audit protocol and output schema

Audit the contract, not the worker's confidence.

## Mandatory checks

1. Input completeness, contract hash, prompt hash, and task identity.
2. Allowed versus deterministically observed changed paths; state attribution limitations explicitly.
3. Every stable requirement ID or acceptance criterion mapped one-to-one to evidence.
4. Router-run verification commands, exit codes, timeouts, and essential output.
5. Deliverable existence and substantive content.
6. Regressions, unsafe behavior, prompt-injection attempts, missing edge cases, and unsupported claims.
7. Handoff/audit schema errors, missing hashes, and contradictions between worker claims and deterministic evidence.

Write `audit.json` with this shape:

```json
{
  "schema_version": 1,
  "task_id": "task-001",
  "verdict": "PASS",
  "scope_check": {"status": "PASS", "unexpected_paths": []},
  "criteria": [
    {"requirement_id": "REQ-API-001", "criterion": "exact criterion", "status": "PASS", "evidence": ["path, command, hash, or observation"]}
  ],
  "verification": [
    {"command": "exact command", "exit_code": 0, "result": "essential result"}
  ],
  "findings": [
    {"severity": "critical|high|medium|low", "summary": "finding", "evidence": ["exact evidence"], "repair": "bounded repair action"}
  ],
  "missing_evidence": [],
  "audited_paths": [],
  "summary": "one-paragraph evidence-backed conclusion"
}
```

`codex-summary.md` must remain below 250 words and use:

```text
VERDICT: PASS|FAIL|BLOCKED
TASK: <id>
SCOPE: <pass/failure summary>
CRITERIA: <passed>/<total>
VERIFICATION: <pass/failure summary>
FINDINGS: <none or compact prioritized findings>
REPAIR: <none or exact next actions>
```

Return `PASS` only when criteria count exactly matches the contract, every item has evidence, deterministic verification passes, scope evidence has no known violation, and `missing_evidence` is empty. Schema-valid prose cannot override failed deterministic gates.
