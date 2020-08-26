import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from telepyrobot import COMMAND_HAND_LER, TG_MAX_SELECT_LEN
from telepyrobot.utils.admin_check import admin_check


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__HELP__ = f"""
`{COMMAND_HAND_LER}purge`: Deletes messages upto replied message.
Usage: {COMMAND_HAND_LER}purge <as a reply to the message>

`{COMMAND_HAND_LER}del`: Deletes a single message.
Usage: {COMMAND_HAND_LER}del <as a reply to the message>"""


@Client.on_message(filters.command("purge", COMMAND_HAND_LER) & filters.me)
async def purge(client, message):
    if message.chat.type in ("supergroup", "channel"):
        await message.edit("`Incinerating these useless messages...`")
        is_admin = await admin_check(message)
        if not is_admin:
            await message.edit("I'm not admin nub nibba")
            await asyncio.sleep(2)
            await message.delete()
            return
    if message.chat.type in ["private", "bot", "group"]:
        await message.edit("`You are not allowed to use this command here!`")
        await asyncio.sleep(2)
        await message.delete()
        return

    message_ids = []
    count_del_etion_s = 0

    if message.reply_to_message:
        for a_s_message_id in range(
            message.reply_to_message.message_id, message.message_id
        ):
            message_ids.append(a_s_message_id)
            if len(message_ids) == TG_MAX_SELECT_LEN:
                await client.delete_messages(
                    chat_id=message.chat.id, message_ids=message_ids, revoke=True
                )
                count_del_etion_s += len(message_ids)
                message_ids = []
        if len(message_ids) > 0:
            await client.delete_messages(
                chat_id=message.chat.id, message_ids=message_ids, revoke=True
            )
            count_del_etion_s += len(message_ids)

    await message.edit(f"`Deleted <u>{count_del_etion_s}</u> messages`")
    await asyncio.sleep(3)
    await message.delete()


@Client.on_message(filters.command("del", COMMAND_HAND_LER) & filters.me, group=3)
async def del_msg(client, message):
    if message.reply_to_message:
        if message.chat.type in ("supergroup", "channel"):
            is_admin = await admin_check(message)
            if not is_admin:
                await message.reply("`I'm not admin nub Nibba`")
                await asyncio.sleep(3)
                await message.delete()
                return
        await client.delete_messages(
            chat_id=message.chat.id, message_ids=message.reply_to_message.message_id
        )
    else:
        await message.edit("`Reply to a message to delete!`")

    await asyncio.sleep(0.5)
    await message.delete()
