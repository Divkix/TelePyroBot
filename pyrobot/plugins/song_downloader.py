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
`{COMMAND_HAND_LER}spotdl <song name>`

The link should be of spotify or youtube!

**Warning:** __It doesn't correctly work with many Indian Songs.__
"""

@Client.on_message(Filters.command("spotdl", COMMAND_HAND_LER) & Filters.me)
async def spotify_dl(client, message):
	if len(message.text.split(' ', 1)) == 2:
		songname = message.text.split(" ",1)[1]
	elif message.reply_to_message:
		songname = message.reply_to_message.text
	subprocess.run(["spotdl", "--song", songname])
	l = glob.glob("*.mp3")
	loa = l[0]
	rply = await message.edit_text("`Uploading Song...`")
	await message.reply_document(
				document=loa,
				parse_mode="html",
				disable_notification=True,
				reply_to_message_id=message.message_id
				)
	subprocess.Popen("rm -rf *.mp3", shell=True)
	await rply.delete()
