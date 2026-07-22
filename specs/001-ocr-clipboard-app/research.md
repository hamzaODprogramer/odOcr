# Research: odOcr OCR Clipboard Desktop App

## OCR Engine Comparison

### Tesseract 5.x (via pytesseract)

| Aspect | Details |
|--------|---------|
| **Size** | ~30MB (eng + basic deps), ~50MB with common languages |
| **Accuracy** | Good on clean printed text (≥95% CER on documents/screenshots) |
| **Speed** | Fast — 0.5–3s for standard images |
| **Languages** | 100+ language packs available, loaded on demand |
| **Windows support** | Well-supported via pre-built binaries, chocolatey, or bundled |
| **License** | Apache 2.0 |
| **Deps weight** | `pytesseract` + `Pillow` + Tesseract binary (~25MB total Python deps) |

**Decision**: Use Tesseract as the primary OCR engine for v1.

**Rationale**: Smallest footprint (fits easily within 100MB budget), excellent
accuracy for printed text / screenshots (the primary use case), mature Windows
support, on-demand language pack loading.

### PaddleOCR

| Aspect | Details |
|--------|---------|
| **Size** | ~100MB+ (model + deps), lighter `paddleocr` package available |
| **Accuracy** | Better on handwriting, curved text, non-English scripts |
| **Speed** | Moderate — 1–5s per image (GPU optional, CPU default) |
| **Windows support** | Good, but requires more setup |
| **License** | Apache 2.0 |

**Decision**: Not for v1. Re-evaluate if OCR accuracy targets cannot be met
with Tesseract for specific use cases (handwriting, Arabic/Darija script).

### EasyOCR

| Aspect | Details |
|--------|---------|
| **Size** | ~80MB base (model), grows per additional language |
| **Accuracy** | Comparable to Tesseract on printed text, better on some non-Latin scripts |
| **Speed** | Moderate |
| **Windows support** | Good |

**Decision**: Not for v1. Falls between Tesseract and PaddleOCR — not
lightweight enough to beat Tesseract, not accurate enough to beat PaddleOCR.

## Global Hotkey Implementation (Windows)

| Approach | Admin Required | Reliability | Dep Size |
|----------|---------------|-------------|----------|
| `keyboard` library | Yes (on Win 10+) | Good | ~150KB |
| `pynput` | No | Good (event-driven) | ~100KB |
| Win32 API via `ctypes` | No | Excellent (native) | 0 (stdlib) |
| `system_hotkey` | No | Moderate | ~30KB |

**Decision**: Use Win32 API via `ctypes` (zero-dependency, most reliable,
no admin required).

**Rationale**: Aligns with constitution principle II (Lightweight) by adding
zero storage overhead, and principle V (Simplicity) by using the native API
directly instead of wrapping it in a library.

**Implementation pattern**: Register `RegisterHotKey` with `MOD_CONTROL |
MOD_NOREPEAT` + `VK_O` → listen via `GetMessage` in a background thread.

## System Tray Implementation

| Approach | Dep Size | Notes |
|----------|----------|-------|
| `pystray` | ~60KB | Cross-platform, PIL-based icon |
| `infi.systray` | ~40KB | Windows-only, lightweight |
| Win32 API via `ctypes` | 0 | Full control, zero deps |

**Decision**: Use `pystray` for v1. It's well-maintained, cross-platform
(if we ever want Linux/macOS), and lightweight at ~60KB.

**Fallback**: If cross-platform not needed, Win32 API via `ctypes` is the
constitution-preferred zero-dep approach.

## Clipboard Access

| Approach | Dep Size | Notes |
|----------|----------|-------|
| `PIL.ImageGrab` | included w/ Pillow | Can grab clipboard as image directly |
| `pyperclip` | ~20KB | Text clipboard (for copying results back) |
| `win32clipboard` via `ctypes` | 0 | Native, reliable |

**Decision**: Use `PIL.ImageGrab.grabclipboard()` for image retrieval
(Pillow is already a Tesseract dependency) + `pyperclip` for copying
text results back to clipboard.

## Image Preprocessing

For optimal Tesseract accuracy, apply these preprocessing steps:

- Convert to grayscale
- Binarize (Otsu's threshold or adaptive threshold)
- Deskew (rotate to horizontal)
- Denoise (median/blur filter)
- Resize if too small (<300 DPI effective)

**Libraries**: All achievable with `Pillow` + `numpy` (numpy is a ~15MB dep
but widely useful). If we can avoid numpy, use `Pillow` alone for basic ops.

## Image Captioning (P2 — `--describe`)

| Model | Size | CPU Speed | Accuracy |
|-------|------|-----------|----------|
| BLIP-2 (base) | ~1.2GB | Slow | Excellent |
| Florence-2 (base) | ~350MB | Moderate | Very good |
| Moondream 2 | ~200MB | Fast (1.3B params) | Good for basic description |
| API-based (GPT-4V, Claude) | 0 | Fast | Best quality, requires internet |

**Decision**: Defer to v2. For v1, the `--describe` flag returns a clear
message: "Image description requires additional model download (~200MB).
Run `odOcr --install-describe` to enable." This keeps v1 within budget.

**If implemented in v2**: Moondream 2 is the best accuracy-to-size ratio
at ~200MB. It runs on CPU, is Apache 2.0 licensed, and handles general
image captioning well.

## Language Support

Tesseract supports on-demand language pack downloads:

| Language | Pack Size | Notes |
|----------|-----------|-------|
| English (eng) | ~2MB | Bundled by default |
| French (fra) | ~3MB | Optional install |
| Arabic (ara) | ~2MB | Optional (relevant for Darija/Arabic users) |
| Spanish (spa) | ~3MB | Optional install |

**Decision**: Bundle only `eng` in the base install (~2MB). Additional
languages installed on demand via `odOcr --install-lang <code>`.

## Storage Budget Breakdown

| Component | Size |
|-----------|------|
| Python runtime (embedded or system) | 0 (user's Python or bundled) |
| Tesseract binary | ~25MB |
| English language pack | ~2MB |
| Python deps (pytesseract, Pillow, pystray, pyperclip) | ~15MB |
| odOcr source + assets | ~1MB |
| **Total base** | **~43MB** |
| Headroom for growth | ~57MB |
| **Budget** | **100MB** (per constitution) |

## Technology Stack Decision

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Language | Python 3.10+ | Best OCR lib ecosystem, cross-platform, rapid dev |
| OCR Engine | Tesseract 5.x | Lightweight, accurate for printed text, mature |
| CLI Framework | `argparse` (stdlib) | Zero-dependency, constitution-compliant (lightweight) |
| Image Processing | Pillow | Already a Tesseract dependency, sufficient for preprocessing |
| System Tray | pystray | ~60KB, cross-platform |
| Global Hotkey | Win32 API via ctypes | Zero-dependency, most reliable on Windows |
| Clipboard (read) | Pillow.ImageGrab | Zero additional deps |
| Clipboard (write) | pyperclip | ~20KB, reliable text clipboard writing |
| Testing | pytest + pytest-mock | Industry standard for Python |
| Packaging | PyInstaller | Bundles Python + deps into single .exe |
