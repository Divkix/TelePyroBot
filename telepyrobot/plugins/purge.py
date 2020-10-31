import os
import asyncio
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from telepyrobot import COMMAND_HAND_LER, TG_MAX_SELECT_LEN
from telepyrobot.utils.admin_check import admin_check


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}purge`: Deletes messages upto replied message.
Usage: {COMMAND_HAND_LER}purge <as a reply to the message>

`{COMMAND_HAND_LER}del`: Deletes a single message.
Usage: {COMMAND_HAND_LER}del <as a reply to the message>"""


@TelePyroBot.on_message(filters.command("purge", COMMAND_HAND_LER) & filters.me)
async def purge(c: TelePyroBot, m: Message):
    if m.chat.type in ("supergroup", "channel"):
        await m.edit_text("`Incinerating these useless messages...`")
        is_admin = await admin_check(c, m)
        if not is_admin:
            await m.edit_text("I'm not admin nub nibba")
            await asyncio.sleep(2)
            await m.delete()
            return
    if m.chat.type in ["private", "bot", "group"]:
        await m.edit_text("`You are not allowed to use this command here!`")
        await asyncio.sleep(2)
        await m.delete()
        return

    message_ids = []
    count_del_etion_s = 0

    if m.reply_to_message:
        for a_s_message_id in range(m.reply_to_message.message_id, m.message_id):
            message_ids.append(a_s_message_id)
            if len(message_ids) == TG_MAX_SELECT_LEN:
                await c.delete_messages(
                    chat_id=m.chat.id, message_ids=message_ids, revoke=True
                )
                count_del_etion_s += len(message_ids)
                message_ids = []
        if len(message_ids) > 0:
            await c.delete_messages(
                chat_id=m.chat.id, message_ids=message_ids, revoke=True
            )
            count_del_etion_s += len(message_ids)

    await m.edit_text(f"`Deleted <u>{count_del_etion_s}</u> messages.`")
    await asyncio.sleep(3)
    await m.delete()


@TelePyroBot.on_message(filters.command("del", COMMAND_HAND_LER) & filters.me, group=3)
async def del_msg(c: TelePyroBot, m: Message):
    if m.reply_to_message:
        if m.chat.type in ("supergroup", "channel"):
            is_admin = await admin_check(c, m)
            if not is_admin:
                await m.reply_text("`I'm not admin nub Nibba`")
                await asyncio.sleep(3)
                await m.delete()
                return
        await c.delete_messages(
            chat_id=m.chat.id, message_ids=m.reply_to_message.message_id
        )
    else:
        await m.edit_text("`Reply to a message to delete!`")

    await asyncio.sleep(0.5)
    await m.delete()
