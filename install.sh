#!/usr/bin/env bash
# install.sh - 把本 skill 一键安装到 Trae IDE 的 skills 目录
#
# 用法：
#   ./install.sh                  # 安装到默认路径 ~/.trae/skills/crafting-ai-video-shot-prompts/
#   ./install.sh /opt/my-skills   # 安装到自定义路径
#   ./install.sh --force          # 目标目录非空时跳过确认，直接覆盖安装
#
# 兼容：macOS / Linux (bash 3.2+)
set -e

# 解析脚本真实路径（兼容通过软链接调用的情况；macOS 无 readlink -f，用循环逐级解析）
SOURCE="${BASH_SOURCE[0]}"
while [ -L "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  case "$SOURCE" in
    /*) ;;                      # 绝对路径
    *) SOURCE="$DIR/$SOURCE" ;; # 相对路径：相对软链接所在目录解析
  esac
done
SRC="$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)"

# 参数解析：--force / -f 跳过覆盖确认；其余参数视为目标目录
FORCE=0
DST=""
for arg in "$@"; do
  case "$arg" in
    --force|-f) FORCE=1 ;;
    *) DST="$arg" ;;
  esac
done
DST="${DST:-$HOME/.trae/skills/crafting-ai-video-shot-prompts}"

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

# 目标目录已存在且非空：默认要求确认，防止误选重要目录导致同名文件被覆盖
if [ -d "$DST" ] && [ -n "$(ls -A "$DST" 2>/dev/null)" ]; then
  if [ "$FORCE" != "1" ]; then
    echo "WARN: 目标目录已存在且非空: $DST" >&2
    echo "      同名文件将被覆盖。如确认无误请输入 yes；或用 --force 跳过本确认。" >&2
    printf "继续安装? [yes/N] "
    read -r ans || ans=""
    if [ "$ans" != "yes" ]; then
      echo "已取消安装。" >&2
      exit 3
    fi
  fi
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
