"""Dashboard page: server stats with auto-refresh."""

import os
import platform
import shutil
import time
from pathlib import Path

from flask import Blueprint, abort, jsonify, render_template

import settings_store

bp = Blueprint("dashboard", __name__)

MENU = [
    {"label": "Dashboard", "endpoint": "dashboard.index", "icon": "▦", "order": 10},
]


def _uptime_seconds() -> float | None:
    try:
        with open("/proc/uptime") as f:
            return float(f.read().split()[0])
    except OSError:
        return None


def _memory() -> dict | None:
    try:
        info = {}
        with open("/proc/meminfo") as f:
            for line in f:
                key, value = line.split(":", 1)
                info[key] = int(value.split()[0]) * 1024
        total, avail = info["MemTotal"], info["MemAvailable"]
        return {
            "total": total,
            "used": total - avail,
            "percent": round((total - avail) / total * 100, 1),
        }
    except (OSError, KeyError):
        return None


def collect_stats() -> dict:
    disk = shutil.disk_usage("/")
    load1, load5, load15 = os.getloadavg() if hasattr(os, "getloadavg") else (0, 0, 0)
    return {
        "hostname": platform.node(),
        "system": f"{platform.system()} {platform.release()}",
        "cpu_count": os.cpu_count(),
        "load": [round(load1, 2), round(load5, 2), round(load15, 2)],
        "memory": _memory(),
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "percent": round(disk.used / disk.total * 100, 1),
        },
        "uptime": _uptime_seconds(),
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
    }


def _read_properties(path: Path) -> dict:
    """Parse a Java-style key=value file (server.properties)."""
    props = {}
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith(("#", "!")) or "=" not in line:
            continue
        key, value = line.split("=", 1)
        props[key.strip()] = value.strip()
    return props


def grab_servers(server_directory: Path) -> list[dict]:
    servers = []
    if not server_directory.is_dir():
        return servers
    for folder in sorted(server_directory.iterdir()):
        if not folder.is_dir():
            continue
        servers.append(
            {
                "name": folder.name,
                "path": str(folder),
            }
        )
    return servers


@bp.route("/")
def index():
    folder = Path(settings_store.load()["servers_folder"])
    return render_template(
        "pages/dashboard.html",
        stats=collect_stats(),
        servers=grab_servers(folder),
        title="Dashboard",
    )


@bp.route("/api/stats")
def api_stats():
    """JSON used by the dashboard's auto-refresh."""
    return jsonify(collect_stats())


@bp.route("/servers/<name>")
def server(name):
    folder = Path(settings_store.load()["servers_folder"])
    match = next((s for s in grab_servers(folder) if s["name"] == name), None)
    if match is None:
        abort(404)
    return render_template("pages/server.html", server=match, title=match["name"])
