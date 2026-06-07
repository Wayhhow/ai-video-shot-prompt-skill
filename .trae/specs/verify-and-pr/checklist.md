# Checklist

完成本 spec 后，逐项验证。

## A. 回归测试 (Task 1)

- [x] A1. `tests/test_regression.py` 存在
- [x] A2. 跑 `pytest tests/test_regression.py -v` 14 个测试（4 类 × 3 模板 + 1 红线 + 1 baseline 结构）全过
- [x] A3. 删除 `docs/baseline-v0.1.txt` 后跑测试，全部 14 个测试应 skip 而非 fail（实测 14 skipped, exit 0）
- [x] A4. 把 `docs/baseline-v0.1.txt` 恢复后跑测试，14 个测试应恢复 pass

## B. 端到端模拟 (Task 2)

- [x] B1. `tests/test_simulate_workflow.py` 存在
- [x] B2. 跑 `pytest tests/test_simulate_workflow.py -v` 3 个测试（full_cycle + stdin_echo + strict_vs_non_strict）全过
- [x] B3. `test_workflow_full_cycle` 第二个断言（修复后通过）是有效红线，issues 数从 N>=2 降至 0

## C. 本地 CI 复刻 (Task 3)

- [x] C1. `scripts/ci_local.sh` 存在，`chmod +x` 后可执行
- [x] C2. 跑 `bash scripts/ci_local.sh` 8 步全过（pytest / shellcheck skipped on Linux / py_compile / 3 模板 / 2 个 bash 语法）
- [x] C3. README.md 的"### 本地复刻 CI"段含 `bash scripts/ci_local.sh` 一行

## D. PR 描述 (Task 4)

- [x] D1. `docs/PR_v0.2.0.md` 存在
- [x] D2. 含 7 个段：Title / Motivation / Changes / Test Matrix / Risk & Rollback / Upgrade Guide / Checklist
- [x] D3. Changes 段把 27 / 14 / 3 个测试用例 + 3 套模板 + 1 个 CI 文件列出
- [x] D4. Upgrade Guide 段含 v0.1 → v0.2 的 3 步迁移（含 GNU sed / BSD sed 双命令）
- [x] D5. 文件末尾含 `gh pr create --body-file docs/PR_v0.2.0.md --base main` 命令

## E. 下阶段路线 (Task 5)

- [x] E1. `docs/NEXT_STEPS.md` 存在
- [x] E2. v0.3 / v0.4 / v1.0 三段齐全
- [x] E3. 每段含"输入 / 输出 / 验收标准 / 风险"4 字段
- [x] E4. v0.3 验收标准含"与 Mx-Shell 人工分配对比，相对误差 < 10%"
- [x] E5. v0.4 验收标准含"与人工评分 ρ > 0.7"
- [x] E6. v1.0 验收标准含"成功调用 1+ 个平台 API"

## F. CHANGELOG 链接 (Task 6)

- [x] F1. `CHANGELOG.md` 的 `[0.2.0]` 段含"PR 描述"和"下阶段路线"两个链接
- [x] F2. 两个链接都指向真实存在的 markdown 文件（`docs/PR_v0.2.0.md` 与 `docs/NEXT_STEPS.md`）

## G. 整体收尾 (Task 7)

- [x] G1. `bash scripts/ci_local.sh` 跑通
- [x] G2. `pytest tests/ -v` 全部 44 个测试通过（27 v0.2 + 14 regression + 3 workflow）
- [x] G3. `docs/verify-v0.2-log.md` 含"完成时间 / 全部测试通过 / 下一步可 push"三行
- [x] G4. 本 spec 的 checklist.md 末尾含"最终状态"段

## H. 文档与版权边界

- [x] H1. 三大段方法论、关键词库、模板的写作风格未改
- [x] H2. CREDITS.md 未改
- [x] H3. .gitignore 未改
- [x] H4. v0.2 引入的 4 个 bug fix、5 套预设、CI、测试未被回退

---

## 最终状态 Final Status

| 维度 | 数值 | 备注 |
| --- | --- | --- |
| 完成日期 | 2026-06-07 |  |
| Spec 数（累计） | 2 | `audit-and-roadmap` + `verify-and-pr` |
| 单元测试 | 27 | v0.2 行为测试 |
| 回归测试 | 14 | 3 套模板 × 4 维度 + 2 边界 |
| 端到端测试 | 3 | 写→检→修→检 + stdin vs file + strict |
| **总测试数** | **44** | pytest 全部通过 |
| 本地 CI 步数 | 8 | 全部通过 |
| 3 套模板自检 | 3 / 3 | issues = 0 |
| 文档 | 3 | PR 描述 / NEXT_STEPS / verify-v0.2-log |
| 待 push 提交 | 1 | 见 `docs/PR_v0.2.0.md` 末尾的 `gh pr create` 命令 |
