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
    rply = "**Local notes:**\n" + get_notes
    await message.edit(rply)
    return


@Client.on_message(Filters.command("notesnum", COMMAND_HAND_LER) & Filters.me)
async def num_local_notes(client, message):
    num_notes = db.num_notes(message.from_user.id)
    await message.edit("`There are {} notes!`".format(num_notes))
    return


@Client.on_message(Filters.command("save", COMMAND_HAND_LER) & Filters.me)
async def save_notes(client, message):
    if message.reply_to_message and len(message.text.split(" ",1)) == 2:
        notename = message.text.split(" ",1)[1]
        text_data = message.reply_to_message.text
    else:
        await message.edit("`Only Text messages supported right now`")
        return
    db.add_note_to_db(message.from_user.id, notename, text_data)
    await message.edit(f"`Saved note {notename}`")
    return


@Client.on_message(Filters.command("get", COMMAND_HAND_LER) & Filters.me)
async def get_notes(client, message):
    if len(message.text.split(" ",1)) == 2:
        notename = message.text.split(" ",1)[1]
    else:
        await message.edit(f"__Use `{COMMAND_HAND_LER}get <notename>` __to get the note!__`",
                    parse_mode="markdown")
    note_data = db.get_note(message.from_user.id, notename)
    await message.edit(note_data, parse_mode="html")
    return
