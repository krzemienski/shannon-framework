# Shannon CLI Setup System

Foolproof installation and framework detection system for Shannon CLI.

## Overview

The setup system ensures Shannon Framework is properly installed and accessible before allowing CLI usage. It provides:

- **Automatic detection** across multiple locations
- **Interactive wizard** for guided installation
- **Framework validation** with comprehensive checks
- **Auto-repair** for incomplete installations
- **Offline support** via bundled framework

## Architecture

### FrameworkDetector

Searches for Shannon Framework in priority order:

1. `SHANNON_FRAMEWORK_PATH` environment variable (highest priority)
2. Claude Code plugin directory (`~/.claude/plugins/shannon`)
3. Bundled with CLI (`src/shannon/bundled/shannon-framework`)
4. Development location (`~/Desktop/shannon-framework`)
5. System installation (`/usr/local/share/shannon-framework`)

Validation checks:
- ✅ Plugin metadata (`.claude-plugin/plugin.json`)
- ✅ Skills directory (minimum 15 skills required)
- ✅ Commands directory (minimum 12 commands required)
- ✅ Core framework files

### SetupWizard

Interactive 5-step installation process:

1. **Python Version Check** - Verifies Python 3.10+
2. **Claude Agent SDK** - Installs if missing
3. **Shannon Framework** - Detects or guides installation
4. **Serena MCP** - Optional integration check
5. **Final Verification** - End-to-end validation

## Usage

### First-Time Setup

```bash
# Run interactive wizard
shannon setup

# Or let commands auto-trigger setup
shannon analyze spec.md  # Prompts for setup if needed
```

### Installation Options

The wizard provides three installation methods:

#### Option 1: Claude Code Plugin System (Recommended)

```bash
# In Claude Code, run:
/plugin marketplace add shannon-framework/shannon
/plugin install shannon@shannon-framework
```

Benefits:
- ✅ Automatic updates
- ✅ Integrated with Claude Code
- ✅ Managed dependencies

#### Option 2: Git Clone (Manual)

```bash
git clone https://github.com/shannon-framework/shannon.git ~/Desktop/shannon-framework
```

Benefits:
- ✅ Full control over updates
- ✅ Access to latest development changes
- ✅ Local modifications possible

#### Option 3: Bundled Snapshot (Offline)

Automatically used if framework is bundled with CLI installation.

Benefits:
- ✅ Works offline/airgapped
- ❌ No automatic updates
- ❌ Limited to snapshot version

### Diagnostics

```bash
# Show all framework locations and their status
shannon diagnostics
```

Output example:
```
Shannon Framework Diagnostics

Location                              Path                                    Status
────────────────────────────────────────────────────────────────────────────────────
Environment Variable                  None                                    ❌ Not Found
Claude Code Plugin Directory          /Users/nick/.claude/plugins/shannon     ✅ Valid
Bundled with CLI                      /path/to/bundled/shannon-framework      ❌ Not Found
Development Location                  /Users/nick/Desktop/shannon-framework   ⚠️ Invalid
System Installation                   /usr/local/share/shannon-framework      ❌ Not Found
```

## Environment Variables

### SHANNON_FRAMEWORK_PATH

Override automatic detection with explicit path:

```bash
export SHANNON_FRAMEWORK_PATH=/custom/path/to/shannon-framework
shannon analyze spec.md  # Uses custom path
```

Use cases:
- Testing multiple framework versions
- Custom installation locations
- CI/CD environments
- Development workflows

### Configuration Persistence

Framework path is saved to `~/.shannon/config.json`:

```json
{
  "log_level": "DEBUG",
  "session_dir": "/Users/nick/.shannon/sessions",
  "token_budget": 150000,
  "framework_path": "/Users/nick/.claude/plugins/shannon"
}
```

## Bundling Framework

For offline distribution or airgapped systems:

```bash
# Bundle framework with CLI
python scripts/bundle_framework.py --verify

# Bundle from custom location
python scripts/bundle_framework.py --source /path/to/framework --verify

# Clean and rebundle
python scripts/bundle_framework.py --clean --verify
```

Bundle is created at: `src/shannon/bundled/shannon-framework/`

Size: ~5-10 MB (excludes .git, tests, caches)

