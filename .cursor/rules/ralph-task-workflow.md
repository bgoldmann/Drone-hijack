# Ralph Task Workflow (Reference)

**Note:** This is a reference guide for understanding the Ralph workflow pattern. The current Ralph implementation uses `prd.json` format instead of task lists.

This document describes an alternative Ralph workflow using task dependencies (based on Amp's task_list system). For the standard Ralph workflow using `prd.json`, see `.cursorrules` and `README.md`.

## Overview

This workflow pattern involves breaking features into tasks with dependencies, where each task is completable in one iteration.

## Key Concepts

### Task Size

**Each task must be completable in ONE Ralph iteration (~one context window).**

If a task is too big, the LLM runs out of context before finishing.

### Right-sized tasks:
- Add a database column + migration
- Create a single UI component
- Implement one server action
- Add a filter to an existing list
- Write tests for one module

### Too big (split these):
- "Build the entire dashboard" → Split into: schema, queries, components, filters
- "Add authentication" → Split into: schema, middleware, login UI, session handling
- "Refactor the API" → Split into one task per endpoint

**Rule of thumb:** If you can't describe the change in 2-3 sentences, it's too big.

## Task Ordering: Dependencies First

Tasks execute in dependency order. Earlier tasks must not depend on later ones.

**Correct order:**
1. Schema/database changes (migrations)
2. Server actions / backend logic
3. UI components that use the backend
4. Dashboard/summary views that aggregate data

**Wrong order:**
1. UI component (depends on schema that does not exist yet)
2. Schema change

## Acceptance Criteria: Must Be Verifiable

Each criterion must be something verifiable, not vague.

### Good criteria (verifiable):
- "Add `status` column to tasks table with default 'pending'"
- "Filter dropdown has options: All, Active, Completed"
- "Clicking delete shows confirmation dialog"
- "npm run typecheck passes"
- "npm test passes"

### Bad criteria (vague):
- "Works correctly"
- "User can do X easily"
- "Good UX"
- "Handles edge cases"

### Always include:
```
npm run typecheck passes
```

For stories with testable logic, also include:
```
npm test passes
```

For stories that change UI, also include:
```
Verify in browser using Cursor's browser capabilities
```

## Using with Ralph

If you want to use a task-based workflow with Ralph:

1. Convert your tasks to `prd.json` format using the ralph-conversion guide
2. Use the standard Ralph workflow with `prd.json` and `ralph.sh`
3. Tasks become user stories with priority ordering

The `prd.json` format is simpler and doesn't require external task management systems.
