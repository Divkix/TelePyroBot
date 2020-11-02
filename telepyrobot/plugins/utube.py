import os
from io import BytesIO
import math
import time
import traceback
from datetime import datetime
from telepyrobot.setclient import TelePyroBot
from pyrogram import filters, errors
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER, MAX_MESSAGE_LENGTH
from telepyrobot.utils.dl_helpers import progress_for_pyrogram
from youtube_dl import YoutubeDL, utils
from telepyrobot.utils.check_size import get_directory_size

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Youtube Downloader using youtube-dl Python Library!

**Commands:**
`{COMMAND_HAND_LER}ytv <link>`: Download Video from YouTube and then upload it to telegram.
`{COMMAND_HAND_LER}yta <link>`: Download Audio from YouTube and then upload it to telegram.
`{COMMAND_HAND_LER}ytp <link>`: Download Playlist from YouTube.
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
    # outtmpl key updated later!
    "geo_bypass": True,
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
    # Embed Thumbnail
    'postprocessors': [
            {'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'},
            {'key': 'EmbedThumbnail',},]
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
    artist = infoSearched["uploader"]
    pid = infoSearched["id"]
    entries = infoSearched["entries"]
    return artist, title, pid, entries


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
        try:
            artist, duration, timeS, title, vid = await GetVidInfo(
                link
            )  # Get information about video!
        except utils.DownloadError:
            await m.edit_text("Could not extract video data, please try agin later!")
            return
        await m.edit_text(
            (
                f"<i>Downloading Video...</i>\n\n"
                f"<b>ID:</b> <code>{vid}</code>\n"
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
                    video=dl_location + file,
                    caption=f"Uploader: {artist}\nDuration: {duration}\nTitle: {title}\nLink: {link}",
                    progress=progress_for_pyrogram,
                    # supports_streaming=True,
                    progress_args=(f"Uploading <i>{file}</i>...", m, c_time),
                )
            else:
                await m.reply_document(
                    document=dl_location + file,
                    progress=progress_for_pyrogram,
                    progress_args=(f"Uploading <i>{file}</i>...", m, c_time),
                )
        await m.delete()
    return


@TelePyroBot.on_message(filters.command("yta", COMMAND_HAND_LER) & filters.me)
async def yta_dl(c: TelePyroBot, m: Message):
    link = m.text.split(None, 1)[1]
    if "youtube.com" or "youtu.be" in link:
        await m.edit_text("<i>Getting Music Information...</i>")
        try:
            artist, duration, timeS, title, mid = await GetVidInfo(
                link
            )  # Get information about video!
        except utils.DownloadError:
            await m.edit_text("Could not extract video data, please try agin later!")
            return
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
                caption=title,
                progress=progress_for_pyrogram,
                progress_args=(f"Uploading <i>{title}</i> ...", m, c_time),
            )
        await m.delete()
    return


@TelePyroBot.on_message(filters.command("ytp", COMMAND_HAND_LER) & filters.me)
async def ytp_dl(c: TelePyroBot, m: Message):
    link = m.text.split(None, 1)[1]
    if "youtube.com" or "youtu.be" in link:
        await m.edit_text("<i>Getting Playlist Information...</i>")
        try:
            artist, title, pid, entries = await GetPlaylistInfo(
                link
            )  # Get information about video!
        except utils.DownloadError:
            await m.edit_text("Could not extract video data, please try agin later!")
            return

        dl_location = f"/root/telepyrobot/cache/ytp/{vid}/"
        num = 0  # To show download number

        Download_Text = (
            "<b>Downloading Playlist ({numbytotal}))</b>\n{progress}\n"
            "<b>Title:</b> {title}\n"
            "<b>Uploader:</b> {uploader}\n"
            "<b>Duration:</b> {duration}"
        )
        Ers = "Errors while Downloading:\n\n"
        total_vids = len(entries)

        for p in entries:
            ytp_opts["outtmpl"] = (
                "/root/telepyrobot/cache/ytp/" + str(pid) + "/%(title)s.%(ext)s"
            )  # vid = Playlist ID
            try:
                url = p["webpage_url"]
                with YoutubeDL(ytp_opts) as ydl:
                    ydl.download([url])  # Use link in list!
                print(f"Downloaded {p}!")
                num += 1
                title = p["title"]
                uploader = p["uploader"]
                duration = await time_length(p["duration"])
                percentage = (num / total_vids) * 100  # Percentage
                progress_str = "<b>[{0}{1}]</b>\n<b>Progress:</b> <i>{2}%</i>".format(
                    "".join(["●" for i in range(math.floor(percentage / 5))]),
                    "".join(["○" for i in range(20 - math.floor(percentage / 5))]),
                    round(percentage, 2),
                )
                try:
                    await m.edit_text(
                        Download_Text.format(
                            numbytotal=f"{num}/{total}",
                            progress=progress_str,
                            entries=total_vids,
                            title=title,
                            uploader=uploader,
                            duration=duration,
                        )
                    )
                except errors.MessageNotModified:  # SHould not happen, but still!
                    pass
            except Exception:
                exc = traceback.format_exc()
                Ers += exc + "\n"

        files = os.listdir(dl_location)
        files.sort()

        output = f"Playlist Downloaded to <code>{dl_location}</code> ({get_directory_size(os.path.abspath(dl_location))})\n\n"
        for file in files:
            output += f"• <code>{file}</code>\n ({get_directory_size(os.path.abspath(dl_location+file))})\n"

        output += f"\nTo upload, use <code>{COMMAND_HAND_LER}batchup {dl_location}</code> to upload all contents of this folder!"

        await m.edit_text(output)
        if not Ers.endswith("Downloading:\n\n"):
            with BytesIO(str.encode(Ers)) as f:
                f.name = "ytp_errors.txt"
                await m.reply_document(
                    document=f,
                    caption=f"Download Errors!",
                )
    return
