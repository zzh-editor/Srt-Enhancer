# SRT Enhancer

字幕优化 Agent Skill — 去口癖、ASR 纠错、的/得/地修正、中西文混排空格、标点清理、专名大小写规范化、语义断句、碎片合并。

## 触发词

在支持 Agent Skills 的 CLI（OpenCode、Claude Code、Cursor 等）中，说以下任意一句 + 字幕文件路径即可自动调用：

```
优化字幕 / 增强字幕
优化这个字幕 / 增强这个字幕
optimize subtitles / enhance SRT
clean up ASR transcript / filler removal
```

输入后 Agent 会自动：检测字幕领域 → 加载对应术语表 → 执行 8 步流水线 → 生成 diff 审核表 → 用户确认后输出。

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
                    AI Phase (2-3 rounds)
 输入 SRT → 解析 → domain_scanner.py → 构建 JSON config
 (含系统性作品名扫描 → title_candidates)
                     (对照表 > 静态表 > 联网搜索)
                          │
                          ▼ 🔴 CHECKPOINT
                用户确认 Config 后继续
                          │
                          ▼
                 enhance.py (0 AI, fully deterministic)
      normalize → terminology → spacing → capitalization → terminology → refine → merge → finalize
      └ defiller+de_de+ratio_format             └ depunct+hotkeys
      └ ASR 结巴处理        └ 禁止「的」切点
                          └ Merge Pass
                          │
                          ▼
                Segment Quality Review (--review)
              静态复核：字数量/时长/含逗号未拆/短段警告
                          │
                          ▼
               AI Review Phase (1-2 rounds)
   title_marker.py → confidence_scorer.py → diff 审核 →
                          │
                          ▼ 🔴 CHECKPOINT
            用户确认 diff → 写入输出 → 持久化修正
                          │
                          ▼
              `{源文件名}_Enhancer.srt`
```

## 处理能力

| 功能 | 说明 |
|------|------|
| 去口癖 | 啊/哦/嗯/呃/哎/噢/唔/欸 等，保留话语标记(说白了/也就是说) |
| ASR 结巴处理 | 自动合并连续重复字（这这这这 → 这） |
| 的得地修正 | R1 V+的+比较(越来越多)→得 / R2 V+的+极端补语(要命)→得 / R3 副词的+V→地 |
| ASR 术语校准 | correction-table.md + 用户 overrides，三级模糊匹配（精确→大小写折叠→归一化） |
| 领域自适应 | 11 领域（Maya/Python/Gaming/AI-3D/Substance/Blender/Unreal/Houdini/ZBrush/Photoshop/General），domain_scanner.py 自动检测 |
| 中西文混排 | CJK-Latin 自动空格、脚本边界间距、代码/公式保护、数字单位紧凑 |
| 专名保护 | PROTECTION_PATTERNS 保护 Hyper3D/ComfyUI/TapNow 等 18+ 复合词不被间距规则拆散 |
| 复合词重新粘合 | FIXUP_COMPOUNDS 将误拆分的专名重新合并（Hyp er3D → Hyper3D） |
| 专名大小写 | step_capitalization 从 correction-table.md「大小写校准」节加载 80+ 专名 + 领域感知大小写组 |
| 语义断句 | 8 级级联切割（句末标点/转折连词/话题标记/话语标记/时间状语/OK隔离），禁止「的」作切点 |
| Post-refine 合并 | merge pass 自动合并不当切分的连续段（重叠字检测/极短段/句末助词粘连） |
| 双轮术语修正 | terminology 步骤执行两次（spacing + capitalization 前后），复合术语二次匹配（Image2 3D → Image To 3D） |
| 快捷键 | Ctrl+E/Ctrl+C/Ctrl+V 标准化，最后执行避免 + 被剥离 |
| 置信度评分 | 每项修改标注置信度，低置信度需用户确认 |
| 增量学习 | 用户确认的修正持久化到 correction-table.md |

## Pipeline 步骤详情

| 步骤 | CLI 名 | 功能 | 子步骤 |
|------|--------|------|--------|
| 1 | `normalize` | 文本规范化 | defiller(去口癖+ASR结巴) → de_de(的得地) → ratio_format(16:9) |
| 2 | `terminology`（第一轮） | ASR 术语替换 | correction-table.md + overrides 三级模糊匹配 |
| 3 | `spacing` | 混排空格 | PROTECTION_PATTERNS 保护专名 → CJK-Latin 空格 → 代码/公式保护 → FIXUP_COMPOUNDS 粘合 |
| 4 | `capitalization` | 专名大小写 | correction-table.md「大小写校准」节 80+ 专名 + 领域感知大小写组 |
| 5 | `terminology`（第二轮） | 复合术语二次匹配 | spacing + capitalization 后重新匹配（Image2 3D → Image To 3D） |
| 6 | `refine` | 语义断句 | 8 级级联切割，禁止「的」作切点 |
| 7 | `merge` | 碎片合并 | 重叠字检测/极短段/句末助词粘连自动合并 |
| 8 | `finalize` | 最终清理 | depunct(去标点,保护《》/代码域) → hotkeys(Ctrl+E标准化) |

> 默认 pipeline 包含双轮 `terminology`。旧版单步名可通过 `--steps` 使用。
> `--skip refine` 可在上游已断句时跳过断句步骤。

## 直接调用脚本

```bash
# 基础
python3 scripts/enhance.py input.srt -o output_Enhancer.srt --lang zh --domain maya

