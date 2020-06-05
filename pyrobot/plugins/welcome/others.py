from pyrogram import (
    Client,
    Filters
)

from pyrobot import (
    COMMAND_HAND_LER,
    DB_URI,
    MAX_MESSAGE_LENGTH
)

from pyrobot.helper_functions.admin_check import admin_check
from pyrobot.helper_functions.cust_p_filters import sudo_filter
if DB_URI is not None:
    import pyrobot.helper_functions.sql_helpers.welcome_sql as sql


@Client.on_message(Filters.command(["clearwelcome", "resetwelcome"], COMMAND_HAND_LER) & sudo_filter)
async def clear_note(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    status_message = await message.reply_text(
        "Checking....",
        quote=True
    )
    sql.rm_welcome_setting(message.chat.id)
    await status_message.edit_text(
        "Welcome message cleared from current chat."
    )
