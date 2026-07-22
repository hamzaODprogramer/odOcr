import os
import time
from pathlib import Path
from typing import Optional

import pytesseract
from pytesseract.pytesseract import TesseractNotFoundError
from PIL import Image

from .image import preprocess, resize_if_needed
from .models import OCRResult


_LOCATIONS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
]

def _locate_tesseract() -> str:
    env = os.environ.get("TESSERACT_PATH") or os.environ.get("TESSDATA_PREFIX")
    if env:
        candidate = Path(env) / "tesseract.exe" if Path(env).is_dir() else Path(env)
        if candidate.is_file():
            return str(candidate.resolve())
    for loc in _LOCATIONS:
        if Path(loc).is_file():
            return loc
    return "tesseract"

tesseract_cmd = _locate_tesseract()
if Path(tesseract_cmd).is_file():
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd


def extract_text(image: Image.Image, language: str = "eng",
                 describe: bool = False) -> OCRResult:
    start = time.perf_counter()
    source_desc = "image"

    try:
        processed = preprocess(image)
        processed = resize_if_needed(processed)
        data = pytesseract.image_to_data(
            processed, lang=language, output_type=pytesseract.Output.DICT
        )
        elapsed = int((time.perf_counter() - start) * 1000)

        text_parts = []
        confidences = []
        for i, text in enumerate(data["text"]):
            text = text.strip()
            if text and int(data["conf"][i]) > 0:
                text_parts.append(text)
                confidences.append(int(data["conf"][i]))

        text = " ".join(text_parts)
        avg_confidence = (sum(confidences) / len(confidences) / 100.0
                          if confidences else 0.0)

        if not text:
            return OCRResult(
                success=False,
                text=None,
                confidence=0.0,
                language=language,
                processing_time_ms=elapsed,
                source=source_desc,
                error="No text detected in the image",
                error_code=1,
            )

        return OCRResult(
            success=True,
            text=text,
            confidence=round(avg_confidence, 2),
            language=language,
            processing_time_ms=elapsed,
            source=source_desc,
        )

    except TesseractNotFoundError:
        elapsed = int((time.perf_counter() - start) * 1000)
        return OCRResult.error_result(
            "Tesseract is not installed or not in PATH. "
            "Install Tesseract OCR from https://github.com/UB-Mannheim/tesseract/wiki",
            3, elapsed
        )
    except Exception as e:
        elapsed = int((time.perf_counter() - start) * 1000)
        return OCRResult.error_result(
            f"OCR processing failed: {str(e)}", 3, elapsed
        )


def get_tesseract_languages() -> list:
    try:
        return pytesseract.get_languages()
    except Exception:
        return ["eng"]


def install_language(lang_code: str) -> str:
    from .config import LANGUAGES_DIR
    msg = (
        f"Language pack '{lang_code}' cannot be auto-downloaded in this version.\n"
        f"To install manually:\n"
        f"  1. Download {lang_code}.traineddata from "
        f"https://github.com/tesseract-ocr/tessdata\n"
        f"  2. Place it in your Tesseract tessdata directory\n"
        f"  3. Run: odOcr --language {lang_code}"
    )
    return msg
