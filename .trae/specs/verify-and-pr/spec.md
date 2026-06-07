# v0.2 验证与 PR Spec

## Why

`audit-and-roadmap` spec 已把 v0.2.0 实施完毕（4 bug 修复 + 5 套预设 + 工程化基础设施 + 文档收尾），但还有三件"上线前必做"没做：

1. **回归验证** — v0.1 的 3 套提示词模板在 v0.2 自检脚本下应该**全部通过**（基线已存 `docs/baseline-v0.1.txt`）。这是"原来的东西无误"的最基本要求。
2. **PR 描述** — 27 个测试 + 1 个 CI + 1 个 BREAKING + 1 个文档结构，变更范围远超一个常规提交，需要结构化 PR 让 reviewer 一眼看懂。
3. **下一步路线** — v0.3（多分镜节奏自动分配）/ v0.4（LLM-as-judge）/ v1.0（平台 API）已在 CHANGELOG `Planned` 段占位，但缺少"输入/输出/验收标准"级别的设计稿。

本 spec 不引入新功能，**只为 v0.2 收尾做最后一道质量门**。

## What Changes

- **新增** `tests/test_regression.py`：把 3 套模板的基线输出逐行与 v0.1 行为对比，作为"未引入回归"的金标准
- **新增** `tests/test_simulate_workflow.py`：模拟"用户从 stdin 输入提示词 → validate_prompt.py 检查 → 修复 → 通过"的端到端流程
- **新增** `docs/PR_v0.2.0.md`：完整 PR 描述（标题、动机、改动列表、测试矩阵、风险与回滚、升级指引）
- **新增** `docs/NEXT_STEPS.md`：v0.3 / v0.4 / v1.0 三个 spec 的"输入/输出/验收标准"草稿
- **新增** `scripts/ci_local.sh`：本地一键复刻 GitHub Actions（pytest + shellcheck），方便不联网时验证
- **更新** `CHANGELOG.md`：[0.2.0] 段补充一个指向 PR 与 NEXT_STEPS 的链接

## Impact

- **Affected specs**: `audit-and-roadmap`（无修改，仅引用其输出）
- **Affected code**:
  - 新增 `tests/test_regression.py` / `tests/test_simulate_workflow.py`
  - 新增 `docs/PR_v0.2.0.md` / `docs/NEXT_STEPS.md`
  - 新增 `scripts/ci_local.sh`
  - `CHANGELOG.md` [0.2.0] 段加 2 个链接
- **Affected code (校验)**：无运行时影响；只跑测试与端到端模拟
- **下游影响**：
  - 任何 v0.2 升级用户都能从 `docs/PR_v0.2.0.md` 看到 BREAKING 升级路径
  - 任何后续 spec 作者能从 `docs/NEXT_STEPS.md` 拿到 v0.3/0.4/1.0 的输入输出草稿

## ADDED Requirements

### Requirement: 模板基线回归测试

新增 `tests/test_regression.py`，把 `docs/baseline-v0.1.txt` 与当前 v0.2 的 `validate_prompt.py` 输出做对比。

**对比规则**：
- 对 3 套模板（single-shot / multi-shot / action-scene）分别跑 `validate_prompt.py`
- 对 multi-shot / action-scene 跑 `--min-chars 200 --max-chars 3000`（与 baseline 一致）
- 比对"通过项数 / 警告数 / 严重数"三类计数
- 期望：三类计数与 baseline 完全相同

#### Scenario: 模板通过率不退化
- **WHEN** 跑 `pytest tests/test_regression.py`
- **THEN** 3 套模板都判定为"通过项数 >= 基线"，无回归

#### Scenario: baseline 文件缺失
- **WHEN** `docs/baseline-v0.1.txt` 不存在
- **THEN** 测试 skip 而非 fail（首次跑或清理后不阻塞）

### Requirement: 端到端工作流模拟

新增 `tests/test_simulate_workflow.py`，模拟"写 → 检 → 修 → 检"循环：

1. 准备一份**故意有缺陷**的提示词（缺【基础设定】、顺序错乱、字数过少）
2. 跑 `validate_prompt.py` → 期望退出码 1
3. 改写提示词（补全【基础设定】、调整顺序、补字数）
4. 再跑 `validate_prompt.py --strict` → 期望退出码 0
5. 对比前后输出文件，确认 issues 数从 N 降到 0

#### Scenario: 缺陷提示词被检出
- **WHEN** 把故意有缺陷的提示词喂给 validate_prompt.py
- **THEN** 退出码 = 1，且报告 `n_issues >= 3`

