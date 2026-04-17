---
name: resume
description: "Resume work on a specific project. Reads project STATUS, recent git history, and latest plan. One command replaces HANDOVER.md."
---

# /resume

**Usage:** `/resume seminar_paper` or `/resume msc_thesis`

## Workflow

### Step 1: Read project status
```
Read projects/<project>/STATUS.md
```
This contains: current state, decisions made, outstanding tasks, and the NEXT action.

### Step 2: Read recent git history
```bash
git log -5 --oneline --all
```
Shows what was done in the last few sessions.

### Step 3: Read latest plan (if any)
```bash
# Find most recent plan file
ls -t quality_reports/plans/ | head -1
```
Read the first 30 lines of the most recent plan for session context.

### Step 4: Present briefing
Produce a 10-line session briefing:

```markdown
## Session Briefing: <project>

**Status:** <one-line from STATUS.md>
**NEXT:** <the NEXT action from STATUS.md>
**Last 3 commits:**
- <commit 1>
- <commit 2>
- <commit 3>
**Latest plan:** <plan filename and its one-line summary>
**Ready to work.** What would you like to do?
```

## What this replaces
- HANDOVER.md (deleted — always drifted)
- Manual session-start reading protocol
- The old "read CLAUDE.md + HANDOVER.md + MEMORY.md" startup burn

## What it does NOT do
- Does not auto-load MEMORY.md (loaded by CLAUDE.md already)
- Does not auto-load theory modules or lit notes (on-demand only)
- Does not read the full pipeline or draft (too large for startup)
