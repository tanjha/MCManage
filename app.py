"""
Web app template: dashboard + settings, with a menu driven by a page registry.

Run on the server:
    python3 app.py

Then from your own computer:
    ssh -L 8000:localhost:8000 user@your-server
    open http://localhost:8000
"""
import os

from flask import Flask

import settings_store
from pages import register_pages

HOST = os.environ.get("APP_HOST", "127.0.0.1")   # localhost only; reach it via SSH tunnel
PORT = int(os.environ.get("APP_PORT", "8000"))


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("APP_SECRET_KEY", "change-me-in-production")

    # Make saved settings available to every template as {{ settings.xxx }}
    @app.context_processor
    def inject_settings():
        return {"settings": settings_store.load()}

    register_pages(app)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=os.environ.get("APP_DEBUG") == "1")
