import pytest
from PIL import Image, ImageDraw

from odOcr.image import preprocess, resize_if_needed


class TestPreprocess:
    def test_returns_image(self):
        img = Image.new("RGB", (100, 100), color="white")
        result = preprocess(img)
        assert isinstance(result, Image.Image)

    def test_grayscale_output(self):
        img = Image.new("RGB", (100, 100), color="blue")
        result = preprocess(img)
        assert result.mode == "L"

    def test_grayscale_values(self):
        img = Image.new("RGB", (100, 100), color="white")
        result = preprocess(img)
        assert result.mode == "L"
        w, h = result.size
        assert w > 0 and h > 0


class TestResize:
    def test_small_image_unchanged(self):
        img = Image.new("RGB", (100, 100))
        result = resize_if_needed(img, max_pixels=4000)
        assert result.size == (100, 100)

    def test_large_image_resized(self):
        img = Image.new("RGB", (8000, 8000))
        result = resize_if_needed(img, max_pixels=4000)
        assert result.size[0] <= 4000
        assert result.size[1] <= 4000
