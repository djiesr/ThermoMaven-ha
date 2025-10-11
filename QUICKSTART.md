# Quick Start Guide

## Local Installation (Before GitHub)

### 1. Create Your Configuration File

```bash
# Copy the template
cp env.example .env

# Edit with your real credentials
# (use nano, vim, or your preferred editor)
nano .env
```

⚠️ **Important**: You need to find the `app_key` value first! See README.md for details.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Test the Client

```bash
python thermomaven_client.py
```

**Expected Result Without App Key:**
```
Status: 200
Response: {"code":"40000","msg":"Sign error"}
[ERROR] Sign error
=== FAILED ===
```

## Verify What Will Be Sent to GitHub

```bash
# See the list of files to be included
git add -n .

# Should only show:
# - thermomaven_client.py
# - whatweknow/part1.txt
# - whatweknow/part2.txt
# - README.md
# - requirements.txt
# - .gitignore
# - .gitattributes
# - env.example
# - QUICKSTART.md
```

## Current Project Structure

```
ThermoMaven-ha/
├── .gitignore              ✓ Created (excludes Frida, root, etc.)
├── .gitattributes          ✓ Created (for GitHub)
├── README.md               ✓ Created (documentation)
├── QUICKSTART.md           ✓ Created (this file)
├── env.example             ✓ Created (config template)
├── requirements.txt        ✓ Created (dependencies)
├── thermomaven_client.py   ✓ Secured (no credentials)
├── whatweknow/             ✓ To include
│   ├── part1.txt
│   └── part2.txt
├── Frida/                  ✗ Excluded (.gitignore)
├── root/                   ✗ Excluded (.gitignore)
├── thermomaven_decompiled/ ✗ Excluded (.gitignore)
└── thermomaven_client - Copie.py  ✗ Excluded (.gitignore)
```

## Next Steps

1. **Find the app_key** - Critical for API to work
2. **Test locally** - Verify the client works
3. **Check .gitignore** - `git status` should not show excluded folders
4. **Initialize Git** - Already done if you followed the setup
5. **Push to GitHub** - Already done if you followed the setup

## Verification Commands

```bash
# 1. Verify folders are excluded
ls -la | grep -E "(Frida|root|thermomaven_decompiled)"
# These folders must exist locally

git status
# These folders should NOT appear in git status

# 2. Verify the structure to be pushed
git ls-files  # (after git add .)
# Should only show desired files

# 3. Verify no credentials in code
grep -r "djiesr" .
# Should return nothing (or only in .env which is ignored)
```

## Git Commands Reference

```bash
# View repository status
git status

# Add modifications
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push

# View history
git log --oneline

# Create new branch
git checkout -b branch-name

# Return to main
git checkout main
```

## Help

If you see unwanted files:

```bash
# Remove a file from Git index (without deleting it)
git rm --cached filename

# Remove a folder from Git index
git rm -r --cached foldername/

# Then commit
git commit -m "Remove unwanted files"
git push
```

## Finding the App Key

The `app_key` is essential for the API to work. Possible locations:

1. **Native libraries** (`.so` files in the APK)
2. **Obfuscated strings** in decompiled code
3. **Network traffic** captures
4. **Configuration files** embedded in resources

Check `thermomaven_decompiled/` folder for clues.
