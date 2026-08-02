# 安装指南

## 目标位置

Trae IDE 默认从以下位置发现 skill：

| 范围 | 路径 | 适用 |
| --- | --- | --- |
| 项目级 | `<项目根>/.trae/skills/<skill-name>/` | 仅当前项目可见，可入 git |
| 用户级 | `~/.trae/skills/<skill-name>/` | 当前用户全部项目可见 |

> Claude Code 路径不同：`~/.claude/skills/` 或项目下 `.claude/skills/`。

## 方法 1：使用 install 脚本（v0.2 推荐）

仓库根目录下已有可执行脚本，无需自己写：

```bash
# Linux / macOS（默认装到 ~/.trae/skills/crafting-ai-video-shot-prompts/）
./install.sh

# 自定义目标
./install.sh /opt/my-skills

# Windows PowerShell
.\install.ps1

# Windows PowerShell 自定义目标
.\install.ps1 -DestDir "C:\my\skills\foo"

# 目标目录已存在且非空时，脚本会先要求确认；确认要覆盖可用 --force / -Force 跳过确认
./install.sh --force
.\install.ps1 -Force
```

脚本会：
- 自动跳过 `.git/` 目录
- 把仓库所有内容（含隐藏文件 `.github/`、`.gitignore`、`.trae/` 等）复制到目标
- 防止目标目录是 `/` 或源目录本身（保护性检查）
- 目标目录已存在且非空时提示确认，防止误覆盖重要目录（`--force` / `-Force` 可跳过）
- 通过软链接调用 install.sh 时也能正确定位仓库真实路径
- 打印"下一步"指引

## 方法 2：手动复制

如果不想用脚本：

### Windows PowerShell

```powershell
# 项目级（推荐：跟项目绑定）
$src = "<skill 仓库路径>"
$dst = "<项目根>\.trae\skills\crafting-ai-video-shot-prompts"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Get-ChildItem -Path $src -Force | Where-Object { $_.Name -ne ".git" } | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination (Join-Path $dst $_.Name) -Recurse -Force
}

# 用户级（所有项目可见）
$userDst = "$env:USERPROFILE\.trae\skills\crafting-ai-video-shot-prompts"
New-Item -ItemType Directory -Force -Path $userDst | Out-Null
Get-ChildItem -Path $src -Force | Where-Object { $_.Name -ne ".git" } | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination (Join-Path $userDst $_.Name) -Recurse -Force
}
```

### macOS / Linux

```bash
SRC="$HOME/path/to/ai-video-shot-prompt-skill"
DST="$HOME/.trae/skills/crafting-ai-video-shot-prompts"
mkdir -p "$DST"
# 跳过 .git
for item in "$SRC"/*; do
  [ "$(basename "$item")" = ".git" ] && continue
  cp -R "$item" "$DST/"
done
```

## 验证安装

1. 重启 Trae IDE 或重载窗口
2. 输入 `/help` 查找 `crafting-ai-video-shot-prompts`
3. 或者在对话中提到「写一个 AI 视频提示词」，观察 Trae 是否加载本 skill
4. 进阶验证：跑 `python ~/.trae/skills/crafting-ai-video-shot-prompts/scripts/validate_prompt.py <任意 .md>` 确认脚本可执行

## 故障排查

- **skill 没被识别**：检查 `SKILL.md` 是否存在且 frontmatter 的 `name` 与目录名一致
- **description 不触发**：description 必须包含 (1) 功能 (2) 触发条件，例如 "When user asks to write..."、"Use when..."
- **路径问题**：Trae 可能不识别带空格的目录；建议 skill 目录放在无空格路径
- **Python 脚本中文乱码**：脚本已 `reconfigure(encoding="utf-8")`，但运行环境的 stdout 若不支持 UTF-8，请设置 `PYTHONIOENCODING=utf-8` 环境变量

## 脚本开发指南

`install.sh` / `install.ps1` 是 v0.2 引入的真实可执行文件（已可用，非占位脚本）。如果你想修改：
- 修改后请在 Linux/macOS 跑 `bash -n install.sh` 检查语法
- 在 Windows 跑 `powershell -NoProfile -Command "Get-Command ./install.ps1 | Out-Null"` 检查语法
- 在 GitHub Actions 跑 `shellcheck install.sh`（已配置在 `.github/workflows/ci.yml`）
