import importlib
from pyrobot.plugins import ALL_MODULES
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
            workdir="./pyrobot/session",
            api_id=APP_ID,
            api_hash=API_HASH,
        )


    async def start(self):
        await super().start()
        await get_self()
        for modul in ALL_MODULES:
            imported_module = importlib.import_module("pyrobot.plugins." + modul)
            if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
                imported_module.__MODULE__ = imported_module.__MODULE__
        LOGGER.info("-----------------------")
        LOGGER.info("Userbot Plugins: " + str(ALL_MODULES))
        LOGGER.info(f"PyroGramBot based on Pyrogram v{__version__} (Layer {layer}) started.")
        LOGGER.info("Bot run successfully!")
        usr_bot_me = await self.get_me()
        OWNER_ID = usr_bot_me.id
        if getself.last_name:
            OWNER_NAME = getself.first_name + " " + getself.last_name
        else:
            OWNER_NAME = getself.first_name
        OWNER_USERNAME = usr_bot_me.username
        LOGGER.info(f"Hello {OWNER_NAME} ({OWNER_USERNAME} - {OWNER_ID})")


    async def stop(self, *args):
        await super().stop()
        LOGGER.info("PyroGramBot stopped. Bye.")
