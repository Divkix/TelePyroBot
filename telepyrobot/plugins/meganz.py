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

__help__ = f"""
`{COMMAND_HAND_LER}megainfo`: Get account info.
`{COMMAND_HAND_LER}megals`: List files on mega.nz.
`{COMMAND_HAND_LER}megadl` / `{COMMAND_HAND_LER}dlmega`: Download file from mega.nz link.
`{COMMAND_HAND_LER}megafind <filename>`: Find file or folder in mega drive.
`{COMMAND_HAND_LER}megaup <file location>`: Upload the file and export its link.
`{COMMAND_HAND_LER}megaupdir <folder location>`: Upload contents of folder to your mega drive.
`{COMMAND_HAND_LER}megaimport <url>`: Download file from mega url to your account.
"""
mega, megaC = None, None


def megaLogin():
    global mega, megaC
    if (mega or megaC) is None:
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
    if (MEGANZ_EMAIL or MEGANZ_PASSWORD) is None:
        await m.edit_text(
            "Setup `MEGANZ_EMAIL` and `MEGANZ_PASSWORD` vars to use this."
        )
        return
    megaLogin()
    user = megaC.get_user()
    storage = megaC.get_storage_space(giga=True)
    details = (
        "</b>User Details:</b>\n"
        f"Name: {user['name']}\n"
        f"Email: {user['email']}\n"
        f"Joined: {user['since']}\n\n"
    )
    details += f"Quota:\n{megaC.get_quota()}\n\n"
    details += f"Used: {round(storage['used'], 3)}GB, Total: {storage['total']}GB"
    await m.edit_text(details)
    return


@TelePyroBot.on_message(filters.command("megadl", COMMAND_HAND_LER) & filters.me)
async def mega_dl(c: TelePyroBot, m: Message):
    megaLogin()
    if len(m.command) >= 2:
        dlurl = m.text.split(" ", 1)[1]
        if ("https://mega.co.nz" or "mega.co.nz", "mega.nz") in dl_url:
            megaC.download_url(dlurl, TMP_DOWNLOAD_DIRECTORY)
            await m.edit_text("Downloaded file to `telepyrobot/downloads` folder")
        else:
            await m.edit_text("This doesn't seem like a mega link.")
    else:
        await m.edit_text("No link given")
    return


@TelePyroBot.on_message(filters.command("megafind", COMMAND_HAND_LER) & filters.me)
async def mega_find(c: TelePyroBot, m: Message):
    if (MEGANZ_EMAIL or MEGANZ_PASSWORD) is None:
        await m.edit_text(
            "Setup `MEGANZ_EMAIL` and `MEGANZ_PASSWORD` vars to use this."
        )
        return
    megaLogin()
    if len(m.command) >= 2:
        foldername = m.text.split(" ", 1)[1]
        folder = megaC.find(foldername)[0]
        await m.edit_text(f"Searched for: {foldername}\n\nResults:\n{folder}")
    else:
        await m.edit_text("No link given")
    return


@TelePyroBot.on_message(filters.command("megaup", COMMAND_HAND_LER) & filters.me)
async def mega_upload(c: TelePyroBot, m: Message):
    if (MEGANZ_EMAIL or MEGANZ_PASSWORD) is None:
        await m.edit_text(
            "Setup `MEGANZ_EMAIL` and `MEGANZ_PASSWORD` vars to use this."
        )
        return
    megaLogin()
    if len(m.text.split()) >= 2:
        await m.reply_text("Uploading file...")
        fileLoc = m.text.split(" ", 1)[1]
        try:
            file = megaC.upload(fileLoc)
            link = megaC.get_upload_link(file)
        except Exception as ef:
            await m.edit_text(ef)
            return
        await m.edit_text(f"File <i>{fileLoc}</i> Uploaded!\n\n<b>Link:</b> {link}")
    else:
        await m.edit_text("No file specified!")
    return


@TelePyroBot.on_message(filters.command("megaupdir", COMMAND_HAND_LER) & filters.me)
async def mega_upload_dir(c: TelePyroBot, m: Message):
    if (MEGANZ_EMAIL or MEGANZ_PASSWORD) is None:
        await m.edit_text(
            "Setup `MEGANZ_EMAIL` and `MEGANZ_PASSWORD` vars to use this."
        )
        return
    megaLogin()
    if len(m.text.split()) >= 2:
        await m.reply_text("Uploading file...")
        folderLoc = m.text.split(" ", 1)[1]
        remoteFolder = megaC.find('Uploads')[0]
        if not folderLoc.endswith("/"):
            folderLoc += "/"
        if os.path.exists(folderLoc):
            files = os.listdir(folderLoc)
            files.sort()
            for file in files:
                try:
                    required_file = folderLoc + file
                    megaC.upload(required_file, remoteFolder)
                except Exception as ef:
                    await m.edit_text(ef)
                    return
            await m.reply_text(f"Files from Directory <i>{folderLoc}</i> uploaded to your Mega Cloud Drive!")
            await m.delete()
    else:
        await m.edit_text("No directory specified for upload!")
    return


@TelePyroBot.on_message(filters.command("megaimport", COMMAND_HAND_LER) & filters.me)
async def mega_import(c: TelePyroBot, m: Message):
    if (MEGANZ_EMAIL or MEGANZ_PASSWORD) is None:
        await m.edit_text(
            "Setup `MEGANZ_EMAIL` and `MEGANZ_PASSWORD` vars to use this."
        )
        return
    megaLogin()
    if len(m.text.split()) >= 2:
        await m.reply_text("Importing file...")
        fileurl = m.text.split(" ", 1)[1]
        try:
            if ("https://mega.co.nz" or "mega.co.nz", "mega.nz") in dl_url:
                megaC.import_public_url(fileurl)
                await m.edit_text("Imported file to your mega drive!")
            else:
                await m.edit_text("This doesn't seem like a mega link.")
        except Exception as ef:
            await m.edit_text(ef)
    else:
        await m.edit_text("No link given")
    return
