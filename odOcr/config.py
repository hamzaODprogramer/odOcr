import json
import os
from pathlib import Path

from .models import AppConfig

CONFIG_DIR = Path.home() / ".odOcr"
CONFIG_PATH = CONFIG_DIR / "config.json"
LANGUAGES_DIR = CONFIG_DIR / "languages"
DESCRIBE_MODEL_DIR = CONFIG_DIR / "describe-model"


def ensure_dirs():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    LANGUAGES_DIR.mkdir(parents=True, exist_ok=True)
    DESCRIBE_MODEL_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> AppConfig:
    ensure_dirs()
    if not CONFIG_PATH.exists():
        config = AppConfig()
        save_config(config)
        return config

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return AppConfig(**data)
    except (json.JSONDecodeError, TypeError, KeyError):
        config = AppConfig()
        save_config(config)
        return config


def save_config(config: AppConfig):
    ensure_dirs()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "hotkey": config.hotkey,
            "output_format": config.output_format,
            "describe": config.describe,
            "language": config.language,
            "dark_mode": config.dark_mode,
            "auto_copy": config.auto_copy,
            "installed_languages": config.installed_languages,
            "describe_model_installed": config.describe_model_installed,
        }, f, indent=2)
