# SRT Enhancer

字幕增强工具（SRT/TXT），提供去口癖、ASR 纠错、的/得/地修正、中西文混排空格、标点清理等流水线处理。

## 安装

```bash
# 使用 npx 安装（推荐）
npx skills@latest install https://github.com/zzh-editor/Srt-Enhancer

# 或直接克隆
git clone https://github.com/zzh-editor/Srt-Enhancer.git
cd Srt-Enhancer
```

> 需要 Python 3.8+。

## Pipeline

```
输入 SRT/TXT
      │
      ▼
① 领域检测 (domain_scanner.py)
      │   Maya / Python / Gaming / AI-3D / Substance / General
      │
      ▼
② AI 配置：语言检测 + 术语校准 + 对照表构建
      │   用户 overrides > correction-table.md > 领域联网搜索 > AI 猜测
      │
      ▼
③ enhance.py 确定性流水线 (0 AI)
   defiller → de_de → ratio_format → terminology → spacing → depunct → singleline
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
- **7 步流水线**：去口癖 → 的/得/地 → 比率格式 → 术语校准 → 混排空格 → 去标点 → 单行化
- **对照表优先**：用户 overrides > 静态 correction-table > 领域联网搜索 > AI 上下文猜测
- **领域自适应**：自动检测字幕领域（Maya/Python/Gaming/AI-3D/Substance/General）加载对应术语
- **置信度评分**：每项修改标注置信度，低置信度需用户确认
- **增量学习**：用户确认的修正持久化到 correction-table.md，跨会话复用
- **中西文混排规范**：CJK-Latin 自动加空格、代码保护、数字单位紧凑、专名大写

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
python3 scripts/enhance.py input.srt --skip defiller,depunct

# 干跑预览
python3 scripts/enhance.py input.srt --dry-run
```

### Pipeline 步骤

| 步骤 | CLI 名 | 功能 |
|------|--------|------|
| 1 | `defiller` | 去口癖（啊/哦/嗯/呃），保留话语标记 |
| 2 | `de_de` | 的/得/地修正 |
| 3 | `ratio_format` | `16比9` → `16:9`，`4比3` → `4:3` |
| 4 | `terminology` | ASR→正确术语映射 + 模糊匹配 |
| 5 | `spacing` | CJK-Latin 混排空格 |
| 6 | `depunct` | 去标点，保护 `《》` 和代码区域 |
| 7 | `singleline` | 多行合并，语义边界拆分 |

## 脚本

- **`scripts/enhance.py`** — 主增强流水线，支持 `--config`、`--steps`、`--skip`、`--overrides`、`--dry-run`
- **`scripts/apply_spacing.py`** — CJK-Latin 混排空格工具
- **`scripts/domain_scanner.py`** — 关键词频次领域检测
- **`scripts/title_marker.py`** — 游戏/影视作品《》书名号标记
- **`scripts/confidence_scorer.py`** — 置信度评分

## 文件结构

```
srt-enhancer/
├── scripts/
│   ├── enhance.py            # 主流水线脚本
│   ├── apply_spacing.py      # CJK-Latin 空格
│   ├── domain_scanner.py     # 领域检测
│   ├── title_marker.py       # 书名号标记
│   └── confidence_scorer.py  # 置信度评分
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

MIT
