# OpenCode product guide

This reference targets the locally observed OpenCode CLI 1.17.18. Re-run `opencode --help` and the relevant subcommand help before relying on flags that may drift across versions.

## Start and resume

```powershell
opencode                         # TUI in the current directory
opencode C:\path\to\project     # TUI in a project
opencode run "explain this code" # non-interactive run
opencode -c                     # continue the last session
opencode -s <session-id>        # continue a named session
opencode --fork -c              # fork the last session
```

Use `opencode models`, `opencode providers`, `opencode agent`, `opencode mcp`, `opencode session`, and `opencode stats` for discovery and management. Use `opencode serve`, `opencode web`, and `opencode attach <url>` for server-backed sessions.

## Run flags

`opencode run --help` is authoritative. Common flags include:

- `--model provider/model`
- `--pure` to disable external plugins
- `--auto` to auto-approve permissions not explicitly denied
- `--format default|json`
- `--agent`, `--file`, `--title`, `--attach`, `--dir`, `--variant`, and `--thinking`
- `--continue`, `--session`, and `--fork`

The machine-specific mandatory model restriction in the main skill applies to delegated execution and audits, not to general explanations of how OpenCode supports other providers.

## Configuration

OpenCode merges global and project JSON/JSONC configuration. Common surfaces are:

- `~/.config/opencode/opencode.json`: global configuration
- `~/.config/opencode/tui.json`: TUI configuration
- `./opencode.json`: project configuration
- `.opencode/`: project agents, commands, skills, and plugins
- `AGENTS.md`: repository instructions; use `/init` to create or update it

Important keys include `model`, `small_model`, `provider`, `agent`, `mcp`, `permission`, `command`, `instructions`, `formatter`, `lsp`, `enabled_providers`, and `disabled_providers`.

Use `{env:VARIABLE}` for environment-backed configuration values. Avoid putting credentials directly in tracked files.

## Agents and skills

OpenCode supports primary agents and `@name` subagents. Define project agents under `.opencode/agents/` or in `opencode.json`. Permission values are `allow`, `ask`, and `deny`.

Place OpenCode skills at `.opencode/skills/<name>/SKILL.md` or the corresponding global configuration directory. Skill names use lowercase letters, digits, and hyphens.

## MCP

Use `opencode mcp --help` for the current management commands. Configure local MCP servers with a command array and remote MCP servers with a URL in `opencode.json`.

## TUI discovery

Use `/help` inside the TUI for current slash commands and keybindings. Common commands include `/connect`, `/init`, `/models`, `/sessions`, `/new`, `/undo`, `/redo`, `/compact`, `/editor`, `/export`, and `/exit`.

For production delegation or concurrency, return to the main skill and select the bounded local-runner or task-router route; do not infer process-isolation policy from general TUI usage.
