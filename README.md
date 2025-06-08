# LLM FlatChat

LLM FlatChat is a small chat client built with [Flet](https://flet.dev). It connects to a [KoboldCPP](https://github.com/LostRuins/koboldcpp) server and stores your settings locally in `settings.json`. The app lets you swap between a chat view and a settings view via the navigation drawer.

## Requirements

- Python 3.11+
- Flet (installed automatically via `uv` or `poetry`)

## Running the App

### Using uv

```bash
uv run flet run              # Desktop
uv run flet run --web        # Web
```

### Using Poetry

```bash
poetry install               # install dependencies
poetry run flet run          # Desktop
poetry run flet run --web    # Web
```

Start your KoboldCPP server first. On initial launch you will be prompted for your name. Open the settings view to change the API URL if it differs from the default. The URL is persisted in `settings.json`.

## Building Distributables

Flet can package the application for multiple platforms:

```bash
flet build apk -v       # Android
flet build ipa -v       # iOS
flet build macos -v     # macOS
flet build linux -v     # Linux
flet build windows -v   # Windows
```

See the [Flet publish guide](https://flet.dev/docs/publish/) for signing and distribution details.

## Features

- Chat with KoboldCPP via a clean Flet UI
- Chat history context awareness
- Persistent settings (KoboldCPP URL)

## TODO

- [x] Bring in last messages as context
- [x] Settings menu to set LLM URL (KoboldCPP URL)
- [ ] Markdown rendering
- [ ] Make messages editable
- [ ] Let LLM regenerate last message
- [ ] Improve styling
- [ ] Long term memory

