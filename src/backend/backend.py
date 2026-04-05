import logging

class Backend:
    def __init__(self):
        self.logger = logging.getLogger("Backend")

    async def start(self):
        self.logger.info("Starting backend...")

    async def stop(self):
        self.logger.info("Stopping backend...")

    async def send_message(self, message: str) -> str:
        self.logger.info(f"Received message: {message}")
        response = f"Echo: {message}"
        self.logger.info(f"Sending response: {response}")
        return response

    def get_latest_chat(self) -> str:
        return "Welcome to P2Py! This is the latest chat message."