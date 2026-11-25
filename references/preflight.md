# Standalone 偏好问卷

独立调用 `srt-enhancer` 时，在解析 SRT、运行领域扫描或安装依赖前，通过当前 Agent 的交互问答能力连续收集用户尚未明确提供的设置。用户请求里已经写明的选项直接复用。

1. 中西文混排：保持默认开启 / 关闭中西文空格 / 自定义规则。
2. 领域策略：自动检测（推荐）/ 指定领域。
3. 术语括注：开启 / 关闭。

选择“自定义规则”或“指定领域”时，立即补问规则文本或领域名。回答统一记录为：

```yaml
enhancer_preferences:
  mixed_typesetting: enabled | disabled   # custom 与 custom_spacing_rule 尚未实现，填了会被忽略
  terminology_annotation: true | false
  domain_policy: auto | override
  domain_override: <仅 override 时填写>
```

所有答案收齐后再解析字幕。`domain_policy=auto` 时运行自动检测和现有纠偏规则，正常结果无需再次确认；只有结果仍不确定或有冲突时再问领域。`terminology_annotation` 只控制 §7 的括注，不影响其他增强步骤。

独立调用时，用一个唯一的任务临时目录保存候选 SRT 和 diff；不要覆盖输入或同名现有输出。用户确认后才写 `{原始文件名}_Enhancer.srt`，并清理本次生成的候选与 diff 文件。