# 带用户覆盖术语
python3 scripts/enhance.py input.srt -o output_Enhancer.srt \
  --lang zh --domain maya \
  --overrides '{"Owatch":"Overwatch","R Center":"Art Center"}'

# 仅特定步骤
python3 scripts/enhance.py input.srt --steps terminology,spacing

# 跳过 refine
python3 scripts/enhance.py input.srt --skip refine

# 干跑预览
python3 scripts/enhance.py input.srt --dry-run

# 质量复核
python3 scripts/enhance.py input.srt --review
```

## 专名保护系统

| 层级 | 名称 | 位置 | 作用 | 示例 |
|------|------|------|------|------|
| 1 | PROTECTION_PATTERNS | apply_spacing.py | 保护专名不被间距规则拆散 | `Hyper3D Rodin`, `ComfyUI` |
| 2 | FIXUP_COMPOUNDS | apply_spacing.py | 将已误拆分的词重新粘合 | `Hyp er3D` → `Hyper3D` |
| 3 | 大小写校准表 | correction-table.md | 80+ 专名大写 + 领域感知大小写组 | `cpu` → `CPU`, `macos` → `macOS` |

## 脚本

| 脚本 | 用途 |
|------|------|
| `scripts/enhance.py` | 主流水线，8 步零 AI 确定性处理，支持 `--steps`/`--skip`/`--overrides`/`--dry-run`/`--review` |
| `scripts/apply_spacing.py` | CJK-Latin 混排空格 + 专名保护 + 复合词粘合（仅空格，不含大小写） |
| `scripts/refine_segments.py` | 级联语义断句引擎 + post-refine merge + segment quality review |
| `scripts/domain_scanner.py` | 关键词频次领域检测（11 领域） |
| `scripts/title_marker.py` | 游戏/影视作品《》书名号标记（120+ 硬编码名） |
| `scripts/confidence_scorer.py` | 置信度评分 |
| `scripts/casing_verify.py` | 专名大小写联网核实（heuristic + Wikipedia API） |
| `scripts/setup.sh` | 依赖自动安装 |

## 文件结构

```
srt-enhancer/
├── scripts/            # 可执行脚本（8 个）
├── references/         # 术语表、大小写校准表、领域定义、规则文档
├── SKILL.md            # Agent skill 定义（含完整工作流）
└── README.md
```

## License

[MIT](LICENSE)
