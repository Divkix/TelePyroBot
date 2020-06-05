import asyncio
from pyrobot import COMMAND_HAND_LER
from pyrogram import Client, Filters
from pyrobot.helper_functions.cust_p_filters import sudo_filter

@Client.on_message(Filters.command("restart", COMMAND_HAND_LER) & sudo_filter)
async def updater(client, message):
    await message.reply_text(
        "Restarted! "
        f"Do `{COMMAND_HAND_LER}alive` or `{COMMAND_HAND_LER}start` to check if I am online...", parse_mode="md")
    await client.restart()
