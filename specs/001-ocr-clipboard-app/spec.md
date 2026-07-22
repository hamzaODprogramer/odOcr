# Feature Specification: OCR Clipboard Desktop App

**Feature Branch**: `001-ocr-clipboard-app`

**Created**: 2026-07-22

**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Paste-and-OCR from Clipboard (Priority: P1)

A user copies an image containing text to the clipboard (screenshot, scanned document, photo of text), presses the shortcut key, and receives the extracted text immediately.

**Why this priority**: This is the core use case — image-to-text extraction is the primary reason for the app's existence. Everything else is additive.

**Independent Test**: Can be fully tested by copying any image with text to the clipboard, triggering OCR, and verifying that the extracted text matches the visible text in the image.

**Acceptance Scenarios**:

1. **Given** the odOcr app is running in the background, **When** the user copies an image containing printed text to the clipboard and presses Ctrl+O, **Then** the extracted text is copied to the clipboard and displayed in a popup notification.
2. **Given** the odOcr app is running, **When** the user copies a screenshot of a document to the clipboard and runs `odOcr` from the terminal, **Then** the extracted text is printed to stdout.
3. **Given** the clipboard contains a non-image item (text, file, etc.), **When** the user triggers OCR, **Then** the app shows a clear error message saying no image was found in the clipboard.

---

### User Story 2 - Image Content Description (Priority: P2)

A user copies an image that may or may not contain text and wants a brief description of what the image shows, in addition to any extracted text.

**Why this priority**: This extends OCR into image understanding, adding significant value for accessibility and content discovery, but it is optional ("if possible") per the user.

**Independent Test**: Can be tested by copying an image with both text and visual content (e.g., a meme or infographic), triggering OCR with description mode, and verifying that both extracted text and a meaningful description are returned.

**Acceptance Scenarios**:

1. **Given** the user has enabled image description mode, **When** they trigger OCR on an image containing text and visual content, **Then** the output includes both the extracted text and a short natural-language description of the image content.
2. **Given** image description mode is enabled, **When** the image contains no legible text (e.g., a photo of a landscape), **Then** the output contains only the image description with a note that no text was found.
3. **Given** image description mode is disabled (default), **When** the user triggers OCR, **Then** only extracted text is returned — no image description is generated.

---

### User Story 3 - Terminal CLI Workflow (Priority: P1)

A user runs `odOcr` from the terminal with an image file path or piped input and receives extracted text directly in the console.

**Why this priority**: Terminal access is explicitly required ("the app should run from terminal using 'odOcr'") and aligns with the constitution's CLI-First principle. Both this and User Story 1 are P1 because they serve different primary workflows.

**Independent Test**: Can be tested by running `odOcr path\to\image.png` and verifying text is output to stdout, or running `odOcr` without arguments and seeing help text.

**Acceptance Scenarios**:

1. **Given** an image file exists at a known path, **When** the user runs `odOcr path\to\image.png`, **Then** the extracted text is printed to stdout.
2. **Given** no arguments are provided, **When** the user runs `odOcr`, **Then** usage help text is displayed showing available commands and options.
3. **Given** the `--describe` flag is passed, **When** the user runs `odOcr --describe path\to\image.png`, **Then** both extracted text and an image description are printed to stdout.
4. **Given** an invalid file path is provided, **When** the user runs `odOcr nonexistent.png`, **Then** a clear error message is printed to stderr and the exit code is non-zero.

### Edge Cases

- Clipboard contains a corrupted or unreadable image format — system shows a descriptive error.
- Image is very large (high resolution) — OCR runs within reasonable time (<10 seconds) or the user is informed of progress.
- Image contains no text at all — system returns empty text with a note that no text was detected.
- Multiple text regions in one image (e.g., multi-column document) — all text is extracted and combined in reading order.
- Clipboard is empty when shortcut is pressed — system notifies the user that clipboard is empty.
- The `odOcr` command conflicts with an existing system command — installer should confirm before adding to PATH.
- Image description requires downloading a model — user is informed of the download progress and storage impact.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST extract text from image data retrieved from the system clipboard.
- **FR-002**: System MUST print extracted text to stdout when invoked via terminal.
- **FR-003**: System MUST copy the extracted text to the system clipboard after a shortcut-triggered OCR.
- **FR-004**: System MUST register a global hotkey (Ctrl+O) that triggers OCR on the current clipboard contents.
- **FR-005**: System MUST support running as a background process (system tray) for hotkey-based workflows.
- **FR-006**: System MUST accept image file paths as CLI arguments: `odOcr <file-path>`.
- **FR-007**: System MUST display usage/help text when `odOcr` is run without arguments, showing all flags and options.
- **FR-008**: System MUST provide a `--describe` flag to enable image content description alongside text extraction.
- **FR-009**: System MUST gracefully handle non-image clipboard content with a user-friendly error message.
- **FR-010**: System MUST output errors to stderr and use non-zero exit codes for failures.
- **FR-011**: System MUST support JSON output format (`--json` flag) for programmatic consumption.
- **FR-012**: System MUST clean up temporary files created during OCR processing.

### Key Entities *(include if feature involves data)*

- **ImageSource**: The source of an image for OCR — can be the system clipboard or a file path.
- **OCRResult**: The output of OCR processing — contains extracted text, optional image description, processing metadata (confidence score, processing time).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can extract text from a clipboard image with a single keystroke (Ctrl+O) in under 5 seconds for standard images (up to 4K resolution).
- **SC-002**: The terminal command `odOcr <file>` returns extracted text to stdout within 10 seconds for images up to 10MB.
- **SC-003**: 95% of standard printed-text images (clean documents, screenshots) return text with less than 5% character error rate.
- **SC-004**: The application's total disk footprint (installation + default models) does not exceed 100MB in its base (OCR-only) configuration.
- **SC-005**: The background process (system tray) consumes less than 50MB of RAM when idle.

## Assumptions

- The primary target platform is Windows (matching the user's environment and clipboard API).
- The app will run in the background as a system tray application for hotkey-based workflows.
- The OCR engine will support English text extraction by default; additional languages will be an optional install to minimize storage footprint.
- Image description capability will use a local lightweight model rather than an online API, to keep the app offline-capable and preserve privacy.
- The `odOcr` command will be added to the system PATH during installation for terminal access.
- Ctrl+O is the default hotkey; users may configure it later but this is not a v1 requirement.
- Source code will be written in a language with good clipboard API support and cross-platform potential (Windows focus for v1).
