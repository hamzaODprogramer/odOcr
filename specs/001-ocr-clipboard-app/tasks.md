---

description: "Task list for odOcr OCR Clipboard Desktop App"
---

# Tasks: OCR Clipboard Desktop App

**Input**: Design documents from specs/001-ocr-clipboard-app/

**Organization**: Tasks grouped by phase. [P] = can run in parallel.

## Phase 1: Setup (Shared Infrastructure)

- [X] T001 Create project structure: src/, tests/, assets/ directories
- [X] T002 Create pyproject.toml with dependencies (pytesseract, Pillow, pystray, pyperclip)
- [X] T003 [P] Create .gitignore with Python patterns
- [X] T004 [P] Create assets/icon.png (simple tray icon placeholder)

---

## Phase 2: Core Library Modules

- [X] T005 Create src/models.py - OCRResult, AppConfig dataclasses
- [X] T006 Create src/config.py - config file load/save from ~/.odOcr/config.json
- [X] T007 Create src/image.py - image preprocessing (grayscale, binarize, deskew, denoise)
- [X] T008 Create src/ocr.py - Tesseract OCR wrapper via pytesseract
- [X] T009 Create src/clipboard.py - clipboard read (PIL.ImageGrab) and write (pyperclip)
- [X] T010 Create src/output.py - text and JSON output formatting

---

## Phase 3: CLI & Background Process

- [X] T011 Create src/cli.py - argparse CLI with all flags per CLI contract
- [X] T012 Create src/hotkey.py - Win32 API global hotkey via ctypes (Ctrl+O)
- [X] T013 Create src/tray.py - system tray icon via pystray
- [X] T014 Create src/__main__.py - entry point wiring CLI -> OCR pipeline

---

## Phase 4: Tests

- [X] T015 [P] Create tests/test_models.py - dataclass and config tests
- [X] T016 [P] Create tests/test_image.py - preprocessing tests
- [X] T017 [P] Create tests/test_ocr.py - OCR engine tests (mocked Tesseract)
- [X] T018 [P] Create tests/test_cli.py - argument parsing tests
- [X] T019 [P] Create tests/test_output.py - output formatting tests

---

## Phase 5: Integration & Polish

- [X] T020 Create setup.py / pyproject.toml entry point for `odOcr` command
- [X] T021 Verify end-to-end: `odOcr` with image, `odOcr --hotkey`, `odOcr --json`
