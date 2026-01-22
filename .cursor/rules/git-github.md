# Git & GitHub Workflow Guide

Comprehensive guide for using Git and GitHub in Cursor IDE. Covers branching strategies, commit conventions, pull requests, and collaboration workflows.

## Git Basics

### Configuration

```bash
# Set up user identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Useful aliases
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
```

### Common Commands

```bash
# Initialize repository
git init

# Clone repository
git clone https://github.com/user/repo.git

# Check status
git status

# Add files
git add .
git add specific-file.ts

# Commit
git commit -m "feat: add user authentication"

# Push
git push origin main

# Pull
git pull origin main

# View history
git log --oneline
git log --graph --all
```

## Branching Strategy

### Git Flow

```bash
# Main branches
main          # Production-ready code
develop       # Integration branch

# Feature branches
feature/user-auth
feature/dashboard

# Release branches
release/1.0.0

# Hotfix branches
hotfix/critical-bug
```

### Branch Workflow

```bash
# Create feature branch
git checkout -b feature/user-authentication

# Work on feature
git add .
git commit -m "feat: implement login form"

# Keep branch updated
git checkout develop
git pull origin develop
git checkout feature/user-authentication
git merge develop

# Push feature branch
git push origin feature/user-authentication
```

## Commit Conventions

### Conventional Commits

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, semicolons, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding/updating tests
- `chore`: Maintenance tasks (dependencies, config)

### Examples

```bash
feat(auth): add JWT token authentication
fix(api): resolve user creation validation error
docs(readme): update installation instructions
refactor(components): extract reusable button component
test(users): add unit tests for user service
chore(deps): update dependencies to latest versions
```

### Good Commit Messages

```bash
# BAD
git commit -m "fix bug"
git commit -m "update"
git commit -m "changes"

# GOOD
git commit -m "fix(auth): resolve session expiration issue"
git commit -m "feat(dashboard): add revenue analytics chart"
git commit -m "refactor(api): simplify error handling logic"
```

## Pull Requests

### PR Best Practices

1. **Clear Title**: Descriptive title using commit convention
2. **Description**: Explain what and why, not just what
3. **Small PRs**: Keep changes focused and reviewable
4. **Link Issues**: Reference related issues/PRs
5. **Testing**: Describe how to test the changes

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] Edge cases considered

## Related Issues
Closes #123
```

## GitHub Workflow

### Issues

```markdown
# Issue Title: Brief, descriptive

## Description
Detailed description of the issue or feature request

## Steps to Reproduce (for bugs)
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: macOS
- Browser: Chrome
- Version: 1.0.0
```

### Labels

- `bug`: Something isn't working
- `enhancement`: New feature or improvement
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed

## Git Commands

### Undoing Changes

```bash
# Unstage files
git reset HEAD file.ts

# Discard local changes
git checkout -- file.ts

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert a commit (creates new commit)
git revert <commit-hash>
```

### Stashing

```bash
# Save current changes
git stash

# List stashes
git stash list

# Apply stash
git stash apply
git stash pop  # Apply and remove

# Drop stash
git stash drop
```

### Branch Management

```bash
# List branches
git branch
git branch -a  # All branches including remote

# Delete branch
git branch -d feature/old-feature
git push origin --delete feature/old-feature

# Rename branch
git branch -m old-name new-name
```

## Collaboration

### Rebasing

```bash
# Interactive rebase
git rebase -i HEAD~3

# Rebase feature branch onto main
git checkout feature/my-feature
git rebase main

# If conflicts, resolve and continue
git rebase --continue
```

### Conflict Resolution

```bash
# When conflict occurs
git status  # See conflicted files

# Edit files to resolve conflicts
# Look for <<<<<<< HEAD markers

# After resolving
git add resolved-file.ts
git commit  # or git rebase --continue
```

## GitHub Actions (Basic)

### Workflow Example

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm test
      - run: npm run lint
```

## Best Practices

### 1. Commit Often

Make small, logical commits rather than large ones.

### 2. Write Good Commit Messages

Follow conventional commits format.

### 3. Keep Branches Up to Date

Regularly merge/rebase from main branch.

### 4. Review Before Push

```bash
# Check what will be pushed
git log origin/main..HEAD

# Review diff
git diff origin/main
```

### 5. Use .gitignore

```gitignore
# Dependencies
node_modules/
__pycache__/

# Environment variables
.env
.env.local

# Build outputs
dist/
build/
.next/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

## Checklist for Git Workflow

Before committing:

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] No debugging code left in
- [ ] Commit message follows convention
- [ ] Related files committed together
- [ ] .gitignore updated if needed
- [ ] Large files not committed (use Git LFS if needed)

Before pushing:

- [ ] Branch is up to date with main
- [ ] All commits have descriptive messages
- [ ] No sensitive data in commits (API keys, passwords)
- [ ] Changes are tested

Before PR:

- [ ] PR title is clear and descriptive
- [ ] PR description explains changes
- [ ] All CI checks pass
- [ ] Code reviewed by yourself
- [ ] Related issues linked
