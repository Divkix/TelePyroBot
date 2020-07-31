from pyrobot.utils.sql_helpers import gmute_sql as db
import asyncio
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, PRIVATE_GROUP_ID
import os
from pyrobot.utils.pyrohelpers import extract_user


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Gmute users easily!
They will not be able to speak until you ungmute them!

**Commands:**
`{COMMAND_HAND_LER}gmute` as a reply to user or entering user id
`{COMMAND_HAND_LER}ungmute` as a reply to user or entering user id
"""


@Client.on_message(Filters.command("gmute", COMMAND_HAND_LER) & Filters.me)
async def start_sgmute(client, message):
    await message.edit("`Putting duct tape...`")
    user_id, user_first_name = extract_user(message)

    if db.is_gmuted(user_id):
        await message.edit("`This user is already gmuted!`")
        return
    try:
        db.gmute(user_id)
    except Exception as e:
        await message.edit(f"<b>Error:</b>\n\n{str(e)}")
    else:
        await message.edit("`Successfully gmuted that person`")
        await client.send_message(PRIVATE_GROUP_ID, f"#GMUTE\nUser:<a herf='tg://user?id={user_id}'>{user_first_name}</a>\nChat: {message.chat.title} (`{message.chat.id}`)")
    return


@Client.on_message(Filters.command("ungmute", COMMAND_HAND_LER) & Filters.me)
async def end_gmute(client, message):
    await message.edit("`Removing duct tape...`")
    user_id, user_first_name = extract_user(message)

    if not db.is_gmuted(user_id):
        await message.edit("`This user is not gmuted!`")
        return
    try:
        db.ungmute(user_id)
    except Exception as e:
        await message.edit(f"<b>Error:</b>\n\n{str(e)}")
    else:
        await message.edit("`Successfully ungmuted that person`")
        await client.send_message(PRIVATE_GROUP_ID, f"#UNGMUTE\nUser:<a herf='tg://user?id={user_id}'>{user_first_name}</a>\nChat: {message.chat.title} (`{message.chat.id}`)")
    return

@Client.on_message(Filters.command("gmutelist", COMMAND_HAND_LER) & Filters.me)
async def list_gmuted(client, message):
    await message.edit("`Loading users...`")
    users = db.get_gmute_users()
    users_list = "`Currently Gmuted users:`\n"
    for x in users:
        user = client.get_users(x)
        users_list += f"{user.first_name}: {user.id}"
    await message.edit(users_list)
    return


@Client.on_message(Filters.group, group=5)
async def watcher(client, message):
    if db.is_gmuted(message.from_user.id):
        try:
            await client.delete_messages(
                chat_id=message.chat.id,
                message_ids=message.message_id)
        except Exception as err:
            print(f"Could not delete message!\nError:\n\n{str(err)}")
    return
