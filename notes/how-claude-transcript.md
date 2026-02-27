# How to Save Claude Code Transcripts

_Exported from Claude Code session — 2026-02-21_

---

## Q: What's the best way to save Claude Code transcripts?

### Automatic Storage

Claude Code **automatically saves all sessions** locally in `~/.claude/`. Sessions are retained for 30 days by default.

### Export a Conversation

The simplest way to explicitly save a transcript:

```
/export                   # Copy to clipboard
/export transcript.md     # Save to a file
```

### Resume Past Sessions

```bash
claude --continue          # Resume most recent session
claude --resume            # Interactive session picker
claude --resume my-session # Resume by name
```

### Name Your Sessions

Use `/rename` during a session to make it easy to find later:

```
/rename auth-refactor
```

### Headless/Programmatic Export

For scripting, control the output format:

```bash
claude -p "query" --output-format json > transcript.json
claude -p "query" --output-format stream-json > stream.jsonl
claude -p "query" --output-format text > output.txt
```

### Best Practices

1. **Name sessions** with `/rename` so they're searchable later
2. **Export important conversations** to markdown files you can version-control
3. **Use CLAUDE.md** for knowledge that should persist across all sessions (architectural decisions, conventions, etc.)
4. **Use `--output-format json`** if you want full metadata (tool calls, timestamps, etc.)
5. **Export before long sessions compact** — when context fills up, older details get summarized

The `/export` command to a `.md` file is the most practical approach for archiving important conversations.

---

### Session Commands Reference

| Need | Solution | Command |
|------|----------|---------|
| Resume previous work | Session picker | `/resume` or `claude --resume` |
| Find specific session | Search/filter | `/resume` then type to search |
| Export conversation | Export command | `/export filename.md` |
| Name session | Rename command | `/rename descriptive-name` |
| Preserve across sessions | Documentation | Update CLAUDE.md |
| Preview session before resuming | Session picker preview | `/resume` then press `P` |
| Continue most recent | Quick resume | `claude --continue` |
| Archive for records | Manual export | `/export > transcripts/` |
| Disable auto-save (one-off) | Print mode flag | `claude -p --no-session-persistence` |

### Storage Details

- **Location**: `~/.claude/` (override with `CLAUDE_CONFIG_DIR`)
- **Retention**: 30 days for inactive sessions (`cleanupPeriodDays` setting)
- **Scope**: Sessions are stored per project directory
- **Backup**: Local only — export important conversations for off-machine backup
