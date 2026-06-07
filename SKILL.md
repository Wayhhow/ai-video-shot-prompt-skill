---
name: crafting-ai-video-shot-prompts
description: >
  为 AI 视频生成（即梦/Vidu/可灵/小云雀/Sora/Runway 等）编写、评审和润色中文分镜提示词。
  整合 Mx-Shell《丧尸清道夫》创作者公开的"基础设定/氛围画质/画面内容"三大部分框架与去 AI 味技巧。
  当用户需要写一个镜头提示词、规划多分镜短剧、为 AI 短片打分、或希望降低生成画面的 AI 痕迹
  （特别是动作/原子朋克/末日/电影感场景）时调用。
  Writes, reviews, and refines Chinese shot-list prompts for AI video generators
  (即梦/Vidu/可灵/小云雀/Sora/Runway). Encapsulates the three-part
  "基础设定/氛围画质/画面内容" framework and de-AI-flavor techniques from
  Mx-Shell's "Zombie Scavenger" methodology. Use when the user wants to write a
  single shot, plan a multi-shot short, score an AI video script, or reduce AI
  artifacts (plastic skin, stiff motion, game-CG feel) in action / cinematic /
  atomic-punk / zombie / wuxia / cyberpunk scenes.
keywords:
  - ai video prompt
  - shot list
  - chinese
  - sora
  - runway
  - kling
  - 即梦
  - vidu
  - atomic punk
  - cinematic
  - action
  - scoring
---

# Crafting AI Video Shot Prompts

把"丧尸清道夫"创作者 Mx-Shell 的提示词方法论封装为可复用的工作流。当用户给出故事想法、参考图、或一句"帮我写个 AI 视频提示词"时，按本 skill 的三大部分框架产出可直接喂给 AI 视频模型的提示词。

## 何时调用

- 用户要写/改/评审 AI 视频提示词（任意题材，尤其是动作、奇观、电影感、原子朋克、末日、丧尸、机甲、武打）
- 用户要把已有分镜整理成 AI 视频模型可用的 prompt
- 用户希望降低生成画面的"AI 味"（塑料感、动作僵硬、游戏 CG 感）
- 用户用小云雀短剧 Agent 2.0、即梦、Vidu、可灵、Sora、Runway 等生成视频前需要写提示词

## 不调用

- 用户只想做纯文字剧本/故事大纲（用 brainstorming）
- 用户在做代码/网页/PPT 等与视频提示词无关的任务
- 用户只是单纯想看 B 站视频文案（用 jina reader / 本地 transcript）

## 工作流（5 步）

执行时严格按以下顺序与 Claude 协作：

### 1. 收集输入

从用户处至少拿到以下信息（缺什么就问什么）：

- **场景一句话**：1-2 句话概括这个镜头在发生什么
- **风格基调**：原子朋克 / 末日丧尸 / 电影动作 / 喜剧幽默 / 古风仙侠 / ……
- **画面主体**：人物/生物/物体 + 关键动作
- **时间 / 地点 / 时代背景**
- **参考图**（如有）：必须先用一句话描述参考图内容，再交给 AI
- **生成目标平台**：决定是否需要限制声音（见 §3.1）

### 2. 按"三大部分"框架起草

提示词**必须**按以下顺序组织（顺序敏感，因为模型对前文权重更高）：

1. **基础设定**（时间 / 地点 / 人物 / 参考图描述 / 声音限制）
2. **氛围画质**（风格核心 + 限制词 + 视觉基调 + 色彩影调）
3. **画面内容**（分镜 / 景别 / 构图 / 运镜 / 故事内容）

每部分的写法见 [references/framework.md](references/framework.md)。

### 3. 应用"去 AI 味"关键词

强制在第二部分（氛围画质）里加入以下关键词之一或组合，显著降低塑料感：

- `超写实`、`极致逼真`、`真人实景拍摄`
- 题材相关：动作片加 `电影动作捕捉`、末日加 `废墟纪实风格`、原子朋克加 `复古胶片质感`
- 限制词：`杜绝游戏CG感`、`杜绝动作僵硬`、`杜绝镜头漂移`

完整关键词库见 [references/keyword-library.md](references/keyword-library.md)。

### 4. 选择景别/构图/运镜

按场景情绪从以下清单各选 1 项（或多选组合），写入"画面内容"：

- **景别**：特写 / 近景 / 中景 / 远景 / 全景 / 微距 / 大广角 / 监控 / 第一人称
- **构图**：三分线 / 黄金分割 / 对角线 / 引导线 / 荷兰角 / 中心对称
- **运镜**：推 / 拉 / 摇 / 移 / 跟 / 固定 / 手持 / 第一人称模拟 / 希区柯克变焦 / 环绕 / 低角度仰拍 / 航拍

详细解释和适用场景见 [references/camera-and-composition.md](references/camera-and-composition.md)。

### 5. 输出 + 自检

