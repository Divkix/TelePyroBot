import time
from pyrogram import Client, Filters
from pyrobot.utils.list_to_string import listToString
from pyrobot import COMMAND_HAND_LER

@Client.on_message(Filters.command("fban", COMMAND_HAND_LER) & Filters.me)
async def fban_user(client, message):
    fban_msg = listToString(message.command[1:])
    await client.send_message("@MissRose_bot", f"/fban {fban_msg}")
    time.sleep(2)
    msg = await client.get_history("@MissRose_bot", 1)
    msg_id = msg[0]["message_id"]
    await client.forward_messages(message.chat.id, "@MissRose_bot", msg_id)
    await client.read_history("@MissRose_bot")
    await message.delete()
