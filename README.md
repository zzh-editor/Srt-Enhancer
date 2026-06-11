# SRT Enhancer · 字幕增强技能

适用于 AI 编程助手（如 OpenCode、Claude Code、Cursor 等）的 SRT 字幕与 TXT 逐字稿增强 skill —— 自动去口癖、修正 ASR 误识别、规范中西文混排。

## Features

- **去口癖** — 识别并删除犹豫声（啊/嗯/呃）和无意义句末语气词
- **的/得/地 修正** — 基于句法位置的智能判定（定语→的，状语→地，补语→得）
- **术语校准** — **游戏行业特化术语表**，覆盖 Rookies/Concept Art/Keyframe/Paint Over 等游戏美术术语，以及 Overwatch/Art Center 等工作室/机构名；附带 Maya 绑定与 Python 开发术语
- **联网验证** — 低置信度 ASR 误识别自动 web search 校准
- **中西文混排** — CJK-Latin 间距、代码保护、数字单位格式化
- **书名号标记** — 为确认的游戏/影视标题自动添加《》
- **去多余标点** — 保留保护区域（代码/路径/数学公式）
- **置信度打分** — 每条修改标置信度，低置信项标记 ❗ 等待用户确认
- **Diff 审核** — 对话窗口对比表，逐条确认后写入
- **增量学习** — 同会话记住用户确认过的修正，避免重复确认

## 安装

### 方式一：npx skills（推荐）

```bash
npx skills add zzh-editor/Srt-Enhancer
```

自动安装到当前 agent（OpenCode / Claude Code / Cursor 等均可）。

### 方式二：手动复制

```bash
# OpenCode 项目级
cp -r Srt-Enhancer .opencode/skills/

# OpenCode 用户级
cp -r Srt-Enhancer ~/.config/opencode/skills/

# Claude Code
cp -r Srt-Enhancer ~/.claude/skills/

# Cursor
cp -r Srt-Enhancer ~/.cursor/skills/
```

## 使用

### 触发词

```
优化字幕 / 增强字幕 / 优化这个字幕
optimize subtitles / enhance SRT / clean up ASR transcript
```

### 工作流

1. 上传 `.srt` 或 `.txt` 文件
2. 确认混排设置（默认开启）
3. 自动检测领域并加载术语表
4. 逐条字幕执行：去口癖 → 的得地 → 术语修正 → 联网校准 → 混排 → 去标点 → 书名号
5. 展示 Diff 审核表等待用户确认
6. 用户确认后输出 `{源文件名}_Enhancer.srt`

### 示例

**输入:**
```srt
1
00:00:00,100 --> 00:00:05,000
嗯今天我们要来看一下Python3.9的新功能啊
```

**处理后:**
```srt
1
00:00:00,100 --> 00:00:05,000
今天我们要来看一下 Python 3.9 的新功能
```

## 目录结构

```
srt-enhancer/
├── SKILL.md                         # 技能定义（核心文件）
├── references/
│   ├── terminology.md               # 游戏行业特化术语表（兼 Maya/Python）
│   ├── enhancement-rules.md         # 口癖/错字语义分析规则
│   ├── asr-corrections-gaming.md    # 游戏行业 ASR 校准表
│   ├── mixed-typesetting.md         # 中西文混排完整规范
│   └── example.md                   # 完整处理示例
└── scripts/
    └── apply_spacing.py             # CJK-Latin 间距脚本
```

## 依赖

- Python 3.10+（仅 `scripts/apply_spacing.py` 需要，AI 处理部分由语言模型原生完成）
- `pathlib`（Python 标准库）

## License

MIT
