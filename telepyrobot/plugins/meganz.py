import os
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


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__HELP__ = f"""
`{COMMAND_HAND_LER}megainfo`: Get account info!
`{COMMAND_HAND_LER}megals`: List files on mega.nz.
`{COMMAND_HAND_LER}megadl` / `{COMMAND_HAND_LER}dlmega`: Download file from mega.nz link.
`{COMMAND_HAND_LER}megafind <filename>`: Find file or folder in mega drive.
`{COMMAND_HAND_LER}megaup <file location>`: Upload the file and export its link.
"""
mega, megaC = None, None

def megaLogin():
    global mega, megaC
    if not mega or megaC:
        del mega
        del megaC
        mega = Mega()
        try:
            if MEGANZ_EMAIL and MEGANZ_PASSWORD:
                megaC = mega.login(MEGANZ_EMAIL, MEGANZ_PASSWORD)
            else:
                megaC = mega.login()
        except Exception as ef:
            LOGGER.info(ef)
    return


@TelePyroBot.on_message(filters.command("megainfo", COMMAND_HAND_LER) & filters.me)
async def mega_info(c: TelePyroBot, m: Message):
    if not (MEGANZ_EMAIL and MEGANZ_PASSWORD):
        await m.edit_text(
            "Setup `MEGANZ_EMAIL` and `MEGANZ_PASSWORD` vars to use this."
        )
        return
    megaLogin()
    details = f"User:\n{megaC.get_user()}\n\n"
    details += f"Quota:\n{megaC.get_quota()}\n\n"
    details += f"Storage:\n{megaC.get_storage_space(kilo=True)}"
    await m.edit_text(details)
    return


@TelePyroBot.on_message(filters.command("megals", COMMAND_HAND_LER) & filters.me)
async def mega_ls(c: TelePyroBot, m: Message):
    if not (MEGANZ_EMAIL and MEGANZ_PASSWORD):
        await m.edit_text(
            "Setup `MEGANZ_EMAIL` and `MEGANZ_PASSWORD` vars to use this."
        )
        return
    megaLogin()
    files = f"Files\n{megaC.get_files()}"
    await m.edit_text(files)
    return


@TelePyroBot.on_message(filters.command("megadl", COMMAND_HAND_LER) & filters.me)
async def mega_dl(c: TelePyroBot, m: Message):
    megaLogin()
    if len(m.command) == 2:
        dlurl = m.text.split(" ", 1)[1]
        if ("https://mega.co.nz" or "mega.co.nz", "mega.nz") in dl_url:
            megaC.download_url(dlurl, TMP_DOWNLOAD_DIRECTORY)
    return


@TelePyroBot.on_message(filters.command("megafind", COMMAND_HAND_LER) & filters.me)
async def mega_find(c: TelePyroBot, m: Message):
    if not (MEGANZ_EMAIL and MEGANZ_PASSWORD):
        await m.edit_text(
            "Setup `MEGANZ_EMAIL` and `MEGANZ_PASSWORD` vars to use this."
        )
        return
    megaLogin()
    if len(m.command) == 2:
        foldername = m.text.split(" ", 1)[1]
        folder = megaC.find(foldername)
        await m.edit_text(f"Searched for: {foldername}\n\nResults:\n{folder}")
    return


@TelePyroBot.on_message(filters.command("megaup", COMMAND_HAND_LER) & filters.me)
async def mega_find(c: TelePyroBot, m: Message):
    if not (MEGANZ_EMAIL and MEGANZ_PASSWORD):
        await m.edit_text(
            "Setup `MEGANZ_EMAIL` and `MEGANZ_PASSWORD` vars to use this."
        )
        return
    megaLogin()
    if len(m.text.split) >= 2:
        await m.reply_text("Uploading file...")
        fileLoc = m.text.split(" ", 2)
        try:
            file = megaC.upload(fileLoc)
            link = megaC.get_upload_link(file)
        except Exception as ef:
            await m.edit_text(ef)
        await m.edit_text(f"File <i>{fileLoc}</i> Uploaded!\n\n<b>Link:</b> {link}")
    return
