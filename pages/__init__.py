"""
Page registry.

Every page lives in its own module in this folder and defines:
    bp    -- a Flask Blueprint with the page's routes
    MENU  -- a list of menu entries (dicts), each with:
               label     text shown in the sidebar
               endpoint  Flask endpoint, e.g. "dashboard.index"
               icon      optional emoji/short text
               section   optional sidebar group heading (default "Main")
               order     optional sort number (lower = higher up)

To add a page: create pages/<name>.py, then add "<name>" to PAGE_MODULES.
"""
from importlib import import_module

from flask import Flask, request, url_for

# Order here does not affect menu order; use each entry's "order" for that.
PAGE_MODULES = [
    "dashboard",
    "settings",
    # "reports",   # <- example: add new page modules here
]


def register_pages(app: Flask) -> None:
    menu = []
    for name in PAGE_MODULES:
        module = import_module(f"pages.{name}")
        app.register_blueprint(module.bp)
        menu.extend(getattr(module, "MENU", []))

    menu.sort(key=lambda m: (m.get("order", 100), m["label"]))

    @app.context_processor
    def inject_menu():
        sections: dict[str, list] = {}
        for item in menu:
            entry = dict(item)
            entry["url"] = url_for(item["endpoint"])
            entry["active"] = request.endpoint == item["endpoint"]
            sections.setdefault(item.get("section", "Main"), []).append(entry)
        return {"menu_sections": sections}
