import json
import pytest
from odOcr.models import OCRResult, AppConfig, ImageSource, ImageSourceType


class TestOCRResult:
    def test_success_result(self):
        r = OCRResult(success=True, text="hello", confidence=0.95,
                      processing_time_ms=100, source="clipboard")
        assert r.success
        assert r.text == "hello"
        assert r.confidence == 0.95
        assert r.processing_time_ms == 100

    def test_error_result(self):
        r = OCRResult.error_result("test error", 2, 50)
        assert not r.success
        assert r.error == "test error"
        assert r.error_code == 2
        assert r.processing_time_ms == 50

    def test_to_dict(self):
        r = OCRResult(success=True, text="hello", confidence=0.95,
                      processing_time_ms=100, source="clipboard")
        d = r.to_dict()
        assert d["success"] is True
        assert d["text"] == "hello"
        assert d["confidence"] == 0.95

    def test_to_json(self):
        r = OCRResult(success=True, text="hello", confidence=0.95,
                      processing_time_ms=100, source="clipboard")
        j = r.to_json()
        d = json.loads(j)
        assert d["text"] == "hello"


class TestAppConfig:
    def test_defaults(self):
        c = AppConfig()
        assert c.hotkey == "ctrl+o"
        assert c.language == "eng"
        assert c.describe is False
        assert c.auto_copy is True
        assert c.installed_languages == ["eng"]

    def test_custom(self):
        c = AppConfig(hotkey="ctrl+shift+o", language="fra",
                      describe=True, auto_copy=False)
        assert c.hotkey == "ctrl+shift+o"
        assert c.language == "fra"
        assert c.describe is True
        assert c.auto_copy is False


class TestImageSource:
    def test_clipboard_source(self):
        s = ImageSource(type=ImageSourceType.CLIPBOARD,
                        raw_data=b"fake", format="PNG", size_bytes=4)
        assert s.type == ImageSourceType.CLIPBOARD
        assert s.format == "PNG"
        assert s.size_bytes == 4

    def test_file_source(self):
        s = ImageSource(type=ImageSourceType.FILE, path="/test.png")
        assert s.type == ImageSourceType.FILE
        assert s.path == "/test.png"
