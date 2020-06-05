from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.admin_check import admin_check
from pyrobot.helper_functions.extract_user import extract_user

from pyrobot.helper_functions.cust_p_filters import sudo_filter

@Client.on_message(Filters.command(["unban", "unmute"], COMMAND_HAND_LER) & sudo_filter)
async def un_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.unban_member(
            user_id=user_id
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "Well, that has changed ... and now"
                f"{user_first_name} ക്ക് "
                "You can join the group!"
            )
        else:
            await message.reply_text(
                "Well, that has changed ... and now"
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a> ക്ക് "
                "You can join the group!"
            )
