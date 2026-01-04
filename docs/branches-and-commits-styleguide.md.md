# Git & GitHub Collaboration Guide

> **Source:** This document is based on the conventions from [Git Branch Naming and Commit Best Practices Cheatsheet](https://medium.com/@mandolkarmakarand94/git-branch-naming-and-commit-best-practices-cheatsheet-875316b9ca20), with additional enhancements and organization for collaborative development workflows.

---

## Table of Contents

1. [Branch Naming Conventions](#branch-naming-conventions)
2. [Commit Message Conventions](#commit-message-conventions)
3. [Common Workflow Commands](#common-workflow-commands)
4. [Branch Management](#branch-management)
5. [Collaboration & Synchronization](#collaboration--synchronization)
6. [Stash Operations](#stash-operations)
7. [Undo & Fix Operations](#undo--fix-operations)
8. [Clean Branch Operations](#clean-branch-operations)
9. [GitHub-Specific Commands](#github-specific-commands)
10. [Useful Shortcuts & Aliases](#useful-shortcuts--aliases)

---

## Branch Naming Conventions

### Format Rules
- Use lowercase and hyphens
- Format: `type/short-description`
- Keep descriptions concise and descriptive

### Common Branch Types

| Type | Description | Example |
|------|-------------|---------|
| `feature/` | New features | `feature/user-authentication` |
| `bugfix/` | Bug fixes | `bugfix/login-error` |
| `hotfix/` | Urgent production fixes | `hotfix/security-patch` |
| `release/` | Releases | `release/v1.2.0` |
| `docs/` | Documentation | `docs/api-documentation` |
| `refactor/` | Code restructuring | `refactor/database-layer` |
| `test/` | Tests | `test/integration-tests` |
| `chore/` | Maintenance tasks | `chore/update-dependencies` |

---

## Commit Message Conventions

### Format
```
type(optional-scope): short summary

Optional detailed description explaining what and why.
```

### Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): add OAuth2 login` |
| `fix` | Bug fix | `fix(api): resolve timeout issue` |
| `docs` | Documentation | `docs: update README` |
| `refactor` | Code restructuring | `refactor: simplify user service` |
| `test` | Tests | `test: add unit tests for auth` |
| `chore` | Maintenance | `chore: update dependencies` |
| `perf` | Performance improvement | `perf: optimize database queries` |
| `revert` | Revert changes | `revert: revert commit abc123` |
| `build` | Build system | `build: update webpack config` |
| `ci` | CI/CD | `ci: add GitHub Actions workflow` |

### Commit Message Rules
- Use imperative verbs (add, fix, update, remove)
- Keep summary under 50 characters
- One logical change per commit
- Add detailed description if needed (separated by blank line)

---

## Common Workflow Commands

### Creating and Switching Branches

```bash
# Create and switch to new branch
git checkout -b feature/my-feature

# Create branch from specific branch/commit
git checkout -b feature/new-feature main
git checkout -b bugfix/issue-123 abc1234

# Switch to existing branch
git checkout main
git checkout feature/my-feature

# Switch to previous branch
git checkout -
```

### Making Changes

```bash
# Stage all changes
git add .

# Stage specific files
git add file1.py file2.py

# Stage files interactively
git add -p

# Commit changes
git commit -m "feat: add new feature"

# Commit with detailed message
git commit -m "feat: add new feature" -m "Detailed description here"

# Stage and commit in one step (only for tracked files)
git commit -am "fix: update bug"
```

### Pushing Changes

```bash
# Push branch to remote
git push origin feature/my-feature

# Push and set upstream
git push -u origin feature/my-feature

# Push all branches
git push --all origin

# Push tags
git push origin --tags
```

---

## Branch Management

### Listing Branches

```bash
# List local branches
git branch

# List remote branches
git branch -r

# List all branches (local and remote)
git branch -a

# List branches with last commit info
git branch -v

# List merged branches
git branch --merged

# List unmerged branches
git branch --no-merged
```

### Renaming and Deleting Branches

```bash
# Rename current branch
git branch -m new-branch-name

# Rename other branch
git branch -m old-name new-name

# Delete local branch
git branch -d feature/old-feature

# Force delete local branch
git branch -D feature/old-feature

# Delete remote branch
git push origin --delete feature/old-feature
```

---

## Collaboration & Synchronization

### Fetching and Pulling

```bash
# Fetch latest changes from remote
git fetch origin

# Fetch all remotes
git fetch --all

# Pull changes (fetch + merge)
git pull origin main

# Pull with rebase (recommended for clean history)
git pull --rebase origin main

# Pull specific branch
git pull origin feature/other-feature
```

### Rebasing

```bash
# Rebase current branch onto main
git rebase main

# Interactive rebase (last 3 commits)
git rebase -i HEAD~3

# Continue rebase after resolving conflicts
git rebase --continue

# Abort rebase
git rebase --abort

# Skip current commit in rebase
git rebase --skip
```

### Merging

```bash
# Merge branch into current branch
git merge feature/my-feature

# Merge with no-fast-forward (creates merge commit)
git merge --no-ff feature/my-feature

# Merge with squash (combines commits into one)
git merge --squash feature/my-feature
git commit -m "feat: add complete feature"
```

---

## Stash Operations

### Basic Stash Commands

```bash
# Stash current changes
git stash

# Stash with message
git stash save "WIP: working on feature"

# List stashes
git stash list

# Apply most recent stash (keeps stash)
git stash apply

# Apply specific stash
git stash apply stash@{1}

# Pop most recent stash (removes from stash)
git stash pop

# Pop specific stash
git stash pop stash@{1}

# Drop stash
git stash drop stash@{1}

# Clear all stashes
git stash clear

# Show stash content
git stash show
git stash show -p  # with diff
```

---

## Undo & Fix Operations

### Amending Commits

```bash
# Amend last commit message
git commit --amend -m "New commit message"

# Amend last commit (add more changes)
git add forgotten-file.py
git commit --amend --no-edit

# Amend commit author
git commit --amend --author="Name <email>"
```

### Resetting Changes

```bash
# Unstage files (keep changes)
git reset HEAD file.py

# Unstage all files
git reset HEAD

# Reset to commit (keep changes)
git reset --soft HEAD~1

# Reset to commit (discard changes in staging)
git reset --mixed HEAD~1
git reset HEAD~1  # same as --mixed

# Reset to commit (discard all changes)
git reset --hard HEAD~1

# Reset to specific commit
git reset --hard abc1234

# Reset remote branch (use with caution!)
git push --force origin branch-name
```

### Reverting Commits

```bash
# Revert commit (creates new commit)
git revert HEAD
git revert abc1234

# Revert merge commit
git revert -m 1 merge-commit-hash
```

### Discarding Changes

```bash
# Discard changes in working directory
git checkout -- file.py

# Discard all changes
git checkout -- .

# Discard changes (newer syntax)
git restore file.py
git restore .
```

---

## Clean Branch Operations

### Create Clean Branch (No History)

```bash
git checkout --orphan new-branch
git rm -rf .
git add .
git commit -m "Initial commit"
git push origin new-branch
```

### Remove Old Commits

#### Option 1: Orphan Reset

```bash
git checkout my-branch
git checkout --orphan temp-branch
git add .
git commit -m "Clean start"
git branch -D my-branch
git branch -m my-branch
git push --force origin my-branch
```

#### Option 2: Hard Reset

```bash
git checkout my-branch
git reset --soft $(git commit-tree HEAD^{tree} -m "Initial clean commit")
git push --force origin my-branch
```

---

## GitHub-Specific Commands

### Working with Remote Repositories

```bash
# View remote repositories
git remote -v

# Add remote repository
git remote add origin https://github.com/user/repo.git

# Change remote URL
git remote set-url origin https://github.com/user/new-repo.git

# Remove remote
git remote remove origin

# Fetch from upstream
git fetch upstream
git merge upstream/main
```

### Working with Pull Requests

```bash
# Checkout pull request locally (GitHub)
git fetch origin pull/123/head:pr-123
git checkout pr-123

# Alternative: using GitHub CLI
gh pr checkout 123
```

### Tags

```bash
# List tags
git tag

# Create lightweight tag
git tag v1.0.0

# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tag to remote
git push origin v1.0.0

# Push all tags
git push origin --tags

# Delete tag
git tag -d v1.0.0
git push origin --delete v1.0.0
```

---

## Useful Shortcuts & Aliases

### Common Aliases Setup

```bash
# View status
git config --global alias.st status

# Short log
git config --global alias.lg "log --oneline --graph --decorate --all"

# Last commit
git config --global alias.last "log -1 HEAD"

# Unstage
git config --global alias.unstage "reset HEAD --"

# Amend
git config --global alias.amend "commit --amend --no-edit"

# Quick add and commit
git config --global alias.ac "!git add -A && git commit"

# View branches
git config --global alias.br branch
git config --global alias.co checkout
```

### Useful Git Commands

```bash
# Show commit history (one line per commit)
git log --oneline

# Show commit history with graph
git log --oneline --graph --all --decorate

# Show commits by author
git log --author="John Doe"

# Show commits in date range
git log --since="2 weeks ago"
git log --until="2024-01-01"

# Show file history
git log --follow file.py

# Show differences
git diff                    # Working directory vs staging
git diff --staged          # Staging vs last commit
git diff HEAD              # Working directory vs last commit
git diff main..feature     # Between two branches

# Show what changed in commit
git show abc1234

# Search in commit messages
git log --grep="bugfix"

# Count commits
git rev-list --count HEAD
```

---

## Quick Reference Workflow

### Typical Feature Development Workflow

```bash
# 1. Update local main branch
git checkout main
git pull --rebase origin main

# 2. Create feature branch
git checkout -b feature/my-feature

# 3. Make changes and commit
git add .
git commit -m "feat: add new feature"

# 4. Push branch
git push -u origin feature/my-feature

# 5. Keep branch updated with main
git fetch origin
git rebase origin/main

# 6. After code review, merge to main (on GitHub) or locally:
git checkout main
git pull origin main
git merge --no-ff feature/my-feature
git push origin main

# 7. Delete feature branch
git branch -d feature/my-feature
git push origin --delete feature/my-feature
```

---

## Tips for Collaborative Development

1. **Always pull with rebase** when updating your branch: `git pull --rebase origin main`
2. **Keep commits focused** - one logical change per commit
3. **Write clear commit messages** following conventions
4. **Review before pushing** - use `git log` and `git diff` to review changes
5. **Use feature branches** - never commit directly to `main`
6. **Keep branches up to date** - regularly rebase on main
7. **Use pull requests** for code review before merging
8. **Delete merged branches** to keep repository clean
9. **Use stashes** when switching branches with uncommitted work
10. **Communicate** with team about force pushes or major changes

---

*Last updated: Enhanced guide for collaborative Git/GitHub workflows*