按 [templates/single-shot.md](templates/single-shot.md) 或 [templates/multi-shot.md](templates/multi-shot.md) 输出最终提示词；多镜头动作戏用 [templates/action-scene.md](templates/action-scene.md)。

随后用 [scripts/validate_prompt.py](scripts/validate_prompt.py) 做结构自检，确保三大段都齐、关键词就位、参考图描述存在。

## 三大部分速查（详细见 references/）

```
【基础设定】
- 时间：例如 "黄昏 / 末日第 7 天"
- 地点：例如 "废弃加油站、加州 1 号公路旁"
- 人物：主角名字、年龄、关键特征、装备
- 参考图描述：先用 1-2 句话描述参考图内容（让 AI 知道你给的是啥）
- 声音限制：（仅 C-Dance 类自动配乐平台）明确写"无需背景音乐、无需氛围音、保留对白与环境音"

【氛围画质】
- 风格核心：原子朋克、末日丧尸、电影动作、复古胶片、……（3-5 个关键词）
- 去 AI 味关键词：超写实、极致逼真、真人实景拍摄（强制）
- 限制词：杜绝游戏CG感、杜绝动作僵硬、杜绝镜头漂移（按需）
- 视觉基调：模拟设备（如 ARRI Alexa 65、RED Komodo、胶片摄影机、手机竖屏、监控）
- 氛围描述：例如"温馨的下午茶场景与突然闯入的丧尸形成荒诞反差"
- 色彩影调：青橙对比 / 暖黄高光 / 去饱和冷调 / 黑白高反差（1 句话即可）

【画面内容】
- 分镜：单镜头一镜到底 / 多分镜（说明每个分镜的侧重）
- 景别：特写 / 近景 / 中景 / 远景 / 微距 / 大广角
- 构图：三分线 / 黄金分割 / 对角线 / 引导线 / 荷兰角
- 运镜：推拉摇移 / 手持 / 第一人称 / 希区柯克变焦
- 故事内容：用"要怎么做 → 为什么要这样做 → 想要什么效果"三段式描述动作
  例：鸵鸟脚掌猛踩报纸（怎么做）→ 脚被粘住不舒服（为什么）→ 改为单脚跳跃前进、滑稽荒诞（效果）
```

## 反模式（必须避免）

- ❌ 用命令式语气："给我做一个"、"必须出现 X"——把 AI 当伙伴而非工具
- ❌ 直接丢参考图不描述——AI 不知道你给的是什么
- ❌ 多分镜不写时间占比——AI 不会精准卡时长，应给"前 2/3 是……最后 1/3 是……"
- ❌ 写武戏只写"打"——要写具体的动作序列（掏枪→射击→收枪→转身）
- ❌ 不加"为什么这样做"——AI 不知道因果链，画面容易崩坏
- ❌ 完全依赖 AI 写提示词——AI 给的稿还要人工细化分镜/时长/动作细节

> 完整 12 条可勾选质量清单见 [references/prompt-quality-checklist.md](references/prompt-quality-checklist.md)（v0.2 引入）。

## 配套资源

| 文件 | 用途 |
| --- | --- |
| [references/framework.md](references/framework.md) | 三大部分逐项详解 |
| [references/keyword-library.md](references/keyword-library.md) | 风格/限制/设备/色调关键词库 |
| [references/prompt-quality-checklist.md](references/prompt-quality-checklist.md) | 写完后的 12 条可勾选质量清单（v0.2 引入） |
| [references/camera-and-composition.md](references/camera-and-composition.md) | 景别、构图、运镜完整清单与适用场景 |
| [references/workflow-and-storyboard.md](references/workflow-and-storyboard.md) | 小云雀短剧 Agent 2.0 工作流 + 抽卡策略 |
| [references/post-production.md](references/post-production.md) | 后期剪辑：动作匹配转场、调色、色彩克隆、速度调整、太阳/旗杆等空间一致性 |
| [references/examples.md](references/examples.md) | 视频中提到的完整示例（鸵鸟粘报纸、机器人踢丧尸等） |
| [templates/single-shot.md](templates/single-shot.md) | 单镜头提示词模板 |
| [templates/multi-shot.md](templates/multi-shot.md) | 多分镜提示词模板 |
| [templates/action-scene.md](templates/action-scene.md) | 动作/打斗分镜模板 |
| [templates/style-presets.md](templates/style-presets.md) | 原子朋克/末日丧尸/电影动作等风格预设 |
| [scripts/validate_prompt.py](scripts/validate_prompt.py) | 提示词结构自检脚本 |
| [assets/transcribe.py](assets/transcribe.py) | faster-whisper 转录脚本（供用户自行从 B 站源视频生成转录，仓库不包含任何转录/音频产物） |

## 安装到 Trae IDE

把本目录复制到 `.trae/skills/crafting-ai-video-shot-prompts/` 即可被 Trae 自动发现并调用。详细步骤见 [INSTALL.md](INSTALL.md)。
