import os
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER

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
            from_chat = await client.get_chat(user_id)
        except Exception:
            await message.edit("`no valid user_id or message specified`")
            return
    elif message.reply_to_message:
        from_user = await client.get_users(message.reply_to_message.from_user.id)
        from_chat = await client.get_chat(message.reply_to_message.from_user.id)
    elif message.reply_to_message.forward_from:
        from_user = await client.get_users(message.reply_to_message.forward_from.from_user.id)
        from_chat = await client.get_chat(message.reply_to_message.forward_from.from_user.id)
    else:
        await message.edit("`no valid user_id or message specified`")
        return
    if from_user or from_chat is not None:
        pp_c = await client.get_profile_photos_count(from_user.id)
        message_out_str = "<b>USER INFO:</b>\n\n"
        message_out_str += f"<b>First Name:</b> <code>{from_user.first_name}</code>\n"
        message_out_str += f"<b>Last Name:</b> <code>{from_user.last_name}</code>\n"
        message_out_str += f"<b>Username:</b> @{from_user.username}\n"
        message_out_str += f"<b>DC ID:</b> <code>{from_user.dc_id}</code>\n"
        message_out_str += f"<b>Is Bot:</b> <code>{from_user.is_bot}</code>\n"
        message_out_str += f"<b>Is Restricted:</b> <code>{from_user.is_scam}</code>\n"
        message_out_str += "<b>Is Verified by Telegram:</b> "
        message_out_str += f"<code>{from_user.is_verified}</code>\n"
        message_out_str += f"<b>User ID:</b> <code>{from_user.id}</code>\n"
        message_out_str += f"<b>Profile Photos:</b> <code>{pp_c}</code>\n"
        message_out_str += f"<b>Bio:</b> <code>{from_chat.description}</code>\n\n"
        message_out_str += f"<b>Last Seen:</b> <code>{from_user.status}</code>\n"
        message_out_str += "<b>🔗 Permanent Link To Profile:</b> "
        message_out_str += f"<a href='tg://user?id={from_user.id}'>{from_user.first_name}</a>"

        if from_user.photo:
            local_user_photo = await client.download_media(message=from_user.photo.big_file_id)
            await client.send_photo(chat_id=message.chat.id,
                                    photo=local_user_photo,
                                    caption=message_out_str,
                                    parse_mode="html",
                                    disable_notification=True)
            os.remove(local_user_photo)
            await message.delete()
        else:
            message_out_str = "<b>NO DP Found 📷</b>\n\n" + message_out_str
            await message.edit(message_out_str)
