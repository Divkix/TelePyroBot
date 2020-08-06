from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, PRIVATE_GROUP_ID
import os


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ =  f"""
Have lot of deleted account's in your group? Want to get rid of them?
Then this module is for you!

**Usage:**
`{COMMAND_HAND_LER}zombies`: Check the number of deleted accounts in a group and display them.
`{COMMAND_HAND_LER}zombies clean`: Remove all the deleted accounts from the group!

**Note:** Clean only works in groups where you are admin!
"""

@Client.on_message(Filters.command("zombies", COMMAND_HAND_LER) & Filters.me)
async def zombies_clean(client, message):
    if len(message.text.split(" ")) != 2:
        await message.edit("`Counting deleted accounts!!!`")
        del_users = []
        async for x in client.iter_chat_members(chat_id=message.chat.id):
            if x.user.is_deleted:
                del_users.append(x.user.id)
        if del_users:
        	await message.edit(f"`Found {len(del_users)} deleted accounts!` **__Use__** `{COMMAND_HAND_LER}zombies clean` __**to remove them from group**__")
    	else:
    		await message.edit("`No deleted accounts found!\nGroup is clean as Hell!`")
    elif len(message.text.split(" ")) == 2 and message.text.split(" ",1)[1] == "clean":
        await message.edit("`Cleaning deleted accounts....`")
        del_users = []
        u = 0
        async for x in client.iter_chat_members(chat_id=message.chat.id):
            await asyncio.sleep(0.5)
            if x.user.is_deleted:
                del_users.append(x.user.id)
                a = await client.get_chat_member(message.chat.id, x.user.id)
                if a.user.status not in ("administrator", "creator"):
                    try:
                        await client.kick_chat_member(message.chat.id, x.user.id)
                        u += 1
                        await asyncio.sleep(0.5)
                    except:
                        pass
        await message.edit(f"**Done Cleaning Group ✅**\n`Removed {u} deleted accounts`")
        await client.send_message(PRIVATE_GROUP_ID, f"#ZOMBIES\n\nCleaned {len(del_users)} accounts from **{message.chat.title}** - `{message.chat.id}`")
    else:
        await message.edit(f"__Check__ `{COMMAND_HAND_LER}help zombies` __to see how it works!__")
    return
