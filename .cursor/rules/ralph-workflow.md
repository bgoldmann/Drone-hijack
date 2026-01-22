# Ralph Workflow Guide

Comprehensive guide for understanding and using the Ralph autonomous agent loop system in Cursor IDE. This document explains how `ralph.sh` works and how to effectively use Ralph for iterative feature development.

## Overview

Ralph is an autonomous AI agent loop that uses Cursor IDE Composer repeatedly until all PRD items are complete. Each iteration uses Cursor Composer with clean context guided by `.cursorrules`. Memory persists via git history, `progress.txt`, and `prd.json`.

## Core Components

### Required Files

- **`prd.json`** - Product Requirements Document with user stories and completion status
- **`ralph.sh`** - Bash script that orchestrates the iteration loop
- **`.cursorrules`** - Instructions for Cursor AI when working on stories
- **`.cursor/composer-prompt-template.md`** - Template for generating story prompts
- **`progress.txt`** - Append-only log of learnings and patterns (auto-created)

### Generated Files

- **`.cursor/composer-prompt.md`** - Generated prompt for current story (updated each iteration)
- **`.last-branch`** - Tracks last branch for archive detection
- **`archive/`** - Archived runs when branch changes (optional)

## How `ralph.sh` Works

### Initialization Phase

1. **Check for PRD**: Verifies `prd.json` exists in the script directory
2. **Check template**: Ensures `.cursor/composer-prompt-template.md` exists
3. **Initialize progress**: Creates `progress.txt` if it doesn't exist
4. **Archive detection**: Compares current branch with last branch:
   - If branch changed, archives previous run to `archive/YYYY-MM-DD-feature-name/`
   - Resets `progress.txt` for new feature
5. **Track branch**: Saves current branch to `.last-branch`

### Main Loop

For each iteration (up to `max_iterations`, default 10):

1. **Check completion**: If all stories have `passes: true`, exit successfully
2. **Get next story**: Selects highest priority story where `passes: false`
3. **Generate prompt**: Creates `.cursor/composer-prompt.md` from template with story details
4. **Display instructions**: Shows how to use Cursor Composer
5. **Wait for user**: Pauses for user to complete implementation
6. **Check completion again**: Exits if all stories complete after user's work

### Story Selection Logic

```bash
# Pseudocode of get_next_story function
- Filter: userStories where passes == false
- Sort by: priority (ascending, lower number = higher priority)
- Select: First story in sorted list
```

### Prompt Generation

The `generate_composer_prompt` function:
- Extracts story details from `prd.json`
- Reads `.cursor/composer-prompt-template.md`
- Replaces placeholders:
  - `[STORY_ID]` → Story identifier (e.g., "US-001")
  - `[STORY_TITLE]` → Story title
  - `[STORY_PRIORITY]` → Priority number
  - `[STORY_DESCRIPTION]` → Full description
  - `[ACCEPTANCE_CRITERIA_LIST]` → Bulleted list of criteria
  - `[PROJECT_NAME]` → From PRD project field
  - `[BRANCH_NAME]` → From PRD branchName field
  - `[FEATURE_DESCRIPTION]` → From PRD description field
- Writes result to `.cursor/composer-prompt.md`

## Using Ralph

### Starting Ralph

```bash
# From project root (where ralph.sh and prd.json are located)
./ralph.sh

# Specify max iterations
./ralph.sh 20

# Make script executable (first time only)
chmod +x ralph.sh
```

### Prerequisites

1. **PRD in JSON format**: `prd.json` must exist (see `prd.json.example`)
2. **Cursor IDE**: Cursor must be installed and configured
3. **jq**: Required for JSON manipulation (`brew install jq` or `choco install jq`)
4. **Git repository**: Project should be a git repository

### Complete Workflow

#### Step 1: Prepare PRD

Create or convert your PRD to `prd.json` format:

```json
{
  "project": "MyApp",
  "branchName": "ralph/feature-name",
  "description": "Feature description",
  "userStories": [
    {
      "id": "US-001",
      "title": "Story title",
      "description": "As a user...",
      "acceptanceCriteria": [
        "Criterion 1",
        "Criterion 2"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

#### Step 2: Run Ralph

```bash
./ralph.sh
```

Ralph will:
- Check for incomplete stories
- Generate `.cursor/composer-prompt.md`
- Display instructions
- Wait for you to complete the story

#### Step 3: Implement Story

1. Open Cursor Composer (`Ctrl+I` or `Cmd+I`)
2. Reference or copy content from `.cursor/composer-prompt.md`
3. Cursor implements the story guided by `.cursorrules`
4. Review and verify the implementation

#### Step 4: Complete Story

After implementation:

1. **Run quality checks:**
   ```bash
   npm run typecheck  # or equivalent
   npm test           # if applicable
   npm run lint       # if applicable
   ```

2. **Commit changes:**
   ```bash
   git add .
   git commit -m "feat: US-001 - Story title"
   ```

3. **Update PRD:**
   ```bash
   # Using jq (recommended)
   jq '(.userStories[] | select(.id == "US-001") | .passes) = true' prd.json > prd.json.tmp && mv prd.json.tmp prd.json
   
   # Or edit manually
   ```

4. **Update progress.txt:**
   Append your learnings following the format in `.cursorrules`

5. **Press ENTER** in the terminal where Ralph is running

#### Step 5: Continue

Ralph will automatically:
- Check if all stories are complete
- If not, generate the next story prompt
- Continue the loop

## Archive System

Ralph automatically archives previous runs when the branch changes:

```
archive/
└── YYYY-MM-DD-feature-name/
    ├── prd.json
    └── progress.txt
