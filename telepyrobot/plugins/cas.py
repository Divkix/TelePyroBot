import requests
from time import sleep
import asyncio
import os
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER
from telepyrobot.utils.pyrohelpers import extract_user

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Easily Check CAS ban of a user!

`{COMMAND_HAND_LER}cas <user_id>` or as a reply to the message to check the CAS status of the user.
"""


@TelePyroBot.on_message(filters.command("cas", COMMAND_HAND_LER) & filters.me)
async def cas(c: Client, m: Message):
    user_id, user_first_name = extract_user(message)
    results = requests.get(f"https://api.cas.chat/check?user_id={user_id}").json()
    offenses_cas = results["result"]["offenses"]
    offense_msg = results["result"]["messages"]
    cas_ban_time = results["result"]["time_added"]
    try:
        text = (
            f"**User ID:** `{user_id}`\n"
            f"**Name:** `{user_first_name}`\n"
            f"**Offenses:** `{offenses_cas}`\n"
            f"**Messages:** `\n{offense_msg}`\n"
            f"**Time Added:** `{cas_ban_time}`"
        )
    except:
        text = "`Not banned in CAS`"
    await m.edit(text, parse_mode="markdown")
