import os
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER
from telepyrobot.utils.parser import mention_markdown
from telepyrobot.utils.pyrohelpers import extract_user

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}whois` / info <username/userid> or as a reply to message: Get the information about a user.
"""


@TelePyroBot.on_message(
    filters.command(["whois", "info"], COMMAND_HAND_LER) & filters.me
)
async def upload_as_document(c: TelePyroBot, m: Message):
    await m.edit_text("`Collecting Whois Info.. Hang on!`")
    user_id, user_first_name = await extract_user(c, m)
    if user_id is not None:
        from_user = await c.get_users(user_id)
        message_out_str = (
            "<b>Fetched information from</b> @TelePyroBot <b>Database<!/b>\n"
        )
        message_out_str += (
            f"    <b>First Name:</b> <code>{from_user.first_name}</code>\n"
        )
        if from_user.last_name:
            message_out_str += (
                f"    <b>Last Name:</b> <code>{from_user.last_name}</code>\n"
            )
        message_out_str += f"    <b>Username:</b> @{from_user.username}\n"
        message_out_str += f"    <b>User ID:</b> <code>{from_user.id}</code>\n"
        message_out_str += f"    <b>Permanent Link To Profile:</b> {mention_markdown(from_user.first_name, from_user.id)}"
        await m.edit_text(message_out_str)
    else:
        await m.edit_text("`**Error:**\nCannot find user or error, please check logs!`")
    return
