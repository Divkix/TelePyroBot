import os
import time
import asyncio
import traceback
from datetime import datetime
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER, MAX_MESSAGE_LENGTH

# from telepyrobot.utils.run_shell_cmnd import run_command
from telepyrobot.utils.clear_string import clear_string
from telepyrobot.utils.dl_helpers import progress_for_pyrogram

# Ytdl Search
from youtube_dl import YoutubeDL

ydl_search_opts = {
    "quiet": True,
    "skip_download": True,
    "forcetitle": True,
    "forceduration": True,
}


async def time_length(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    if hour:
        time_song = "%d:%02d:%02d" % (hour, minutes, seconds)
    elif minutes:
        time_song = "%02d:%02d" % (minutes, seconds)
    else:
        time_song = "%02d" % (seconds)

    return time_song


async def GetVidInfo(link):
    with YoutubeDL(ydl_search_opts) as ydl:
        infoSearched = ydl.extract_info(link)

    duration = await time_length(infoSearched["duration"])
    title = infoSearched["title"]
    link_video = infoSearched["webpage_url"]
    artist = infoSearched["uploader"]

    return artist, duration, title


__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Youtube Downloader using youtube-dl python library!

**Commands:**
`{COMMAND_HAND_LER}ytv <link>`: Download Video from YouTube.
"""

ytv_opts = {
    "verbose": True,
    "merge_output_format": "mkv",
    "geo_bypass": True,
    "outtmpl": "/root/telepyrobot/downloads/%(title)s/%(title)s.%(ext)s",
    "restrictfilenames": True,
    "writeautomaticsub": True,
    "writedescription": True,
    "format": "(bestvideo[height>=720]+bestaudio/bestvideo+bestaudio)",
}


@TelePyroBot.on_message(filters.command("ytv", COMMAND_HAND_LER) & filters.me)
async def ytv_dl(c: TelePyroBot, m: Message):
    link = m.text.split(None, 1)[1]
    if "youtube.com" or "youtu.be" in link:
        await m.edit_text("<code>Getting Video Information...</code>")
        artist, duration, title = await GetVidInfo(link)  # Get information about video!
        await m.edit_text(
            f"<code>Downloading Video...</code>\n\nUploader: {artist}\nDuration: {duration}\nTitle: {title}"
        )
        dl_location = "/root/telepyrobot/downloads/%(title)s/"

        # ytdlv_cmd = [
        #     "youtube-dl",  # Main command
        #     "-f",  # Format
        #     "'(bestvideo[height>=720]+bestaudio/bestvideo+bestaudio)'",  # Best Video + best video
        #     "-vcio",  # Verbose, Continue download, Ignore errors, output format
        #     "'telepyrobot/downloads/%(title)s.%(ext)s'",  # Download Location
        #     "--write-description",  # Write Description file, if available
        #     "--write-auto-sub",  # Write auto subtitle file, if available
        #     "--merge-output-format mkv",  # Use mkv format
        #     link,  # Youtube link
        # ]
        # stdout, stderr = await run_command(ytdlv_cmd)

        # OUTPUT += f"<b>stderr</b>: \n<code>{stderr}</code>\n\n"
        # OUTPUT += f"<b>stdout</b>: \n<code>{stdout}</code>"

        # if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        #     OUTPUT = clear_string(OUTPUT)
        #     with BytesIO(str.encode(OUTPUT)) as f:
        #         f.name = "youtube-dl.txt"
        #         await m.reply_document(
        #             document=f,
        #             caption=link,
        #         )
        #     await m.delete()
        # else:
        #     await m.edit_text(OUTPUT)
        # return
        try:
            with YoutubeDL(ytv_opts) as ydl:
                ydl.download([link])  # Use link in list!
        except Exception:
            exc = traceback.format_exc()
            await m.reply_text(exc)

        if os.path.exists(dl_location):
            files = os.listdir(temp_dir)
            files.sort()
            for file in files:
                c_time = time.time()
                if file.endswith(".mkv"):
                    try:
                        thumb_image_path = await is_thumb_image_exists(i)
                    except Exception:
                        exc = traceback.format_exc()
                        await m.reply_text(exc)
                await m.reply_document(
                    document=file,
                    thumb=thumb_image_path,
                    caption=f"Uploader: {artist}\nDuration: {duration}\nTitle: {title}\nLink: {link}",
                    progress=progress_for_pyrogram,
                    progress_args=("Uploading file...", m, c_time),
                )
            return