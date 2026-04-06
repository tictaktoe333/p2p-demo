from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, ListView, ListItem, Label, RichLog, Static
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual import on
from datetime import datetime


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
            with Vertical(id="chat-area"):
                yield Static(" alice", id="chat-header")
                yield RichLog(id="message-log", highlight=True, markup=True, wrap=True)
                with Horizontal(id="input-bar"):
                    yield Input(placeholder="message alice...", id="msg-input")
        yield Footer()

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
            log.write(f"[dim]{ts}[/dim]  [bold #5dff9a]you[/bold #5dff9a]  {text}")
        else:
            log.write(f"[dim]{ts}[/dim]  [bold #ff9a5d]{sender}[/bold #ff9a5d]  {text}")

    def watch_active_session(self, new_session: str) -> None:
        # Guard against watcher firing before the DOM is mounted
        if not self.is_mounted:
            return
        self.query_one("#chat-header", Static).update(f" {new_session}")
        self.query_one("#msg-input", Input).placeholder = f"message {new_session}..."
        self.load_session(new_session)

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