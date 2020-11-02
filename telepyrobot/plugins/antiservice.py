import os
from telepyrobot.setclient import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot.db import antiservice_db as db
from telepyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Commands to delete antiservice messages in a chat!

`{COMMAND_HAND_LER}asenable`: Enable antiservice for chat.
`{COMMAND_HAND_LER}asdisable`: Disable antiservice for chat.
"""


@TelePyroBot.on_message(filters.command("asenable", COMMAND_HAND_LER) & filters.me)
async def anti_service_enable(c: TelePyroBot, m: Message):
    try:
        db.enable_antiservice(m.chat.id)
        await m.edit_text("Enabled AntiService for this chat.")
    except Exception as ef:
        await m.edit_text(ef)
    return


@TelePyroBot.on_message(filters.command("asdisable", COMMAND_HAND_LER) & filters.me)
async def anti_service_disable(c: TelePyroBot, m: Message):
    try:
        db.disable_antiservice(m.chat.id)
        await m.edit_text("Disabled AntiService for this chat.")
    except Exception as ef:
        await m.edit_text(ef)
    return


@TelePyroBot.on_message(filters.service, group=11)
async def anti_service_check(c: TelePyroBot, m: Message):
    try:
        if db.get_antiservice(m.chat.id):
            await m.delete()
            return
    except:  # Pass at any other error
        pass