#### Scenario: 修复后再检查通过
- **WHEN** 把修复后的提示词喂给 validate_prompt.py --strict
- **THEN** 退出码 = 0，issues 数为 0

### Requirement: PR 描述文档

新增 `docs/PR_v0.2.0.md`，结构：

1. **Title**: `feat: v0.2.0 — 5 new style presets + cross-platform scripts + pytest + CI`
2. **Motivation** (3-5 句)：v0.1 收尾后的三大问题（macOS 不可用 / 缺测试 / 5 套预设缺位）
3. **Changes**（分 4 个区块）：Added / Changed / Breaking / Docs
4. **Test Matrix**：本地 27/27 + CI 矩阵 + 3 模板回归
5. **Risk & Rollback**：BREAKING 影响面 + 单 PR revert 方案
6. **Upgrade Guide**：v0.1 → v0.2 升级 3 步（改大节标题、修正脚本入口、跑新测试）
7. **Checklist**：与 [checklist.md](../.trae/specs/audit-and-roadmap/checklist.md) 联动

#### Scenario: 完整 PR 描述
- **WHEN** reviewer 阅读 PR 描述
- **THEN** 5 分钟内能回答"为什么改 / 改了什么 / 是否安全 / 怎么升级 / 测试过了吗"

### Requirement: 下一步路线草稿

新增 `docs/NEXT_STEPS.md`，为 v0.3 / v0.4 / v1.0 各列：

- **输入 / 输出 / 验收标准 / 风险** 四字段
- v0.3：多分镜节奏自动分配器（输入 N + 总时长 → 输出每镜时长；验收：与人工分配误差 < 10%）
- v0.4：LLM-as-judge（输入 prompt.md → 输出 0-100 分 + 5 条改进建议；验收：与人工评分 ρ > 0.7）
- v1.0：平台 API 对接（输入 prompt + 模型选择 → 输出生成视频 URL；验收：成功调用 1+ 个平台 API）

#### Scenario: 设计稿可执行
- **WHEN** 后续 spec 作者读 NEXT_STEPS
- **THEN** 能直接基于此文档写 v0.3/v0.4/v1.0 的 spec.md，不需要重新调研

### Requirement: 本地 CI 复刻脚本

新增 `scripts/ci_local.sh`，顺序跑：
1. `pytest tests/ -v`
2. `shellcheck install.sh`（如果命令存在）
3. `python -m py_compile scripts/*.py assets/*.py`
4. `python scripts/validate_prompt.py templates/single-shot.md`
5. `python scripts/validate_prompt.py templates/multi-shot.md --min-chars 200 --max-chars 3000`
6. `python scripts/validate_prompt.py templates/action-scene.md --min-chars 200 --max-chars 3000`
7. `bash -n install.sh`（语法检查）
8. `bash -n scripts/ci_local.sh`（自身语法检查）

#### Scenario: 一键本地验证
- **WHEN** 开发者跑 `bash scripts/ci_local.sh`
- **THEN** 在不联网的情况下复刻 GitHub Actions 的关键检查

### Requirement: CHANGELOG 链接补全

`CHANGELOG.md` 的 `[0.2.0]` 段加 2 个链接：
- `[PR 描述 → docs/PR_v0.2.0.md](../docs/PR_v0.2.0.md)`
- `[下阶段路线 → docs/NEXT_STEPS.md](../docs/NEXT_STEPS.md)`

#### Scenario: CHANGELOG 自包含
- **WHEN** 用户只读 CHANGELOG
- **THEN** 1 跳可达 PR 描述 + 下阶段路线

## MODIFIED Requirements

无。

## REMOVED Requirements

无。

## 不在本次 spec 范围

- 实际 `gh pr create` 命令执行（本环境为 CI 沙箱，无 git remote / 无 GitHub 凭据；PR 文档已就位，真实环境只需 `gh pr create --body-file docs/PR_v0.2.0.md`）
- 任何新功能（v0.3/0.4/1.0 都推迟到独立 spec）
- 任何 v0.2 代码修改（仅验证 + 文档）

## 风险与回滚

- **风险 1**：regression 测试对 baseline 的格式变化敏感。**回滚**：把 baseline 视为"接口契约"，要改格式时同步更新 baseline 并在 CHANGELOG 记录。
- **风险 2**：`ci_local.sh` 的 `shellcheck` 在 macOS 默认未装。**回滚**：脚本已用 `command -v shellcheck` 检测，跳过而非失败。
- **风险 3**：`docs/NEXT_STEPS.md` 是设计草稿，可能与实际 v0.3/0.4 spec 有出入。**回滚**：在后续 spec 启动时校对 NEXT_STEPS 草稿与本 spec 的差异，更新到 NEXT_STEPS.md。
