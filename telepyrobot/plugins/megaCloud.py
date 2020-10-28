from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import (
    COMMAND_HAND_LER,
    MEGANZ_EMAIL,
    MEGANZ_PASSWORD,
    LOGGER,
    TMP_DOWNLOAD_DIRECTORY,
)
from mega import Mega

mega = Mega()

try:
    if MEGANZ_EMAIL and MEGANZ_PASSWORD:
        megaC = mega.login(MEGANZ_EMAIL, MEGANZ_PASSWORD)
    else:
        megaC = mega.login()
except Exception as ef:
    LOGGER.info(ef)


@TelePyroBot.on_message(filters.command("megainfo", COMMAND_HAND_LER) & filters.me)
async def mega_info(c: TelePyroBot, m: Message):
    if not (MEGANZ_EMAIL and MEGANZ_PASSWORD):
        await m.reply_text(
            "Setup `MEGANZ_EMAIL` and `MEGANZ_PASSWORD` vars to use this."
        )
        return
    details = f"User:\n{megaC.get_user()}\n\n"
    details += f"Quota:\n{megaC.get_quota()}\n\n"
    details += f"Storage:\n{megaC.get_storage_space(kilo=True)}"
    await m.reply_text(details)
    return


@TelePyroBot.on_message(filters.command("megals", COMMAND_HAND_LER) & filters.me)
async def mega_ls(c: TelePyroBot, m: Message):
    if not (MEGANZ_EMAIL and MEGANZ_PASSWORD):
        await m.reply_text(
            "Setup `MEGANZ_EMAIL` and `MEGANZ_PASSWORD` vars to use this."
        )
        return
    files = f"Files\n{megaC.get_files()}"
    await m.reply_text(files)
    return


@TelePyroBot.on_message(
    filters.command(["megadl", "dlmega"], COMMAND_HAND_LER) & filters.me
)
async def mega_dl(c: TelePyroBot, m: Message):
    if len(m.command) == 2:
        dlurl = m.text.split(" ", 1)[1]
        if dlurl.startswith("https://mega.co.nz"):
            megaC.download_url(dlurl, TMP_DOWNLOAD_DIRECTORY)
    return


@TelePyroBot.on_message(filters.command("megafind", COMMAND_HAND_LER) & filters.me)
async def mega_find(c: TelePyroBot, m: Message):
    if len(m.command) == 2:
        foldername = m.text.split(" ", 1)[1]
        folder = megaC.find(foldername)
        await m.reply_text(f"Searched for: {foldername}\n\nResults:\n{folder}")

    return