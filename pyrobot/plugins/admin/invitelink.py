from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import sudo_filter
from pyrobot.helper_functions.admin_check import admin_check

@Client.on_message(Filters.command("invitelink", COMMAND_HAND_LER) & sudo_filter)
async def invitelink(client, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    chat_id = message.chat.id
    link = client.export_chat_invite_link(chat_id)
    await message.reply_text(link)
