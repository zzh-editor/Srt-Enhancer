# Incremental Terminology Learning

Maintain an in-memory session terminology table. When a user confirms a correction in the diff review, append it to `references/correction-table.md` for reuse across sessions. Do not load the full table into model context; use `term-lookup.md` for candidate checks.

## How It Works

1. User-requested overrides take precedence over static terms.
2. The enhancement script loads `correction-table.md` locally for deterministic matching.
3. AI uses the lookup command for the terms it identified; only unmatched terms go to web calibration.
4. Persist only user-confirmed corrections; never add rejected guesses.

## Session Table

```text
session_terminology = {
  "Owatch": "Overwatch",
  "R Center": "Art Center"
}
```

## User Commands

| User says | Action |
|-----------|--------|
| `记住：XXX 的正确写法是 YYY` | Add a session override; persist after user confirmation |
| `XXX 不应该被改成 YYY` | Mark the candidate as rejected; do not re-suggest it this session |
| `删除术语：XXX` | Locate the persisted row, show it to the user, and remove it only after confirmation |
| `清除本次学习的术语` | Reset the session table |
| `显示本次学习的术语` | Print the session table contents |

Persisted records are not deleted by session reset.
