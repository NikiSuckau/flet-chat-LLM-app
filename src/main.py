import flet as ft
import requests
import json

# -------------------------------------------------------
# 1) Korrektes Streaming-Endpoint für Chat-Completions:
KOBOLDCPP_API_URL = "http://localhost:5001/v1/chat/completions"
# -------------------------------------------------------

# 2) Globale Chat-Historie initialisieren
chat_history = [
    {"role": "system", "content": "Du bist ein hilfreicher Assistent."}
]


class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.Colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_initials(self, user_name: str):
        return user_name[:1].upper() if user_name else "?"

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.Colors.AMBER, ft.Colors.BLUE, ft.Colors.BROWN,
            ft.Colors.CYAN, ft.Colors.GREEN, ft.Colors.INDIGO,
            ft.Colors.LIME, ft.Colors.ORANGE, ft.Colors.PINK,
            ft.Colors.PURPLE, ft.Colors.RED, ft.Colors.TEAL,
            ft.Colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


def generate_with_stream():
    """
    Sendet chat_history an KoboldCPP mit Streaming und gibt die vollständige Antwort zurück.
    """
    try:
        response = requests.post(
            KOBOLDCPP_API_URL,
            json={
                "model": "kobold_chat_v2",
                "messages": chat_history,
                "max_tokens": 200,
                "temperature": 0.8,
                "stream": True
            },
            timeout=120,
            stream=True
        )
        response.raise_for_status()
    except Exception as ex:
        return f"[error connecting to KoboldCPP: {ex}]"

    bot_reply = ""
    for chunk in response.iter_lines(decode_unicode=True):
        if not chunk:
            continue
        if chunk.startswith("data:"):
            json_str = chunk[len("data:"):].strip()
            try:
                j = json.loads(json_str)
            except json.JSONDecodeError:
                continue
            delta = j["choices"][0]["delta"].get("content", "")
            if delta:
                bot_reply += delta
            if j["choices"][0].get("finish_reason") == "stop":
                break
    return bot_reply


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.title = "Flet + KoboldCPP: Voller Chatkontext"

    # 3) “Join” Dialog
    join_user_name = ft.TextField(
        label="Enter your name to join the chat",
        autofocus=True,
        on_submit=lambda e: join_chat_click(e),
    )
    welcome_dlg = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=lambda e: join_chat_click(e))],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(welcome_dlg)

    chat = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=lambda e: send_message_click(e),
    )

    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update()
            return

        page.session.set("user_name", join_user_name.value)
        welcome_dlg.open = False
        new_message.prefix = ft.Text(f"{join_user_name.value}: ")
        page.pubsub.send_all(
            Message(
                user_name=join_user_name.value,
                text=f"{join_user_name.value} has joined the chat.",
                message_type="login_message",
            )
        )
        page.update()

    def send_message_click(e):
        text = new_message.value.strip()
        if not text:
            return

        user_name = page.session.get("user_name") or "Unknown"

        # 4) User-Nachricht lokal anzeigen
        page.pubsub.send_all(
            Message(
                user_name=user_name,
                text=text,
                message_type="chat_message",
            )
        )

        # 5) User-Nachricht an chat_history anhängen
        chat_history.append({"role": "user", "content": text})

        new_message.value = ""
        new_message.focus()
        page.update()

        # 6) KoboldCPP mit vollständiger Historie (Streaming) aufrufen
        bot_reply = generate_with_stream()

        # 7) Bot-Antwort an chat_history anhängen
        chat_history.append({"role": "assistant", "content": bot_reply})

        # 8) Bot-Antwort lokal anzeigen
        page.pubsub.send_all(
            Message(
                user_name="Bot",
                text=bot_reply,
                message_type="chat_message",
            )
        )
        page.update()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.Colors.BLACK45, size=12)
        else:
            return

        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.Icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=lambda e: send_message_click(e),
                ),
            ]
        ),
    )


if __name__ == "__main__":
    ft.app(target=main)

