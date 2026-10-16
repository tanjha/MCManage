"""Settings page: edit values stored in data/settings.json."""

from flask import Blueprint, flash, redirect, render_template, request, url_for

import settings_store

bp = Blueprint("settings", __name__, url_prefix="/settings")

MENU = [
    {
        "label": "Settings",
        "endpoint": "settings.index",
        "icon": "⚙",
        "section": "System",
        "order": 90,
    },
]


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        errors = []
        app_name = request.form.get("app_name", "").strip()
        if not app_name:
            errors.append("App name can't be empty.")

        theme = request.form.get("theme", "system")
        if theme not in ("system", "light", "dark"):
            errors.append("Unknown theme.")

        try:
            refresh = int(request.form.get("refresh_seconds", 5))
            if not 0 <= refresh <= 3600:
                raise ValueError
        except ValueError:
            errors.append("Refresh interval must be a number from 0 to 3600.")
            refresh = None

        servers_folder = request.form.get("servers_folder", "").strip()

        if errors:
            for e in errors:
                flash(e, "error")
        else:
            settings_store.save(
                {
                    "app_name": app_name,
                    "theme": theme,
                    "refresh_seconds": refresh,
                    "show_disk": "show_disk"
                    in request.form,  # unchecked boxes aren't submitted
                    "servers_folder": servers_folder,
                }
            )
            flash("Settings saved.", "success")
        return redirect(url_for("settings.index"))

    return render_template("pages/settings.html", title="Settings")
