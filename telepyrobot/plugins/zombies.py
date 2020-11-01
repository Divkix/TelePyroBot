from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER, PRIVATE_GROUP_ID
import os
import asyncio


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Have lot of deleted account's in your group? Want to get rid of them?
Then this module is for you!

**Usage:**
`{COMMAND_HAND_LER}zombies`: Check the number of deleted accounts in a group and display them.
`{COMMAND_HAND_LER}zombies clean`: Remove all the deleted accounts from the group!

**Note:** Clean only works in groups where you are admin!
"""


@TelePyroBot.on_message(filters.command("zombies", COMMAND_HAND_LER) & filters.me)
async def zombies_clean(c: TelePyroBot, m: Message):
    if len(m.text.split(" ")) != 2:
        await m.edit_text("`Counting deleted accounts!!!`")
        del_users = []
        async for x in c.iter_chat_members(chat_id=m.chat.id):
            if x.user.is_deleted:
                del_users.append(x.user.id)
        if del_users:
            await m.edit_text(
                f"`Found {len(del_users)} deleted accounts!` **__Use__** `{COMMAND_HAND_LER}zombies clean` __**to remove them from group**__"
            )
        else:
            await m.edit_text("`No deleted accounts found!\nGroup is clean as Hell!`")
    elif len(m.text.split(" ")) == 2 and m.text.split(None, 1)[1] == "clean":
        await m.edit_text("`Cleaning deleted accounts....`")
        del_users = []
        u = 0
        async for x in c.iter_chat_members(chat_id=m.chat.id):
            await asyncio.sleep(0.1)
            if x.user.is_deleted:
                del_users.append(x.user.id)
                a = await c.get_chat_member(m.chat.id, x.user.id)
                if a.user.status not in ("administrator", "creator"):
                    try:
                        await c.kick_chat_member(m.chat.id, x.user.id)
                        u += 1
                        await asyncio.sleep(0.1)
                    except:
                        pass
        await m.edit_text(f"**Done Cleaning Group ✅**\n`Removed {u} deleted accounts`")
        await c.send_message(
            PRIVATE_GROUP_ID,
            f"#ZOMBIES\n\nCleaned {len(del_users)} accounts from **{m.chat.title}** - `{m.chat.id}`",
        )
    else:
        await m.edit_text(
            f"__Check__ `{COMMAND_HAND_LER}help zombies` __to see how it works!__"
        )
    return
