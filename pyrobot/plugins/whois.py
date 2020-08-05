import os
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.utils.parser import mention_markdown
from pyrobot.utils.pyrohelpers import extract_user

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}whois` / info <username/userid> or as a reply to message: Get the information about a user.
"""

@Client.on_message(Filters.command(["whois", "info"], COMMAND_HAND_LER) & Filters.me)
async def upload_as_document(client, message):
    await message.edit("`Collecting Whois Info.. Hang on!`")
    user_id, user_first_name = await extract_user(client, message)
    if user_id is not None:
        from_user = await client.get_users(user_id)
        message_out_str = "<b>USER INFO:</b>\n\n"
        message_out_str += f"  <b>First Name:</b> <code>{from_user.first_name}</code>\n"
        if from_user.last_name:
            message_out_str += f"  <b>Last Name:</b> <code>{from_user.last_name}</code>\n"
        message_out_str += f"  <b>Username:</b> @{from_user.username}\n"
        message_out_str += f"  <b>User ID:</b> <code>{from_user.id}</code>\n"
        message_out_str += f"  <b>Permanent Link To Profile:</b> {mention_markdown(from_user.first_name, from_user.id)}"
        await message.edit(message_out_str)
    else:
        await message.edit("`**Error:**\nCannot find user or error, please check logs!s`")
