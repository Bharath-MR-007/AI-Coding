# Git Workflow Guide

This guide explains how to sync your local project files with GitHub. Follow these steps whenever you add, modify, or delete files in this repository.

## 1. Check Git Status
```
git status
```
See which files have changed.

## 2. Stage Your Changes
```
git add <filename>
```
Or to add all changes:
```
git add .
```

## 3. Commit Your Changes
```
git commit -m "Describe your changes here"
```

## 4. Pull Latest Changes (to avoid conflicts)
```
git pull origin main
```

## 5. Push Your Changes to GitHub
```
git push origin main
```

## 6. Resolve Conflicts (if any)
If you see a conflict, edit the files to fix them, then repeat steps 2–5.

---

**Tip:**
- Always pull before you push to avoid conflicts.
- Use clear commit messages.
- For more advanced workflows (branches, pull requests), see the official [GitHub Docs](https://docs.github.com/en/get-started/quickstart).
