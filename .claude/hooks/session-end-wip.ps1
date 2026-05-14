# session-end-wip.ps1
# Fires when a Claude Code session ends. Writes a structured session-log entry
# derived from git state, auto-commits tracked memory + quality-report changes,
# and pushes to origin.
#
# Triggered by: .claude/settings.json SessionEnd hook
# Outputs:
#   - quality_reports/session_logs/_auto/YYYY-MM-DD_HHmm_session-end.md (structured entry)
#   - git commit (auto: session end YYYY-MM-DD_HHmm) if anything tracked changed
#   - git push (best-effort; failures swallowed so they don't block session close)
#
# Safe by design:
#   - Never overwrites existing session logs (timestamped filenames)
#   - Stages only auto-managed paths (MEMORY.md + quality_reports/session_logs/ + .claude/state/)
#   - Never edits CLAUDE.md, skills, agents, rules
#   - Push failures are silent — next session retries

$ErrorActionPreference = "SilentlyContinue"

$repo = $env:CLAUDE_PROJECT_DIR
if (-not $repo) { exit 0 }

Set-Location $repo

# Gather state
$statusArr     = & git status --porcelain 2>$null
$branch        = (& git rev-parse --abbrev-ref HEAD 2>$null) -join ""
$aheadArr      = & git log --oneline "origin/$branch..HEAD" 2>$null
$diffStat      = & git diff --stat HEAD 2>$null
$recentCommits = & git log --oneline -10 2>$null

$status = if ($statusArr)     { $statusArr     -join "`n" } else { "" }
$ahead  = if ($aheadArr)      { $aheadArr      -join "`n" } else { "" }
$diff   = if ($diffStat)      { $diffStat      -join "`n" } else { "" }
$recent = if ($recentCommits) { $recentCommits -join "`n" } else { "" }

$ts      = Get-Date -Format "yyyy-MM-dd_HHmm"
$autoDir = Join-Path $repo "quality_reports\session_logs\_auto"
if (-not (Test-Path $autoDir)) { New-Item -ItemType Directory -Path $autoDir -Force | Out-Null }

# Write structured log only if there's actually session activity to log
$hasSessionActivity = -not ([string]::IsNullOrWhiteSpace($status) -and [string]::IsNullOrWhiteSpace($ahead))

if ($hasSessionActivity) {
    $outFile = Join-Path $autoDir "${ts}_session-end.md"
    $body = @"
# Auto session-end checkpoint — $ts

**Branch:** $branch

## Uncommitted at session end
``````
$status
``````

## Diff stat (uncommitted)
``````
$diff
``````

## Commits ahead of origin/$branch (will be pushed)
``````
$ahead
``````

## Recent commits (last 10)
``````
$recent
``````
"@
    Set-Content -Path $outFile -Value $body -Encoding utf8
}

# Auto-commit auto-managed paths if any are dirty
if (-not [string]::IsNullOrWhiteSpace($status)) {
    & git add MEMORY.md quality_reports/session_logs/ .claude/state/ 2>$null
    & git diff --cached --quiet
    if ($LASTEXITCODE -ne 0) {
        & git commit -m "auto: session end $ts" 2>$null
    }
}

# Push if anything is ahead (best-effort)
$aheadAfterCommit = & git log --oneline "origin/$branch..HEAD" 2>$null
if ($aheadAfterCommit) {
    & git push 2>$null
}

exit 0
