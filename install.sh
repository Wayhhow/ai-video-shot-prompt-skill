#!/usr/bin/env bash
# install.sh - 把本 skill 一键安装到 Trae IDE 的 skills 目录
#
# 用法：
#   ./install.sh                  # 安装到默认路径 ~/.trae/skills/crafting-ai-video-shot-prompts/
#   ./install.sh /opt/my-skills   # 安装到自定义路径
#
# 兼容：macOS / Linux (bash 3.2+)
set -e

# 解析脚本所在目录
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 目标目录（参数 1 或默认）
DST="${1:-$HOME/.trae/skills/crafting-ai-video-shot-prompts}"

# 防止把脚本装到自己头上
if [ "$SRC" = "$DST" ]; then
  echo "ERROR: 源目录与目标目录相同: $SRC" >&2
  exit 2
fi

# 防止装到根目录
if [ "$DST" = "/" ] || [ -z "$DST" ]; then
  echo "ERROR: 目标目录无效: $DST" >&2
  exit 2
fi

mkdir -p "$DST"

# 用 cp -R 把当前仓库的 *所有* 内容复制到目标
# 注意：源文件里的隐藏文件（.github/、.gitignore、.trae/）需要一并复制
shopt -s dotglob nullglob 2>/dev/null || true
for item in "$SRC"/*; do
  name="$(basename "$item")"
  # 跳过 .git 目录（如果有）
  if [ "$name" = ".git" ]; then
    continue
  fi
  cp -R "$item" "$DST/"
done

echo "Installed to $DST"
echo ""
echo "下一步："
echo "  1. 重启 Trae IDE 或重载窗口"
echo "  2. 在对话中提到「写一个 AI 视频提示词」即可触发本 skill"
