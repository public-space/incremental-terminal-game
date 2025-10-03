# Git Workflow for Colony.sh Development

**Version Stamp:** `[v0.2 Planning - 2025-10-03]`

---

## 🌿 Branch Strategy

### Main Branch
- **Purpose:** Stable, working versions only
- **Contains:** Released versions (v0.1, v0.2, etc.)
- **Rule:** Never push broken code to main

### Development Branches
- **Naming:** `v0.X-dev` (e.g., `v0.2-dev`, `v0.3-dev`)
- **Purpose:** Active development and testing
- **Merge to main:** Only after thorough testing

---

## 📋 How to Create a New Version Branch

### For v0.2 (Bug Fixes)

```bash
# Make sure you're on main and up to date
git checkout main
git pull origin main

# Create and switch to v0.2-dev branch
git checkout -b v0.2-dev

# Verify you're on the new branch
git branch
# Should show: * v0.2-dev
```

### For v0.3 (Features)

```bash
# Start from main (or from v0.2-dev if merged)
git checkout main
git pull origin main

# Create v0.3 branch
git checkout -b v0.3-dev
```

---

## 💾 Committing Changes

### Standard Commit Flow

```bash
# Check what's changed
git status

# See the actual changes
git diff

# Stage files you want to commit
git add <filename>

# Or stage everything
git add .

# Commit with descriptive message
git commit -m "v0.2: Fix building construction type error

- Fixed ResourceManager multiplication error
- Buildings now properly calculate production
- Tested with Solar Array and Mining Rig

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Commit Message Format

**Template:**
```
v0.X: [Brief summary of change]

- Bullet point details
- What was fixed/added
- Testing notes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Examples:**
```bash
# Bug fix
git commit -m "v0.2: Fix research purchase argument error"

# Feature addition
git commit -m "v0.3: Add intro dialog system"

# Multiple changes
git commit -m "v0.2: Fix menu flickering and border alignment

- Reduced screen refresh rate
- Fixed border calculations
- Tested on multiple terminal sizes"
```

---

## 🚀 Pushing to GitHub

### First Time Pushing a New Branch

```bash
# Push and set upstream tracking
git push -u origin v0.2-dev
```

The `-u` flag sets up tracking so future pushes are simpler.

### Subsequent Pushes

```bash
# Just push (tracking already set up)
git push
```

### Push Specific Branch

```bash
git push origin v0.2-dev
```

---

## 🔄 Switching Between Branches

### Switch to Main

```bash
git checkout main
```

### Switch to Development Branch

```bash
git checkout v0.2-dev
```

### Check Current Branch

```bash
git branch
# The current branch will have an asterisk: * v0.2-dev
```

---

## 🔀 Merging v0.2 Back to Main (When Ready)

### Step 1: Test Everything

Make absolutely sure v0.2-dev is working:
- All bugs fixed ✓
- Game runs without errors ✓
- Save/load works ✓
- Extensively playtested ✓

### Step 2: Merge

```bash
# Switch to main branch
git checkout main

# Make sure main is up to date
git pull origin main

# Merge v0.2-dev into main
git merge v0.2-dev

# If no conflicts, push to GitHub
git push origin main
```

### Step 3: Tag the Release (Optional but Recommended)

```bash
# Create a version tag
git tag -a v0.2 -m "Colony.sh v0.2 - Bug Fixes

- Fixed building construction error
- Fixed research purchase error
- Fixed menu flickering
- Fixed border alignment"

# Push the tag
git push origin v0.2
```

---

## 🔍 Useful Git Commands

### Check Status

```bash
git status              # See what's changed
git log --oneline       # See recent commits
git diff                # See unstaged changes
git diff --staged       # See staged changes
```

### Undo Mistakes

```bash
# Unstage a file (keep changes)
git reset HEAD <filename>

# Discard changes to a file (CAREFUL!)
git checkout -- <filename>

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

### View Branch Info

```bash
git branch              # List local branches
git branch -a           # List all branches (local + remote)
git remote -v           # Show remote repository info
```

---

## 📊 Development Workflow Example

### v0.2 Development Cycle

```bash
# 1. Create branch
git checkout -b v0.2-dev

# 2. Fix a bug
# ... edit files ...
git add .
git commit -m "v0.2: Fix building construction error"

# 3. Push to GitHub
git push -u origin v0.2-dev

# 4. Fix another bug
# ... edit files ...
git add .
git commit -m "v0.2: Fix research purchase error"
git push

# 5. Test thoroughly
./colony.sh

# 6. When all bugs fixed and tested
git checkout main
git merge v0.2-dev
git push origin main
git tag -a v0.2 -m "v0.2 Release - All bugs fixed"
git push origin v0.2
```

---

## 🎯 Quick Reference

### Create branch:
```bash
git checkout -b v0.X-dev
```

### Commit changes:
```bash
git add .
git commit -m "v0.X: Description"
```

### Push first time:
```bash
git push -u origin v0.X-dev
```

### Push after that:
```bash
git push
```

### Merge to main:
```bash
git checkout main
git merge v0.X-dev
git push origin main
```

---

## 💡 Pro Tips

1. **Commit often** - Small, focused commits are easier to understand and debug
2. **Test before merge** - Never merge broken code to main
3. **Use branches** - Keep experimental features isolated
4. **Write good messages** - Future you will thank you
5. **Push regularly** - Don't lose work, backup to GitHub often

---

## 🚨 Emergency: "I Messed Up"

### Accidentally committed to main instead of branch

```bash
# Create branch with current changes
git branch v0.2-dev

# Reset main to remote
git reset --hard origin/main

# Switch to new branch
git checkout v0.2-dev
```

### Want to start over on current branch

```bash
# See what's different from main
git diff main

# If you want to throw away ALL changes and match main
git reset --hard main
```

### Conflicts during merge

```bash
# Git will tell you which files have conflicts
# Open them and look for:
<<<<<<< HEAD
(your changes)
=======
(their changes)
>>>>>>> branch-name

# Fix manually, then:
git add <fixed-files>
git commit -m "Resolved merge conflicts"
```

---

**Remember:**
- `main` = stable and working
- `vX.X-dev` = active development
- Commit early, commit often
- Test before merging
- Document everything

---

*Happy coding! 🚀*