## Decorator Usage

Protect commands with framework requirement:

```python
from shannon.setup.framework_detector import FrameworkDetector
from shannon.cli.commands import require_framework

@cli.command()
@require_framework()
def analyze(spec_file: str):
    """Framework is guaranteed to be available here."""
    # Your implementation
    pass
```

The decorator:
1. Checks for framework availability
2. Validates framework completeness
3. Prompts user to run setup wizard if missing
4. Exits gracefully if setup is declined

## Error Handling

### Framework Not Found

```
⚠ Shannon Framework not detected

Shannon CLI requires Shannon Framework to be installed.

You have two options:
  1. Run the setup wizard: shannon setup
  2. Set SHANNON_FRAMEWORK_PATH environment variable

Run setup wizard now? [Y/n]:
```

### Incomplete Framework

```
⚠ Framework validation failed: Only 8 skills found (expected at least 15).
Framework may be incomplete.

Run shannon setup to repair or reinstall.
```

### Git Clone Failed

```
✗ Clone failed: [error details]

Manual installation:
  git clone https://github.com/shannon-framework/shannon.git ~/Desktop/shannon-framework
```

## Testing Setup System

```python
# Test framework detection
from shannon.setup import FrameworkDetector

path = FrameworkDetector.find_framework()
if path:
    is_valid, msg = FrameworkDetector.verify_framework(path)
    print(f"Found: {path}")
    print(f"Valid: {is_valid}")
    print(f"Message: {msg}")

# Test all locations
for loc in FrameworkDetector.search_all_locations():
    print(f"{loc['location_name']}: {loc['exists']}")
```

## Integration with CI/CD

```yaml
# GitHub Actions example
- name: Setup Shannon Framework
  run: |
    git clone https://github.com/shannon-framework/shannon.git shannon-framework
    export SHANNON_FRAMEWORK_PATH=$(pwd)/shannon-framework
    shannon diagnostics

- name: Verify framework
  run: |
    python -c "
    from shannon.setup import FrameworkDetector
    path = FrameworkDetector.find_framework()
    assert path, 'Framework not found'
    is_valid, _ = FrameworkDetector.verify_framework(path)
    assert is_valid, 'Framework invalid'
    "
```

## Troubleshooting

### Framework found but validation fails

```bash
# Check framework structure
ls -la ~/.claude/plugins/shannon/

# Expected structure:
# .claude-plugin/
#   plugin.json
# skills/
#   skill-1/SKILL.md
#   skill-2/SKILL.md
#   ...
# commands/
#   command-1.md
#   command-2.md
#   ...
# core/
```

### Multiple frameworks detected

Priority order determines which is used. Override with `SHANNON_FRAMEWORK_PATH`.

### Permission errors

```bash
# Fix plugin directory permissions
chmod -R u+rw ~/.claude/plugins/shannon/

# Or use different location
export SHANNON_FRAMEWORK_PATH=~/Documents/shannon-framework
```

## API Reference

### FrameworkDetector

```python
class FrameworkDetector:
    @classmethod
    def find_framework() -> Optional[Path]:
        """Search for framework in known locations."""

    @classmethod
    def verify_framework(path: Path) -> Tuple[bool, str]:
        """Verify framework completeness."""

    @classmethod
    def get_framework_info(path: Path) -> Dict[str, any]:
        """Extract detailed framework metadata."""

    @classmethod
    def search_all_locations() -> List[Dict[str, any]]:
        """Search all locations and return diagnostics."""
```

### SetupWizard

```python
class SetupWizard:
    def run() -> bool:
        """Run complete setup wizard."""

    def show_diagnostics():
        """Display framework detection diagnostics."""
```

## Future Enhancements

- [ ] Automatic framework updates
- [ ] Version compatibility checking
- [ ] Multiple framework profiles
- [ ] Docker container detection
- [ ] Windows compatibility improvements
- [ ] Framework health monitoring
- [ ] Auto-repair for common issues

## Support

If setup fails:

1. Run `shannon diagnostics` to check all locations
2. Verify framework structure manually
3. Try clean installation with `shannon setup`
4. Check GitHub issues: https://github.com/shannon-cli/shannon-cli/issues
