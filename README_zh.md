# OpenCode Relay

面向 OpenCode Worker、以证据为先的任务委派、编排与独立审计工具。

> 状态：Alpha。当前版本主要面向 Windows 和 PowerShell 设计与测试。在重要代码仓库中使用前，请务必审查生成的更改。

## 概述

OpenCode Relay 是一个 Codex Skill，用于将本地开发任务安全地委派给 OpenCode。它通过单一入口和渐进式信息披露机制提供以下能力：

- OpenCode CLI、TUI、配置、Agent、Skill 和 MCP 使用指导
- 由一个或多个 OpenCode Worker 执行边界明确的任务
- 支持恢复的依赖感知并行任务路由
- 明确的读写边界与隔离的 Worker 状态
- 确定性验证与证据采集
- 独立的任务审计和集成审计

不能仅凭 Worker 声称成功就接受其结果。任务完成必须得到产物、退出码、验证结果和审计证据的共同支持。

## 当前策略

委派执行、审计、重试和修复任务统一使用：

```text
opencode-go/deepseek-v4-flash
```

这是有意设置的部署策略，并非 OpenCode 本身的限制。未来计划支持可配置的模型配置方案。

## 环境要求

- Windows，PowerShell 5.1 或更高版本
- Python 3.10 或更高版本
- `PATH` 中能够找到 OpenCode
- 能够访问 `opencode-go/deepseek-v4-flash`
- 支持本地 Skill 的 Codex

```powershell
python --version
opencode --version
opencode models
```

## 安装

将 [`using-opencode`](using-opencode/) 目录放入 Codex Skill 目录：

```text
%USERPROFILE%\.codex\skills\using-opencode
```

如果 Codex 没有自动发现该 Skill，请重启 Codex。

## 使用方法

在 Codex 中调用该 Skill：

```text
Use $using-opencode to delegate this task to OpenCode.
```

对于批量任务：

```text
Use $using-opencode to divide this work into bounded tasks, dry-run the plan,
execute the tasks, and independently audit the results.
```

每个被派发的任务都必须明确说明目标、准确的读取范围、独占写入范围、排除项、有序操作、交付物、验收标准、验证方式和停止条件。

## 批量任务路由

按照 [Manifest Schema](using-opencode/references/manifest-schema.md) 文档创建 Manifest，然后在执行前进行验证：

```powershell
.\using-opencode\scripts\invoke-opencode-task.ps1 `
  -Manifest C:\repo\.artifacts\opencode-relay\batch-001\manifest.json `
  -DryRun
```

Dry-run 会验证并生成任务计划，但不会调用模型，也不会写入任务负责的文件。其摘要永远不会被标记为已完成。

审查计划后，执行任务：

```powershell
.\using-opencode\scripts\invoke-opencode-task.ps1 `
  -Manifest C:\repo\.artifacts\opencode-relay\batch-001\manifest.json
```

再次运行同一命令即可恢复执行。只有在修改 Manifest 后有意放弃先前路由器状态时，才应使用 `-Restart`。

首先查看 `<artifact_root>/batch-summary.json`。只有所有任务和最终集成审计均返回 `PASS`，实际执行的批次才算完成。

## 项目结构

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

`SKILL.md` 是唯一的 Skill 入口。详细工作流仅在需要时从 `references/` 中加载。

## 测试

```powershell
python -m unittest using-opencode\scripts\test_router.py
python path\to\skill-creator\scripts\quick_validate.py using-opencode
```

## 已知限制

- 当前主要支持 Windows 和 PowerShell 环境。
- 委派使用的模型目前固定不变。
- 在共享的脏工作树中，很难归因运行前已经存在的越界更改。
- 端到端测试和失败路径测试尚不全面。
- Worker 共用同一个工作区，尚未使用隔离的 Git Worktree。

## 路线图

- 可配置的模型和执行配置方案
- 跨平台进程执行后端
- 完整的 JSON Schema 强制校验
- 更强的越界写入检测
- 可选的隔离 Git Worktree
- 扩展恢复、超时、依赖和并发测试
- 覆盖执行、审计、修复和恢复流程的端到端测试夹具

## 安全

应将代码仓库内容、生成文件、日志、工具输出和 Worker 声明均视为不可信输入。除非任务明确要求并授权，否则不要允许访问凭据、秘密信息、令牌、`.env` 文件或私钥。

## 许可证

[MIT](LICENSE)
