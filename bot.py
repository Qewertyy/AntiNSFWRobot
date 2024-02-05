# Copyright 2024 Qewertyy, MIT License

import uvloop
uvloop.install()
import datetime,logging, sys
from pyrogram import Client
from config import Config
import httpx
from web_utils import create_server

# Get logging configurations
logging.basicConfig(
    format="%(asctime)s - [BOT] - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

StartTime = datetime.datetime.now()

class Bot(Client):
    def __init__(self):
        super().__init__(
            "AntiNSFWRobot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="modules"),
        )
    async def start(self):
        await super().start()
        LOGGER.info("Bot Started")

    async def stop(self):
        await super().stop()
        LOGGER.info("Stopped Services")

if __name__ == "__main__":
    Bot().run()