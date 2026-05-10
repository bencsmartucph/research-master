# session-end-wip.ps1
# Fires when a Claude Code session ends. Captures a lightweight WIP log
# of any uncommitted changes — no git mutations. Next session's /resume
# (or you, manually) can read this to recover where things left off.
#
# Triggered by: .claude/settings.json SessionEnd hook
# Output: quality_reports/session_logs/_auto/YYYY-MM-DD_HHmm_session-end.md
#
# Safe by design:
#  - Never runs git add / commit / stash / push
#  - Never edits CLAUDE.md, MEMORY.md, skills, agents, rules
#  - Writes to a single file in _auto/ which /recall can index but doesn't pollute the main log

$ErrorActionPreference = "SilentlyContinue"

$repo = $env:CLAUDE_PROJECT_DIR
if (-not $repo) { exit 0 }

Set-Location $repo

# Gather state (join arrays with newlines so they format cleanly in markdown)
$statusArr = & git status --porcelain 2>$null
$branch    = (& git rev-parse --abbrev-ref HEAD 2>$null) -join ""
$aheadArr  = & git log --oneline origin/$branch..HEAD 2>$null

$status = if ($statusArr) { $statusArr -join "`n" } else { "" }
$ahead  = if ($aheadArr)  { $aheadArr  -join "`n" } else { "" }

# If clean and nothing ahead, nothing worth logging
if ([string]::IsNullOrWhiteSpace($status) -and [string]::IsNullOrWhiteSpace($ahead)) {
    exit 0
}

# Build log
$ts      = Get-Date -Format "yyyy-MM-dd_HHmm"
$dateOnly = Get-Date -Format "yyyy-MM-dd"
$autoDir = Join-Path $repo "quality_reports\session_logs\_auto"
if (-not (Test-Path $autoDir)) { New-Item -ItemType Directory -Path $autoDir -Force | Out-Null }

$outFile = Join-Path $autoDir "${ts}_session-end.md"

$body = @"
# Auto session-end checkpoint — $ts

> Written automatically by .claude/hooks/session-end-wip.ps1 when the session ended.
> No git actions were taken. Run /done if you want to formally capture; run /resume to pick up.

**Branch:** $branch

## Uncommitted at session end
``````
$status
``````

## Commits ahead of origin/$branch
``````
$ahead
``````
"@

Set-Content -Path $outFile -Value $body -Encoding utf8

exit 0
