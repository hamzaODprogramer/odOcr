from dataclasses import dataclass, field, asdict
from typing import Optional
from enum import Enum


class ImageSourceType(Enum):
    CLIPBOARD = "clipboard"
    FILE = "file"
    STDIN = "stdin"


class OutputFormat(Enum):
    TEXT = "text"
    JSON = "json"


class DarkMode(Enum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


@dataclass
class ImageSource:
    type: ImageSourceType
    path: Optional[str] = None
    raw_data: Optional[bytes] = None
    format: Optional[str] = None
    size_bytes: int = 0


@dataclass
class OCRResult:
    success: bool
    text: Optional[str] = None
    confidence: float = 0.0
    language: str = "eng"
    processing_time_ms: int = 0
    source: str = ""
    description: Optional[str] = None
    error: Optional[str] = None
    error_code: Optional[int] = None

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        import json
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    @staticmethod
    def error_result(error: str, error_code: int,
                     processing_time_ms: int = 0) -> "OCRResult":
        return OCRResult(
            success=False,
            error=error,
            error_code=error_code,
            processing_time_ms=processing_time_ms,
        )


@dataclass
class AppConfig:
    hotkey: str = "ctrl+o"
    output_format: str = "text"
    describe: bool = False
    language: str = "eng"
    dark_mode: str = "system"
    auto_copy: bool = True
    installed_languages: list = field(default_factory=lambda: ["eng"])
    describe_model_installed: bool = False
