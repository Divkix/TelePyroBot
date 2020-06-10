from pyrogram import Client
from pyrogram import __version__
from pyrogram.api.all import layer
import importlib
from pyrobot.plugins import ALL_PLUGINS
from pyrobot import (
    APP_ID,
    API_HASH,
    HU_STRING_SESSION,
    LOGGER)

HELP_COMMANDS = {}

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

        for oof in ALL_PLUGINS:
            imported_module = importlib.import_module("pyrobot.plugins." + oof)
            if import_module = "pyrobot.plugins.help":
                continue
            if not hasattr(imported_module, "__PLUGIN__"):
                imported_module.__PLUGIN__ = imported_module.__name__

            if not imported_module.__PLUGIN__.lower() in HELP_COMMANDS:
                HELP_COMMANDS[imported_module.__PLUGIN__.lower()] = imported_module
            else:
                raise Exception("Can't have two modules with the same name! Please change one")

            if hasattr(imported_module, "__help__") and imported_module.__help__:
                HELP_COMMANDS[imported_module.__PLUGIN__.lower()] = imported_module.__help__

        usr_bot_me = await self.get_me()
        LOGGER.info(
            f"PyroGramBot based on Pyrogram v{__version__} "
            f"(Layer {layer}) started..."
            f"Hey {usr_bot_me.first_name}")


    async def stop(self, *args):
        await super().stop()
        LOGGER.info("PyroGramBot stopped. Bye.")
