# LLM FlatChat

LLM FlatChat is a small chat client built with [Flet](https://flet.dev). It connects to a [KoboldCPP](https://github.com/LostRuins/koboldcpp) server and stores your settings locally in `storage/settings.json`. The app lets you swap between a chat view and a settings view via the navigation drawer.

## Requirements

- Python 3.11+
- Flet (installed via `pip install flet[all]`)

## Running the App
After installing the requirements, you can run the app by executing the following command in the project directory:
```bash
flet run
```

Start your KoboldCPP server first. On initial launch you will be prompted for your name. Open the settings view to change the API URL if it differs from the default. The URL is persisted in `storage/settings.json` and diary entries are stored in `storage/diary_entries.json`.

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
- Simple diary to store notes
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

## TODO


- Settings menu
  - [x] Settings menu to set LLM URL (KoboldCPP URL)
  - [ ] Settings for LLM system prompt
  - [ ] Settings for LLM temperature
  - [ ] Settings for LLM max tokens
- Chat
  - [x] Bring in last messages as context
  - [ ] Make past messages of LLM or user editable
  - [ ] Let LLM regenerate last message
  - [ ] Save chat 
  - [ ] Long term memory via Langchain
  - [ ] fix streaming messages, despite ```"stream": True``` in backend.py it does not work
  - [ ] Markdown rendering

- Diary functionality, to let users write and save diary entries (Can be used later on as context for the LLM through Langchain)
  - [x] Create diary button in navigation drawer which leads into a diary view
  - [x] Give diary view a text editor style to write diary entries

- Frontend general
  - [ ] Improve styling

- User functionality (Needs way more thoughts and planning, e. g. how to handle multiple users, how and where to store user data, etc.)
  - [x] User name input on first launch
  - [ ] Change User welcome name inpput on first launch (Its temporary and not saved). Instead i would like to have a user managment system where users can log in and out. Last user is remembered.

