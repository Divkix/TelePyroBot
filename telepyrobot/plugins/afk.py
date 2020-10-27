import os
import time
import asyncio
from datetime import datetime
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from telepyrobot import (
    COMMAND_HAND_LER,
    TG_MAX_SELECT_LEN,
    PRIVATE_GROUP_ID,
    OWNER_ID,
    OWNER_NAME,
)
from telepyrobot.utils.admin_check import admin_check
from telepyrobot.utils.parser import mention_markdown, escape_markdown
from telepyrobot.utils.msg_types import Types, get_message_type
from telepyrobot.utils.sql_helpers.afk_db import set_afk, get_afk


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__HELP__ = f"""
Set yourself to afk.

If you're restart your bot, all counter and data in cache will be reset.
But you will still in afk, and always reply when got mentioned.

**Set AFK status**:
`{COMMAND_HAND_LER}afk <reason>` Set yourself to afk, give a reason if need.
* reason is optional

whenever you send any message to any other chat that your `PRIVATE_GROUP_ID`,
the afk status would be set to False!
"""

# Set priority to 11 and 12
global afk_start
global afk_end
afk_time = None
afk_start = {}
MENTIONED = []
AFK_RESTIRECT = {}
DELAY_TIME = 60  # seconds


@TelePyroBot.on_message((filters.command("afk", COMMAND_HAND_LER)) & filters.me)
async def afk(c: Client, m: Message):
    if PRIVATE_GROUP_ID is None:
        await m.edit(
            "<b><i>Please set the variable</b></i> `PRIVATE_GROUP_ID` for this to function."
        )
        return
    global afk_start
    afk_time = None
    afk_end = {}
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    if len(message.text.split()) >= 2:
        await m.edit_text(
            "I am going AFK now...\nBecause of {}".format(
                message.text.split(None, 1)[1]
            )
        )
        await c.send_message(
            PRIVATE_GROUP_ID,
            "You are AFK!\nBecause of {}".format(message.text.split(None, 1)[1]),
        )
        await asyncio.sleep(2)
        await m.delete()
        await asyncio.sleep(2)
        set_afk(True, message.text.split(None, 1)[1])

    else:
        await m.edit_text(
            "{} is now AFK!".format(
                mention_markdown(message.from_user.first_name, m.from_user.id)
            )
        )
        await c.send_message(
            PRIVATE_GROUP_ID,
            "{} is now AFK!".format(
                mention_markdown(message.from_user.first_name, m.from_user.id)
            ),
        )
        await asyncio.sleep(2)
        await m.delete()
        await asyncio.sleep(2)
        set_afk(True, "")
    return


@TelePyroBot.on_message(
    filters.mentioned & ~filters.bot & ~filters.chat(PRIVATE_GROUP_ID), group=11
)
async def afk_mentioned(c: Client, m: Message):
    global MENTIONED
    global afk_time
    global afk_start
    global afk_end
    get = get_afk()
    if get and get["afk"]:
        current_time_afk = datetime.now()
        afk_end = current_time_afk.replace(microsecond=0)
        if afk_start != {}:
            total_afk_time = str((afk_end - afk_start))
        afk_since = "**a while ago**"
        if afk_time:
            now = datetime.datetime.now()
            datime_since_afk = now - afk_time
            time_of_akf = float(datime_since_afk.seconds)
            days = time_of_akf // (24 * 3600)
            time_of_akf = time_of_akf % (24 * 3600)
            hours = time_of_akf // 3600
            time_of_akf %= 3600
            minutes = time_of_akf // 60
            time_of_akf %= 60
            seconds = time_of_akf
            if days == 1:
                afk_since = "**Yesterday**"
            elif days > 1:
                if days > 6:
                    date = now + datetime.timedelta(
                        days=-days, hours=-hours, minutes=-minutes
                    )
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime("%A")
            elif hours > 1:
                afk_since = f"`{int(hours)}h{int(minutes)}m` **ago**"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m{int(seconds)}s` **ago**"
            else:
                afk_since = f"`{int(seconds)}s` **ago**"

        if "-" in str(message.chat.id):
            cid = str(message.chat.id)[4:]
        else:
            cid = str(message.chat.id)

        if cid in list(AFK_RESTIRECT) and int(AFK_RESTIRECT[cid]) >= int(time.time()):
            return
        AFK_RESTIRECT[cid] = int(time.time()) + DELAY_TIME
        if get["reason"]:
            await m.reply_text(
                "Sorry, My Master {} is AFK right now!\nReason: {}\n\nAFK Since:{}".format(
                    mention_markdown(OWNER_NAME, OWNER_ID),
                    get["reason"],
                    total_afk_time,
                )
            )
        else:
            await m.reply_text(
                "Sorry, My Master {} is AFK right now!\n\nAFK Since:{}".format(
                    mention_markdown(OWNER_NAME, OWNER_ID), total_afk_time
                )
            )

        _, message_type = get_message_type(message)
        if message_type == Types.TEXT:
            text = message.text if message.text else message.caption
        else:
            text = message_type.name

        MENTIONED.append(
            {
                "user": message.from_user.first_name,
                "user_id": m.from_user.id,
                "chat": message.chat.title,
                "chat_id": cid,
                "text": text,
                "message_id": message.message_id,
                "time": datetime.now(),
            }
        )
        await c.send_message(
            PRIVATE_GROUP_ID,
            "{}({}) mentioned you in {}({})\nText:\n`{}`\n\nTotal count: `{}`".format(
                mention_markdown(message.from_user.first_name, m.from_user.id),
                m.from_user.id,
                message.chat.title,
                message.chat.id,
                text[:3500],
                len(MENTIONED),
            ),
        )
    await message.stop_propagation()


@TelePyroBot.on_message(
    filters.me & (filters.group | filters.private) & ~filters.chat(PRIVATE_GROUP_ID),
    group=12,
)
async def no_longer_afk(c: Client, m: Message):
    global afk_time
    global afk_start
    global afk_end
    global MENTIONED
    get = get_afk()
    if get and get["afk"]:
        back_alive = datetime.now()
        afk_end = back_alive.replace(microsecond=0)
        if afk_start != {}:
            total_afk_time = str((afk_end - afk_start))
        await c.send_message(
            PRIVATE_GROUP_ID, "`No longer afk!\nWas AFk for: {}`".format(total_afk_time)
        )
        set_afk(False, "")
        text = "**Total {} mentioned you**\n".format(len(MENTIONED))
        for x in MENTIONED:
            msg_text = x["text"]
            if len(msg_text) >= 11:
                msg_text = "{}...".format(x["text"])
            text += "- [{}](https://t.me/c/{}/{}) ({}): `{}`\n".format(
                escape_markdown(x["user"]),
                x["chat_id"],
                x["message_id"],
                x["chat"],
                msg_text,
            )
        await c.send_message(PRIVATE_GROUP_ID, text)
        MENTIONED = []
        afk_time = None
        await message.stop_propagation()
