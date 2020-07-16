import os
import glob
import time
import asyncio
import spotdl
import subprocess
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}sdd <link>`
`{COMMAND_HAND_LER}spotdl <song name>`

The command will download the song from specified link and send to you.

**Warning:** __It doesn't correctly work with many Indian Songs.__
"""

@Client.on_message(Filters.command("sdd", COMMAND_HAND_LER) & Filters.me)
async def sd_downloader(client, message):
	if len(message.command) == 2:
		song_link = message.text.split(" ",1)[1]
	elif message.reply_to_message:
		song_link = message.reply_to_message.text
	await client.send_message("@DeezLoadBot", f"{song_link}")
	await message.edit(f"`Please wait <u>5</u> seconds.`")
	time.sleep(4)
	msg = await client.get_history("@DeezLoadBot", limit=3)
	msg_id = msg[1]["audio"]["message_id"]
	try:
		await client.forward_messages(message.chat.id, "@DeezLoadBot", msg_id)
	except:
		await message.reply_text("`Not able to fetch music :^(`")
	await client.read_history("@DeezLoadBot")
	await message.delete()

@Client.on_message(Filters.command("spotdl", COMMAND_HAND_LER) & Filters.me)
async def spotify_dl(client, message):
	if len(message.text.split(' ', 1)) == 2:
		songname = message.text.split(" ",1)[1]
	elif message.reply_to_message:
		songname = message.reply_to_message.text
	subprocess.run(["spotdl", "--song", songname])
	l = glob.glob("*.mp3")
	loa = l[0]
	rply = await message.reply_text("`Uploading Song...`")
	await message.reply_document(
				document=loa,
				parse_mode="html",
				disable_notification=True,
				reply_to_message_id=message.message_id
				)
	subprocess.Popen("rm -rf *.mp3", shell=True)
	await rply.delete()
