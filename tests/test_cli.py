import pytest
from odOcr.cli import build_parser, parse_args


class TestCliParsing:
    def test_default_action(self):
        args = parse_args([])
        assert args.action == "ocr"
        assert args.file is None

    def test_file_argument(self):
        args = parse_args(["test.png"])
        assert args.action == "ocr"
        assert args.file == "test.png"

    def test_json_flag(self):
        args = parse_args(["--json"])
        assert args.json is True
        assert args.action == "ocr"

    def test_describe_flag(self):
        args = parse_args(["--describe"])
        assert args.describe is True

    def test_help_action(self):
        args = parse_args(["--help"])
        assert args.action == "help"

    def test_version_action(self):
        args = parse_args(["--version"])
        assert args.action == "version"

    def test_hotkey_action(self):
        args = parse_args(["--hotkey"])
        assert args.action == "hotkey"

    def test_install_lang(self):
        args = parse_args(["--install-lang", "ara"])
        assert args.action == "install_lang"
        assert args.install_lang == "ara"

    def test_language_option(self):
        args = parse_args(["-l", "fra"])
        assert args.language == "fra"

    def test_quiet_mode(self):
        args = parse_args(["-q"])
        assert args.quiet is True

    def test_file_with_flags(self):
        args = parse_args(["doc.png", "--json", "--quiet"])
        assert args.file == "doc.png"
        assert args.json is True
        assert args.quiet is True

    def test_stdin_dash(self):
        args = parse_args(["-"])
        assert args.action == "stdin"
        assert args.file == "-"
