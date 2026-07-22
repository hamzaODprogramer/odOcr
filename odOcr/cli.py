import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="odOcr",
        description="Extract text from images using OCR. Reads from clipboard or file.",
        add_help=False,
    )

    parser.add_argument("file", nargs="?", default=None,
                        help="Path to image file (omit to use clipboard)")
    parser.add_argument("-h", "--help", action="store_true",
                        help="Show this help message")
    parser.add_argument("-j", "--json", action="store_true",
                        help="Output as JSON")
    parser.add_argument("-d", "--describe", action="store_true",
                        help="Enable image content description")
    parser.add_argument("-l", "--language", default=None,
                        help="OCR language(s), comma-separated (default: eng)")
    parser.add_argument("--hotkey", action="store_true",
                        help="Run as background process with Ctrl+O")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress non-essential output")
    parser.add_argument("-v", "--version", action="store_true",
                        help="Show version")
    parser.add_argument("--install-lang", default=None, metavar="CODE",
                        help="Install an OCR language pack")
    parser.add_argument("--install-describe", action="store_true",
                        help="Download image description model")
    parser.add_argument("--config", default=None,
                        help="Path to config file (default: ~/.odOcr/config.json)")

    return parser


def parse_args(argv=None) -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.help:
        args.action = "help"
    elif args.version:
        args.action = "version"
    elif args.install_lang:
        args.action = "install_lang"
    elif args.install_describe:
        args.action = "install_describe"
    elif args.hotkey:
        args.action = "hotkey"
    elif args.file == "-":
        args.action = "stdin"
    else:
        args.action = "ocr"

    return args
