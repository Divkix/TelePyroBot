import asyncio
import importlib
import sys
import time
import traceback

from pyrobot import pyrouserbot, OWNER_ID, get_self
from pyrobot.modules import ALL_MODULES

BOT_RUNTIME = 0
HELP_COMMANDS = {}

loop = asyncio.get_event_loop()


async def get_runtime():
    return BOT_RUNTIME


async def reload_userbot():
    await pyrouserbot.start()
    for modul in ALL_MODULES:
        imported_module = importlib.import_module("pyrobot.modules." + modul)
        importlib.reload(imported_module)


async def reinitial_restart():
    await get_self()


async def reboot():
    global BOT_RUNTIME, HELP_COMMANDS
    importlib.reload(importlib.import_module("pyrobot.modules"))
    from pyrobot.modules import ALL_MODULES
    await pyrouserbot.restart()
    await reinitial_restart()
    BOT_RUNTIME = 0
    HELP_COMMANDS = {}
    # PyroUserbot
    for modul in ALL_MODULES:
        imported_module = importlib.import_module("pyrobot.modules." + modul)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if not imported_module.__MODULE__.lower() in HELP_COMMANDS:
                HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
            else:
                raise Exception("Can't have two modules with the same name! Please change one")
        if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
            HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
        importlib.reload(imported_module)


async def restart_all():
    asyncio.get_event_loop().create_task(reboot())


async def reinitial():
    await pyrouserbot.start()
    await get_self()
    await pyrouserbot.stop()


async def start_bot():
    print("----- Checking user and bot... -----")
    await reinitial()
    print("----------- Check done! ------------")
    # PyroUserBot
    await pyrouserbot.start()
    for modul in ALL_MODULES:
        imported_module = importlib.import_module("pyrobot.modules." + modul)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if not imported_module.__MODULE__.lower() in HELP_COMMANDS:
                HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
            else:
                raise Exception("Can't have two modules with the same name! Please change one")
        if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
            HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
    print("-----------------------")
    print("Userbot modules: " + str(ALL_MODULES))
    print("-----------------------")
    print("Bot run successfully!")


if __name__ == '__main__':
    BOT_RUNTIME = int(time.time())
    loop.run_until_complete(start_bot())
