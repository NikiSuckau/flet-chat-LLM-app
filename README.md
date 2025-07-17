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
- **Long-term memory system for personalized responses**
- Persistent settings (KoboldCPP URL and LLM parameters)
- Simple diary stored in an SQLite database
- Diary view bottom bar with command and save buttons
- Self-reflection question command powered by KoboldCPP
- Previous entry summary command powered by KoboldCPP
- Diary questions stream live as they are generated
- Configurable self-reflection prompts and parameters
- View saved diary entries sorted by date
- Tap a saved entry to reopen and edit it
- Delete saved entries with a long press and confirmation popup
- User data is stored under the `storage/` folder

## Long-term Memory

The app now includes an intelligent long-term memory system that remembers information about you across conversations:

- **User Preferences**: Remembers your preferences (e.g., "I prefer dark mode themes")
- **Personal Information**: Stores details you share about yourself (e.g., "My name is Alice", "I work as a developer")
- **Goals and Interests**: Tracks your learning goals and interests (e.g., "I want to learn Python", "I'm interested in AI")

The memory system automatically extracts important information from your conversations and includes relevant context in future chats, providing more personalized and helpful responses. All memory data is stored locally in `storage/data/memory.db`.

You can enable or disable the memory system in the settings (enabled by default).

## Code Structure

The application code lives under the `src` folder and is split into two main
packages:

- `backend/` – Contains logic unrelated to the UI. `backend.py` stores chat
  history and talks to the KoboldCPP API, `models.py` defines the `Message`
  dataclass, `settings_manager.py` loads and saves the persistent
  `AppSettings`, and `memory_manager.py` handles long-term memory extraction
  and storage.
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
  - [x] Save chat 
  - [x] Long term memory via LangChain (`LangMem`)
  - [x] fix streaming messages, despite ```"stream": True``` in backend.py it does not work
  - [ ] Read and print which model is available (```curl http://localhost:5001/v1/models``` gives a list of available models)
  - [ ] Markdown rendering

- Diary functionality, to let users write and save diary entries (Can be used later on as context for the LLM through Langchain)
  - [x] Create diary button in navigation drawer which leads into a diary view
  - [x] Give diary view a text editor style to write diary entries
  - [x] Command popup to trigger LLM self-reflection questions

- Frontend general
  - [ ] Improve styling

- User functionality
  - [x] User name stored in settings

## Bugs users found

- Chat
  - [x] Chat messages are not correctly displayed if being long. We need to wrap them at the end of the display
- Diary
  - [x] Inputed text is not temporarily saved when switching to chat view (annoying when you forget to save and switch to chat view)
  - [ ] Self-reflection question popup does show if the text is very long
- Settings menu
  - [ ] Temperature slider are not labelled 
  - [ ] Not automatically saving settings when changing and not pressing "Save" (annoying when you forget to save and switch to chat view)
