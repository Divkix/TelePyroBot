import os
import subprocess
from spotdl.command_line.core import Spotdl
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
`{COMMAND_HAND_LER}song <song name>`

The link should be of spotify or youtube!

**Warning:** __It doesn't correctly work with some Indian Songs.__
"""

@Client.on_message(Filters.command("song", COMMAND_HAND_LER) & Filters.me)
async def spotify_dl(client, message):
	if len(message.text.split(" ", 1)) >= 2:
		songname = message.text.split(" ",1)[1]
	
	spotdl_handler = Spotdl()

	filename = spotdl_handler.download_track(songname)

	rply = await message.edit_text("`Uploading Song...`")
	await message.reply_document(
				document=filename,
				parse_mode="html",
				disable_notification=True,
				reply_to_message_id=message.message_id)

	subprocess.Popen("rm -rf *.mp3", shell=True)
	await rply.delete()
