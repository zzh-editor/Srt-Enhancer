# Failure Handling

Failure branches for standalone and caller-mode execution. Caller mode must return `FAILED` and leave `output_srt` absent when writing or processing fails.

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| SRT 文件解析失败（格式无效/时间戳错误/编号不连续） | 提示用户并提供行号 | 拒绝处理，要求用户提供有效 SRT 文件 |
| 领域检测无匹配 | 使用通用术语表 | 跳过术语校准，仅执行其他步骤 |
| domain override 后匹配领域仍不准确（联网校准无权威结果） | 回退到 general 领域用通用术语表 | 保留 general 领域，跳过该词条校准，在 diff 中标记 ❗ |
| domain_scanner.py 执行失败（缺依赖/报错） | 回退到 AI 关键词扫描 | 跳过领域检测，用 general |
| 比率格式正则误匹配（如误改"对比"） | 误匹配回退到原文 | 标记 `#ratio_overmatch` |
| 口癖去除后字幕变空 | 保留最小有意义的词组 | 保留原始文本并标记 `#unmodified` |
| 的/得/地修正后语法不通 | 回退到原始版本，标记 `#uncertain` | 保留原始，在 diff 中标记 ❗ |
| 术语表查找无匹配 | 回退到 AI 上下文猜测 | 标记为低置信度（50-69%）提交用户确认 |
| 联网 web search 失败（超时/无结果） | 跳过联网校准，使用本地术语表 | 标记该词为低置信度（50-69%），在 diff 中提示用户自行确认 |
| spacing 脚本执行失败（`python3`/`python` 均不可用或报错） | 回退到纯 AI 混排处理 | 跳过混排步骤，记录警告 |
| 标点去除后字幕变空 | 保留原始文本的骨干部分 | 保留原始并标记 `#punctuation_removed_failed` |
| 游戏书名号标记过泛（误标工具名） | 撤销该条标记 | 保留不做书名号标记 |
| 单行合并后超过 40 字无法拆分（无语义断点） | 在空格/标点处硬拆分 | 保持现状，标记 `#overflow` |
| 用户拒绝所有修改 | 不输出增强文件，删除临时 diff 文件（如存在），仅告知用户「未应用任何修改」 | Caller mode 返回 `REJECTED` |
| 输出文件写入失败（权限/路径问题） | 提示用户并提供输出路径 | Caller mode 返回 `FAILED` 且不在对话里替代输出文件；standalone 可回退到对话窗口 |
| 增量术语表冲突（session 表与静态表不一致） | session 表优先 | 在 diff 中展示两条记录供用户选择 |
| enhance.py 执行失败（脚本报错/超时） | 回退到 AI 逐步骤处理（15-20 轮） | 记录错误日志，通知用户降级模式 |
| enhance.py 输出文件无法写入 | 检查目录权限 | Caller mode 返回 `FAILED`；standalone 回退到对话窗口输出内容 |
| audit.py 出现 ERROR | 查看被标记的词条或点链并回退该修改 | 不写最终输出；保留原 SRT 并说明审计位置 |
| audit.py 只有 WARN | 将命中行放进 diff 交给用户复核 | 不把单独 WARN 当作脚本失败 |
| vertical.py 计划缺失或无效 | 询问是否按标点和 `--max-chars 12` 自动切分 | 用户未确认时保留源字幕，不生成竖屏文件 |
| vertical.py 文本回拼校验失败 | 重做对应条目的语义计划 | 保留原条目；无法修复时不输出不完整竖屏字幕 |
