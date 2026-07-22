# odOcr CLI Interface Contract

## Command Structure

```
odOcr [file] [options]
odOcr --hotkey        # Start background process with Ctrl+O hotkey
odOcr --help          # Show help
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `file` | path | no | Path to image file. Omit to read from clipboard. |

## Options

| Option | Alias | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--help` | `-h` | flag | — | Show help text and exit |
| `--json` | `-j` | flag | `false` | Output results as JSON (stdout) |
| `--describe` | `-d` | flag | `false` | Enable image content description |
| `--language` | `-l` | string | `eng` | OCR language code(s), comma-separated |
| `--hotkey` | — | flag | — | Register Ctrl+O and run as background process |
| `--quiet` | `-q` | flag | `false` | Suppress non-output messages (stderr only for errors) |
| `--version` | `-v` | flag | — | Show version and exit |
| `--install-lang` | — | code | — | Download and install a language pack |
| `--install-describe` | — | flag | — | Download image description model |
| `--config` | — | path | `~/.odOcr/config.json` | Path to config file |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success — text extracted |
| 1 | Error — no text found in image |
| 2 | Error — invalid file or clipboard |
| 3 | Error — OCR engine failure |
| 4 | Error — invalid arguments |

## Stdin Support

If `-` is passed as the file argument, read image data from stdin:
```
cat screenshot.png | odOcr -
```

## JSON Output Schema

**Success** (exit 0):
```json
{
  "success": true,
  "text": "Extracted text content here...",
  "confidence": 0.97,
  "language": "eng",
  "processing_time_ms": 850,
  "source": "clipboard",
  "description": null
}
```

**With --describe** (exit 0):
```json
{
  "success": true,
  "text": "Extracted text...",
  "confidence": 0.97,
  "language": "eng",
  "processing_time_ms": 3200,
  "source": "file:///C:/path/to/image.png",
  "description": "A document page showing meeting notes with bullet points about Q3 planning and budget allocation."
}
```

**No text found** (exit 1):
```json
{
  "success": false,
  "text": null,
  "confidence": 0,
  "language": "eng",
  "processing_time_ms": 620,
  "source": "clipboard",
  "error": "No text detected in the image"
}
```

**Error** (exit 2+):
```json
{
  "success": false,
  "error": "Could not read image from clipboard: clipboard is empty or contains non-image data",
  "error_code": 2,
  "processing_time_ms": 10
}
```

## Config File

Location: `~/.odOcr/config.json`

```json
{
  "hotkey": "ctrl+o",
  "output_format": "text",
  "describe": false,
  "language": "eng",
  "dark_mode": "system",
  "auto_copy": true
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `hotkey` | string | `ctrl+o` | Global hotkey combination |
| `output_format` | enum | `text` | `text` or `json` |
| `describe` | bool | `false` | Enable image description by default |
| `language` | string | `eng` | Default OCR language |
| `dark_mode` | enum | `system` | `light`, `dark`, or `system` |
| `auto_copy` | bool | `true` | Auto-copy extracted text to clipboard |
