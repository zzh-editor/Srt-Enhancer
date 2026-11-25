# Caller Mode

`video-transcribe` 调用时传入完整的调用块：

```yaml
caller_mode: video-transcribe
input_srt: <绝对路径>
output_srt: <绝对路径，与 input_srt 不同>
scratch_dir: <调用方任务临时目录的绝对路径>
enhancer_preferences:
  mixed_typesetting: enabled | disabled   # custom 与 custom_spacing_rule 尚未实现，填了会被忽略
  terminology_annotation: true | false
  domain_policy: auto | override
  domain_override: <仅 override 时填写>
```

调用规则：

- 先逐项核对，缺任一项就返回 `INVALID_CALL` 和缺失字段名，**不要套用默认偏好继续跑**（用户的问卷选择会因此丢失）：
  1. `input_srt` 存在且能解析；
  2. `output_srt` 与 `input_srt` 不同，父目录存在；
  3. `scratch_dir` 存在且可写；
  4. `enhancer_preferences` 四个字段齐全——`mixed_typesetting`、`terminology_annotation`、`domain_policy`，`domain_policy: override` 时还要 `domain_override`。
- 不要让用户重答问卷。
- 只读 `input_srt`，不覆盖它。偏好已由调用方收集，不再弹同一类问题。
- `domain_policy=auto` 时运行领域检测；仅在结果仍不可靠或有冲突时向用户确认。`override` 时以 `domain_override` 为准。
- 在 `scratch_dir` 用唯一临时路径生成候选 SRT，在对话中审核其文本 diff。审核前保持 `output_srt` 不存在；用户批准后才将候选写到 `output_srt`，随后清理候选文件。
- 全部修改获批或逐条审核后返回 `APPROVED`；没有修改时原样复制输入到 `output_srt` 并返回 `NO_CHANGES`；用户拒绝所有修改返回 `REJECTED`；参数不全返回 `INVALID_CALL`；处理或写入失败返回 `FAILED`。`REJECTED`、`INVALID_CALL`、`FAILED` 时清理候选并保持 `output_srt` 不存在。
- 变更摘要写在对话里，不要附加到 SRT 文本末尾。

在回复末尾输出状态块。`CALLER_STATUS` 只能填写一个实际状态：

```text
CALLER_STATUS: APPROVED | NO_CHANGES | REJECTED | INVALID_CALL | FAILED
OUTPUT_SRT: <绝对路径，或 NONE>
DETAIL: <简短原因或修改摘要>
```
