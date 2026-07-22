import threading
from PIL import Image, ImageDraw, ImageFont


def create_default_icon(size=(64, 64)) -> Image.Image:
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    w, h = size
    margin = w // 8

    draw.rounded_rectangle(
        [margin, margin, w - margin, h - margin],
        radius=6,
        fill=(74, 108, 247, 255),
        outline=(50, 80, 200, 255),
        width=2,
    )

    cx, cy = w // 2, h // 2 - 2
    try:
        font = ImageFont.truetype("segoeui.ttf", size=w // 2)
    except Exception:
        font = ImageFont.load_default()

    draw.text((cx - 3, cy - 8), "O", fill="white", font=font)

    r = w // 5
    draw.ellipse(
        [cx + r - 2, cy + r - 2, cx + r + 8, cy + r + 8],
        fill=(74, 108, 247, 0),
        outline=(200, 200, 200, 255),
        width=3,
    )

    return img


def run_tray(on_ocr, on_exit):
    import pystray

    icon_image = create_default_icon()

    def on_run_ocr(icon, item):
        if on_ocr:
            on_ocr()

    def on_quit(icon, item):
        icon.stop()
        if on_exit:
            on_exit()

    def on_click(icon, button):
        if button == pystray.Button.LEFT and on_ocr:
            on_ocr()

    menu = pystray.Menu(
        pystray.MenuItem("Run OCR Now", on_run_ocr, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("odOcr v0.1.0", None, enabled=False),
        pystray.MenuItem("Exit", on_quit),
    )

    icon = pystray.Icon("odOcr", icon_image, "odOcr", menu)
    icon.on_activate = on_click
    icon.run()
