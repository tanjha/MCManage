"""Tiny JSON-file settings store. Add new settings to DEFAULTS."""

import json
import threading
from pathlib import Path

SETTINGS_FILE = Path(__file__).parent / "data" / "settings.json"

DEFAULTS = {
    "app_name": "My Web App",
    "theme": "system",  # system | light | dark
    "refresh_seconds": 5,  # dashboard auto-refresh interval
    "servers_folder": "/",
    "show_disk": True,
}

_lock = threading.Lock()


def load() -> dict:
    data = dict(DEFAULTS)
    try:
        data.update(json.loads(SETTINGS_FILE.read_text()))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return data


def save(updates: dict) -> dict:
    with _lock:
        data = load()
        data.update({k: v for k, v in updates.items() if k in DEFAULTS})
        SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
        SETTINGS_FILE.write_text(json.dumps(data, indent=2))
    return data
