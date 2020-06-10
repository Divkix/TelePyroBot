import logging
import os
import re
import shutil
import subprocess
import sys
import traceback
import asyncio
import json
import math
import time
import urllib.parse
from random import choice

import requests
from bs4 import BeautifulSoup
from pyDownload import Downloader

import pafy
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, Filters
from pytube import YouTube

from pyrobot import COMMAND_HAND_LER
from pyrobot.utils.misc.parser import escape_markdown

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
{COMMAND_HAND_LER}yt / youtube <search query>: Get information about a video.

{COMMAND_HAND_LER}yta / ytaudio / ytmusic <link>: Download YouTube Video's Audio.
"""

# --- Extras --- #
async def time_parser(start, end):
    time_end = end - start
    month = time_end // 2678400
    days = time_end // 86400
    hours = time_end // 3600 % 24
    minutes = time_end // 60 % 60
    seconds = time_end % 60

    times = ""
    if month:
        times += "{} month, ".format(month)
    if days:
        times += "{} days, ".format(days)
    if hours:
        times += "{} hours, ".format(hours)
    if minutes:
        times += "{} minutes, ".format(minutes)
    if seconds:
        times += "{} seconds".format(seconds)
    if times == "":
        times = "{} miliseconds".format(time_end)

    return times

async def download_url(url, file_name):
    start = int(time.time())
    downloader = Downloader(url=url)
    end = int(time.time())
    times = await time_parser(start, end)
    downlaoded = f"⬇️ Downloaded `{file_name}` in {times}"
    downlaoded += "\n🗂 File name: {}".format(file_name)
    size = os.path.getsize(downloader.file_name)
    if size > 1024000000:
        file_size = round(size / 1024000000, 3)
        downlaoded += "\n💿 File size: `" + str(file_size) + " GB`\n"
    elif 1024000 < size < 1024000000:
        file_size = round(size / 1024000, 3)
        downlaoded += "\n💿 File size: `" + str(file_size) + " MB`\n"
    elif 1024 < size < 1024000:
        file_size = round(size / 1024, 3)
        downlaoded += "\n💿 File size: `" + str(file_size) + " KB`\n"
    elif size < 1024:
        file_size = round(size, 3)
        downlaoded += "\n💿 File size: `" + str(file_size) + " Byte`\n"

    try:
        os.rename(downloader.file_name, "pyrobot/downloads/" + file_name)
    except OSError:
        return "Failed to download file\nInvaild file name!"
    return downlaoded
# --- End Extras --- #


@Client.on_message(Filters.command(["youtube", "yt"], COMMAND_HAND_LER) & Filters.me)
async def youtube_search(client, message):
	args = message.text.split(None, 1)
	if len(args) == 1:
		await message.edit("Write any args here!")
		return
	teks = args[1]
	responce = requests.get('https://www.youtube.com/results?search_query=' + teks.replace(" ", "%20"))
	soup = BeautifulSoup(responce.content, "html.parser")
	divs = soup.find_all("div", {"class": "yt-lockup"})
	yutub = "<b>Results of {}</b>\n".format(teks)
	nomor = 0
	for i in divs:
		title = i.find('h3', {'class': "yt-lockup-title"}).a.get('title')
		url = i.find('h3', {'class': "yt-lockup-title"}).a.get('href')
		vidtime = i.find("span", {"class": "video-time"})
		if vidtime:
			vidtime = str("(" + vidtime.text + ")")
		else:
			vidtime = ""
		nomor += 1
		yutub += '<b>{}.</b> <a href="{}">{}</a> {}\n'.format(nomor, "https://www.youtube.com" + url, title, vidtime)
	await message.edit(yutub, disable_web_page_preview=True, parse_mode="html")


@Client.on_message(Filters.command(["ytdl"], COMMAND_HAND_LER) & Filters.me)
async def youtube_download(client, message):
	args = message.text.split(None, 2)
	await message.edit("Checking")
	if len(args) == 1:
		await message.edit("Write any args here!")
		return
	try:
		yt = YouTube(args[1])
	except ValueError:
		await message.edit("Invalid URL!")
		return

	if len(args) == 2:
		link = args[1]
		text = "🎬 **Title:** [{}]({})\n".format(escape_markdown(yt.title), link)
		status = "**Downloading video...**\n"
		await message.edit(status + text, disable_web_page_preview=True)
		YouTube(link).streams.first().download('pyrobot/downloads', filename="tempvid")
		status = "**Uploading File To Telegram...**\n"
		await message.edit(status + text, disable_web_page_preview=True)
		await client.send_video(message.chat.id, video="pyrobot/downloads/tempvid.mp4")
		status = "**Removing Temp File...**"
		await message.edit(status)
		os.remove('pyrobot/downloads/tempvid.mp4')
		status = "** Done ✔️✔️**\n"
		await message.edit(status + text, disable_web_page_preview=True)

		return
	if len(args) == 3:
		link = args[1]
		reso = args[2]
		text = "🎬 **Title:** [{}]({})\n".format(escape_markdown(yt.title), link)
		status = "**Downloading video...**\n"
		await message.edit(status + text, disable_web_page_preview=True)
		stream = yt.streams.filter(file_extension='mp4').filter(resolution="{}".format(reso)).first()
		stream.download('pyrobot/downloads', filename="tempvid")
		status = "**Uploading File To Telegram...**\n"
		await message.edit(status + text, disable_web_page_preview=True)
		await client.send_video(message.chat.id, video="pyrobot/downloads/tempvid.mp4")
		status = "**Removing Temp File...**"
		await message.edit(status)
		os.remove('pyrobot/downloads/tempvid.mp4')
		status = "**Done ✔️✔️**\n"
		await message.edit(status + text, disable_web_page_preview=True)
		return


@Client.on_message(Filters.command(["ytmusic", "ytaudio", "yta"], COMMAND_HAND_LER) & Filters.me)
async def youtube_music(client, message):
	args = message.text.split(None, 1)
	if len(args) == 1:
		await message.edit("Send URL here!")
		return
	teks = args[1]
	try:
		video = pafy.new(teks)
	except ValueError:
		await message.edit("Invaild URL!")
		return
	try:
		audios = [audio for audio in video.audiostreams]
		audios.sort(key=lambda a: (int(a.quality.strip('k')) * -1))
		music = audios[0]
		text = "[⁣](https://i.ytimg.com/vi/{}/0.jpg)🎬 **Title:** [{}]({})\n".format(video.videoid,
																					 escape_markdown(video.title),
																					 video.watchv_url)
		text += "👤 **Author:** `{}`\n".format(video.author)
		text += "🕦 **Duration:** `{}`\n".format(video.duration)
		origtitle = re.sub(r'[\\/*?:"<>|\[\]]', "", str(music.title + "." + music._extension))
		musictitle = re.sub(r'[\\/*?:"<>|\[\]]', "", str(music.title))
		musicdate = video._ydl_info['upload_date'][:4]
		titletext = "**Downloading music...**\n"
		await message.edit(titletext + text, disable_web_page_preview=False)
		r = requests.get("https://i.ytimg.com/vi/{}/maxresdefault.jpg".format(video.videoid), stream=True)
		if r.status_code != 200:
			r = requests.get("https://i.ytimg.com/vi/{}/hqdefault.jpg".format(video.videoid), stream=True)
			if r.status_code != 200:
				r = requests.get("https://i.ytimg.com/vi/{}/sddefault.jpg".format(video.videoid), stream=True)
				if r.status_code != 200:
					r = requests.get("https://i.ytimg.com/vi/{}/mqdefault.jpg".format(video.videoid), stream=True)
					if r.status_code != 200:
						r = requests.get("https://i.ytimg.com/vi/{}/default.jpg".format(video.videoid), stream=True)
						if r.status_code != 200:
							avthumb = False
		if r.status_code == 200:
			avthumb = True
			with open("pyrobot/cache/thumb.jpg", "wb") as stk:
				shutil.copyfileobj(r.raw, stk)
		try:
			os.remove("pyrobot/downloads/{}".format(origtitle))
		except FileNotFoundError:
			pass
		if "manifest.googlevideo.com" in music.url:
			download = await download_url(music._info['fragment_base_url'], origtitle)
		else:
			download = await download_url(music.url, origtitle)
		if download == "Failed to download file\nInvaild file name!":
			return await message.edit(download)
		titletext = "**Converting music...**\n"
		await message.edit(titletext + text, disable_web_page_preview=False)
		try:
			process = subprocess.Popen("ffmpeg", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		except Exception as err:
			if "The system cannot find the file specified" in str(err) or "No such file or directory" in str(err):
				await message.edit("You need to install ffmpeg first!")
				return
		if avthumb:
			os.system(
				f'ffmpeg -loglevel panic -i "pyrobot/downloads/{origtitle}" -i "pyrobot/cache/thumb.jpg" -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (Front)" -metadata title="{music.title}" -metadata author="{video.author}" -metadata album="{video.author}" -metadata album_artist="{video.author}" -metadata genre="{video._category}" -metadata date="{musicdate}" -acodec libmp3lame -aq 4 -y "pyrobot/downloads/{musictitle}.mp3"')
		else:
			os.system(
				f'ffmpeg -loglevel panic -i "pyrobot/downloads/{origtitle}" -metadata title="{music.title}" -metadata author="{video.author}" -metadata album="{video.author}" -metadata album_artist="{video.author}" -metadata genre="{video._category}" -metadata date="{musicdate}" -acodec libmp3lame -aq 4 -y "pyrobot/downloads/{musictitle}.mp3"')
		try:
			os.remove("pyrobot/downloads/{}".format(origtitle))
		except FileNotFoundError:
			pass
		titletext = "**Uploading...**\n"
		await message.edit(titletext + text, disable_web_page_preview=False)
		getprev = requests.get(video.thumb, stream=True)
		with open("pyrobot/cache/prev.jpg", "wb") as stk:
			shutil.copyfileobj(getprev.raw, stk)
		await client.send_audio(message.chat.id, audio="pyrobot/downloads/{}.mp3".format(musictitle),
							 thumb="pyrobot/cache/prev.jpg", title=music.title, caption="🕦 `{}`".format(video.duration),
							 reply_to_message_id=message.message_id)
		try:
			os.remove("pyrobot/cache/prev.jpg")
		except FileNotFoundError:
			pass
		try:
			os.remove("pyrobot/cache/thumb.jpg")
		except FileNotFoundError:
			pass
		titletext = "**Done! 🤗**\n"
		await message.edit(titletext + text, disable_web_page_preview=False)
	except Exception as err:
		if "command not found" in str(err) or "is not recognized" in str(err):
			await message.edit("You need to install ffmpeg first!")
			return
		exc_type, exc_obj, exc_tb = sys.exc_info()
		errors = traceback.format_exception(etype=exc_type, value=exc_obj, tb=exc_tb)
		await message.edit("**An error has accured!**")
		logging.exception("Execution error")
