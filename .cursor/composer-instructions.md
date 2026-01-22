# Using Ralph with Cursor Composer

This guide explains how to use Ralph's autonomous workflow with Cursor IDE's Composer feature.

## Overview

Ralph works by generating Composer prompts for each user story in your PRD. You use Cursor Composer to execute each story, guided by `.cursorrules`.

## Workflow

### 1. Start Ralph

Run the Ralph script from your project root:

```bash
./ralph.sh [max_iterations]
```

Default is 10 iterations.

The script will:
- Analyze `prd.json` to find the next incomplete story
- Generate `.cursor/composer-prompt.md` with the current story details
- Display instructions for using Cursor Composer

### 2. Use Cursor Composer

1. Open Cursor Composer (usually `Ctrl+I` or `Cmd+I`)
2. The generated prompt in `.cursor/composer-prompt.md` will contain:
   - The current story ID and details
   - Acceptance criteria
   - Instructions for implementation
3. Copy the prompt or reference it in Composer
4. Cursor will be guided by `.cursorrules` to implement the story

### 3. After Implementation

After Composer completes the implementation:

1. **Verify quality checks pass** - Run typecheck, tests, lint as required
2. **Review the changes** - Ensure they match the acceptance criteria
3. **Commit the changes** - Use the commit message format: `feat: [Story ID] - [Story Title]`
4. **Update prd.json** - Mark the story as `passes: true`:

```bash
# Use jq to update the PRD
jq '.userStories[] | select(.id == "US-001") | .passes = true' prd.json > prd.json.tmp && mv prd.json.tmp prd.json
```

Or update manually in the JSON file.

5. **Update progress.txt** - Add your learnings following the format in `.cursorrules`

### 4. Continue to Next Story

Run `./ralph.sh` again to generate the next story prompt, or continue until all stories are complete.

## Composer Prompt Location

The generated Composer prompt is saved at:
```
.cursor/composer-prompt.md
```

This file is updated automatically by `ralph.sh` for each iteration.

## Tips

- Read `.cursorrules` before starting - it contains all the guidelines Ralph follows
- Check `progress.txt` for Codebase Patterns - these are consolidated learnings from previous iterations
- Update AGENTS.md files if you discover reusable patterns
- Each story should be small enough to complete in one Composer session

## Troubleshooting

### Story Not Updating in prd.json

If `ralph.sh` doesn't detect completion, manually verify `prd.json` has all stories marked `passes: true`.

### Quality Checks Failing

Do not commit if quality checks fail. Fix the issues first, then commit and update the PRD.

### Missing Context

If Composer needs more context, reference:
- `progress.txt` - Previous learnings and patterns
- `AGENTS.md` - Directory-specific patterns
- `.cursorrules` - Core workflow rules
