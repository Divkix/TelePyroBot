import os
import asyncio
from pyrogram import Client, Filters, ChatPermissions
from pyrobot import COMMAND_HAND_LER, PRIVATE_GROUP_ID
from pyrobot.utils.admin_check import admin_check
from pyrobot.utils.pyrohelpers import extract_user
from pyrobot.utils.string import extract_time
from pyrobot.utils.parser import mention_markdown

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Add a known user to a group easily!

`{COMMAND_HAND_LER}invite`: Add the user to your Group.
Usage: {COMMAND_HAND_LER}invite <Username or User ID>
"""


@Client.on_message(Filters.command("invite", COMMAND_HAND_LER) & Filters.me)
async def invite_user(client, message):
    if PRIVATE_GROUP_ID is None:
        await message.edit("Please set `PRIVATE_GROUP_ID` variable to make me work!")
        return
    is_admin = await admin_check(message)
    if not is_admin:
        await msg.edit("`I'm not admin nub nibba!`")
        await asyncio.sleep(2)
        await message.delete()
        return
    if len(message.command) > 2:
        await message.edit(f"__Only one user can be invited at a time,\ncheck__ `{COMMAND_HAND_LER}help` __for more info.__")
        return
    user_id, user_first_name = extract_user(client, message)
    try:
        await message.chat.add_members(user_id=user_id)
        if str(user_id).lower().startswith("@"):
            await message.edit(f"**Added** {user_first_name}")
            await client.send_message(PRIVATE_GROUP_ID, f"#INVITE\nAdded {user_first_name} in chat {message.chat.title}")
        else:
            await message.edit(f"**Added** <a herf='tg://user?id={user_id}'>{user_first_name}</a>")
            await client.send_message(PRIVATE_GROUP_ID, f"#INVITE\nAdded {mention_markdown(user_first_name, user_id)} in chat {message.chat.title}")
    except Exception as ef:
        await message.edit(f"<b>Error:</b>\n`{ef}`")
        return
