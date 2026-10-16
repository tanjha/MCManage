# MC Manager

An open source Minecraft Server manager - modded support + containerization for easy deployments and usage.

## Run it on the server

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py            # listens on 127.0.0.1:8000
```

## Use it from another computer

```bash
ssh -L 8000:localhost:8000 user@your-server
```

Then open http://localhost:8000 in your browser.

## Project layout

```
app.py                  entry point (host/port, secret key)
settings_store.py       saved settings (data/settings.json) + defaults
pages/__init__.py       page registry -> PAGE_MODULES list builds the menu
pages/dashboard.py      dashboard routes + menu entry
pages/settings.py       settings routes + menu entry
templates/base.html     shared layout: sidebar, top bar, flash messages
templates/pages/*.html  one template per page
static/style.css        all styling (light/dark themes)
```

## Environment variables

| Variable         | Default                   | Purpose                      |
|------------------|---------------------------|------------------------------|
| `APP_HOST`       | `127.0.0.1`               | Address to listen on         |
| `APP_PORT`       | `8000`                    | Port                         |
| `APP_SECRET_KEY` | `change-me-in-production` | Signs session/flash cookies  |
| `APP_DEBUG`      | unset                     | Set to `1` for auto-reload   |

See the "Adding Pages & Menus" guide for how to extend it.
