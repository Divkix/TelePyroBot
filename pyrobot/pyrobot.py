import logging
from pyrogram import Client

from pyrobot import (
    APP_ID,
    API_HASH,
    HU_STRING_SESSION,
    LOGGER,
    TMP_DOWNLOAD_DIRECTORY)

class PyroBot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        if HU_STRING_SESSION is not None:
            super().__init__(
                HU_STRING_SESSION,
                plugins=dict(root=f"{name}/plugins"),
                workdir=TMP_DOWNLOAD_DIRECTORY,
                api_id=APP_ID,
                api_hash=API_HASH)
        else:
            logging.error("You need to set HU_STRING_SESSION Var first!")
            quit(1)

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        LOGGER.info(f"TelePyroBot based on Pyrogram started Successfully! Hello {usr_bot_me}.")

    async def stop(self, *args):
        await super().stop()
        print("TelePyroBot stopped. Bye.")
