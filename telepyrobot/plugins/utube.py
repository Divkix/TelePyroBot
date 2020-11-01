import os
import time
import asyncio
import traceback
from datetime import datetime
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER
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
    "outtmpl": "/root/telepyrobot/cache/%(title)s/%(title)s.%(ext)s",
    "restrictfilenames": True,
    "writeautomaticsub": True,
    "writedescription": True,
    "format": "(bestvideo[height>=720]+bestaudio/bestvideo+bestaudio)",
}


@TelePyroBot.on_message(filters.command("ytv", COMMAND_HAND_LER) & filters.me)
async def ytv_dl(c: TelePyroBot, m: Message):
    link = m.text.split(None, 1)[1]
    if "youtube.com" or "youtu.be" in link:
        await m.edit_text("<i>Getting Video Information...</i>")
        artist, duration, title = await GetVidInfo(link)  # Get information about video!
        await m.edit_text(
            f"<code>Downloading Video...</code>\n\n<b>Uploader:</b> {artist}\n<b>Duration:</b> {duration}\n<b>Title:</b> {title}"
        )
        dl_location = f"/root/telepyrobot/cache/{title}/".replace("&", "_").replace(
            " ", "_"
        )
        try:
            with YoutubeDL(ytv_opts) as ydl:
                ydl.download([link])  # Use link in list!
                print("Downloaded!")
        except Exception:
            exc = traceback.format_exc()
            await m.reply_text(exc)

        files = os.listdir(dl_location)
        files.sort()
        for file in files:
            c_time = time.time()
            await m.reply_document(
                document=dl_location + file,
                caption=f"Uploader: {artist}\nDuration: {duration}\nTitle: {title}\nLink: {link}",
                progress=progress_for_pyrogram,
                progress_args=(f"Uploading __{file}__...", m, c_time),
            )
    return