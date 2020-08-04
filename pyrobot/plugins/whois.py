import os
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.utils.parser import mention_markdown

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}whois` / info <username/userid> or as a reply to message: Get the information about a user.
"""

@Client.on_message(Filters.command(["whois", "info"], COMMAND_HAND_LER) & Filters.me)
async def upload_as_document(client, message):
    await message.edit("`Collecting Whois Info.. Hang on!`")
    if len(message.command) == 2:
        user_id = message.command[1]
        try:
            from_user = await client.get_users(user_id)
        except Exception:
            await message.edit("`no valid user_id or message specified`")
            return
    elif message.reply_to_message:
        if message.reply_to_message.forward_from:
            from_user = await client.get_users(message.reply_to_message.forward_from.id)
        else:
            from_user = await client.get_users(message.reply_to_message.from_user.id)
    else:
        await message.edit("`no valid user_id or message specified`")
        return
    if from_user is not None:
        pp_c = await client.get_profile_photos_count(from_user.id)
        message_out_str = "<b>USER INFO:</b>\n\n"
        message_out_str += f"<b>First Name:</b> <code>{from_user.first_name}</code>\n"
        message_out_str += f"<b>Last Name:</b> <code>{from_user.last_name}</code>\n"
        message_out_str += f"<b>Username:</b> @{from_user.username}\n"
        message_out_str += f"<b>User ID:</b> <code>{from_user.id}</code>\n"
        message_out_str += "<b>Permanent Link To Profile:</b> "
        message_out_str += f"{mention_markdown(from_user.first_name, from_user.id)}"

        await message.edit(message_out_str)
        return
