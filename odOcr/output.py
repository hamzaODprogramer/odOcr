import json

from .models import OCRResult


def format_text_output(result: OCRResult) -> str:
    if not result.success:
        return f"Error: {result.error}"

    lines = []
    lines.append("OCR Result")
    lines.append("-" * 40)
    if result.text:
        lines.append("")
        lines.append(result.text)
        lines.append("")
    lines.append("-" * 40)
    lines.append(f"Confidence: {result.confidence:.0%}")
    lines.append(f"Language: {result.language}")
    lines.append(f"Time: {result.processing_time_ms}ms")

    if result.description:
        lines.append("")
        lines.append(f"Image description: {result.description}")

    return "\n".join(lines)


def format_json_output(result: OCRResult) -> str:
    return json.dumps(result.to_dict(), indent=2, ensure_ascii=False)


def print_help() -> str:
    return """Usage: odOcr [file] [options]

Extract text from images using OCR. Reads from clipboard or file.

Arguments:
  file              Path to image file (omit to use clipboard)

Options:
  -h, --help        Show this help message
  -j, --json        Output as JSON
  -d, --describe    Enable image content description
  -l, --language    OCR language(s), comma-separated (default: eng)
  --hotkey          Run as background process with Ctrl+O
  -q, --quiet       Suppress non-essential output
  -v, --version     Show version
  --install-lang    Install an OCR language pack
  --install-describe  Download image description model
  --config          Path to config file (default: ~/.odOcr/config.json)

Examples:
  odOcr                     OCR from clipboard
  odOcr image.png           OCR from file
  odOcr --json              JSON output from clipboard
  odOcr --language ara      OCR with Arabic language
  odOcr --hotkey            Run in background with Ctrl+O
"""


def print_version() -> str:
    return "odOcr version 0.1.0"
