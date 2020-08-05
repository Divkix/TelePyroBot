from pyrogram import Message, Client


def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id

async def extract_user(client, message: Message) -> (int, str):
    user_id = None
    user_first_name = None

    if len(message.command) == 2 and not message.reply_to_message and message.command[1].startswith("@"):
        user = await client.get_users(message.command[1])
        user_id = user.id
        user_first_name = user.first_name
        return user_id, user_first_name

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_first_name = message.reply_to_message.from_user.first_name
        return user_id, user_first_name

    if len(message.command) > 1 and not message.command[1].startswith("@"):
        if len(message.entities) >= 1:
            required_entity = message.entities[-1]
            if required_entity.type == "text_mention":
                user_id = required_entity.user.id
                user_first_name = required_entity.user.first_name
            elif required_entity.type == "mention":
                user_id = message.text[
                    required_entity.offset:
                    required_entity.offset + required_entity.length
                ]
                user_first_name = user_id

    else:
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name

    return user_id, user_first_name
