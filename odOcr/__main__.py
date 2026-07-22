import sys
import time
import threading
from pathlib import Path

from .cli import parse_args
from .config import load_config, save_config
from .clipboard import grab_image_from_clipboard, open_image_from_file, copy_text_to_clipboard
from .ocr import extract_text, install_language
from .output import format_text_output, format_json_output, print_help, print_version
from .hotkey import HotkeyListener
from .tray import run_tray
from .models import OCRResult


def main():
    args = parse_args()

    if args.action == "help":
        print(print_help())
        return

    if args.action == "version":
        print(print_version())
        return

    config = load_config()

    if args.language:
        config.language = args.language

    if args.json:
        config.output_format = "json"

    if args.describe:
        config.describe = True

    if args.action == "install_lang":
        result = install_language(args.install_lang)
        print(result)
        if args.install_lang not in config.installed_languages:
            config.installed_languages.append(args.install_lang)
            save_config(config)
        return

    if args.action == "install_describe":
        print(
            "Image description model download is not available in v0.1.0.\n"
            "This feature will be available in a future release.\n"
            "For now, use --describe to enable the feature (requires model)."
        )
        return

    if args.action == "hotkey":
        run_hotkey_mode(config)
        return

    if args.action == "ocr":
        run_single_ocr(args, config)
        return


def run_single_ocr(args, config):
    img_source = None
    if args.file:
        img_source = open_image_from_file(args.file)
        if img_source is None:
            result = OCRResult.error_result(
                f"Cannot open file: {args.file}", 2
            )
            _output_result(result, config)
            sys.exit(2)
    else:
        img_source = grab_image_from_clipboard()
        if img_source is None:
            result = OCRResult.error_result(
                "No image found in clipboard. "
                "Copy an image first or provide a file path.", 2
            )
            _output_result(result, config)
            sys.exit(2)

    from PIL import Image
    import io
    pil_img = Image.open(io.BytesIO(img_source.raw_data))
    result = extract_text(pil_img, language=config.language,
                          describe=config.describe)
    result.source = img_source.type.value

    if result.success and config.auto_copy and result.text:
        copy_text_to_clipboard(result.text)

    _output_result(result, config)

    if not result.success:
        sys.exit(result.error_code or 1)


def _output_result(result: OCRResult, config):
    if config.output_format == "json":
        print(result.to_json())
    else:
        print(format_text_output(result))
        if result.success and config.auto_copy and result.text:
            print("\n(Copied to clipboard)")


def run_hotkey_mode(config):
    stop_event = threading.Event()
    tray_icon_ref = []

    def do_ocr():
        try:
            img_source = grab_image_from_clipboard()
            if img_source is None:
                _notify(tray_icon_ref, "odOcr",
                        "No image found in clipboard. Copy an image first.")
                return

            from PIL import Image
            import io
            pil_img = Image.open(io.BytesIO(img_source.raw_data))
            result = extract_text(pil_img, language=config.language,
                                  describe=config.describe)

            if result.success and config.auto_copy and result.text:
                copy_text_to_clipboard(result.text)

            if result.success:
                preview = result.text[:100] + "..." if len(result.text) > 100 else result.text
                _notify(tray_icon_ref, "odOcr - Text Extracted", preview)
            else:
                _notify(tray_icon_ref, "odOcr", result.error or "No text detected")
        except Exception as e:
            _notify(tray_icon_ref, "odOcr Error", str(e))

    def on_exit():
        stop_event.set()
        if hotkey_listener:
            hotkey_listener.stop()

    hotkey_listener = HotkeyListener(do_ocr)
    hotkey_listener.start()

    print("odOcr running in background.")
    print("  • Click tray icon → OCR clipboard")
    print("  • Press Ctrl+O    → OCR clipboard")
    print("  • Right-click tray → Exit")

    tray_thread = threading.Thread(
        target=lambda: _run_tray_with_ref(tray_icon_ref, do_ocr, on_exit),
        daemon=True
    )
    tray_thread.start()

    try:
        while not stop_event.is_set():
            stop_event.wait(1)
    except KeyboardInterrupt:
        pass
    finally:
        hotkey_listener.stop()


def _run_tray_with_ref(tray_icon_ref, do_ocr, on_exit):
    from .tray import run_tray
    import pystray

    original_run = run_tray

    def wrapped_run(ocr_cb, exit_cb):
        from .tray import create_default_icon

        icon_image = create_default_icon()

        def on_run_ocr(icon, item):
            ocr_cb()

        def on_quit(icon, item):
            icon.stop()
            exit_cb()

        def on_click(icon, button):
            if button == pystray.Button.LEFT:
                ocr_cb()

        menu = pystray.Menu(
            pystray.MenuItem("Run OCR Now", on_run_ocr, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("odOcr v0.1.0", None, enabled=False),
            pystray.MenuItem("Exit", on_quit),
        )

        icon = pystray.Icon("odOcr", icon_image, "odOcr", menu)
        icon.on_activate = on_click
        tray_icon_ref.append(icon)
        icon.run()

    wrapped_run(do_ocr, on_exit)


def _notify(tray_icon_ref, title, message):
    if tray_icon_ref:
        try:
            tray_icon_ref[0].notify(message, title)
            return
        except Exception:
            pass
    print(f"[{title}] {message}")


if __name__ == "__main__":
    main()
