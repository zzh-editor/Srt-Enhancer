# SRT Enhancer

字幕增强工具（SRT/TXT），提供去口癖、ASR 纠错、的/得/地修正、中西文混排空格、标点清理等流水线处理。

## 安装

```bash
# 使用 npx 安装（推荐）
npx skills@latest install https://github.com/zzh-editor/Srt-Enhancer

# 或直接克隆
git clone https://github.com/zzh-editor/Srt-Enhancer.git
cd Srt-Enhancer
bash scripts/setup.sh
```

> 需要 Python 3.8+。

## Pipeline

```
输入 SRT/TXT
      │
      ▼
① 领域检测 (domain_scanner.py)
      │   Maya / Python / Gaming / AI-3D / Substance / General
      ▼
② AI 配置：语言检测 + 术语校准 + 对照表构建
      │   用户 overrides > correction-table.md > 领域联网搜索 > AI 猜测
      ▼
③ enhance.py 确定性流水线 (0 AI)
   normalize → terminology → spacing → refine → finalize
   └─ defiller+de_de+ratio_format           └─ depunct+hotkeys
      │
      ▼
④ AI 复核：书名号标记 + 置信度评分
      │
      ▼
⑤ diff 审核 → 用户确认 → 写入输出
      │
      ▼
⑥ `{源文件名}_Enhancer.srt`
```

## 特性

- **混合 AI + 确定性脚本**：AI 负责感知（语种/领域/术语校准），脚本负责处理（零幻觉风险）
- **5 步流水线**：normalize(去口癖+的得地+比率格式) → 术语校准 → 混排空格 → **语义断句** → finalize(去标点+快捷键)
- **的得地修正增强**：R1 V+的+比较(越来越多) → 得 / R2 V+的+极端补语(要命/不行/够呛) → 得 / R3 常见副词的+动词 → 地
- **快捷键标准化**：Ctrl+E/Ctrl+C/Ctrl+V 等快捷键最后执行，避免 `+` 被去标点剥离
- **级联语义断句**：句末标点/转折连词/话题标记/话语标记/时间状语/OK 隔离/响应标记/重复检测 8 级递归切割
- **对照表优先**：用户 overrides > 静态 correction-table > 领域联网搜索 > AI 上下文猜测
- **领域自适应**：自动检测字幕领域（Maya/Python/Gaming/AI-3D/Substance/General）加载对应术语
- **置信度评分**：每项修改标注置信度，低置信度需用户确认
- **增量学习**：用户确认的修正持久化到 correction-table.md，跨会话复用
- **中西文混排规范**：CJK-Latin 自动加空格、代码保护、数字-字母再紧凑(2D/3D/4K/UV)、专名大写
- **`--skip refine`**：上游流程（如 [video-transcribe](https://github.com/zzh-editor/video-transcribe)）已做语义断句时跳过，避免重复分割

## 使用

```bash
# 基础用法
python3 scripts/enhance.py input.srt -o output_Enhancer.srt --lang zh --domain maya

# 带用户覆盖术语
python3 scripts/enhance.py input.srt -o output_Enhancer.srt \
  --lang zh --domain maya+gaming \
  --overrides '{"Owatch":"Overwatch","R Center":"Art Center"}'

# 仅运行指定步骤
python3 scripts/enhance.py input.srt --steps terminology,spacing

# 跳过指定步骤
python3 scripts/enhance.py input.srt --skip refine

# 干跑预览
python3 scripts/enhance.py input.srt --dry-run
```

### Pipeline 步骤

| 步骤 | CLI 名 | 功能 | 子步骤 |
|------|--------|------|--------|
| 1 | `normalize` | 文本规范化 | defiller(去口癖) → de_de(的得地修正) → ratio_format(16比9→16:9) |
| 2 | `terminology` | ASR 术语替换 | correction-table.md + overrides，三级模糊匹配(精确→大小写→归一化) |
| 3 | `spacing` | 混排空格 | CJK-Latin 加空格、数字-字母再紧凑、代码/公式保护 |
| 4 | `refine` | 级联语义断句 | 句末标点/转折连词/话题标记/话语标记/时间状语/OK隔离/响应标记/重复检测 |
| 5 | `finalize` | 最终清理 | depunct(去标点,保护《》/代码域) → hotkeys(Ctrl+E标准化) |

> `normalize` 和 `finalize` 是合并步骤。旧版单步名 `defiller,de_de,ratio_format,depunct,hotkeys` 仍可通过 `--steps` 使用（向后兼容）。

## 脚本

- **`scripts/enhance.py`** — 主增强流水线，支持 `--config`、`--steps`、`--skip`、`--overrides`、`--dry-run`
- **`scripts/refine_segments.py`** — 级联语义断句引擎（8 级递归切割：句末标点/转折连词/话题标记/话语标记/时间状语/OK 隔离/响应标记/重复检测）
- **`scripts/apply_spacing.py`** — CJK-Latin 混排空格工具（inline 调用，无子进程开销）
- **`scripts/domain_scanner.py`** — 关键词频次领域检测（Maya 18 关键词，覆盖多领域）
- **`scripts/title_marker.py`** — 游戏/影视作品《》书名号标记
- **`scripts/confidence_scorer.py`** — 置信度评分
- **`scripts/setup.sh`** — 依赖自动安装脚本

## 文件结构

```
srt-enhancer/
├── scripts/
│   ├── enhance.py            # 主流水线脚本（5 步）
│   ├── refine_segments.py    # 级联语义断句引擎
│   ├── apply_spacing.py      # CJK-Latin 空格（inline）
│   ├── domain_scanner.py     # 领域检测
│   ├── title_marker.py       # 书名号标记
│   ├── confidence_scorer.py  # 置信度评分
│   └── setup.sh              # 依赖自动安装脚本
├── references/
│   ├── correction-table.md   # ASR→正确术语映射
│   ├── domains.yaml          # 领域定义（关键词 + 搜索上下文）
│   ├── enhancement-rules.md  # 详细规则
│   ├── mixed-typesetting.md  # 混排规范
│   └── example.md            # 完整工作示例
├── SKILL.md                  # Agent skill 定义
└── README.md
```

## License

[MIT](LICENSE)
