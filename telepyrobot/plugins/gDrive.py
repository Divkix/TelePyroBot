import asyncio
import io
import json
import math
import httplib2
import os
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from mimetypes import guess_type
from telepyrobot.utils.cust_p_filters import sudo_filter
from oauth2client.client import OAuth2WebServerFlow
from telepyrobot.setclient import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import (
    COMMAND_HAND_LER,
    DATABASE_URL,
    G_DRIVE_CLIENT_ID,
    G_DRIVE_CLIENT_SECRET,
    LOGGER,
    TMP_DOWNLOAD_DIRECTORY,
)
import telepyrobot.db.gDrive_db as db
from telepyrobot.utils.dl_helpers import progress_for_pyrogram

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Plugin used to help you manage your **Google Drive**!

`{COMMAND_HAND_LER}gdrive upload <file location>` or as a reply to message to upload file to your Google Drive and get it's link.
`{COMMAND_HAND_LER}gdrive folder <folder id>` to set file uploads specific folder
`{COMMAND_HAND_LER}gdrive reset`: Reset the G Drive credentials.
`{COMMAND_HAND_LER}gdrive setup`: To setup GDrive, only needed if reset grive credentials or setting-up first time.
`{COMMAND_HAND_LER}gdrive search <query>`: To search a file in your GDrive.
"""

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = "https://www.googleapis.com/auth/drive"
# Redirect URI for installed apps, can be left as is
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
# global variable to indicate mimeType of directories in gDrive
G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"
# global variable to save the state of the authentication FLOW
flow = None


@TelePyroBot.on_message(filters.command("gdrive", COMMAND_HAND_LER) & filters.me)
async def g_drive_commands(c: TelePyroBot, m: Message):
    status_m = await m.reply_text("...")
    if len(m.command) == 1:
        await status_m.edit_text(
            f"Check <code>{COMMAND_HAND_LER}help gdrive</code> to ceck help on how to use command!"
        )
        return
    if len(m.command) > 1:
        current_recvd_command = m.command[1]
        if current_recvd_command == "folder":
            db.set_parent_id(m.from_user.id, m.text.split()[2])
            await m.reply_text(f"Set folder ID to {db.get_parent_id}")
            return
        if current_recvd_command == "setup":
            await g_drive_setup(m)
            return
        elif current_recvd_command == "reset":
            db.clear_credential(m.from_user.id)
            await status_m.edit_text(text="Cleared Saved credentials and folder ID!")
            return
        elif current_recvd_command == "confirm":
            if len(m.command) == 3:
                await AskUserToVisitLinkAndGiveCode(status_m, m.command[2])
            else:
                await status_m.edit_text(text="please give auth_code correctly")
        elif current_recvd_command == "search":
            creds = db.get_credential(m.from_user.id)
            if not creds or not creds.invalid:
                if creds and creds.refresh_token:
                    creds.refresh(get_new_http_instance())
                    db.set_credential(m.from_user.id, creds)

                    if len(m.command) > 2:
                        search_query = " ".join(m.command[2:])
                        message_string = "<b>gDrive <i>Search Query</i></b>:"
                        message_string += f"<code>{search_query}</code>\n\n"
                        message_string += "<i>Results</i>:\n"
                        message_string += await search_g_drive(creds, search_query)
                        await status_m.edit_text(
                            text=message_string, disable_web_page_preview=True
                        )
                    else:
                        await status_m.edit_text(
                            "<b>Syntax:</b>\n"
                            f"<code>{COMMAND_HAND_LER}gdrive search (QUERY)</code> "
                        )
                else:
                    await status_m.edit_text(
                        "<b>Invalid credentials!</b>\n"
                        f"<i>Use</i> <code>{COMMAND_HAND_LER}gdrive reset</code> <i>to clear saved credentials.</i>",
                        parse_mode="html",
                    )
                    return
            else:
                await status_m.edit_text(
                    text=f"<i>Please run</i> <code>{COMMAND_HAND_LER}gdrive setup</code> <i>first</i>",
                    parse_mode="html",
                )
    return


@TelePyroBot.on_message(filters.command("ugdrive", COMMAND_HAND_LER) & sudo_filter)
async def upload_file(c: TelePyroBot, m: Message):
    creds = db.get_credential(m.from_user.id)
    folder_id = db.get_parent_id(m.from_user.id)
    status_m = awaitm.reply_text("<i>Checking...!</i>")

    if not creds or not creds.invalid:
        if creds and creds.refresh_token:
            creds.refresh(get_new_http_instance())
            db.set_credential(m.from_user.id, creds)
            if len(m.command) > 2:
                upload_file_name = " ".join(m.command[1:])
                if not os.path.exists(upload_file_name):
                    await status_m.edit_text("invalid file path provided?")
                    return
                gDrive_file_id = await gDrive_upload_file(
                    creds, upload_file_name, status_m, parent_id=folder_id
                )
                reply_message_text = ""
                if gDrive_file_id is not None:
                    reply_message_text += "Uploaded to <a href='"
                    reply_message_text += "https://drive.google.com/open?id="
                    reply_message_text += gDrive_file_id
                    reply_message_text += "'>" + gDrive_file_id + "</a>"
                else:
                    reply_message_text += "failed to upload.. check logs?"
                await status_m.edit_text(
                    text=reply_message_text, disable_web_page_preview=True
                )
            elif m.reply_to_message is not None:
                if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
                    os.makedirs(TMP_DOWNLOAD_DIRECTORY)
                download_location = TMP_DOWNLOAD_DIRECTORY
                c_time = time.time()
                the_real_download_location = await c.download_media(
                    message=m.reply_to_message,
                    file_name=download_location,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "`Trying to download to Local Storage...`",
                        status_m,
                        c_time,
                    ),
                )
                await status_m.edit(
                    f"<b>Downloaded to</b> <code>{the_real_download_location}</code>"
                )
                if not os.path.exists(the_real_download_location):
                    await m.edit_text("invalid file path provided?")
                    return
                gDrive_file_id = await gDrive_upload_file(
                    creds,
                    the_real_download_location,
                    status_m,
                    parent_id=folder_id,
                )
                reply_message_text = ""
                if gDrive_file_id is not None:
                    reply_message_text += "Uploaded to <a href='"
                    reply_message_text += "https://drive.google.com/open?id="
                    reply_message_text += gDrive_file_id
                    reply_message_text += "'>" + gDrive_file_id + "</a>"
                else:
                    reply_message_text += (
                        "<b><i>Failed to upload...</b><i>\n<i>Please check Logs</i>"
                    )
                os.remove(the_real_download_location)
                await status_m.edit_text(
                    text=reply_message_text, disable_web_page_preview=True
                )
            else:
                await status_m.edit_text(
                    "<b>Syntax:</b>\n"
                    f"<code>{COMMAND_HAND_LER}gdrive upload (file name)</code>"
                )
        else:
            await status_m.edit_text(
                "<b>Invalid credentials!</b>\n"
                f"Use <code>{COMMAND_HAND_LER}gdrive reset</code> to clear saved credentials"
            )
            return
    else:
        await status_m.edit_text(
            text=f"<i>Please run</i> <code>{COMMAND_HAND_LER}gdrive setup</code> <i>first</i>"
        )
    return


async def g_drive_setup(m):
    creds = db.get_credential(m.from_user.id)
    if not creds or not creds.invalid:
        if creds and creds.refresh_token:
            creds.refresh(get_new_http_instance())
            db.set_credential(m.from_user.id, creds)
            #
            await m.edit_text(text="gDrive authentication credentials, refreshed")
        else:
            global flow
            flow = OAuth2WebServerFlow(
                G_DRIVE_CLIENT_ID,
                G_DRIVE_CLIENT_SECRET,
                OAUTH_SCOPE,
                redirect_uri=REDIRECT_URI,
            )
            authorize_url = flow.step1_get_authorize_url()
            reply_string = f"please visit {authorize_url} and "
            reply_string += "send back "
            reply_string += (
                f"<code>{COMMAND_HAND_LER}gdrive confirm (RECEIVED_CODE)</code>"
            )
            await m.edit_text(text=reply_string, disable_web_page_preview=True)
    else:
        await m.edit_text(text="`Setup Done Already!`")


async def AskUserToVisitLinkAndGiveCode(m, code):
    creds = None
    global flow
    if flow is None:
        await m.edit_text(
            text=f"run <code>{COMMAND_HAND_LER}gdrive setup</code> first.",
            parse_mode="html",
        )
        return
    await m.edit_text(text="`Checking received code...``")
    creds = flow.step2_exchange(code)
    db.set_credential(m.reply_to_message.from_user.id, creds)
    #
    await m.edit_text(text="<b>Saved gDrive credentials</b>")
    flow = None


async def search_g_drive(creds, search_query):
    service = build("drive", "v3", credentials=creds, cache_discovery=False)
    #
    query = f"name contains '{search_query}'"
    page_token = None
    results = (
        service.files()
        .list(
            q=query,
            spaces="drive",
            fields="nextPageToken, files(id, name)",
            pageToken=page_token,
        )
        .execute()
    )
    items = results.get("files", [])
    message_string = ""
    if not items:
        message_string = "no files found in your gDrive?"
    else:
        for item in items:
            message_string += "#-- <a href='https://drive.google.com/open?id="
            message_string += item.get("id")
            message_string += "'>"
            message_string += item.get("name")
            message_string += "</a>"
            message_string += "\n"
    return message_string


async def gDrive_upload_file(creds, file_path, m, parent_id=None):
    service = build("drive", "v3", credentials=creds, cache_discovery=False)
    mime_type = guess_type(file_path)[0]
    mime_type = mime_type if mime_type else "text/plain"
    media_body = MediaFileUpload(
        file_path, mimetype=mime_type, chunksize=150 * 1024 * 1024, resumable=True
    )
    file_name = os.path.basename(file_path)
    body = {
        "name": file_name,
        "description": "Uploaded using TelePyroBot gDrive plugin!",
        "mimeType": mime_type,
    }
    if parent_id is not None:
        body["parents"]: [parent_id]
    u_file_obj = service.files().create(body=body, media_body=media_body)
    response = None
    display_message = ""
    while response is None:
        status, response = u_file_obj.next_chunk()
        if status:
            percentage = int(status.progress() * 100)
            progress_str = "[{0}{1}]\nProgress: {2}%\n".format(
                "".join(["●" for i in range(math.floor(percentage / 5))]),
                "".join(["○" for i in range(20 - math.floor(percentage / 5))]),
                round(percentage, 2),
            )
            current_message = (
                f"Uploading to gDrive\nFile Name: {file_name}\n{progress_str}"
            )
            if display_message != current_message:
                try:
                    await m.edit_text(current_message)
                    display_message = current_message
                except Exception as e:
                    LOGGER.info(str(e))
                    pass
    file_id = response.get("id")
    return file_id


# https://github.com/googleapis/google-api-python-client/blob/master/docs/thread_safety.md
# Create a new Http() object for every request
def build_request(http, *args, **kwargs):
    new_http = httplib2.Http()
    return apiclient.http.HttpRequest(new_http, *args, **kwargs)


def get_new_http_instance():
    return httplib2.Http()
