from pyrogram import Client
from pyrogram import __version__
from pyrogram.api.all import layer

from pyrobot import (
    APP_ID,
    API_HASH,
    HU_STRING_SESSION,
    LOGGER)


class PyroBot(Client):

    def __init__(self):
        name = self.__class__.__name__.lower()

        super().__init__(
            HU_STRING_SESSION,
            plugins=dict(root=f"{name}/plugins"),
            workdir=f"{name}/session",
            api_id=APP_ID,
            api_hash=API_HASH)


    async def start(self):
        await super().start()

        usr_bot_me = await self.get_me()
        LOGGER.info(
            f"PyroGramBot based on Pyrogram v{__version__} "
            f"(Layer {layer}) started..."
            f"Hey {usr_bot_me.first_name}")


    async def stop(self, *args):
        await super().stop()
        LOGGER.info("PyroGramBot stopped. Bye.")
