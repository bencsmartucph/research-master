---
name: resume
description: "Resume work on a specific project. Reads project STATUS, recent git history, and latest plan. One command replaces HANDOVER.md."
---

# /resume

**Usage:** `/resume seminar_paper` or `/resume msc_thesis`

## Workflow

### Step 0: Validate argument
```bash
test -d "projects/$PROJECT" || { echo "Unknown project. Available:"; ls -1 projects/; exit 1; }
test -f "projects/$PROJECT/STATUS.md" || { echo "projects/$PROJECT exists but has no STATUS.md"; exit 1; }
```

### Step 1: Read project status
`Read projects/<project>/STATUS.md` in full — it's small by design (~50 lines cap).

### Step 2: Read recent git history
```bash
git log -5 --oneline          # current branch only; --all pulls noise
```

### Step 3: Read latest plan (if any)
```bash
LATEST=$(ls -t quality_reports/plans/*.md 2>/dev/null | head -1)
[ -z "$LATEST" ] && echo "(no plans on disk yet)" || head -40 "$LATEST"
```
Read ~40 lines to catch Status + Approach + NEXT (plans have metadata at top, but the NEXT line can be deeper).

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