```

**When archiving happens:**
- New `branchName` detected in `prd.json`
- Different from branch in `.last-branch`

**Archive contents:**
- Copy of `prd.json` from previous run
- Copy of `progress.txt` from previous run

## Completion Detection

Ralph checks for completion by:
1. Counting stories where `passes == false`
2. If count is 0, all stories are complete
3. Exits with success message

**Manual completion check:**
```bash
jq '[.userStories[] | select(.passes == false)] | length' prd.json
# Returns 0 if all complete
```

## Error Handling

### Missing PRD

If `prd.json` doesn't exist:
```
Error: prd.json not found in /path/to/project
Please create a PRD first. See README.md for instructions.
```

**Solution:** Create `prd.json` from `prd.json.example` or use PRD generation guides.

### Missing Template

If `.cursor/composer-prompt-template.md` is missing:
```
Error: Composer template not found: .cursor/composer-prompt-template.md
Please ensure .cursor/composer-prompt-template.md exists.
```

**Solution:** Ensure the `.cursor/` directory structure is set up correctly.

### No Incomplete Stories

If no stories with `passes: false` are found:
```
No incomplete stories found!
```

**Solution:** Either all stories are complete, or check `prd.json` format.

## Best Practices

### 1. Small Stories

Each story should be completable in one context window:
- ✅ "Add priority column to tasks table"
- ❌ "Build entire dashboard"

### 2. Proper Prioritization

Set priorities correctly in `prd.json`:
- Lower number = higher priority
- Dependencies first (database → backend → frontend)

### 3. Quality Checks

Always run quality checks before marking story complete:
- Type checking
- Tests (if applicable)
- Linting
- Browser verification (for UI stories)

### 4. Progress Documentation

Document learnings in `progress.txt`:
- Patterns discovered
- Gotchas encountered
- Useful context for future iterations

### 5. Git Workflow

- Work on feature branch (from `prd.json` branchName)
- Commit after each story completion
- Keep commits focused and atomic

## Integration with Cursor Rules

Ralph works seamlessly with other Cursor Rules:

- **`.cursorrules`** - Primary agent instructions
- **`.cursor/rules/prd-generation.md`** - Creating PRDs from scratch
- **`.cursor/rules/prd-from-external.md`** - Creating PRDs from websites/apps
- **`.cursor/rules/ralph-task-workflow.md`** - Task sizing guidelines
- **All 25 rules** - Available for reference during implementation

## Troubleshooting

### Ralph Not Progressing

**Issue:** Ralph keeps showing the same story.

**Check:**
- Did you update `prd.json` to set `passes: true`?
- Is the story ID correct in your update?

**Verify:**
```bash
jq '.userStories[] | select(.id == "US-001") | .passes' prd.json
# Should return: true
```

### Stories Skipped

**Issue:** Ralph jumps to a different story than expected.

**Cause:** Stories are sorted by priority, not order in file.

**Solution:** Check priority values in `prd.json`.

### Max Iterations Reached

**Issue:** Ralph stops before completing all stories.

**Solution:** Continue with more iterations:
```bash
./ralph.sh 10  # Run 10 more iterations
```

## Advanced Usage

### Custom Iteration Count

```bash
./ralph.sh 1    # Single iteration
./ralph.sh 50   # Extended run
```

### Script Location

Ralph can be run from any directory, but it looks for files relative to where `ralph.sh` is located:
```bash
/path/to/ralph/ralph.sh  # Works from anywhere
cd /path/to/project && ./scripts/ralph/ralph.sh  # If Ralph is in subdirectory
```

### Branch Management

Ralph respects the `branchName` in `prd.json`:
- Check if branch exists
- Create from main if needed
- Archive when branch changes

**Note:** Ralph doesn't automatically checkout branches - handle in your workflow or via `.cursorrules`.

## Example Session

```bash
$ ./ralph.sh 5

Starting Ralph - Max iterations: 5

═══════════════════════════════════════════════════════
  Ralph Iteration 1 of 5
═══════════════════════════════════════════════════════

Next story: US-001 - Add priority field to database

Composer prompt generated: .cursor/composer-prompt.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INSTRUCTIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Open Cursor Composer (Ctrl+I or Cmd+I)
2. Open the generated prompt: .cursor/composer-prompt.md
...
[User implements story, commits, updates prd.json]
...
Press ENTER after completing the story... [ENTER]

Continuing to next story...

[Loop continues...]
```

## Key Principles

1. **One story per iteration** - Focus on single, complete stories
2. **Clean context** - Each iteration starts fresh, guided by `.cursorrules`
3. **Persistent memory** - Git history, `progress.txt`, and `prd.json` maintain state
4. **Quality first** - All checks must pass before completion
5. **Documentation** - Learnings compound in `progress.txt` and `AGENTS.md`

## Related Documentation

- **`.cursorrules`** - Agent instructions for story implementation
- **`.cursor/composer-instructions.md`** - User guide for Composer workflow
- **`README.md`** - Main Ralph documentation
- **`AGENTS.md`** - Agent patterns and instructions
- **`.cursor/rules/prd-generation.md`** - PRD creation guide

## Checklist

Before running Ralph:

- [ ] `prd.json` exists with valid structure
- [ ] `.cursor/composer-prompt-template.md` exists
- [ ] Git repository initialized
- [ ] `jq` installed for JSON manipulation
- [ ] Cursor IDE available
- [ ] Stories are properly prioritized
- [ ] Branch strategy planned

During Ralph session:

- [ ] Follow Composer prompt instructions
- [ ] Run all quality checks
- [ ] Commit with proper message format
- [ ] Update `prd.json` to mark story complete
- [ ] Document learnings in `progress.txt`
- [ ] Press ENTER to continue
