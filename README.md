# SRT Enhancer

字幕优化 Agent Skill — 去口癖、ASR 纠错、的/得/地修正、中西文混排空格、标点清理、专名大小写规范化。

## 触发词

在支持 Agent Skills 的 CLI（OpenCode、Claude Code、Cursor 等）中，说以下任意一句 + 字幕文件路径即可自动调用：

```
优化字幕 / 增强字幕
优化这个字幕 / 增强这个字幕
optimize subtitles / enhance SRT
clean up ASR transcript / filler removal
```

输入后 Agent 会自动：检测字幕领域 → 加载对应术语表 → 执行 6 步流水线 → 生成 diff 审核表 → 用户确认后输出。

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

## 使用方式

所有字幕优化只用一句话描述需求 + 字幕文件，Agent 自动处理后续。

### 基础优化

```
用户：优化这个字幕 meeting.srt
Agent：检测到字幕文件 → 领域检测 → 执行 6 步流水线
       生成 diff 审核表
       🔴 CHECKPOINT: 确认修改
       用户确认 → 写入 meeting_Enhancer.srt
```

```
用户：增强字幕 lecture.srt
Agent：检测到字幕文件 → 通用领域 → 流水线处理
       生成 diff 审核表 → 用户确认 → 写入 lecture_Enhancer.srt
```

### 混排空格控制

```
用户：优化字幕 tutorial.srt 关闭空格
Agent：检测到字幕文件 → 关闭混排空格功能
       跳过 spacing 步骤 → 其余 5 步正常执行
       用户确认后写入
```

```
用户：优化字幕 tutorial.srt 开启空格
Agent：检测到字幕文件 → 开启混排空格
       完整 6 步流水线 → 用户确认后写入
```

### 指定领域

```
用户：优化字幕 code.srt --domain python
Agent：检测到字幕文件 → 设置 Python 领域
       CASE_GROUPS 按 Python 领域规范化（保持文件扩展名小写）
       输出时 PyCharm 等品牌工具保持原样
```

### 自定义覆盖术语

```
用户：优化字幕 game.srt --overrides '{"Owatch":"Overwatch","R Center":"Art Center"}'
Agent：检测到字幕文件 → 加载默认术语表
       合并用户自定义覆盖 → 流水线处理
```

### 预览模式

```
用户：优化字幕 draft.srt --dry-run
Agent：检测到字幕文件 → 执行流水线但不写入
       仅展示 diff 审核表供预览
       用户可决定是否正式执行
```

### 大小写一致性检查

```
用户：优化字幕 asset.srt --check-casing
Agent：检测到字幕文件 → 流水线处理
       额外扫描输出中英文术语大小写不一致
       给出规范化建议表
```

## 工作流程

```
用户说"优化字幕"
      │
      ▼
Agent 收到并加载 skill
      │
      ▼ 🔴 CHECKPOINT
确认混排规范开关（默认开启 / 关闭空格 / 自定义）
      │
      ▼
解析文件 → 领域检测 (domain_scanner.py) → AI 构建 config + 联网校准术语
      │
      ▼
enhance.py 零 AI 流水线（双轮 terminology）
 normalize → terminology → spacing → terminology → refine → finalize
      │
      ▼ 🔴 CHECKPOINT
AI 复核 + 置信度评分 → diff 审核表 → 用户确认 → 写入输出
```

## 处理能力

| 功能 | 说明 |
|------|------|
| 去口癖 | 啊/哦/嗯/呃/哎/噢/唔/欸 等，保留话语标记(说白了/也就是说) |
| 的得地修正 | R1 V+的+比较(越来越多)→得 / R2 V+的+极端补语(要命)→得 / R3 副词的+V→地 |
| ASR 术语校准 | correction-table.md + 用户 overrides，三级模糊匹配（精确→大小写折叠→归一化） |
| 领域自适应 | Maya(18关键词)/Python/Gaming/AI-3D/Substance/General，domain_scanner.py 自动检测 |
| 中西文混排 | CJK-Latin 自动空格、脚本边界间距、代码/公式保护、数字单位紧凑、专名大小写 |
| 专名保护 | PROTECTION_PATTERNS 保护 Hyper3D/ComfyUI/TapNow 等 18+ 复合词不拆分 |
| 复合词重新粘合 | FIXUP_COMPOUNDS 将误拆分的专名重新合并（Hyp er3D → Hyper3D） |
| 领域感知大小写 | CASE_GROUPS 按文件格式(lowercase)/通用缩写(UPPER)/品牌工具(原样)/AI 工具(原样)自动规范化 |
| 语义断句 | 预清洗(去空/零时长/重复) → 8 级切割 + 教学口语标记 + 动态最小字数防过度碎切 |
| 双轮术语修正 | terminology 步骤执行两次（spacing 前后），复合术语二次匹配（Image2 3D → Image To 3D） |
| 快捷键 | Ctrl+E/Ctrl+C/Ctrl+V 标准化，最后执行避免 + 被剥离 |
| 置信度评分 | 每项修改标注置信度，低置信度需用户确认 |
| 增量学习 | 用户确认的修正持久化到 correction-table.md |
| 大小写不一致检测 | `--check-casing` 扫描输出文件中的英文术语大小写不一致并给出规范化建议 |

