# LLM FlatChat

LLM FlatChat is a small chat client built with [Flet](https://flet.dev). It connects to a [KoboldCPP](https://github.com/LostRuins/koboldcpp) server and stores your settings locally in `storage/settings.json`. The navigation drawer lets you switch between chat, settings, diary, saved entries and a memories view that shows long-term memories from your conversations.

## Requirements

- Python 3.11+
- Flet (installed via `pip install flet[all]`)

## Running the App
After installing the requirements, you can run the app by executing the following command in the project directory:
```bash
flet run
```

Start your KoboldCPP server first. Open the settings view to enter your name above the KoboldCPP URL and adjust the API endpoint if needed. The URL is persisted in `storage/settings.json` and diary entries are stored in `storage/diary.db`.

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
- Persistent settings (KoboldCPP URL and LLM parameters)
- Simple diary stored in an SQLite database
- Backslash-triggered command popup in the diary view
- The triggering backslash is removed after executing a command
- Self-reflection question command powered by KoboldCPP
- Configurable self-reflection prompts and parameters
- View saved diary entries sorted by date
- Tap a saved entry to reopen and edit it
 - Delete saved entries with a long press and confirmation popup
- User data is stored under the `storage/` folder

## Code Structure

The application code lives under the `src` folder and is split into two main
packages:

- `backend/` – Contains logic unrelated to the UI. `backend.py` stores chat
  history and talks to the KoboldCPP API, `models.py` defines the `Message`
  dataclass, while `settings_manager.py` loads and saves the persistent
  `AppSettings`.
- `frontend/` – All Flet UI components. `app.py` wires everything together,
  `chat_view.py` displays the message list, `chat_message.py` renders individual
  messages, and `settings_view.py` hosts the settings form.

Execution begins in `main.py` which creates the backend and loads settings
before handing control to Flet.

## Development

Development guidelines and testing instructions are described in
[`AGENTS.md`](AGENTS.md). To run the unit tests yourself install the project with
the optional development dependencies and execute:

```bash
pip install -e .[dev]
python -m pytest
```

## Documentation

Offline documentation for Flet lives under `docs/flet-docs` and can be consulted without internet access. Langchain documentation resides under `docs/langchain-docs` and currently includes the `LangMem` module.

## TODO


- Settings menu
  - [x] Settings menu to set LLM URL (KoboldCPP URL)
  - [x] Settings for LLM system prompt
  - [x] Settings for LLM temperature
  - [x] Settings for LLM max tokens
  - [x] Diary question prompt and parameters
- Chat
  - [x] Bring in last messages as context
  - [ ] Make past messages of LLM or user editable
  - [ ] Let LLM regenerate last message
  - [ ] Save chat 
  - [x] Long term memory via Langchain (`LangMem`)
  - [ ] fix streaming messages, despite ```"stream": True``` in backend.py it does not work
  - [ ] Markdown rendering

- Diary functionality, to let users write and save diary entries (Can be used later on as context for the LLM through Langchain)
  - [x] Create diary button in navigation drawer which leads into a diary view
  - [x] Give diary view a text editor style to write diary entries
  - [x] Command popup to trigger LLM self-reflection questions

- Frontend general
  - [ ] Improve styling

- User functionality
  - [x] User name stored in settings

