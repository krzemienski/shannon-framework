# Shannon Framework Scripts

This directory contains implementation scripts for Shannon Framework features.

## Custom Instructions Generator

**Status**: V5 Feature - Implementation in progress

**Purpose**: Auto-generate project-specific custom instructions from project structure

**Files**:
- `generate_custom_instructions.py` - Main generator script (to be implemented)
- Integration with `/shannon:generate_instructions` command

**Implementation TODO**:
1. Create `generate_custom_instructions.py` following spec in `core/PROJECT_CUSTOM_INSTRUCTIONS.md`
2. Implement project type detection (CLI, web app, library)
3. Implement build command extraction (package.json, Makefile, etc.)
4. Implement CLI argument pattern detection
5. Implement staleness detection algorithm
6. Test with Python, JavaScript, Rust projects

**Estimated Effort**: 4-6 hours

**See**: `core/PROJECT_CUSTOM_INSTRUCTIONS.md` for complete specification

## Future Scripts

Additional scripts for Shannon automation will be added here.

