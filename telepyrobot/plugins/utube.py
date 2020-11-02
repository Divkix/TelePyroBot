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

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Youtube Downloader using youtube-dl Python Library!

**Commands:**
`{COMMAND_HAND_LER}ytv <link>`: Download Video from YouTube and then upload it!
`{COMMAND_HAND_LER}yta <link>`: Download Audio from YouTube and then upload it!
"""

ydl_search_opts = {
    "quiet": True,
    "skip_download": True,
    "forcetitle": True,
    "forceduration": True,
}

ytv_opts = {
    "verbose": True,
    "merge_output_format": "mkv",
    "geo_bypass": True,
    "outtmpl": "/root/telepyrobot/cache/ytv/%(id)s/%(title)s.%(ext)s",
    "restrictfilenames": True,
    "writeautomaticsub": True,
    "writedescription": True,
    "format": "(bestvideo[height>=720]+bestaudio/bestvideo+bestaudio)",
}

yta_opts = {
    "verbose": True,
    "writethumbnail": True,
    "geo_bypass": True,
    "restrictfilenames": True,
    "outtmpl": "/root/telepyrobot/cache/yta/%(id)s/%(title)s.%(ext)s",
    "extractaudio": True,
    "audioformat": "mp3",
    "format": "(bestaudio[ext=m4a]/bestaudio)",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        },
        {
            "key": "EmbedThumbnail",
        },
    ],
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
    vid = infoSearched["id"]
    return artist, duration, title, vid


@TelePyroBot.on_message(filters.command("ytv", COMMAND_HAND_LER) & filters.me)
async def ytv_dl(c: TelePyroBot, m: Message):
    link = m.text.split(None, 1)[1]
    if "youtube.com" or "youtu.be" in link:
        await m.edit_text("<i>Getting Video Information...</i>")
        artist, duration, title, vid = await GetVidInfo(
            link
        )  # Get information about video!
        await m.edit_text(
            f"<code>Downloading Video...</code>\n\n<b>ID:</b>{vid}<b>Uploader:</b> {artist}\n<b>Duration:</b> {duration}\n<b>Title:</b> {title}"
        )
        dl_location = f"/root/telepyrobot/cache/ytv/{vid}/"
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
            if file.endswith(".mkv"):
                await m.reply_video(
                    document=dl_location + file,
                    caption=f"Uploader: {artist}\nDuration: {duration}\nTitle: {title}\nLink: {link}",
                    progress=progress_for_pyrogram,
                    supports_streaming=True,
                    progress_args=(f"Uploading __{file}__...", m, c_time),
                )
            else:
                await m.reply_video(
                    document=dl_location + file,
                    progress=progress_for_pyrogram,
                    progress_args=(f"Uploading __{file}__...", m, c_time),
                )
    return


@TelePyroBot.on_message(filters.command("yta", COMMAND_HAND_LER) & filters.me)
async def yta_dl(c: TelePyroBot, m: Message):
    link = m.text.split(None, 1)[1]
    if "youtube.com" or "youtu.be" in link:
        await m.edit_text("<i>Getting Video Information...</i>")
        artist, duration, title, mid = await GetVidInfo(
            link
        )  # Get information about video!
        await m.edit_text(
            f"<code>Downloading Video...</code>\n\n<b>ID:</b>{mid}<b>Uploader:</b> {artist}\n<b>Duration:</b> {duration}\n<b>Title:</b> {title}"
        )
        dl_location = f"/root/telepyrobot/cache/yta/{mid}/{title}.mp3"
        try:
            with YoutubeDL(yta_opts) as ydl:
                ydl.download([link])  # Use link in list!
                print("Downloaded Music...!")
        except Exception:
            exc = traceback.format_exc()
            await m.reply_text(exc)

        c_time = time.time()
        await m.reply_audio(
            audio=dl_location,
            title=title,
            performer=artist,
            duration=int(duration),
            caption=f"Downloaded using @TelePyroBot Userbot",
            progress=progress_for_pyrogram,
            progress_args=(f"Uploading __{file}__...", m, c_time),
        )
    return
