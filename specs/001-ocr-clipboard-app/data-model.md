# Data Model: odOcr

## Entities

### ImageSource

Represents where the image for OCR processing comes from.

| Field | Type | Description |
|-------|------|-------------|
| `type` | enum | `clipboard` \| `file` \| `stdin` |
| `path` | string? | File path if type is `file` |
| `raw_data` | bytes? | Raw image bytes if type is `clipboard` or `stdin` |
| `format` | string? | Detected format (PNG, JPEG, BMP, etc.) |
| `size_bytes` | int | Original size in bytes |

### OCRResult

The output produced by the OCR processing pipeline.

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether OCR completed without errors |
| `text` | string? | Extracted text, or null if no text found |
| `confidence` | float | OCR confidence score (0.0–1.0) |
| `language` | string | Language(s) used for recognition |
| `processing_time_ms` | int | Total processing time in milliseconds |
| `source` | string | Origin description for user display |
| `description` | string? | Image content description (if `--describe` used) |
| `error` | string? | Error message if `success` is false |
| `error_code` | int? | Machine-readable error code if failed |

### AppConfig

Persistent configuration for the odOcr application.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `hotkey` | string | `ctrl+o` | Global hotkey combination |
| `output_format` | enum | `text` | Output format (`text` \| `json`) |
| `describe` | bool | `false` | Enable image description by default |
| `language` | string | `eng` | Default OCR language code |
| `dark_mode` | enum | `system` | Theme preference (`light` \| `dark` \| `system`) |
| `auto_copy` | bool | `true` | Auto-copy extracted text to clipboard |
| `installed_languages` | string[] | `["eng"]` | List of installed language packs |
| `describe_model_installed` | bool | `false` | Whether describe model is downloaded |

### ProcessingPipeline

The processing stages applied to an image before and during OCR.

| Stage | Description | Configurable |
|-------|-------------|--------------|
| Preprocessing | Grayscale, threshold, deskew, denoise | Via config flags (v2) |
| OCR | Text recognition via Tesseract | Language selection |
| Postprocessing | Spell-check, whitespace normalization | `--no-postprocess` flag (v2) |
| Description | Image captioning (optional) | `--describe` flag |

## Validation Rules

- `ImageSource.size_bytes` MUST be ≤ 50MB (enforced before processing)
- `OCRResult.confidence` MUST be between 0.0 and 1.0
- `AppConfig.hotkey` MUST match pattern `^[a-z]+(\+[a-z0-9]+)+$`
- `AppConfig.language` MUST be a valid Tesseract language code (3-letter ISO)
- Processing time MUST be tracked with millisecond precision

## State Transitions

### CLI mode (single-shot):
```
Start → Read source → Preprocess → OCR → Postprocess → Output → Exit
                ↑                                    ↓
           Error ← ← ← ← ← Failure ← ← ← ← ← ← ← ←
```

### Hotkey mode (background loop):
```
Start → Register hotkey → Enter message loop
                              ↓
                    Wait for Ctrl+O
                              ↓
                    Grab clipboard → Preprocess → OCR → Copy to clipboard → Show notification
                           ↓                                         ↑
                      Error toast ← Failure ← ← ← ← ← ← ← ← ← ← ← ←
                              ↓
                    Return to message loop
```
