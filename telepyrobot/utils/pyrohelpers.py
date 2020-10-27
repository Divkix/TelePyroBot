from pyrogram.types import Message
from telepyrobot.__main__ import TelePyroBot


def ReplyCheck(m: Message):
    reply_id = None

    if m.reply_to_message:
        reply_id = m.reply_to_message.message_id

    elif not m.from_user.is_self:
        reply_id = m.message_id

    return reply_id


async def extract_user(c: TelePyroBot, m: Message) -> (int, str):
    user_id = None
    user_first_name = None

    if len(m.command) == 2 and not m.reply_to_message and m.command[1].startswith("@"):
        user = await c.get_users(m.command[1])
        user_id = user.id
        user_first_name = user.first_name
        return user_id, user_first_name

    if m.reply_to_message:
        user_id = m.reply_to_message.from_user.id
        user_first_name = m.reply_to_message.from_user.first_name
        return user_id, user_first_name

    if len(m.command) > 1 and not m.command[1].startswith("@"):
        if len(m.entities) >= 1:
            required_entity = m.entities[-1]
            if required_entity.type == "text_mention":
                user_id = required_entity.user.id
                user_first_name = required_entity.user.first_name
            elif required_entity.type == "mention":
                user_id = m.text[
                    required_entity.offset : required_entity.offset
                    + required_entity.length
                ]
                user_first_name = user_id

    else:
        user_id = m.from_user.id
        user_first_name = m.from_user.first_name

    return user_id, user_first_name
