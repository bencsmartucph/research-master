# Gemini Task: Prune Agent/Rules/Skills Infrastructure

## Context
You are working in the `Research_Master` repository. The `.claude/` directory contains agents, rules, and skills that have grown organically. Most are unused. Your job is to archive or delete the unused ones.

## Goal
Reduce the `.claude/` directory to only the actively used files.

---

## Step 1: Archive Agents

**Move** these files FROM `.claude/agents/` TO `.claude/agents/archive/`:
- `orchestrator.md`
- `coder-critic.md`
- `data-engineer.md`
- `domain-referee.md`
- `explorer-critic.md`
- `librarian-critic.md`
- `methods-referee.md`
- `storyteller.md`
- `storyteller-critic.md`
- `strategist.md`
- `strategist-critic.md`
- `verifier.md`
- `writer.md`

**Keep in `.claude/agents/` (do NOT move):**
- `explorer.md`
- `librarian.md`
- `coder.md`
- `writer-critic.md`

**Verify after:** `ls .claude/agents/*.md` should show exactly 4 files.

## Step 2: Delete Rules

**Delete** these files FROM `.claude/rules/`:
- `agents.md`
- `content-standards.md`
- `logging.md`
- `meta-governance.md`
- `quality.md`
- `revision.md`
- `workflow.md`

**Delete the entire directory:** `.claude/rules/archive/` (contains 29 stale files)

**Keep in `.claude/rules/` (do NOT delete):**
- `domain-profile.md`
- `journal-profiles.md`
- `figures.md`
- `tables.md`
- `working-paper-format.md`
- `heavy-reads.md` (newly created)

**Verify after:** `ls .claude/rules/*.md` should show exactly 6 files. `.claude/rules/archive/` should not exist.

## Step 3: Archive Skills

**Move** these directories FROM `.claude/skills/` TO `.claude/skills/archive/`:
- `discover/`
- `revise/`
- `strategize/`
- `submit/`
- `talk/`
- `tools/`

**Keep in `.claude/skills/` (do NOT move):**
- `analyze/`
- `review/`
- `write/`
- `read-paper/` (newly created)
- `resume/` (newly created)
- `critique/` (newly created)
- `archive/` (the archive directory itself stays)

**Verify after:** `.claude/skills/` should contain 6 active skill directories + 1 archive directory.

## Step 4: Clean up WORKFLOW_QUICK_REF.md

**Delete:** `.claude/WORKFLOW_QUICK_REF.md` (superseded by /resume skill)

## Step 5: Verification

Run these checks and report results:
```bash
# Active agents (should be 4)
ls .claude/agents/*.md | wc -l

# Active rules (should be 6)
ls .claude/rules/*.md | wc -l

# Active skills directories (should be 6, excluding archive)
ls -d .claude/skills/*/ | grep -v archive | wc -l

# Rules archive should not exist
ls .claude/rules/archive/ 2>&1
```

## Step 6: Write Build Log

Save to `.claude/PRUNING_LOG.md`:
```markdown
# Infrastructure Pruning Log

**Date:** YYYY-MM-DD
**Performed by:** Gemini

## Agents
- Archived: [list all 13 moved files]
- Kept: explorer.md, librarian.md, coder.md, writer-critic.md
- Already in archive: [list any that were already there]

## Rules
- Deleted: [list all 7 deleted files]
- Deleted archive: [count of files in deleted archive]
- Kept: domain-profile.md, journal-profiles.md, figures.md, tables.md, working-paper-format.md, heavy-reads.md

## Skills
- Archived: [list all 6 moved directories]
- Kept: analyze, review, write, read-paper, resume, critique

## Verification Results
- Active agents: X (expected: 4)
- Active rules: X (expected: 6)
- Active skills: X (expected: 6)

## Uncertainties
- [flag any files you were unsure about]
```

## Step 7: Git Commit

```bash
git add -A .claude/
git commit -m "refactor: prune .claude/ infrastructure (Phase 2)

- Archive 13 unused agents (keep explorer, librarian, coder, writer-critic)
- Delete 7 stale rules + 29-file rules/archive/
- Archive 6 unused skill directories (keep analyze, review, write + 3 new)
- Delete WORKFLOW_QUICK_REF.md (superseded by /resume)"
```

## Important Notes
- Do NOT modify the content of any kept files
- Do NOT delete files that should be archived (moved to archive/)
- The archive directories exist so we can recover files if needed later
- The `.claude/agents/archive/` already contains 16 files from a previous cleanup
