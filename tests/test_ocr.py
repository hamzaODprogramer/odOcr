import pytest
from unittest.mock import patch, MagicMock
from PIL import Image

from odOcr.ocr import extract_text, get_tesseract_languages


class TestExtractText:
    @patch("odOcr.ocr.pytesseract")
    def test_successful_extraction(self, mock_tesseract):
        mock_tesseract.image_to_data.return_value = {
            "text": ["Hello", "World", ""],
            "conf": [95, 90, 0],
        }
        img = Image.new("RGB", (100, 100))
        result = extract_text(img)

        assert result.success
        assert result.text == "Hello World"
        assert result.confidence == 0.93
        assert result.language == "eng"

    @patch("odOcr.ocr.pytesseract")
    def test_no_text_found(self, mock_tesseract):
        mock_tesseract.image_to_data.return_value = {
            "text": ["", "", ""],
            "conf": [0, 0, 0],
        }
        img = Image.new("RGB", (100, 100))
        result = extract_text(img)

        assert not result.success
        assert result.text is None
        assert result.error_code == 1

    @patch("odOcr.ocr.pytesseract")
    def test_tesseract_not_found(self, mock_tesseract):
        mock_tesseract.image_to_data.side_effect = (
            __import__("pytesseract").TesseractNotFoundError()
        )
        img = Image.new("RGB", (100, 100))
        result = extract_text(img)

        assert not result.success
        assert result.error_code == 3
        assert "Tesseract is not installed" in result.error

    @patch("odOcr.ocr.pytesseract")
    def test_general_error(self, mock_tesseract):
        mock_tesseract.image_to_data.side_effect = RuntimeError("engine crash")
        img = Image.new("RGB", (100, 100))
        result = extract_text(img)

        assert not result.success
        assert result.error_code == 3


class TestGetTesseractLanguages:
    @patch("odOcr.ocr.pytesseract")
    def test_success(self, mock_tesseract):
        mock_tesseract.get_languages.return_value = ["eng", "fra", "ara"]
        langs = get_tesseract_languages()
        assert "eng" in langs
        assert "fra" in langs
