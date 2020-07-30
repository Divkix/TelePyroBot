from pyrobot.utils.sql_helpers.gmute_sql import is_gmuted, gmute, ungmute
import asyncio
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, PRIVATE_GROUP_ID
import os
from pyrobot.utils.pyrohelpers import extract_user


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Gmute users easily!
They will not be able to speak until you gmute them!

**Commands:**
`{COMMAND_HAND_LER}gmute` as a reply to user or entering user id
`{COMMAND_HAND_LER}ungmute` as a reply to user or entering user id
"""


@Client.on_message(Filters.command("gmute", COMMAND_HAND_LER) & Filters.me)
async def startgmute(client, message):
    await message.edit("`Putting duct tape...`")
    user_id, user_first_name = extract_user(message)

    if is_gmuted(user_id,):
        await message.edit("`This user is already gmuted!`")
        return
    try:
        gmute(user_id)
    except Exception as e:
        await message.edit(f"<b>Error:</b>\n\n{str(e)}")
    else:
        await message.edit("Successfully gmuted that person")
        await client.send_message(PRIVATE_GROUP_ID, f"#GMUTE\nUser:<a herf='tg://user?id={user_id}'>{user_first_name}</a>\nChat: {message.chat.title} (`{message.chat.id}`)")
    return


@Client.on_message(Filters.command("ungmute", COMMAND_HAND_LER) & Filters.me)
async def endgmute(client, message):
    await message.edit("`Removing duct tape...`")
    user_id, user_first_name = extract_user(message)

    if not is_gmuted(user_id):
        await message.edit("`This user is not gmuted!`")
        return
    try:
        ungmute(user_id)
    except Exception as e:
        await message.edit(f"<b>Error:</b>\n\n{str(e)}")
    else:
        await message.edit("Successfully ungmuted that person")
        await client.send_message(PRIVATE_GROUP_ID, f"#UNGMUTE\nUser:<a herf='tg://user?id={user_id}'>{user_first_name}</a>\nChat: {message.chat.title} (`{message.chat.id}`)")
    return


@Client.on_message(Filters.group)
async def watcher(client, message):
    if is_gmuted(message.from_user.id):
        try:
            await client.delete_messages(
                chat_id=message.chat.id,
                message_ids=message.message_id
            )
        except Exception as err:
            print(f"Could not delete message!\nError:\n\n{str(err)}")
    return