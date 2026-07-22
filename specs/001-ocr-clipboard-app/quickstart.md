# Quickstart: odOcr Validation Guide

## Prerequisites

- Python 3.10+
- Tesseract 5.x installed and in PATH
- Windows (primary target)

## Setup

```bash
# Install odOcr
pip install -e .

# Verify installation
odOcr --version

# Download English language pack (auto-done on first run)
odOcr --install-lang eng
```

## Validation Scenarios

### Scenario 1: Clipboard OCR (Core P1)

```bash
# 1. Copy any image with text to clipboard (screenshot, etc.)
# 2. Run:
odOcr

# Expected: Extracted text printed to stdout
# Verify: Text matches what's visible in the source image
```

**Acceptance check**: Text is extracted accurately (≥95% CER) and printed to stdout.

### Scenario 2: File OCR (Core P1)

```bash
# Create a test image with text, then:
odOcr test_image.png

# Expected: Extracted text printed to stdout

# With JSON output:
odOcr test_image.png --json

# Expected: JSON object with text, confidence, processing_time_ms
```

**Acceptance check**: File-based OCR returns text within 10s for images up to
10MB (per spec SC-002).

### Scenario 3: Hotkey Mode (Core P1)

```bash
# Start background process:
odOcr --hotkey

# Expected: System tray icon appears

# Copy an image to clipboard and press Ctrl+O
# Expected: Notification popup shows extracted text
#           Text is automatically copied to clipboard
```

**Acceptance check**: Ctrl+O triggers OCR within 5s and text is on clipboard
(per spec SC-001).

### Scenario 4: Image Description (P2)

```bash
# Requires describe model installation first:
odOcr --install-describe

# Then:
odOcr --describe image.png

# Expected: Both extracted text and image description printed to stdout

# Or with hotkey mode:
odOcr --describe --hotkey
# Ctrl+O now includes description in output
```

**Acceptance check**: Description meaningfully describes the image content.

### Scenario 5: Error Handling

```bash
# Non-image in clipboard:
odOcr
# Expected: "No image found in clipboard" error message

# Invalid file:
odOcr nonexistent.png
# Expected: Error to stderr, exit code 2

# No text in image:
odOcr blank_image.png
# Expected: "No text detected" message, exit code 1
```

**Acceptance check**: All error cases produce clear, actionable messages.

### Scenario 6: JSON Output (Programmatic Use)

```bash
odOcr test_image.png --json --quiet | python -c "import sys, json; d=json.load(sys.stdin); print(d['text'])"
```

**Acceptance check**: JSON is valid, contains all required fields per CLI
contract.

### Scenario 7: Different Languages

```bash
# Install French:
odOcr --install-lang fra

# OCR a French document:
odOcr --language fra french_doc.png

# Multiple languages:
odOcr --language eng,fra bilingual_doc.png
```

**Acceptance check**: Language packs install to ~/.odOcr/languages/ and are
loaded on demand.

## Verification Checklist

- [ ] `odOcr` without args shows help text
- [ ] `odOcr` with image on clipboard extracts text
- [ ] `odOcr path/to/image.png` extracts text from file
- [ ] `odOcr --json` outputs valid JSON
- [ ] `odOcr --hotkey` shows tray icon and registers Ctrl+O
- [ ] Ctrl+O with image on clipboard shows notification + copies text
- [ ] Ctrl+O with text on clipboard shows "no image" error
- [ ] `odOcr --describe` returns both text and description
- [ ] Non-existent file exits with code 2 and error message
- [ ] Total install size < 100MB
- [ ] Tray icon idle RAM < 50MB

## Cleanup

```bash
# Stop hotkey mode: right-click tray icon → Exit
# Or: taskkill /f /im odOcr.exe

# Uninstall:
pip uninstall odOcr
```
