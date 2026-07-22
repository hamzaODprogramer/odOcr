from typing import Optional

from PIL import Image, ImageGrab

from .models import ImageSource, ImageSourceType


def grab_image_from_clipboard() -> Optional[ImageSource]:
    try:
        img = ImageGrab.grabclipboard()
        if img is None:
            return None
        if isinstance(img, Image.Image):
            import io
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return ImageSource(
                type=ImageSourceType.CLIPBOARD,
                raw_data=buf.getvalue(),
                format="PNG",
                size_bytes=buf.tell(),
            )
        if isinstance(img, list):
            return None
        return None
    except Exception:
        return None


def open_image_from_file(path: str) -> Optional[ImageSource]:
    try:
        from PIL import Image as PILImage
        pil_img = PILImage.open(path)
        pil_img.load()
        import io
        buf = io.BytesIO()
        pil_img.save(buf, format=pil_img.format or "PNG")
        return ImageSource(
            type=ImageSourceType.FILE,
            path=path,
            raw_data=buf.getvalue(),
            format=pil_img.format or "PNG",
            size_bytes=buf.tell(),
        )
    except Exception:
        return None


def copy_text_to_clipboard(text: str) -> bool:
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except Exception:
        return False
