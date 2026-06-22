# SRT Enhancer

字幕优化 Agent Skill — 去口癖、ASR 纠错、的/得/地修正、中西文混排空格、标点清理。

## 触发词

在支持 Agent Skills 的 CLI（OpenCode、Claude Code、Cursor 等）中，说以下任意一句即可自动调用：

```
优化字幕 / 增强字幕
优化这个字幕 / 增强这个字幕
optimize subtitles / enhance SRT
clean up ASR transcript / filler removal
```

输入后 Agent 会自动：检测字幕领域 → 加载对应术语表 → 执行 5 步流水线 → 生成 diff 审核表 → 用户确认后输出。

### 手动指定领域

```
帮我优化这个 Maya 教程的字幕
处理这段 Python 字幕，去掉口癖
这是一段游戏字幕，clean up ASR 错误
```

## 安装

### OpenCode / Claude Code / Cursor 等

```bash
# 安装（自动注册到 skills 列表）
npx skills@latest install https://github.com/zzh-editor/Srt-Enhancer

# 更新
npx skills@latest update https://github.com/zzh-editor/Srt-Enhancer

# 查看已安装的 skills
npx skills@latest list
```

### 直接克隆（开发者）

```bash
git clone https://github.com/zzh-editor/Srt-Enhancer.git
cd Srt-Enhancer
bash scripts/setup.sh
git pull origin main  # 更新
```

> 需要 Python 3.8+。

## 工作流程

```
用户说"优化字幕"
      │
      ▼
Agent 收到并加载 skill
      │
      ▼
AI 阶段: 解析文件 → 检测领域 → 构建术语配置
      │   触发词自动匹配，无需手动传参
      ▼
enhance.py 零 AI 流水线（~265ms / 1127段）
   normalize → terminology → spacing → refine → finalize
   └─ defiller+de_de+ratio_format      └─ depunct+hotkeys
      │
      ▼
AI 审查: 书名号标记 → diff 审核表 → 用户确认 → 写入输出
```

## 处理能力

| 功能 | 说明 |
|------|------|
| 去口癖 | 啊/哦/嗯/呃/哎/噢/唔/欸 等，保留话语标记(说白了/也就是说) |
| 的得地修正 | R1 V+的+比较(越来越多)→得 / R2 V+的+极端补语(要命)→得 / R3 副词的+V→地 |
| ASR 术语校准 | correction-table.md + 用户 overrides，三级模糊匹配 |
| 领域自适应 | Maya(18关键词)/Python/Gaming/AI-3D/Substance/General |
| 中西文混排 | CJK-Latin 自动空格、数字-字母再紧凑(2D/3D/4K/UV)、代码保护 |
| 语义断句 | 8 级递归切割：句末标点/转折连词/话题标记/话语标记/时间状语/OK隔离/响应标记/重复检测 |
| 快捷键 | Ctrl+E/Ctrl+C/Ctrl+V 标准化，最后执行避免 + 被剥离 |
| 置信度评分 | 每项修改标注置信度，低置信度需用户确认 |
| 增量学习 | 用户确认的修正持久化到 correction-table.md |

## Pipeline 步骤详情

| 步骤 | CLI 名 | 功能 | 子步骤 |
|------|--------|------|--------|
| 1 | `normalize` | 文本规范化 | defiller(去口癖) → de_de(的得地修正) → ratio_format(16比9→16:9) |
| 2 | `terminology` | ASR 术语替换 | correction-table.md + overrides，三级匹配(精确→大小写→归一化) |
| 3 | `spacing` | 混排空格 | CJK-Latin 加空格、数字-字母再紧凑、代码/公式保护 |
| 4 | `refine` | 级联语义断句 | 8 级递归切割，无语义断点时合并短片段 |
| 5 | `finalize` | 最终清理 | depunct(去标点,保护《》/代码域) → hotkeys(Ctrl+E标准化) |

> `normalize` 和 `finalize` 是合并步骤。旧版单步名 `defiller,de_de,ratio_format,depunct,hotkeys` 仍可通过 `--steps` 使用。

## 直接调用脚本

```bash
# 基础
python3 scripts/enhance.py input.srt -o output_Enhancer.srt --lang zh --domain maya

# 带用户覆盖术语
python3 scripts/enhance.py input.srt -o output_Enhancer.srt \
  --lang zh --domain maya+gaming \
  --overrides '{"Owatch":"Overwatch","R Center":"Art Center"}'

# 仅特定步骤
python3 scripts/enhance.py input.srt --steps terminology,spacing

# 跳过 refine（上游已做语义断句时）
python3 scripts/enhance.py input.srt --skip refine

# 干跑预览
python3 scripts/enhance.py input.srt --dry-run
```

## 脚本

| 脚本 | 用途 |
|------|------|
| `scripts/enhance.py` | 主流水线，支持 `--config`、`--steps`、`--skip`、`--overrides`、`--dry-run` |
| `scripts/refine_segments.py` | 8 级级联语义断句引擎 |
| `scripts/apply_spacing.py` | CJK-Latin 混排空格（inline 调用，无子进程） |
| `scripts/domain_scanner.py` | 关键词频次领域检测 |
| `scripts/title_marker.py` | 游戏/影视作品《》书名号标记 |
| `scripts/confidence_scorer.py` | 置信度评分 |
| `scripts/setup.sh` | 依赖自动安装 |

## 文件结构

```
srt-enhancer/
├── scripts/            # 可执行脚本
├── references/         # 术语表、领域定义、规则文档
├── SKILL.md            # Agent skill 定义（含完整工作流）
└── README.md
```

## License

[MIT](LICENSE)
