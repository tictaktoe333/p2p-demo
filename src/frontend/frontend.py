from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Input, ListView, ListItem, Label, RichLog, Static
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual import on
from datetime import datetime

from .contact_form import Contact, AddContactModal

MOCK_SESSIONS = [
    "alice",
    "bob",
    "charlie",
    "dave",
]

MOCK_HISTORY = {
    "alice": [
        ("alice", "hey, you there?", "10:01"),
        ("me", "yeah whats up", "10:02"),
        ("alice", "want to test the p2p stuff later?", "10:03"),
        ("me", "sure, spin up a node and ill connect", "10:04"),
    ],
    "bob": [
        ("bob", "did you get the latest changes?", "09:45"),
        ("me", "yeah looks good", "09:46"),
    ],
    "charlie": [
        ("charlie", "yo", "yesterday"),
    ],
    "dave": [],
}


class Frontend(App):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend

    CSS_PATH = "chat.tcss"

    BINDINGS = [("n", "new_contact", "new contact")]
 
    active_session: reactive[str] = reactive("alice")
 
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Static(" sessions", id="sidebar-title")
                yield ListView(
                    *[ListItem(Label(f" {s}"), id=f"session-{s}") for s in MOCK_SESSIONS],
                    id="session-list",
                )
                yield Button("(n)ew contact", id="add-contact-btn")
            with Vertical(id="chat-area"):
                yield Static(" alice", id="chat-header")
                yield RichLog(id="message-log", highlight=True, markup=True, wrap=True)
                with Horizontal(id="input-bar"):
                    yield Input(placeholder="message alice...", id="msg-input")

    def on_mount(self) -> None:
        self.load_session(self.active_session)
        self.query_one("#msg-input", Input).focus()
 
    def load_session(self, name: str) -> None:
        log = self.query_one("#message-log", RichLog)
        log.clear()
        history = MOCK_HISTORY.get(name, [])
        if not history:
            log.write("[dim]no messages yet — say something![/dim]")
        for sender, text, ts in history:
            self._render_message(log, sender, text, ts)
 
    def _render_message(self, log: RichLog, sender: str, text: str, ts: str) -> None:
        if sender == "me":
            log.write(f"[dim]{ts}[/dim]  [bold $accent-green]you[/bold $accent-green]  {text}")
        else:
            log.write(f"[dim]{ts}[/dim]  [bold $accent-orange]{sender}[/bold $accent-orange]  {text}")
 
    def watch_active_session(self, new_session: str) -> None:
        if not self.is_mounted:
            return
        self.query_one("#chat-header", Static).update(f" {new_session}")
        self.query_one("#msg-input", Input).placeholder = f"message {new_session}..."
        self.load_session(new_session)
 
    def action_new_contact(self) -> None:
        self.app.push_screen(AddContactModal(), self._on_contact_added)
 
    @on(Button.Pressed, "#add-contact-btn")
    def open_add_contact(self) -> None:
        self.app.push_screen(AddContactModal(), self._on_contact_added)
 
    def _on_contact_added(self, contact: Contact | None) -> None:
        if contact is None:
            return
        MOCK_SESSIONS.append(contact.nickname)
        MOCK_HISTORY[contact.nickname] = []
        list_view = self.query_one("#session-list", ListView)
        list_view.append(ListItem(Label(f" {contact.nickname}"), id=f"session-{contact.nickname}"))
        self.active_session = contact.nickname
        self.query_one("#msg-input", Input).focus()
 
    @on(ListView.Selected)
    def session_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id or ""
        if item_id.startswith("session-"):
            name = item_id.removeprefix("session-")
            self.active_session = name
            self.query_one("#msg-input", Input).focus()
 
    @on(Input.Submitted, "#msg-input")
    def send_message(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        if not text:
            return
 
        ts = datetime.now().strftime("%H:%M")
        log = self.query_one("#message-log", RichLog)
        self._render_message(log, "me", text, ts)
 
        MOCK_HISTORY.setdefault(self.active_session, []).append(("me", text, ts))
        event.input.clear()

if __name__ == "__main__":
    Frontend().run()