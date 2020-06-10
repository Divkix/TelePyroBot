import aria2p
import asyncio
import os
from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, LOGGER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
A Torrent Client Plugin Based On Aria2 for Userbot

Commands:
Start: `{COMMAND_HAND_LER}ariastart` - Starts the Aria Client!
Magnet link : `{COMMAND_HAND_LER}magnet <magnetLink>`
URL Link: `{COMMAND_HAND_LER}ariaurl <url link>`
Show Downloads: `{COMMAND_HAND_LER}ariashow`
Remove All Downloads: `{COMMAND_HAND_LER}ariaRM`
"""

EDIT_SLEEP_TIME_OUT = 5
aria2_is_running = None

@Client.on_message(Filters.command("ariastart", COMMAND_HAND_LER) & Filters.me)
async def magnet_download(client, message):
    cmd = "aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port 6800  --max-connection-per-server=10 --rpc-max-request-size=1024M --seed-time=0.01 --min-split-size=10M --follow-torrent=mem --split=10 --daemon=true --allow-overwrite=true --dir='/app/pyrobot/downloads'"
    aria2_is_running = os.system(cmd)
    aria2 = aria2p.API(aria2p.Client(host="http://localhost", port=6800, secret=""))
    await message.edit("`Started Aria Client`")


@Client.on_message(Filters.command("addmagnet", COMMAND_HAND_LER) & Filters.me)
async def magnet_download(client, message):
    if aria2_is_running is None:
        await message.edit("__First start the Aria Client using__ `{COMMAND_HAND_LER}aria start`")
        return
    var = message.text
    var = var[8:]
    magnet_uri = var
    magnet_uri = magnet_uri.replace("`","")
    LOGGER.info(magnet_uri)
    try: #Add Magnet URI Into Queue
        download = aria2.add_magnet(magnet_uri)
    except Exception as e:
        LOGGER.info(str(e))
        await message.edit("Error :\n{}".format(str(e)))
        return
    gid = download.gid
    await progress_status(gid=gid,message=message,previous=None)
    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
    new_gid = await check_metadata(gid)
    await progress_status(gid=new_gid,message=message,previous=None)


@Client.on_message(Filters.command("addurl", COMMAND_HAND_LER) & Filters.me)
async def url_download(client, message):
    var = message.text[5:]
    print(var)
    uris = [var]
    try: # Add URL Into Queue
        download = aria2.add_uris(uris, options=None, position=None)
    except Exception as e:
        LOGGER.info(str(e))
        await message.edit("Error :\n`{}`".format(str(e)))
        return
    gid = download.gid
    await progress_status(gid=gid,message=message,previous=None)
    file = aria2.get_download(gid)
    if file.followed_by_ids:
        new_gid = await check_metadata(gid)
        await progress_status(gid=new_gid,message=message,previous=None)


@Client.on_message(Filters.command("ariaRM", COMMAND_HAND_LER) & Filters.me)
async def aria_stopall(client, message):
    try:
        removed = aria2.remove_all(force=True)
        aria2.purge_all()
    except:
        pass
    if removed == False:
        os.system("aria2p remove-all")
    await message.edit("`Removed All Downloads`")


@Client.on_message(Filters.command("showaria", COMMAND_HAND_LER) & Filters.me)
async def aria_downloads(client, message):
    output = "output.txt"
    downloads = aria2.get_downloads()
    msg = ""
    for download in downloads:
        msg = msg+"File: `"+str(download.name) +"`\nSpeed: "+ str(download.download_speed_string())+"\nProgress: "+str(download.progress_string())+"\nTotal Size: "+str(download.total_length_string())+"\nStatus: "+str(download.status)+"\nETA:  "+str(download.eta_string())+"\n\n"
    if len(msg) <= 4096:
        await message.edit("`Current Downloads: `\n"+msg)
    else:
        await message.edit("`Output is huge. Sending as a file...`")
        with open(output,'w') as f:
            f.write(msg)
        await asyncio.sleep(2)
        await message.delete()
        await message.reply_document(output)


async def check_metadata(gid):
	file = aria2.get_download(gid)
	new_gid = file.followed_by_ids[0]
	LOGGER.info("Changing GID " + gid + " to " + new_gid)
	return new_gid


async def progress_status(gid,message,previous):
	try:
		file = aria2.get_download(gid)
		if not file.is_complete:
			if not file.error_message:
				msg = "Downloading File: `"+str(file.name) +"`\nSpeed: "+ str(file.download_speed_string())+"\nProgress: "+str(file.progress_string())+"\nTotal Size: "+str(file.total_length_string())+"\nStatus: "+str(file.status)+"\nETA:  "+str(file.eta_string())+"\n\n"
				if previous != msg:
					await message.edit(msg)
					previous = msg
			else:
				LOGGER.info(str(file.error_message))
				await message.edit("Error : `{}`".format(str(file.error_message)))
				return
			await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
			await progress_status(gid,message,previous)
		else:
			await message.edit("File Downloaded Successfully: `{}`".format(file.name))
			return
	except Exception as e:
		if " not found" in str(e) or "'file'" in str(e):
			await message.edit("Download Canceled :\n`{}`".format(file.name))
			return
		elif " depth exceeded" in str(e):
			file.remove(force=True)
			await message.edit("Download Auto Canceled :\n`{}`\nYour Torrent/Link is Dead.".format(file.name))
		else:
			LOGGER.info(str(e))
			await message.edit("Error :\n`{}`".format(str(e)))
			return