## Pipeline 步骤详情

| 步骤 | CLI 名 | 功能 | 子步骤 |
|------|--------|------|--------|
| 1 | `normalize` | 文本规范化 | defiller(去口癖) → de_de(的得地修正) → ratio_format(16比9→16:9) |
| 2 | `terminology`（第一轮） | ASR 术语替换 | CASE_GROUPS 分层大小写 + correction-table.md + overrides 三级匹配 |
| 3 | `spacing` | 混排空格 + 保护 | PROTECTION_PATTERNS 保护专名 → CJK-Latin 空格 → 代码/公式保护 → 数字单位 → FIXUP_COMPOUNDS 粘合 |
| 4 | `terminology`（第二轮） | 复合术语二次匹配 | spacing 后重新匹配修正（Image2 3D → Image To 3D） |
| 5 | `refine` | 语义断句 | `_clean_segments` 去空/零时长/重复 → 8 级切割 + 教学口语标记 + 动态最小字数 |
| 6 | `finalize` | 最终清理 | depunct(去标点,保护《》/代码域) → hotkeys(Ctrl+E标准化) |

> 默认 pipeline 包含双轮 `terminology`。旧版单步名 `defiller,de_de,ratio_format,depunct,hotkeys` 仍可通过 `--steps` 使用。

## 专名保护系统

SRT Enhancer 包含三层专名保护机制：

| 层级 | 名称 | 作用 | 示例 |
|------|------|------|------|
| 1 | PROTECTION_PATTERNS | 保护专名不被间距规则拆散 | `Hyper3D Rodin`, `ComfyUI`, `Gen2.5`, `Python3.9` |
| 2 | FIXUP_COMPOUNDS | 将已误拆分的词重新粘合 | `Hyp er3D` → `Hyper3D`, `Ta pNow` → `TapNow` |
| 3 | CASE_GROUPS | 按领域规范化大小写 | `hdr` → `HDR` (acronym), `obj` → `obj` (file ext) |

`CASE_GROUPS` 优先级：`generic_acronym > file_format > brand_tool > ai_3d > os_term`。

## 角色大小写领域分组

使用 `--domain` 参数控制大小写规范化：

| 领域 | 文件格式 | 通用缩写 | 品牌工具 | AI/3D 工具 | 系统术语 |
|------|---------|---------|---------|-----------|---------|
| `general` (默认) | obj,fbx,gltf | HDR,PBR | ZBrush,Blender | - | macOS |
| `ai-3d` | obj,fbx,gltf | HDR,PBR | ZBrush | Rodin,Gen | macOS |
| `python` | obj,fbx,gltf | HDR,PBR | PyCharm | - | macOS |

## 脚本

| 脚本 | 用途 |
|------|------|
| `scripts/enhance.py` | 主流水线，支持 `--config`、`--steps`、`--skip`、`--overrides`、`--dry-run`、`--domain`、`--check-casing` |
| `scripts/apply_spacing.py` | CJK-Latin 混排空格 + 专名保护 + 复合词粘合 + 领域感知大小写 |
| `scripts/refine_segments.py` | 级联语义断句引擎 |
| `scripts/domain_scanner.py` | 关键词频次领域检测 |
| `scripts/title_marker.py` | 游戏/影视作品《》书名号标记 |
| `scripts/confidence_scorer.py` | 置信度评分 |
| `scripts/casing_verify.py` | 专名大小写联网核实（heuristic + Wikipedia API），输出 table/JSON/map |
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
