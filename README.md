# SRT Enhancer · 字幕增强技能

适用于 AI 编程助手（OpenCode、Claude Code、Cursor 等）的 SRT 字幕与 TXT 逐字稿增强 skill。

自动去口癖、修正 ASR 误识别、规范中西文混排，保持原始时间轴和结构不变。

## Features

- **去口癖** — 识别并删除犹豫声（啊/嗯/呃）和无意义句末语气词，保留自然话语标记（也就是说/说白了/然后）
- **的/得/地修正** — 基于句法位置智能判定（定语→的，状语→地，补语→得），含高频固定搭配表
- **术语校准** — 游戏美术特化术语表（Rookies/Concept Art/Keyframe/Paint Over），附带 Maya 绑定与 Python 开发术语；同会话增量学习
- **联网验证** — 低置信度 ASR 误识别自动 web search 校准，缓存结果避免重复查询
- **中西文混排** — CJK-Latin 间距、Latin↔Digit 间距（Python3.9→Python 3.9）、代码/路径/公式保护、数字单位紧凑、专有名词大写
- **书名号标记** — 为已确认的游戏/影视标题自动添加《》，不误标引擎/工具/公司名
- **去多余标点** — 保护区域（代码/路径/数学公式/URL）不受影响
- **置信度打分（4 级制）** — High(≥90%) / Medium(70-89%) / Low(50-69%) / Skip(<50%)，低置信项标记 ❗
- **Diff 审核表** — 对话窗口对比预览，逐条确认后写入文件
- **自动领域检测** — 扫描内容识别 Maya/Python/Gaming 领域，加载对应术语表
- **空格清理** — 去口癖后修复多余间距，确保后续步骤输入整洁

## 安装

### 方式一：npx skills（推荐）

```bash
npx skills add zzh-editor/Srt-Enhancer
```

> `.skillignore` 已配置，`README.md` 不会被下载到技能目录中。

自动安装到当前 AI 编程助手。

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
优化字幕 / 增强字幕 / 优化这个字幕 / 增强这个字幕
optimize subtitles / enhance SRT / clean up ASR transcript
```

### 工作流

1. 上传 `.srt` 或 `.txt` 文件
2. 确认混排设置（默认开启）
3. 解析文件结构 → 自动检测领域 → 加载对应术语表
4. 逐条字幕按序执行：去口癖 → 空格清理 → 的得地 → 术语修正 → 联网校准 → 混排(apply_spacing.py) → 去标点 → 书名号 → 单行化
5. 展示 Diff 审核表，等待用户逐条确认
6. 用户确认后输出 `{源文件名}_Enhancer.srt`

### 示例

**输入：**
```srt
1
00:00:00,100 --> 00:00:05,000
嗯今天我们要来看一下Python3.9的新功能啊
```

**处理后：**
```srt
1
00:00:00,100 --> 00:00:05,000
今天我们要来看一下 Python 3.9 的新功能
```

## 目录结构

```
srt-enhancer/
├── .skillignore                     # 排除 README.md 不被 npx skills add 下载
├── SKILL.md                         # 技能定义（核心文件）
├── references/
│   ├── terminology.md               # 游戏/动画/开发术语表（含已知正确术语 §5.5）
│   ├── enhancement-rules.md         # 口癖/错字语义分析与置信度评分规则
│   ├── mixed-typesetting.md         # 中西文混排完整规范
│   └── example.md                   # 完整处理示例
└── scripts/
    └── apply_spacing.py             # CJK-Latin 间距脚本（含 Latin↔Digit 空格）
```

## 依赖

- Python 3.10+（仅 `scripts/apply_spacing.py` 需要，AI 处理由语言模型原生完成）

## License

MIT
