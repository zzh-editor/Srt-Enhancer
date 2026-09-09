# SRT Enhancer

字幕优化工具 — 去口癖、ASR 纠错、的/得/地修正、中西文混排空格、标点清理、专名大小写规范化，可选英文术语中文括注与书名号标记。

支持 11 领域自动检测（Maya/Python/Gaming/AI-3D 等），6 步确定性流水线 + AI 审核，生成 diff 对比表供确认后输出。

在支持 Agent Skills 的 CLI 中，说「优化字幕」+ 文件路径即可自动调用。

## 快速开始

```bash
npx skills@latest install https://github.com/zzh-editor/Srt-Enhancer
```

基础优化：

```
用户：优化这个字幕 meeting.srt
Agent：检测领域 → 构建配置 → 执行 6 步流水线 → 生成 diff 审核表
       用户确认 → 写入 meeting_Enhancer.srt
```

## 使用方式

基础优化：

```
用户：优化这个字幕 meeting.srt
用户：增强字幕 lecture.srt
```

指定领域：

```
用户：优化字幕 code.srt --domain python
```

混排空格控制：

```
用户：优化字幕 tutorial.srt 关闭空格
用户：优化字幕 tutorial.srt 开启空格
```

英文术语中文括注（教学演示用，非默认）：

```
用户：优化字幕 tutorial.srt 术语加注释
用户：加强字幕 tutorial.srt 加中文翻译标注
```

> 触发后，中文字幕里的英文专业术语后紧跟 `(中文)` 括注，如 `joint chain(关节链)`、`position based simulation(基于位置的模拟)`。跳过单字母变量、缩写、代码/公式/路径保护域，翻译优先取术语表并进 diff 审核。

预览模式（不写入文件）：

```
用户：优化字幕 draft.srt --dry-run
```

大小写一致性检查：

```
用户：优化字幕 asset.srt --check-casing
```

## 竖屏字幕输出（9:16 Vertical）

针对竖屏视频重新断句。横屏字幕每行偏长，竖屏单屏可见区域小，需要把每行拆成短句，每行一个完整语义单元。

```
用户：这个字幕导出竖屏字幕 meeting_Enhancer.srt
用户：竖版字幕 lecture_Enhancer.srt
```

规则：每行 4-12 字（目标约 8 字），断在语义边界（动宾/主谓/连接词后），时间轴按各 chunk 字数比例在原段内重排。仅做断句和时间轴重排，不改文本。

```bash
python3 scripts/vertical.py input_Enhancer.srt --splits plan.json -o output_竖屏.srt
```

AI 先生成语义断句计划（JSON，`{"1": ["chunk1", "chunk2"], ...}`），脚本应用计划并重排时间轴；chunk 拼接回原文不一致时自动跳过该条，无计划时回退按 12 字标点感知硬切。

## Pipeline 步骤

| 步骤 | 功能 |
|------|------|
| normalize | 去口癖 + ASR 结巴 + 的得地修正 + 比例格式 |
| terminology（第一轮） | ASR 术语替换，三级模糊匹配 |
| spacing | CJK-Latin 混排空格，专名保护 |
| capitalization | 专名大小写 + 领域感知大小写组 |
| terminology（第二轮） | 复合术语二次匹配 |
| finalize | 去标点 + 快捷键标准化 |

默认 pipeline 包含双轮 terminology，仅在 spacing + capitalization 后英文规范化产生复合术语时生效。

增强后的 AI 审核阶段依次做：书名号标记（title_marker.py，联网验证后的游戏/影名加《》）、未匹配术语联网校准、英文残片扫描合并，并按需做术语中文括注；每项修正按置信度（≥90 高 / 70-89 中 / 50-69 低）分档进入 diff 审核表。混排与领域确认在流程中合并为一次连续选择，不重复弹窗。

## 专名保护系统

| 层级 | 作用 | 示例 |
|------|------|------|
| PROTECTION_PATTERNS | 保护专名不被间距拆散 | `Hyper3D Rodin`, `ComfyUI` |
| FIXUP_COMPOUNDS | 误拆分专名重新粘合 | `Hyp er3D` → `Hyper3D` |
| 大小写校准表 | 80+ 专名大写 + 领域感知大小写组 | `cpu` → `CPU`, `macos` → `macOS` |

## 增量术语学习

每次增强后的确认修正会按「会话表 → correction-table.md 持久化」两级累积，下轮自动命中，无需重复联网校准。

## 文件结构

```
srt-enhancer/
├── scripts/          # 7 个可执行脚本（含 vertical.py 竖屏断句、title_marker.py 书名号）
├── references/       # 术语表、大小写校准、领域定义
├── SKILL.md          # Agent skill 定义
└── README.md
```

## License

[MIT](LICENSE)