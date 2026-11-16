# enhance.py CLI Usage

调用 `enhance.py` 时读取本文件。以已加载的 skill root 为工作目录运行命令，让 `scripts/` 相对解析；候选文件写入调用方或当前任务提供的 `<scratch_dir>/candidate.srt`，diff 获批前不要使用最终输出路径。正常流水线为 `normalize → terminology → spacing → capitalization → terminology → finalize`。

```bash
# Normal run: write only a temporary candidate for the diff review.
python3 scripts/enhance.py "<input_srt>" -o "<scratch_dir>/candidate.srt" \
    --lang zh --domain "<domain>" \
    --overrides '{"Owatch":"Overwatch","R Center":"Art Center"}'

# Dry-run to inspect steps without modifying:
python3 scripts/enhance.py input.srt --dry-run

# Skip specific steps:
python3 scripts/enhance.py input.srt --skip defiller,depunct

# Run only specific steps:
python3 scripts/enhance.py input.srt --steps terminology,spacing
```

**Pipeline steps executed by enhance.py (in order):**

| Step | CLI name | What it does |
|------|----------|-------------|
| 1 | `normalize` | Combined: defiller(去掉口癖+ASR结巴) → de_de(的得地修正) → ratio_format(16比9→16:9) |
| 2 | `terminology` | 第一轮术语替换：Apply ASR→correct mapping from `correction-table.md` + overrides, with fuzzy matching |
| 3 | `spacing` | CJK-Latin spacing via `scripts/apply_spacing.py` (inlined, no subprocess overhead)，仅做空格，不再含大小写 |
| 4 | `capitalization` | 专有名词大写 + 领域感知大小写归一化，从 `correction-table.md`「大小写校准」节加载，支持 AI overrides |
| 5 | `terminology` | 第二轮术语替换：spacing + capitalization 后英文规范化后，再次匹配 correction-table.md 中的复合术语 |
| 6 | `finalize` | Combined: depunct(去标点, 保留`《》`和代码保护域) → hotkeys(标准化Ctrl+E等快捷键, 最后执行避免+被剥离) |

> **关于双 terminology 轮次**：第二轮术语替换捕获 spacing + capitalization 后英文规范化产生的复合术语（如 Image2 3D → Image To 3D）。仅当 ASR 输出包含中文语境中的英文复合术语时有效。若无此类内容，第二轮是空操作，不影响性能。

> **旧版 --steps 向后兼容：** `defiller,de_de,ratio_format,depunct,hotkeys` 等单步名称仍然可用。但推荐使用合并后的步骤名称。`terminology` 在 pipeline 中出现两次（step 2 和 step 5），--steps 默认值：`normalize,terminology,spacing,capitalization,terminology,finalize`。
