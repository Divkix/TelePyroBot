import os
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER
from telepyrobot.utils.parser import mention_html, mention_markdown

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Tag people Easily!

`{COMMAND_HAND_LER}adminlist` / admins: Returns the list of admins of group.

`{COMMAND_HAND_LER}all` / everyone: Tags All the users of group.
"""


@TelePyroBot.on_message(
    filters.command(["adminlist", "admins"], COMMAND_HAND_LER) & filters.me
)
async def adminlist(c: TelePyroBot, m: Message):
    replyid = None
    toolong = False
    if len(m.text.split()) >= 2:
        chat = m.text.split(None, 1)[1]
        grup = await c.get_chat(chat)
    else:
        chat = m.chat.id
        grup = await c.get_chat(chat)
    if m.reply_to_message:
        replyid = m.reply_to_message.message_id
    alladmins = c.iter_chat_members(chat, filter="administrators")
    creator = []
    admin = []
    badmin = []
    async for a in alladmins:
        try:
            nama = a.user.first_name + " " + a.user.last_name
        except:
            nama = a.user.first_name
        if nama is None:
            nama = "☠️ Deleted account"
        if a.status == "administrator":
            if a.user.is_bot:
                badmin.append(mention_markdown(nama, a.user.id))
            else:
                admin.append(mention_markdown(nama, a.user.id))
        elif a.status == "creator":
            creator.append(mention_markdown(nama, a.user.id))
    admin.sort()
    badmin.sort()
    totaladmins = len(creator) + len(admin) + len(badmin)
    teks = f"**Admins in {grup.title}**\n"
    teks += "「 Creator 」\n"
    for x in creator:
        teks += f"│ • {x}\n"
        if len(teks) >= 4096:
            await m.reply_text(
                m.chat.id, teks, reply_to_message_id=replyid, parse_mode="md"
            )
            teks = ""
            toolong = True
    teks += f"「 {len(admin)} Human Administrator 」\n"
    for x in admin:
        teks += f"│ • {x}\n"
        if len(teks) >= 4096:
            await m.reply_text(
                m.chat.id, teks, reply_to_message_id=replyid, parse_mode="md"
            )
            teks = ""
            toolong = True
    teks += f"「 {len(badmin)} Bot Administrator 」\n"
    for x in badmin:
        teks += f"│ • {x}\n"
        if len(teks) >= 4096:
            await m.reply_text(
                m.chat.id, teks, reply_to_message_id=replyid, parse_mode="md"
            )
            teks = ""
            toolong = True
    teks += f"「 Total {totaladmins} Admins 」"
    if toolong:
        await m.reply_text(
            m.chat.id, teks, reply_to_message_id=replyid, parse_mode="md"
        )
    else:
        await m.edit_text(teks, parse_mode="md")


@TelePyroBot.on_message(
    filters.command(["everyone", "all"], COMMAND_HAND_LER) & filters.me
)
async def everyone(c: TelePyroBot, m: Message):
    await m.delete()
    if len(m.text.split()) >= 2:
        text = m.text.split(None, 1)[1]
    else:
        text = "Hi all 🙃"
    kek = c.iter_chat_members(m.chat.id)
    async for a in kek:
        if not a.user.is_bot:
            text += mention_html(a.user.id, "\u200b")
    if m.reply_to_message:
        await c.send_message(
            m.chat.id,
            text,
            reply_to_message_id=m.reply_to_message.message_id,
            parse_mode="html",
        )
    else:
        await c.send_message(m.chat.id, text, parse_mode="html")


@TelePyroBot.on_message(
    filters.command(["bots", "listbots"], COMMAND_HAND_LER) & filters.me
)
async def listbots(c: TelePyroBot, m: Message):
    replyid = None
    if len(m.text.split()) >= 2:
        chat = m.text.split(None, 1)[1]
        grup = await c.get_chat(chat)
    else:
        chat = m.chat.id
        grup = await c.get_chat(chat)
    if m.reply_to_message:
        replyid = m.reply_to_message.message_id
    getbots = c.iter_chat_members(chat)
    bots = []
    async for a in getbots:
        try:
            nama = a.user.first_name + " " + a.user.last_name
        except:
            nama = a.user.first_name
        if nama is None:
            nama = "☠️ Deleted account"
        if a.user.is_bot:
            bots.append(mention_markdown(nama, a.user.id))
    teks = f"**All bots in group {grup.title}**\n"
    teks += "Bots\n"
    for x in bots:
        teks += f"│ • {x}\n"
    teks += f"Total {len(bots)} Bots"
    if replyid:
        await c.send_message(
            m.chat.id, teks, reply_to_message_id=replyid, parse_mode="md"
        )
    else:
        await m.edit_text(teks, parse_mode="md")
