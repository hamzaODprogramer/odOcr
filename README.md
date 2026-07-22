<div align="center">

# odOcr

**Desktop OCR for Windows — paste an image, get text.**

[![Python](https://img.shields.io/badge/Python-%3E=3.10-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Tesseract](https://img.shields.io/badge/Tesseract-5.x-3c873a?style=flat-square)](https://github.com/tesseract-ocr/tesseract)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-8A2BE2?style=flat-square)](https://github.com/new)

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Architecture](#architecture) • [Configuration](#configuration) • [Troubleshooting](#troubleshooting)

</div>

A lightweight OCR utility that extracts text from clipboard images or image files. Runs as a single-shot CLI command or as a background process with a system tray icon and global hotkey (Ctrl+O).

---

## Features

- **Clipboard OCR** — Copy any image, run `odOcr`, get text back (auto-copied to clipboard)
- **Background mode** — System tray icon + Ctrl+O global hotkey for instant OCR
- **File input** — Pass an image path directly: `odOcr screenshot.png`
- **JSON output** — Machine-readable output with confidence scores and timing
- **Tesseract auto-detect** — Finds your Tesseract installation without PATH configuration
- **Lightweight** — ~43MB on disk, no heavy frameworks, no always-on daemon

## Installation

### Prerequisites

- **Python 3.10 or later** installed on your system
- **Tesseract OCR** must be installed separately

> [!NOTE]
> odOcr uses Tesseract 5.x as its OCR engine. The Python package ([pytesseract](https://github.com/madmaze/pytesseract)) is a wrapper and does not include Tesseract itself.

#### Install Tesseract

Download the installer from the [UB-Mannheim Tesseract page](https://github.com/UB-Mannheim/tesseract/wiki) (Windows) or use your package manager:

```powershell
# Windows (winget)
winget install UB-Mannheim.TesseractOCR
```

The default install location `C:\Program Files\Tesseract-OCR\tesseract.exe` is detected automatically — no PATH changes needed.

### Install odOcr

```bash
pip install git+https://github.com/<your-username>/odOcr.git
```

Or from a local clone:

```bash
git clone https://github.com/<your-username>/odOcr.git
cd odOcr
pip install .
```

## Usage

### Quick start

Copy an image to your clipboard (screenshot, photo, scanned document), then:

```bash
odOcr
```

Output:
```
OCR Result
----------------------------------------

Extracted text appears here.

----------------------------------------
Confidence: 95%
Language: eng
Time: 350ms

(Copied to clipboard)
```

### Common commands

```bash
# OCR from an image file
odOcr screenshot.png

# Machine-readable JSON output
odOcr --json

# Use a different language (e.g. French + English)
odOcr -l fra+eng

# Run as background process (tray icon + Ctrl+O)
odOcr --hotkey

# Suppress verbose output
odOcr --quiet
```

### Exit codes

| Code | Meaning |
|------|---------|
| `0` | Text extracted successfully |
| `1` | No text found in image |
| `2` | Invalid file path or empty clipboard |
| `3` | OCR engine failure |

## Architecture

```
Clipboard / File
      |
      v
+-------------+     +----------------+     +-----------+
| clipboard   | --> | image          | --> | ocr       | --> stdout
| .py         |     | .py            |     | .py       |
+-------------+     +----------------+     +-----------+
                      |                       |
                  Grayscale               Tesseract
                  Denoise (median)        5.x
                  Contrast stretch        pytesseract
                  Resize if >4000px       Confidence calc
```

Two runtime modes:

- **Single-shot** (`odOcr`) — grabs clipboard, runs OCR, prints result, exits
- **Background** (`odOcr --hotkey`) — registers Ctrl+O, shows tray icon, stays resident. Left-click tray or press Ctrl+O to trigger OCR on current clipboard content. Right-click tray for Exit.

## Configuration

Settings are persisted in `~/.odOcr/config.json` (created on first run):

```json
{
  "hotkey": "ctrl+o",
  "output_format": "text",
  "language": "eng",
  "auto_copy": true,
  "installed_languages": ["eng"]
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `output_format` | string | `"text"` | `"text"` or `"json"` |
| `language` | string | `"eng"` | Tesseract language code(s) |
| `auto_copy` | boolean | `true` | Auto-copy extracted text to clipboard |
| `installed_languages` | array | `["eng"]` | Installed language packs |

## Troubleshooting

### Tesseract is not installed or not in PATH

odOcr auto-detects Tesseract at `C:\Program Files\Tesseract-OCR\tesseract.exe`. If you installed to a custom location, set the `TESSERACT_PATH` environment variable:

```powershell
$env:TESSERACT_PATH = "D:\path\to\tesseract.exe"
```

### No text detected

- Ensure the image contains clear, machine-printed text
- Screenshots and scanned documents work best
- Try a higher-resolution image

### Hotkey mode doesn't register

- Windows only — `--hotkey` uses Win32 API (`RegisterHotKey`)
- Run without admin privileges (no elevation needed)
- Close other apps that may be using Ctrl+O

## Storage budget

| Component | Size |
|-----------|------|
| Tesseract binary | ~25 MB |
| English language pack | ~2 MB |
| Python dependencies | ~15 MB |
| odOcr source | ~1 MB |
| **Total** | **~43 MB** |

---

<div align="center">
  <sub>Built with Python, Tesseract, and ❤️</sub>
</div>
