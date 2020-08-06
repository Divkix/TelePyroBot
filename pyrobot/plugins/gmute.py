import os
import asyncio
from pyrobot.utils.sql_helpers import gmute_sql as db
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, PRIVATE_GROUP_ID
from pyrobot.utils.pyrohelpers import extract_user
from pyrobot.utils.parser import mention_markdown

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Gmute users easily!
They will not be able to speak until you ungmute them!

**Commands:**
`{COMMAND_HAND_LER}gmute` as a reply to user or entering user id
`{COMMAND_HAND_LER}ungmute` as a reply to user or entering user id
`{COMMAND_HAND_LER}gmutelist`: List all the gmute users
"""

GMUTE_USERS = []

@Client.on_message(Filters.command("gmute", COMMAND_HAND_LER) & Filters.me)
async def start_sgmute(client, message):
    global GMUTE_USERS
    await message.edit("`Putting duct tape...`")
    user_id, user_first_name = await extract_user(client, message)
    if db.is_gmuted(user_id):
        await message.edit("`This user is already gmuted!`")
        return
    try:
        db.gmute(user_id)
    except Exception as e:
        await message.edit(f"<b>Error:</b>\n\n{str(e)}")
    else:
        await message.edit("`Successfully gmuted that person`")
        await client.send_message(PRIVATE_GROUP_ID,
            "#GMUTE\nUser:{} in Chat {}".format(mention_markdown(user_first_name, user_id), message.chat.title))
    GMUTE_USERS = db.get_gmute_users()
    return


@Client.on_message(Filters.command("ungmute", COMMAND_HAND_LER) & Filters.me)
async def end_gmute(client, message):
    global GMUTE_USERS
    await message.edit("`Removing duct tape...`")
    user_id, user_first_name = await extract_user(client, message)

    if not db.is_gmuted(user_id):
        await message.edit("`This user is not gmuted!`")
        return
    try:
        db.ungmute(user_id)
    except Exception as e:
        await message.edit(f"<b>Error:</b>\n\n{str(e)}")
    else:
        await message.edit("`Successfully ungmuted that person`")
        await client.send_message(PRIVATE_GROUP_ID,
            "#UNGMUTE\nUser: {} in Chat {}".format(mention_markdown(user_first_name, user_id), message.chat.title))
    GMUTE_USERS = db.get_gmute_users()
    return


@Client.on_message(Filters.command("gmutelist", COMMAND_HAND_LER) & Filters.me)
async def list_gmuted(client, message):
    global GMUTE_USERS
    await message.edit("`Loading users...`")
    GMUTE_USERS = db.get_gmute_users()
    if not GMUTE_USERS:
        await message.edit("`No users are gmuted!`")
        return
    users_list = "`Currently Gmuted users:`\n"
    u = 0
    for x in GMUTE_USERS:
        u += 1
        user = await client.get_users(x)
        users_list += f"[{u}] {mention_markdown(user.first_name, user.id)}: {user.id}\n"
    await message.edit(users_list)
    return


@Client.on_message(Filters.user(GMUTE_USERS), group=5)
async def watcher_gmute(client, message):
    if db.is_gmuted(message.from_user.id):
        try:
            await client.delete_messages(
                chat_id=message.chat.id,
                message_ids=message.message_id)
        except:
            pass
    return
