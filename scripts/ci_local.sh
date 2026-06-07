#!/usr/bin/env bash
# ci_local.sh - 本地复刻 GitHub Actions 的关键检查
#
# 用法：bash scripts/ci_local.sh
#
# 兼容性：macOS / Linux（bash 3.2+）
# 退出码：0=全部通过；非 0=至少一步失败
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0

step() {
  local name="$1"
  shift
  echo
  echo "=== [Step $((PASS + FAIL + 1))] $name ==="
  if "$@"; then
    echo "    [OK] $name"
    PASS=$((PASS + 1))
  else
    echo "    [X] $name"
    FAIL=$((FAIL + 1))
  fi
}

# 1. pytest 全部测试
step "pytest tests/" python -m pytest tests/ -v

# 2. shellcheck install.sh（如果命令存在）
if command -v shellcheck >/dev/null 2>&1; then
  step "shellcheck install.sh" shellcheck install.sh
else
  echo
  echo "=== [Step 2] shellcheck install.sh ==="
  echo "    [SKIP] shellcheck 未安装（macOS: brew install shellcheck）"
fi

# 3. Python 脚本语法编译
step "py_compile scripts/*.py assets/*.py" python -m py_compile scripts/*.py assets/*.py

# 4-6. 3 套模板自检
step "validate single-shot" python scripts/validate_prompt.py templates/single-shot.md
step "validate multi-shot (--min 200 --max 3000)" python scripts/validate_prompt.py templates/multi-shot.md --min-chars 200 --max-chars 3000
step "validate action-scene (--min 200 --max 3000)" python scripts/validate_prompt.py templates/action-scene.md --min-chars 200 --max-chars 3000

# 7. bash 语法检查
step "bash -n install.sh" bash -n install.sh

# 8. 自身语法检查
step "bash -n scripts/ci_local.sh" bash -n scripts/ci_local.sh

echo
echo "============================================================"
echo "汇总：$PASS 步通过 / $FAIL 步失败"
echo "============================================================"
exit $FAIL
