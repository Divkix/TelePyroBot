import time
import asyncio
import shutil
from pyrobot import COMMAND_HAND_LER, HEROKU_APP
from pyrogram import Client, Filters
from pyrobot.helper_functions.cust_p_filters import sudo_filter

@Client.on_message(Filters.command("restart", COMMAND_HAND_LER) & sudo_filter)
async def updater(client, message):
    await message.reply_text(
        "Restarted! "
        f"Do `{COMMAND_HAND_LER}alive` or `{COMMAND_HAND_LER}start` to check if I am online...", parse_mode="md")
    await client.restart()


@Client.on_message(Filters.command("reboot", COMMAND_HAND_LER) & sudo_filter)
async def restart_cmd_handler(client, message):
    rm = await message.edit("Restarting Userbot Services")
    asyncio.wait(1)
    await rm.edit("Finalizing...")
    asyncio.wait(3)
    rm.delete()
    asyncio.get_event_loop().create_task(client.restart())
