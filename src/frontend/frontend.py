from textual.app import App
from textual import widgets
from src.backend.backend import Backend

class Frontend(App):
    def __init__(self, backend: Backend):
        super().__init__()
        self.backend = backend
        self.chat_window = widgets.TextArea()
        self.input_field = widgets.Input(placeholder="Type your message here...")


    async def on_mount(self):

        yield self.chat_window
        yield self.input_field
