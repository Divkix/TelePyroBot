import os
import asyncio
from telepyrobot.setclient import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot.db import gmute_db as db
from telepyrobot import COMMAND_HAND_LER, PRIVATE_GROUP_ID
from telepyrobot.utils.pyrohelpers import extract_user
from telepyrobot.utils.parser import mention_markdown

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Gmute users easily!
They will not be able to speak until you ungmute them!

**Commands:**
`{COMMAND_HAND_LER}gmute` as a reply to user or entering user id
`{COMMAND_HAND_LER}ungmute` as a reply to user or entering user id
`{COMMAND_HAND_LER}gmutelist`: To view list of currently gmuted users
"""


@TelePyroBot.on_message(filters.command("gmute", COMMAND_HAND_LER) & filters.me)
async def start_gmute(c: TelePyroBot, m: Message):
    await m.edit_text("`Putting duct tape...`")
    user_id, user_first_name = await extract_user(m)
    if db.is_gmuted(user_id):
        await m.edit_text("`This user is already gmuted!`")
        return
    try:
        db.gmute(user_id)
    except Exception as e:
        await m.edit_text(f"<b>Error:</b>\n\n{str(e)}")
    else:
        await m.edit_text("`Successfully gmuted that person`")
        await c.send_message(
            PRIVATE_GROUP_ID,
            "#GMUTE\nUser: {} in Chat {}".format(
                mention_markdown(user_first_name, user_id), m.chat.title
            ),
        )
    return


@TelePyroBot.on_message(filters.command("ungmute", COMMAND_HAND_LER) & filters.me)
async def end_gmute(c: TelePyroBot, m: Message):
    await m.edit_text("`Removing duct tape...`")
    user_id, user_first_name = await extract_user(m)

    if not db.is_gmuted(user_id):
        await m.edit_text("`This user is not gmuted!`")
        return
    try:
        db.ungmute(user_id)
    except Exception as e:
        await m.edit_text(f"<b>Error:</b>\n\n{str(e)}")
    else:
        await m.edit_text("`Successfully ungmuted that person`")
        await c.send_message(
            PRIVATE_GROUP_ID,
            "#UNGMUTE\nUser: {} in Chat {}".format(
                mention_markdown(user_first_name, user_id), m.chat.title
            ),
        )
    return


@TelePyroBot.on_message(filters.command("gmutelist", COMMAND_HAND_LER) & filters.me)
async def list_gmuted(c: TelePyroBot, m: Message):
    await m.edit_text("`Loading users...`")
    users = db.get_gmute_users()
    if not users:
        await m.edit_text("`No users are gmuted!`")
        return
    users_list = "`Currently Gmuted users:`\n"
    u = 0
    for x in users:
        u += 1
        user = await c.get_users(x)
        users_list += f"[{u}] {mention_markdown(user.first_name, user.id)}: {user.id}\n"
    await m.edit_text(users_list)
    return


@TelePyroBot.on_message(filters.group, group=5)
async def watcher_gmute(c: TelePyroBot, m: Message):
    try:
        if db.is_gmuted(m.from_user.id):
            await asyncio.sleep(0.1)
            await c.delete_messages(chat_id=m.chat.id, message_ids=m.message_id)
    except AttributeError:
        pass
    except Exception as ef:
        print(ef)
    return
