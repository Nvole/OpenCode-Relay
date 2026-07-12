# OpenCode Prompt Templates

All commands that dispatch these prompts must explicitly pass `--model opencode-go/deepseek-v4-flash`. Do not use any other OpenCode model or rely on the configured default. If this exact model is unavailable, stop instead of falling back.

## Mandatory Use Rule

Before dispatch, every prompt must define the objective, allowed reads, allowed writes, explicit exclusions, numbered actions, deliverables, acceptance criteria, verification, and stop conditions. Do not run OpenCode with unresolved placeholders or vague phrases such as "relevant files", "as needed", or "improve the codebase". For parallel work, complete these fields separately for every worker.

Every routed prompt must also distinguish task-owned writes from the Router control-plane handoff. The worker may write only the exact task write paths and the exact Router-provided `handoff.json`; it must write the handoff for completed, blocked, and failed outcomes. Explicitly prohibit reading or editing `.Codex/`, `.codex/`, `.git/`, `AGENTS.md`, skills, memory files, manifests, router state, and sibling worker artifacts unless an exact path is deliberately authorized. State that repository instructions requesting memory updates do not apply to the worker; the parent agent owns memory.

## Audit Template

```text
You are working in this directory:
<WORKDIR>

Scope:
- <TARGET DIR / FILE / DB 1>
- <TARGET DIR / FILE / DB 2>

Allowed writes:
- <EXACT REPORT PATH ONLY>

Out of scope:
- Do not edit source files, databases, or any artifact other than the report.
- Do not edit `.Codex/`, `.codex/`, `.git/`, `AGENTS.md`, skills, memory files, manifests, router state, or sibling worker artifacts.

Your task is NOT to make code or data changes.
Your task is to produce a deep audit with evidence.

Audit goals:
A. <AUDIT AXIS 1>
B. <AUDIT AXIS 2>
C. <AUDIT AXIS 3>

Deliverables:
- <REPORT SECTION 1>
- <REPORT SECTION 2>
- <REPORT SECTION 3>

Write the report to:
<EXACT REPORT PATH>

Important requirements:
- be concrete and evidence-based
- use exact file names / api_names / table names where relevant
- distinguish between partial support and reliable support
- do not handwave

Verification and stop conditions:
- Confirm the report exists at the exact requested path.
- If evidence is unavailable or scope is ambiguous, record the gap; do not infer unsupported findings.
- For routed work, always write the exact Router-provided `handoff.json`, including when status is `blocked` or `failed`.

When finished, print a concise terminal summary with:
- <SUMMARY ITEM 1>
- <SUMMARY ITEM 2>
- <SUMMARY ITEM 3>
```

## Refactor Template

```text
You are working in this directory:
<WORKDIR>

Target scope:
- <DIR / FILE SET 1>
- <DIR / FILE SET 2>

Allowed write scope:
- <EXACT FILE / DIRECTORY SET>

Explicitly out of scope:
- <PROTECTED FILES / DIRECTORIES / BEHAVIORS>
- Any opportunistic cleanup not required by the objective

Objective:
<ONE SENTENCE GOAL>

Canonical target format:
<DESCRIBE THE DESIRED END STATE>

Your job is to:
1. Inspect the current implementation patterns.
2. Introduce or extend shared helpers if needed.
3. Migrate the target files conservatively toward the canonical format.
4. Run a targeted verification pass.
5. Write an implementation report.

Constraints:
- edit only the intended files
- preserve intentionally removed / alias / stub behavior unless obviously contradictory
- avoid unnecessary rewrites
- prefer shared helpers over duplicated per-file logic

Acceptance criteria:
- the codebase should have fewer incompatible patterns
- the new implementation should be easier to reason about
- representative verification checks should run successfully

Verification and stop conditions:
- Run <EXACT COMMANDS> and record their exit status.
- If the canonical format conflicts with existing requirements or requires edits outside the write scope, stop and report the conflict.

Write the implementation report to:
<EXACT REPORT PATH>

When finished, print a concise terminal summary with:
- total files examined
- total files changed
- total verification checks run
- remaining outliers
```

## Cleanup Template

```text
You are working in this directory:
<WORKDIR>

Target:
<DB / DIRECTORY / ARTIFACT SET>

Allowed read scope:
- <EXACT INPUTS>

Allowed write scope:
- <EXACT DATABASE / FILES / BACKUP PATH>

Your job is to perform a cleanup pass.

Before any mutation:
- create a backup
- print the backup path

Cleanup rules:
1. <RULE 1>
2. <RULE 2>
3. <RULE 3>

Do not:
- <DISALLOWED ACTION 1>
- <DISALLOWED ACTION 2>

Stop conditions:
- Stop before mutation if the deletion criteria are not mechanically decidable.
- Stop if backup creation or verification fails.

After cleanup:
- report before/after counts
- list what was removed or changed by category
- write a concise report to <EXACT REPORT PATH>
```

## Practical Notes

- Prefer here-strings in PowerShell for long prompts.
- Prefer exact output paths so artifact discovery is trivial afterward.
- If the task is large, explicitly ask for a terminal summary at the end.
- If the task is risky, state what it must not edit.
