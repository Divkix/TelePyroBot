"""Get info about the replied user
Syntax: .whois"""

import os

from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER
from pyrobot.utils.extract_user import extract_user

from pyrobot.utils.cust_p_filters import sudo_filter

@Client.on_message(Filters.command(["whois", "info"], COMMAND_HAND_LER) & sudo_filter)
async def who_is(client, message):
    """ extract user information """
    status_message = await message.reply_text(
        "Finding user...."
    )
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        user_id = from_user_id
        if not str(user_id).startswith("@"):
            user_id = int(user_id)
        from_user = await client.get_users(user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        await status_message.edit("No valid user_id / message specified")
    else:
        msg = ""
        msg += f"ID: <code>{from_user.id}</code>\n"
        msg += f"First Name: <a href='tg://user?id={from_user.id}'>"
        msg += from_user.first_name
        msg += "</a>\n"
        msg += f"Last Name: {from_user.last_name}\n"
        msg += f"DC ID: <code>{from_user.dc_id}</code>\n"
        await message.reply_text(
                text=msg,
                quote=True,
                parse_mode="html",
                disable_notification=True
            )
        await status_message.delete()
