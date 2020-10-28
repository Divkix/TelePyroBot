from pyrogram.types import Message
from telepyrobot.__main__ import TelePyroBot


def ReplyCheck(m: Message):
    reply_id = None

    if m.reply_to_message:
        reply_id = m.reply_to_message.message_id

    elif not m.from_user.is_self:
        reply_id = m.message_id

    return reply_id


async def extract_user(c: Client, m: Message):
    user_id = None
    user_first_name = None

    if m.reply_to_message:
        user_id = m.reply_to_message.from_user.id
        user_first_name = m.reply_to_message.from_user.first_name

    elif not m.reply_to_message:
        if len(m.text.split()) >= 2:
            user = await c.get_users(m.command[1])
            user_id = user.id
            user_first_name = user.first_name

    else:
        user_id = m.from_user.id
        user_first_name = m.from_user.first_name

    return user_id, user_first_name