# FletChat app

## Run the app

### uv

Run as a desktop app:

```
uv run flet run
```

Run as a web app:

```
uv run flet run --web
```

### Poetry

Install dependencies from `pyproject.toml`:

```
poetry install
```

Run as a desktop app:

```
poetry run flet run
```

Run as a web app:

```
poetry run flet run --web
```

For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/getting-started/).

When the app is running use the menu button in the top bar to open **Settings** and
provide your API key. The key is stored locally so you don't have to re-enter it
next time.

## Build the app

### Android

```
flet build apk -v
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS

```
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).



--- 
# LLM FlatChat app
I wrote this app to learn more about Flet and LLM. Its basically  a chat app that uses LLM to generate responses. The API i use i Koboldcpp.

## Features
- Pretty simple so far
- Uses Flet for the UI
- Uses Koboldcpp for the LLM
- Context chat aware
- Settings menu to store your API key

## Todos
- [x] Bring in last messages as context
- [ ] Markdown rendering
- [x] Settings menu to set LLM API
- [ ] Make messages editable
- [ ] Let LLM regenerate last message
- [ ] make it more beautiful
- [ ] Long term memory






