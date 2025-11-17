# SECURITY ISSUE: API Key in Git History

**Severity**: CRITICAL
**Status**: Working copy FIXED, history still contains secret
**Commit**: be86099 (init commit, 205 commits ago)

## Current State

**Working Copy**: ✅ CLEAN
- Commit 358c23d removed hardcoded API key from tests/functional/helpers.sh
- Now requires environment variable

**Git History**: ❌ EXPOSED
- Commit be86099 contains: `***REMOVED_API_KEY***`
- File: tests/functional/helpers.sh
- 205 commits in history, 23 unpushed

## Immediate Action Required

**ROTATE API KEY**: Exposed key should be invalidated immediately

## Git History Cleanup Options

**Option A: Git Filter-Repo** (Recommended)
```bash
# Install if needed
brew install git-filter-repo

# Remove secret from all history
git filter-repo --path tests/functional/helpers.sh --invert-paths --force

# Or use BFG Repo Cleaner
brew install bfg
bfg --replace-text <(echo "***REMOVED_API_KEY***==>***REMOVED***")
```

**Option B: Interactive Rebase** (Manual)
```bash
# Rebase from init commit
git rebase -i --root
# Edit be86099, amend to remove key, continue
```

**Option C: Accept Risk**
- Rotate key
- Document in .gitignore
- Push with warning comment
- Secret remains in public history (not recommended)

## Recommendation

1. Rotate API key IMMEDIATELY
2. Use git filter-repo to clean history
3. Force push to origin (all contributors need to re-clone)
4. Add .env.example for future

## Current Push Status

**Cannot safely push** until:
- API key rotated
- History cleaned OR
- Accepted as known risk

**User decision required** on history cleanup approach.
