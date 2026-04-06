from textual.app import ComposeResult
from textual.widgets import Button, Input, Static
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual import on
from dataclasses import dataclass
 
 
@dataclass
class Contact:
    nickname: str
    ip: str
    port: str
 
class AddContactModal(ModalScreen[Contact | None]):
    def compose(self) -> ComposeResult:
        with Vertical(id="modal-container"):
            yield Static(" new contact", id="modal-title")
            yield Static("nickname", classes="field-label")
            yield Input(placeholder="e.g. nick", id="input-nickname", classes="modal-input")
            yield Static("ip address", classes="field-label")
            yield Input(placeholder="e.g. 192.168.0.1", id="input-ip", classes="modal-input")
            yield Static("port", classes="field-label")
            yield Input(placeholder="e.g. 8080", id="input-port", classes="modal-input")
            with Horizontal(id="modal-buttons"):
                yield Button("cancel", id="btn-cancel")
                yield Button("add contact", id="btn-add")
 

