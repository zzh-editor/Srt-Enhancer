# 术语表按需查询

增强时不要把整份 `correction-table.md` 读入模型上下文。`scripts/enhance.py` 已经在本地读取术语表并负责实际替换；AI 只需查当前字幕里发现的候选词。

1. AI 从字幕中挑出需要核实的术语候选。以下脚本路径相对已加载的 srt-enhancer skill root；执行前以该目录为工作目录。
2. 将候选词序列化为 JSON 数组，再做 Base64 编码（可避免 Windows shell 丢掉 JSON 引号），调用：

   Windows PowerShell：
   ```powershell
   $termsJson = ConvertTo-Json -Compress @('Owatch', 'R Center', 'Rodin')
   $termsB64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($termsJson))
   & '<PYTHON_EXECUTABLE>' '<SKILL_DIR>\scripts\enhance.py' --lookup-terms-base64 $termsB64
   ```

   Bash：
   ```bash
   terms_b64=$(printf '%s' '["Owatch","R Center","Rodin"]' | base64 | tr -d '\r\n')
   python3 scripts/enhance.py --lookup-terms-base64 "$terms_b64"
   ```

3. 只对结果中 `status=unmatched` 的项联网校准；`asr_match` 和 `known_correct` 不搜索。若结果含 `contextual_matches`，先按字幕语境消解歧义，不把其中候选自动写入确定性覆盖。
4. 将联网确认的修正放入 `terminology_overrides`，再照常运行 `enhance.py` 完整流水线。脚本在正式处理时仍会加载原有完整术语表，匹配顺序和输出规则不变。

查表模式只打印所给候选的结果，不读写 SRT，也不输出整张术语表。结果按输入顺序返回：

```json
[
  {"term": "Owatch", "status": "asr_match", "matches": [{"asr": "Owatch", "correct": "Overwatch"}], "resolved": "Overwatch"},
  {"term": "Rodin", "status": "unmatched", "matches": [], "resolved": "Rodin"}
]
```

`contextual_matches` 只在候选命中“仅上下文判断”行时出现；它记录可选写法和备注，不进入普通替换表。
