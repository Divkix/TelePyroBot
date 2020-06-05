import asyncio

from pyrogram import Client, Filters
from pyrobot.helper_functions.cust_p_filters import owner_filter

@Client.on_message(Filters.command("restart", COMMAND_HAND_LER) & sudo_filter)
async def updater(client, message):
    await message.reply_text(
        "Restarted! "
        f"Do `{COMMAND_HAND_LER}alive` to check if I am online...")
    await client.restart()
