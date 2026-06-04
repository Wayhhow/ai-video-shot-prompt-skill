# 安装指南

## 目标位置

Trae IDE 默认从以下位置发现 skill：

| 范围 | 路径 | 适用 |
| --- | --- | --- |
| 项目级 | `<项目根>/.trae/skills/<skill-name>/` | 仅当前项目可见，可入 git |
| 用户级 | `~/.trae/skills/<skill-name>/` | 当前用户全部项目可见 |

> Claude Code 路径不同：`~/.claude/skills/` 或项目下 `.claude/skills/`。

## 方法 1：手动复制（推荐）

### Windows PowerShell

```powershell
# 项目级（推荐：跟项目绑定）
$src = "c:\Users\wayhow\Desktop\AI视频提示词\ai-video-shot-prompt-skill"
$dst = "c:\Users\wayhow\Desktop\AI视频提示词\.trae\skills\crafting-ai-video-shot-prompts"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item -Path "$src\*" -Destination $dst -Recurse -Force

# 用户级（所有项目可见）
$userDst = "$env:USERPROFILE\.trae\skills\crafting-ai-video-shot-prompts"
New-Item -ItemType Directory -Force -Path $userDst | Out-Null
Copy-Item -Path "$src\*" -Destination $userDst -Recurse -Force
```

### macOS / Linux

```bash
SRC="$HOME/path/to/ai-video-shot-prompt-skill"
DST="$HOME/.trae/skills/crafting-ai-video-shot-prompts"
mkdir -p "$DST"
cp -R "$SRC"/. "$DST"/
```

## 方法 2：使用 install 脚本

在 skill 根目录执行：

```bash
# Linux / macOS
./install.sh

# Windows PowerShell
./install.ps1
```

> 脚本需先创建。模板见下方。

## 验证安装

1. 重启 Trae IDE 或重载窗口
2. 输入 `/help` 查找 `crafting-ai-video-shot-prompts`
3. 或者在对话中提到「写一个 AI 视频提示词」，观察 Trae 是否加载本 skill

## 故障排查

- **skill 没被识别**：检查 `SKILL.md` 是否存在且 frontmatter 的 `name` 与目录名一致
- **description 不触发**：description 必须包含 (1) 功能 (2) 触发条件，例如 "When user asks to write..."、"Use when..."
- **路径问题**：Trae 可能不识别带空格的目录；建议 skill 目录放在无空格路径

## install.sh 模板

```bash
#!/usr/bin/env bash
set -e
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DST="${1:-$HOME/.trae/skills/crafting-ai-video-shot-prompts}"
mkdir -p "$DST"
cp -R "$SRC"/. "$DST"/
echo "Installed to $DST"
```

## install.ps1 模板

```powershell
$src = Split-Path -Parent $MyInvocation.MyCommand.Path
$dst = "$env:USERPROFILE\.trae\skills\crafting-ai-video-shot-prompts"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item -Path "$src\*" -Destination $dst -Recurse -Force
Write-Host "Installed to $dst"
```
