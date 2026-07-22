import json
import pytest
from odOcr.models import OCRResult
from odOcr.output import format_text_output, format_json_output, print_help, print_version


class TestFormatTextOutput:
    def test_success(self):
        r = OCRResult(success=True, text="Hello World",
                      confidence=0.95, processing_time_ms=100,
                      source="clipboard")
        out = format_text_output(r)
        assert "Hello World" in out
        assert "95%" in out
        assert "100ms" in out

    def test_error(self):
        r = OCRResult.error_result("test error", 1)
        out = format_text_output(r)
        assert "Error: test error" in out

    def test_with_description(self):
        r = OCRResult(success=True, text="Hello",
                      confidence=0.9, processing_time_ms=50,
                      source="file", description="A document")
        out = format_text_output(r)
        assert "Image description: A document" in out


class TestFormatJsonOutput:
    def test_valid_json(self):
        r = OCRResult(success=True, text="Hello",
                      confidence=0.95, processing_time_ms=100,
                      source="clipboard")
        j = format_json_output(r)
        d = json.loads(j)
        assert d["text"] == "Hello"
        assert d["confidence"] == 0.95

    def test_error_json(self):
        r = OCRResult.error_result("failed", 2)
        j = format_json_output(r)
        d = json.loads(j)
        assert d["success"] is False
        assert d["error"] == "failed"


class TestHelp:
    def test_help_contains_usage(self):
        h = print_help()
        assert "Usage:" in h
        assert "odOcr" in h

    def test_version(self):
        v = print_version()
        assert "odOcr" in v
        assert "0.1.0" in v
