from telepyrobot.__main__ import TelePyroBot
from pyrogram.types import Message
import asyncio


async def admin_check(c: TelePyroBot, m: Message):
    chat_id = m.chat.id
    user_id = m.from_user.id

    check_status = await c.get_chat_member(chat_id=chat_id, user_id=user_id)
    admin_strings = ["creator", "administrator"]
    if check_status.status not in admin_strings:
        await m.edit("`I'm not admin nub nibba!`")
        await asyncio.sleep(2)
        await m.delete()
        return False

    return True
