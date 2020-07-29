from pyrogram import Filters, Client
from pyrobot import COMMAND_HAND_LER
from pyrobot.utils.msg_types import Types, get_note_type
from pyrobot.utils.sql_helpers import notes_db as db


@Client.on_message(Filters.command(["notes", "saved"], COMMAND_HAND_LER) & Filters.me)
async def local_notes(client, message):
    getnotes = db.get_all_chat_notes()
    if not getnotes:
        await message.edit("`There are no notes!`")
        return
    rply = "**Local notes:**\n"
    for x in getnotes:
        if len(rply) >= 1800:
            await message.reply(rply)
            rply = "**Local notes:**\n"
        rply += f"- `{x}`\n"
    await message.edit(rply)
    return


@Client.on_message(Filters.command("num_notes", COMMAND_HAND_LER) & Filters.me)
async def num_local_notes(client, message):
    num_notes = db.num_notes()
    await message.edit("`There are {} notes!`".format(num_notes))
    return
