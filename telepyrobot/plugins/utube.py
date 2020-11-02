import os
import time
import traceback
from datetime import datetime
from telepyrobot.__main__ import TelePyroBot
from pyrogram import filters, errors
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER, MAX_MESSAGE_LENGTH
from telepyrobot.utils.dl_helpers import progress_for_pyrogram
from youtube_dl import YoutubeDL

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Youtube Downloader using youtube-dl Python Library!

**Commands:**
`{COMMAND_HAND_LER}ytv <link>`: Download Video from YouTube and then upload it.
`{COMMAND_HAND_LER}yta <link>`: Download Audio from YouTube and then upload it.
`{COMMAND_HAND_LER}ytp <link>`: Download Playlist from YouTube.
`{COMMAND_HAND_LER}ytpu <link>`: Download Playlist from YouTube and then upload it.
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

ytp_opts = {
    "verbose": True,
    "merge_output_format": "mkv",
    "geo_bypass": True,
    "outtmpl": "/root/telepyrobot/cache/ytp/%(id)s/%(title)s.%(ext)s",
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


async def GetPlaylistInfo(link):

    with YoutubeDL(ydl_search_opts) as ydl:
        infoSearched = ydl.extract_info(link)

    title = infoSearched["title"]
    link_playlist = infoSearched["webpage_url"]
    artist = infoSearched["uploader"]
    vid = infoSearched["id"]
    entries = infoSearched["entries"]

    return artist, title, vid, entries, link_playlist


async def GetVidInfo(link):

    with YoutubeDL(ydl_search_opts) as ydl:
        infoSearched = ydl.extract_info(link)

    duration = await time_length(infoSearched["duration"])
    timeS = infoSearched["duration"]
    title = infoSearched["title"]
    link_video = infoSearched["webpage_url"]
    artist = infoSearched["uploader"]
    vid = infoSearched["id"]

    return artist, duration, timeS, title, vid


@TelePyroBot.on_message(filters.command("ytv", COMMAND_HAND_LER) & filters.me)
async def ytv_dl(c: TelePyroBot, m: Message):
    link = m.text.split(None, 1)[1]
    if "youtube.com" or "youtu.be" in link:
        await m.edit_text("<i>Getting Video Information...</i>")
        artist, duration, timeS, title, vid = await GetVidInfo(
            link
        )  # Get information about video!
        await m.edit_text(
            (
                f"<i>Downloading Video...</i>\n\n"
                f"<b>ID:</b> <code>{mid}</code>\n"
                f"<b>Uploader:</b> <code>{artist}</code>\n"
                f"<b>Duration:</b> <code>{duration}</code>\n"
                f"<b>Title:</b> <code>{title}</code>"
            )
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
                await m.reply_document(
                    document=dl_location + file,
                    progress=progress_for_pyrogram,
                    progress_args=(f"Uploading __{file}__...", m, c_time),
                )
        await m.delete()
    return


@TelePyroBot.on_message(filters.command("yta", COMMAND_HAND_LER) & filters.me)
async def yta_dl(c: TelePyroBot, m: Message):
    link = m.text.split(None, 1)[1]
    if "youtube.com" or "youtu.be" in link:
        await m.edit_text("<i>Getting Music Information...</i>")
        artist, duration, timeS, title, mid = await GetVidInfo(
            link
        )  # Get information about video!
        await m.edit_text(
            (
                f"<i>Downloading Music...</i>\n\n"
                f"<b>ID:</b> <code>{mid}</code>\n"
                f"<b>Uploader:</b> <code>{artist}</code>\n"
                f"<b>Duration:</b> <code>{duration}</code>\n"
                f"<b>Title:</b> <code>{title}</code>"
            )
        )
        dl_location = f"/root/telepyrobot/cache/yta/{mid}/"
        try:
            with YoutubeDL(yta_opts) as ydl:
                ydl.download([link])  # Use link in list!
                print("Downloaded Music...!")
        except Exception:
            exc = traceback.format_exc()
            await m.reply_text(exc)

        c_time = time.time()
        files = os.listdir(dl_location)
        files.sort()

        for file in files:
            await m.reply_audio(
                audio=dl_location + file,
                title=title,
                performer=artist,
                duration=int(timeS),
                caption=f"Downloaded using @TelePyroBot Userbot",
                progress=progress_for_pyrogram,
                progress_args=("Uploading...", m, c_time),
            )
        await m.delete()
    return


@TelePyroBot.on_message(filters.command("ytp", COMMAND_HAND_LER) & filters.me)
async def ytp_dl(c: TelePyroBot, m: Message):
    link = m.text.split(None, 1)[1]
    if "youtube.com" or "youtu.be" in link:
        await m.edit_text("<i>Getting Playlist Information...</i>")
        artist, title, vid, entries, link_playlist = await GetPlaylistInfo(
            link
        )  # Get information about video!

        dl_location = f"/root/telepyrobot/cache/ytp/{vid}/"
        num = 1

        Download_Text = (
            "<b>Downloading Video:</b> {num}/{entries}\n"
            "<b>Title:</b> {title}\n"
            "<b>Uploader:</b> {uploader}\n"
            "<b>Duration:</b> {duration}"
        )
        Errorss = ""

        for p in entries:
            try:
                lk = p["webpage_url"]
                with YoutubeDL(ytp_opts) as ydl:
                    ydl.download([lk])  # Use link in list!
                print(f"Downloaded {p}!")
                num += 1
                title = p["title"]
                uploader = p["uploader"]
                duration = await time_length(p["duration"])
                try:
                    await m.edit_text(
                        Download_Text.format(
                            num=num,
                            entries=len(entries),
                            title=title,
                            uploader=uploader,
                            duration=duration,
                        )
                    )
                except errors.MessageNotModified:
                    pass
            except Exception:
                exc = traceback.format_exc()
                Errorss += exc + "\n"

        files = os.listdir(dl_location)
        files.sort()
        output = "Playlist Downloaded!\n\n"
        for i in files:
            output += f"{dl_location+i}\n"
        await m.edit_text(output)
        if len(Errorss) > MAX_MESSAGE_LENGTH:
            with BytesIO(str.encode(Errorss)) as f:
                f.name = "ytp_errors.txt"
                await m.reply_document(
                    document=f,
                    caption=f"YouTube-dl Playlist Errors",
                )
        else:
            await m.reply_text(OUTPUT)
    return


"""
@TelePyroBot.on_message(filters.command("ytpu", COMMAND_HAND_LER) & filters.me)
async def ytpu_dl(c: TelePyroBot, m: Message):
    link = m.text.split(None, 1)[1]
    if "youtube.com" or "youtu.be" in link:
        await m.edit_text("<i>Getting Playlist Information...</i>")
        artist, title, vid, entries, link_playlist = await GetPlaylistInfo(
            link
        )  # Get information about video!

        dl_location = f"/root/telepyrobot/cache/ytp/{vid}/"
        num = 1

        Download_Text = (
            "<b>Downloading Video:</b> {num}/{entries}\n"
            "<b>Title:</b> {title}\n"
            "<b>Uploader:</b> {uploader}\n"
            "<b>Duration:</b> {duration}"
        )

        for p in entries:
            try:
                lk = p["webpage_url"]
                with YoutubeDL(ytp_opts) as ydl:
                    ydl.download([lk])  # Use link in list!
                print(f"Downloaded {p}!")
                num += 1
                title = p["title"]
                uploader = p["uploader"]
                duration = await time_length(p["duration"])
                try:
                    await m.edit_text(
                        Download_Text.format(
                            num=num,
                            entries=len(entries),
                            title=title,
                            uploader=uploader,
                            duration=duration,
                        )
                    )
                except errors.MessageNotModified:
                    pass
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
                    progress=progress_for_pyrogram,
                    supports_streaming=True,
                    progress_args=(f"Uploading __{file}__...", m, c_time),
                )
            else:
                await m.reply_document(
                    document=dl_location + file,
                    progress=progress_for_pyrogram,
                    progress_args=(f"Uploading __{file}__...", m, c_time),
                )
        await m.delete()
    return
    """
