#!/bin/bash
# Shannon Framework - User Prompt Submit Hook
# Auto-detects large prompts/files and activates forced reading protocol

# Get prompt content from environment
PROMPT="${PROMPT_CONTENT:-}"
PROMPT_LENGTH=${#PROMPT}
PROMPT_LINES=$(echo "$PROMPT" | wc -l)

# Detect referenced files (@file syntax)
REFERENCED_FILES=$(echo "$PROMPT" | grep -oE '@[^ ]+' | sed 's/@//' || true)

# Calculate total content size
TOTAL_LINES=$PROMPT_LINES
LARGE_FILES=()

for file in $REFERENCED_FILES; do
  if [ -f "$file" ]; then
    FILE_LINES=$(wc -l < "$file" 2>/dev/null || echo "0")
    TOTAL_LINES=$((TOTAL_LINES + FILE_LINES))

    # Track large individual files
    if [ "$FILE_LINES" -gt 500 ]; then
      LARGE_FILES+=("$file:$FILE_LINES")
    fi
  fi
done

# Check if forced reading should activate
ACTIVATE_FORCED_READING=false

# Trigger 1: Long prompt
if [ "$PROMPT_LENGTH" -gt 3000 ] || [ "$PROMPT_LINES" -gt 100 ]; then
  ACTIVATE_FORCED_READING=true
  TRIGGER_REASON="Long prompt: $PROMPT_LENGTH chars, $PROMPT_LINES lines"
fi

# Trigger 2: Large individual file
if [ "${#LARGE_FILES[@]}" -gt 0 ]; then
  ACTIVATE_FORCED_READING=true
  TRIGGER_REASON="Large file(s) referenced: ${#LARGE_FILES[@]} files >500 lines"
fi

# Trigger 3: Total content exceeds threshold
if [ "$TOTAL_LINES" -gt 1000 ]; then
  ACTIVATE_FORCED_READING=true
  TRIGGER_REASON="Total content: $TOTAL_LINES lines"
fi

# Trigger 4: Explicit keywords
if echo "$PROMPT" | grep -qiE "(large file|long document|comprehensive spec|complete specification)"; then
  ACTIVATE_FORCED_READING=true
  TRIGGER_REASON="Explicit large content keyword detected"
fi

# Activate forced reading protocol if triggered
if [ "$ACTIVATE_FORCED_READING" = true ]; then
  echo ""
  echo "════════════════════════════════════════════════════════════════"
  echo "🔴 FORCED READING PROTOCOL ACTIVATED"
  echo "════════════════════════════════════════════════════════════════"
  echo ""
  echo "**Trigger**: $TRIGGER_REASON"
  echo ""
  echo "**Content Analysis**:"
  echo "  - Prompt: $PROMPT_LENGTH characters, $PROMPT_LINES lines"
  echo "  - Referenced files: $(echo "$REFERENCED_FILES" | wc -w) files"
  echo "  - Total lines: $TOTAL_LINES"
  echo ""

  # List large files
  if [ "${#LARGE_FILES[@]}" -gt 0 ]; then
    echo "**Large Files Detected**:"
    for file_info in "${LARGE_FILES[@]}"; do
      IFS=':' read -r file lines <<< "$file_info"
      echo "  - $file: $lines lines"
    done
    echo ""
  fi

  echo "**Shannon Requirements (MANDATORY)**:"
  echo "  1. ✅ Read EVERY line before responding"
  echo "  2. ✅ Use checkpoints every 100 lines"
  echo "  3. ✅ Verify comprehension at each checkpoint"
  echo "  4. ✅ Cite specific line numbers in response"
  echo "  5. ✅ Track progress quantitatively"
  echo ""
  echo "**Skill**: forced-reading-auto-activation"
  echo "**Estimated reading time**: $((TOTAL_LINES / 50)) minutes (50 lines/min)"
  echo ""
  echo "════════════════════════════════════════════════════════════════"
  echo "📖 Beginning systematic line-by-line reading..."
  echo "════════════════════════════════════════════════════════════════"
  echo ""

  # Log activation to Serena (if available)
  if command -v serena_write &> /dev/null; then
    serena_write "forced_reading/activations/$(date +%s)" "{
      \"trigger\": \"$TRIGGER_REASON\",
      \"prompt_length\": $PROMPT_LENGTH,
      \"prompt_lines\": $PROMPT_LINES,
      \"referenced_files\": $(echo "$REFERENCED_FILES" | wc -w),
      \"total_lines\": $TOTAL_LINES,
      \"large_files\": ${#LARGE_FILES[@]},
      \"timestamp\": \"$(date -Iseconds)\"
    }"
  fi
fi

# Always exit 0 (hook doesn't block, just informs)
exit 0
