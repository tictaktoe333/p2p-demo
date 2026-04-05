from textual.app import App, ComposeResult
from textual import events
from textual.widgets import Header, Button, Label, Footer, Static, Input  

from src.backend.backend import Backend

class Frontend(App):
    def __init__(self, backend: Backend):
        super().__init__()
        self.backend = backend
        self.chat_box = Static(self.backend.get_latest_chat(), id="chat_box")
        self.text_input = Input(placeholder="Type your message here...", id="text_input")


    # CSS_PATH = "question02.tcss"
    TITLE = "P2Py"
    # SUB_TITLE = "The most important question"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("CHAT", id="chat_label")
        yield self.chat_box
        yield self.text_input
        yield Button("Send", id="send_button")
        yield Footer()

    def on_mount(self) -> None:
        self.chat_box.styles.background = "darkblue"
        self.text_input.styles.background = "black"
        self.chat_box.styles.height = "2fr"
        self.text_input.styles.height = "1fr"

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.exit()