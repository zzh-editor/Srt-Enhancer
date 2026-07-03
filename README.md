# SRT Enhancer

字幕优化工具 — 去口癖、ASR 纠错、的/得/地修正、中西文混排空格、标点清理、专名大小写规范化、语义断句与碎片合并。

支持 11 领域自动检测（Maya/Python/Gaming/AI-3D 等），8 步确定性流水线 + AI 审核，生成 diff 对比表供确认后输出。

在支持 Agent Skills 的 CLI 中，说「优化字幕」+ 文件路径即可自动调用。

## 快速开始

```bash
npx skills@latest install https://github.com/zzh-editor/Srt-Enhancer
```

基础优化：

```
用户：优化这个字幕 meeting.srt
Agent：检测领域 → 构建配置 → 执行 8 步流水线 → 生成 diff 审核表
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

预览模式（不写入文件）：

```
用户：优化字幕 draft.srt --dry-run
```

大小写一致性检查：

```
用户：优化字幕 asset.srt --check-casing
```

## Pipeline 步骤

| 步骤 | 功能 |
|------|------|
| normalize | 去口癖 + ASR 结巴 + 的得地修正 + 比例格式 |
| terminology（第一轮） | ASR 术语替换，三级模糊匹配 |
| spacing | CJK-Latin 混排空格，专名保护 |
| capitalization | 专名大小写 + 领域感知大小写组 |
| terminology（第二轮） | 复合术语二次匹配 |
| refine | 语义断句，8 级级联切割，禁止「的」作切点 |
| merge | 碎片合并：重叠字/极短段/句末助词粘连 |
| finalize | 去标点 + 快捷键标准化 |

默认 pipeline 包含双轮 terminology，仅在 spacing + capitalization 后英文规范化产生复合术语时生效。

## 专名保护系统

| 层级 | 作用 | 示例 |
|------|------|------|
| PROTECTION_PATTERNS | 保护专名不被间距拆散 | `Hyper3D Rodin`, `ComfyUI` |
| FIXUP_COMPOUNDS | 误拆分专名重新粘合 | `Hyp er3D` → `Hyper3D` |
| 大小写校准表 | 80+ 专名大写 + 领域感知大小写组 | `cpu` → `CPU`, `macos` → `macOS` |

## 文件结构

```
srt-enhancer/
├── scripts/          # 8 个可执行脚本
├── references/       # 术语表、大小写校准、领域定义
├── SKILL.md          # Agent skill 定义
└── README.md
```

## License

[MIT](LICENSE)
