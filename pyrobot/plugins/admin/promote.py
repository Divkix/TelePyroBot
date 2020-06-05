from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.extract_user import extract_user
from pyrobot.helper_functions.cust_p_filters import sudo_filter

@Client.on_message(Filters.command("promote", COMMAND_HAND_LER) & sudo_filter)
async def promote(client, message):
    status_message = await message.reply_text("Promoting user...")
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
        user_id=from_user.id
        await message.promote_chat_member(user_id)
        await status_message.edit("Promoted Successfully, gib Party!")
