import os
from pyrogram import Client, filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER
from telepyrobot.utils.parser import mention_html, mention_markdown

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Tag people Easily!

`{COMMAND_HAND_LER}adminlist` \ admins: Returns the list of admins of group.

`{COMMAND_HAND_LER}all` \ everyone: Tags All the users of group.
"""


@Client.on_message(
    filters.command(["adminlist", "admins"], COMMAND_HAND_LER) & filters.me
)
async def adminlist(c: Client, m: Message):
    replyid = None
    toolong = False
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
        grup = await client.get_chat(chat)
    else:
        chat = message.chat.id
        grup = await client.get_chat(chat)
    if m.reply_to_message:
        replyid = m.reply_to_message.message_id
    alladmins = client.iter_chat_members(chat, filter="administrators")
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
    teks = "**Admins in {}**\n".format(grup.title)
    teks += "「 Creator 」\n"
    for x in creator:
        teks += "│ • {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(
                message.chat.id, teks, reply_to_message_id=replyid, parse_mode="md"
            )
            teks = ""
            toolong = True
    teks += "「 {} Human Administrator 」\n".format(len(admin))
    for x in admin:
        teks += "│ • {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(
                message.chat.id, teks, reply_to_message_id=replyid, parse_mode="md"
            )
            teks = ""
            toolong = True
    teks += "「 {} Bot Administrator 」\n".format(len(badmin))
    for x in badmin:
        teks += "│ • {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(
                message.chat.id, teks, reply_to_message_id=replyid, parse_mode="md"
            )
            teks = ""
            toolong = True
    teks += "「 Total {} Admins 」".format(totaladmins)
    if toolong:
        await message.reply(
            message.chat.id, teks, reply_to_message_id=replyid, parse_mode="md"
        )
    else:
        await m.edit(teks, parse_mode="md")


@Client.on_message(filters.command(["everyone", "all"], COMMAND_HAND_LER) & filters.me)
async def everyone(c: Client, m: Message):
    await m.delete()
    if len(message.text.split()) >= 2:
        text = message.text.split(None, 1)[1]
    else:
        text = "Hi all 🙃"
    kek = client.iter_chat_members(message.chat.id)
    async for a in kek:
        if not a.user.is_bot:
            text += mention_html(a.user.id, "\u200b")
    if m.reply_to_message:
        await c.send_message(
            message.chat.id,
            text,
            reply_to_message_id=m.reply_to_message.message_id,
            parse_mode="html",
        )
    else:
        await c.send_message(message.chat.id, text, parse_mode="html")


@Client.on_message(filters.command(["bots", "listbots"], COMMAND_HAND_LER) & filters.me)
async def listbots(c: Client, m: Message):
    replyid = None
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
        grup = await client.get_chat(chat)
    else:
        chat = message.chat.id
        grup = await client.get_chat(chat)
    if m.reply_to_message:
        replyid = m.reply_to_message.message_id
    getbots = client.iter_chat_members(chat)
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
    teks = "**All bots in group {}**\n".format(grup.title)
    teks += "Bots\n"
    for x in bots:
        teks += "│ • {}\n".format(x)
    teks += "Total {} Bots".format(len(bots))
    if replyid:
        await c.send_message(
            message.chat.id, teks, reply_to_message_id=replyid, parse_mode="md"
        )
    else:
        await m.edit(teks, parse_mode="md")
