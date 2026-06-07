# Tasks

按"先验证、后写文档、最后串联"的顺序。每条任务都可在 1 个 PR 内完成。

## Task 0：基线对齐

- [x] SubTask 0.1：先跑 `pytest tests/` 确认 v0.2 既有 27 个测试仍全绿；记录结果到 `docs/verify-v0.2-log.md`（新文件）。
- [x] SubTask 0.2：跑 `python scripts/validate_prompt.py templates/*.md` 三次，把当前 v0.2 输出保存到 `docs/verify-v0.2-current.txt`，便于与 `docs/baseline-v0.1.txt` 对比。

## Task 1：回归测试

- [x] SubTask 1.1：新增 `tests/test_regression.py`，定义 3 个 fixture（single-shot / multi-shot / action-scene 模板）。
- [x] SubTask 1.2：实现 `test_single_shot_regression`：subprocess 跑 validate_prompt.py，断言退出码 0；解析 stdout，断言"通过项数 == baseline 通过项数"。
- [x] SubTask 1.3：实现 `test_multi_shot_regression`：同上，但带 `--min-chars 200 --max-chars 3000`。
- [x] SubTask 1.4：实现 `test_action_scene_regression`：同上。
- [x] SubTask 1.5：实现 `test_baseline_missing_skip`：若 `docs/baseline-v0.1.txt` 不存在，用 `pytest.skip()` 跳过所有 3 个测试（不阻塞）。
- [x] SubTask 1.6：跑 `pytest tests/test_regression.py -v` 全部 4 个测试通过。

## Task 2：端到端工作流模拟

- [x] SubTask 2.1：新增 `tests/test_simulate_workflow.py`。
- [x] SubTask 2.2：实现 `test_workflow_full_cycle`：
  1. 准备缺陷提示词（缺【基础设定】、缺参考图、字数 80）
  2. 跑 validate_prompt.py → 断言退出码 1，n_issues >= 3
  3. 改写提示词（补全所有缺失）
  4. 跑 validate_prompt.py --strict → 断言退出码 0，n_issues == 0
- [x] SubTask 2.3：实现 `test_workflow_stdin_echo`：用 `cat prompt.md | python validate_prompt.py -` 验证 stdin 路径与文件路径输出完全一致（用 `diff` 比对）。
- [x] SubTask 2.4：跑 `pytest tests/test_simulate_workflow.py -v` 全部 2 个测试通过。

## Task 3：本地 CI 复刻脚本

- [x] SubTask 3.1：新增 `scripts/ci_local.sh`，8 步检查（pytest / shellcheck / py_compile / 3 模板 / bash 语法 / 自身语法）。
- [x] SubTask 3.2：跑 `bash scripts/ci_local.sh` 全部 8 步通过。
- [x] SubTask 3.3：在 README.md 的"## 验证安装"段补一行：`本地复刻 CI: bash scripts/ci_local.sh`。

## Task 4：PR 描述文档

- [x] SubTask 4.1：新增 `docs/PR_v0.2.0.md`，按 spec 规定的 7 个段写（Title / Motivation / Changes / Test Matrix / Risk & Rollback / Upgrade Guide / Checklist）。
- [x] SubTask 4.2：在 Changes 段把 27 个测试用例 + 3 套模板 + 1 个 CI 文件列出来；Breaking 段直接引用 `audit-and-roadmap/spec.md` 的 MODIFIED 段。
- [x] SubTask 4.3：Upgrade Guide 段写明 3 步迁移：(1) 把"基础设定："改为"【基础设定】" (2) 跑 `python assets/transcribe.py --audio <path>` 而非无参 (3) 跑 `pytest` 验证。
- [x] SubTask 4.4：在文件末尾加一段"使用 `gh pr create --body-file docs/PR_v0.2.0.md`"的指引。

## Task 5：下阶段路线草稿

- [x] SubTask 5.1：新增 `docs/NEXT_STEPS.md`，三段（v0.3 / v0.4 / v1.0），每段含"输入 / 输出 / 验收标准 / 风险"4 字段。
- [x] SubTask 5.2：v0.3 段：多分镜节奏自动分配器
  - 输入：N 个分镜 + 总时长（秒）
  - 输出：每个分镜的"开始时间 / 结束时间 / 时长（秒）"
  - 验收：与 Mx-Shell 在视频中示范的人工分配对比，相对误差 < 10%
  - 风险：分镜权重悬殊（如 95% vs 5%）时算法可能给太短；需要最小分镜时长（建议 1.5s）
- [x] SubTask 5.3：v0.4 段：LLM-as-judge
  - 输入：prompt.md
  - 输出：0-100 分 + 5 条改进建议
  - 验收：与人工评分 ρ > 0.7
  - 风险：模型可能给出"礼貌高分"；需要 few-shot 示例校准
- [x] SubTask 5.4：v1.0 段：平台 API 对接
  - 输入：prompt.md + 模型选择（即梦 / Vidu / 可灵 / Sora / Runway）
  - 输出：生成视频 URL + 任务 ID
  - 验收：成功调用 1+ 个平台 API；处理 401 / 429 / 5xx 错误
  - 风险：各平台 API 变化频繁；需要版本锁定 + 月度回归测试

## Task 6：CHANGELOG 链接收尾

- [x] SubTask 6.1：在 `CHANGELOG.md` 的 `[0.2.0]` 段加 2 个 markdown 链接：`PR 描述` 与 `下阶段路线`。

## Task 7：最终验证

- [x] SubTask 7.1：跑 `bash scripts/ci_local.sh` 8 步全过。
- [x] SubTask 7.2：跑 `pytest tests/ -v` 全部测试通过（27 v0.2 + 14 regression + 3 workflow = 44 个）。
- [x] SubTask 7.3：把 verify-v0.2-log.md 的"最终汇总"段复制到本 spec 的 checklist.md 末尾的"最终状态"段。
- [x] SubTask 7.4：更新 `docs/verify-v0.2-log.md` 记录"完成时间 / 全部测试通过 / 下一步可 push"。

# Task Dependencies

- [Task 1] 依赖 [Task 0]（要先有 baseline 才能做回归）
- [Task 2] 不依赖其他（独立端到端模拟）
- [Task 3] 依赖 [Task 1, Task 2]（CI 脚本要包含新测试）
- [Task 4] 不依赖（纯文档）
- [Task 5] 不依赖（纯设计稿）
- [Task 6] 依赖 [Task 4, Task 5]（链接要指向已存在的文件）
- [Task 7] 依赖所有上面任务

# 可并行

- Task 1 / Task 2 / Task 3 / Task 4 / Task 5 互相独立，可并行
- Task 6 必须最后串行（在 Task 4/5 完成后）
- Task 7 是收口
