import os
from pyrogram import Filters, Client
from pyrobot import COMMAND_HAND_LER

from pyrobot.utils.sql_helpers.chats_db import update_chat, get_all_chats

MESSAGE_RECOUNTER = 0

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))
__HELP__ = f"""
This module is to manage your chats, when message was received from unknown chat, and that chat was not in database, then save that chat info to your database.
**Export chats**
`{COMMAND_HAND_LER}chatlist`
Send your chatlist to your saved messages.
"""


def get_msgc():
    return MESSAGE_RECOUNTER

@Client.on_message(Filters.group, group=10)
async def updatemychats(client, message):
    global MESSAGE_RECOUNTER
    update_chat(message.chat)
    MESSAGE_RECOUNTER += 1


@Client.on_message(Filters.me & Filters.command("chatlist", COMMAND_HAND_LER))
async def get_chat(client, message):
    await message.edit("`Exporting Chatlist...`")
    all_chats = get_all_chats()
    chatfile = '<---List of chats that you joined--->\n\n'
    u = 0
    for chat in all_chats:
        u += 1
        if str(chat.chat_username) != "None":
            chatfile += "[{}] {} - ({}): @{}\n".format(u, chat.chat_name, chat.chat_id, chat.chat_username)
        else:
            chatfile += "[{}] {} - ({})\n".format(u, chat.chat_name, chat.chat_id)
    chatlist_file = "pyrobot/cache/chatlist.txt"
    with open(chatlist_file, "w", encoding="utf-8") as f:
        f.write(str(chatfile))
        f.close()

    await client.send_document("self", document=chatlist_file,
                               caption="Here is the chat list that you joined.")
    await message.edit("`Chat list exported to my saved messages.`")
    os.remove(chatlist_file)
