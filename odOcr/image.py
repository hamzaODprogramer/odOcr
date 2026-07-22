from PIL import Image, ImageFilter, ImageOps


def preprocess(image: Image.Image) -> Image.Image:
    img = image.convert("L")
    img = _denoise(img)
    img = _enhance_contrast(img)
    return img


def _enhance_contrast(image: Image.Image) -> Image.Image:
    try:
        import numpy as np
        arr = np.array(image, dtype=np.uint8)
        non_white = arr[arr < 255]
        if len(non_white) < 10:
            return image
        p2, p98 = np.percentile(non_white, (2, 98))
        if p98 > p2:
            stretched = np.clip((arr - p2) * 255.0 / (p98 - p2), 0, 255).astype(np.uint8)
            return Image.fromarray(stretched, mode="L")
    except ImportError:
        pass
    return image


def _denoise(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.MedianFilter(size=3))


def resize_if_needed(image: Image.Image, max_pixels: int = 4000) -> Image.Image:
    w, h = image.size
    if w * h > max_pixels * max_pixels:
        ratio = max_pixels / max(w, h)
        new_w = int(w * ratio)
        new_h = int(h * ratio)
        return image.resize((new_w, new_h), Image.Resampling.LANCZOS)
    return image


def get_image_format(image: Image.Image) -> str:
    return image.format or "PNG"
