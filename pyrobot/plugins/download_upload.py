import asyncio
import math
import os
import time
from datetime import datetime
from pySmartDL import SmartDL
from pyrogram import Client, Filters
import re

from pyrobot import COMMAND_HAND_LER, LOGGER, TMP_DOWNLOAD_DIRECTORY
from pyrobot.utils.display_progress_dl_up import (
    progress_for_pyrogram,
    humanbytes
)
from pyrobot.utils.check_if_thumb_exists import is_thumb_image_exists

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Download Telegram Media
Syntax: `{COMMAND_HAND_LER}dl` / download <link> or as a reply to media

Directly download file from supported links!
Syntax: `{COMMAND_HAND_LER}direct <link>`
Supported: __ __

Upload Media to Telegram
Syntax: `{COMMAND_HAND_LER}upload <file location>`

Upload files of a directory to Telegram
Usage: `{COMMAND_HAND_LER}batchup <directory location>`

The command will upload all files from the directory location to the current Telegram Chat.
"""


@Client.on_message(Filters.command(["download", "dl"], COMMAND_HAND_LER) & Filters.me)
async def down_load_media(client, sms):
    message = await sms.reply_text("...", quote=True)
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)
    if sms.reply_to_message is not None:
        start_t = datetime.now()
        download_location = TMP_DOWNLOAD_DIRECTORY + "/"
        c_time = time.time()
        the_real_download_location = await client.download_media(
            message=sms.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                "**__Trying to download...__**", message, c_time
            )
        )
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        await message.edit(f"Downloaded to <code>{the_real_download_location}</code> in <u>{ms}</u> seconds", parse_mode="html")
        await sms.delete()
    elif len(sms.command) > 1:
        start_t = datetime.now()
        the_url_parts = " ".join(sms.command[1:])
        url = the_url_parts.strip()
        custom_file_name = os.path.basename(url)
        if "|" in the_url_parts:
            url, custom_file_name = the_url_parts.split("|")
            url = url.strip()
            custom_file_name = custom_file_name.strip()
        download_file_path = os.path.join(TMP_DOWNLOAD_DIRECTORY, custom_file_name)
        downloader = SmartDL(url, download_file_path, progress_bar=False)
        downloader.start(blocking=False)
        c_time = time.time()
        while not downloader.isFinished():
            total_length = downloader.filesize if downloader.filesize else None
            downloaded = downloader.get_dl_size()
            display_message = ""
            now = time.time()
            diff = now - c_time
            percentage = downloader.get_progress() * 100
            speed = downloader.get_speed(human=True)
            elapsed_time = round(diff) * 1000
            progress_str = "**[{0}{1}]**\n**Progress:** __{2}%__".format(
                ''.join(["●" for i in range(math.floor(percentage / 5))]),
                ''.join(["○" for i in range(20 - math.floor(percentage / 5))]),
                round(percentage, 2))
            estimated_total_time = downloader.get_eta(human=True)
            try:
                current_message = f"__**Trying to download...**__\n"
                current_message += f"**URL:** `{url}`\n"
                current_message += f"**File Name:** `{custom_file_name}`\n"
                current_message += f"{progress_str}\n"
                current_message += f"__{humanbytes(downloaded)} of {humanbytes(total_length)}__\n"
                current_message += f"**Download Speed** __{speed}__\n"
                current_message += f"**ETA:** __{estimated_total_time}__"
                if round(diff % 10.00) == 0 and current_message != display_message:
                    await message.edit(
                        disable_web_page_preview=True,
                        text=current_message
                    )
                    display_message = current_message
                    await asyncio.sleep(10)
            except Exception as e:
                LOGGER.info(str(e))
                pass
        if os.path.exists(download_file_path):
            end_t = datetime.now()
            ms = (end_t - start_t).seconds
            await message.edit(f"Downloaded to <code>{download_file_path}</code> in <u>{ms}</u> seconds", parse_mode="html")
    else:
        await message.edit("`Reply to a Telegram Media, to download it to local server.`")

@Client.on_message(Filters.command("direct", COMMAND_HAND_LER) & Filters.me)
async def direct_link_generator(client, message):
    args = message.text.split(None, 1)
    await message.edit("`Processing...`")
    if len(args) == 1:
        await message.edit("Write any args here!")
        return
    downloadurl = args[1]
    reply = ''
    links = re.findall(r'\bhttps?://.*\.\S+', downloadurl)
    if not links:
        reply = "`No links found!`"
        await message.edit(reply)
    for link in links:
        if 'drive.google.com' in link:
            reply += gdrive(link)
        elif 'zippyshare.com' in link:
            reply += zippy_share(link)
        elif 'yadi.sk' in link:
            reply += yandex_disk(link)
        elif 'mediafire.com' in link:
            reply += mediafire(link)
        elif 'sourceforge.net' in link:
            reply += sourceforge(link)
        elif 'osdn.net' in link:
            reply += osdn(link)
        elif 'github.com' in link:
            reply += github(link)
        elif 'androidfilehost.com' in link:
            reply += androidfilehost(link)
        else:
            reply += re.findall(r"\bhttps?://(.*?[^/]+)",
                                link)[0] + 'is not supported'
    await message.edit(reply)


@Client.on_message(Filters.command("upload", COMMAND_HAND_LER) & Filters.me)
async def upload_as_document(client, message):
    status_message = await message.reply_text("`Uploading...`")
    if " " in message.text:
        local_file_name = message.text.split(" ", 1)[1]
        if os.path.exists(local_file_name):
            thumb_image_path = await is_thumb_image_exists(local_file_name)
            start_t = datetime.now()
            c_time = time.time()
            doc_caption = os.path.basename(local_file_name)
            await message.reply_document(
                document=local_file_name,
                thumb=thumb_image_path,
                caption=doc_caption,
                parse_mode="html",
                disable_notification=True,
                reply_to_message_id=message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    "trying to upload", status_message, c_time
                )
            )
            end_t = datetime.now()
            ms = (end_t - start_t).seconds
            await status_message.edit(f"**Uploaded in {ms} seconds**")
        else:
            await status_message.edit("404: media not found")
    else:
        await status_message.edit(f"<code>{COMMAND_HAND_LER}upload FILE_PATH</code> to upload to current Telegram chat")
    await message.delete()


@Client.on_message(Filters.command("batchup", COMMAND_HAND_LER) & Filters.me)
async def covid(client, message):
    if len(message.text.split(" ")) == 1:
        await message.edit("`Enter a directory location`")
    elif len(message.text.split(" ",1)) == 2:
        temp_dir = message.text.split(" ", 1)[1]
    else:
        await message.edit(f"__Please check help by using__ `{COMMAND_HAND_LER}help batchup`")
    status_message = await message.reply_text("`Uploading Files...`")
    if os.path.exists(temp_dir):
        files = os.listdir(temp_dir)
        files.sort()
        await status_message.edit("`Uploading Files to Telegram...`")
        for file in files:
            c_time = time.time()
            required_file_name = temp_dir+"/"+file
            thumb_image_path = await is_thumb_image_exists(required_file_name)
            doc_caption = os.path.basename(required_file_name)
            LOGGER.info(f"Uploading {required_file_name} from {temp_dir} to Telegram.")
            await client.send_document(
                chat_id=message.chat.id,
                document=required_file_name,
                thumb=thumb_image_path,
                caption=doc_caption,
                parse_mode="html",
                disable_notification=True,
                progress=progress_for_pyrogram,
                progress_args=(
                    "Trying to upload multiple files...", status_message, c_time)
                )
    else:
        await message.edit("Directory Not Found.")
        return
    await status_message.edit(f"Uploaded all files from Directory `{temp_dir}`")



# Additonal Functions!
def gdrive(url: str) -> str:
    """GDrive direct links generator"""
    drive = 'https://drive.google.com'
    try:
        link = re.findall(r'\bhttps?://drive\.google\.com\S+', url)[0]
    except IndexError:
        reply = "`No Google drive links found`\n"
        return reply
    file_id = ''
    reply = ''
    if link.find("view") != -1:
        file_id = link.split('/')[-2]
    elif link.find("open?id=") != -1:
        file_id = link.split("open?id=")[1].strip()
    elif link.find("uc?id=") != -1:
        file_id = link.split("uc?id=")[1].strip()
    url = f'{drive}/uc?export=download&id={file_id}'
    download = requests.get(url, stream=True, allow_redirects=False)
    cookies = download.cookies
    try:
        # In case of small file size, Google downloads directly
        dl_url = download.headers["location"]
        if 'accounts.google.com' in dl_url:  # non-public file
            reply += '`Link is not public!`\n'
            return reply
        name = 'Direct Download Link'
    except KeyError:
        # In case of download warning page
        page = BeautifulSoup(download.content, 'lxml')
        export = drive + page.find('a', {'id': 'uc-download-link'}).get('href')
        name = page.find('span', {'class': 'uc-name-size'}).text
        response = requests.get(export,
                                stream=True,
                                allow_redirects=False,
                                cookies=cookies)
        dl_url = response.headers['location']
        if 'accounts.google.com' in dl_url:
            reply += 'Link is not public!'
            return reply
    reply += f'[{name}]({dl_url})\n'
    return reply


def zippy_share(url: str) -> str:
    """ZippyShare direct links generator"""
    reply = ''
    dl_url = ''
    try:
        link = re.findall(r'\bhttps?://.*zippyshare\.com\S+', url)[0]
    except IndexError:
        reply = "`No ZippyShare links found`\n"
        return reply
    session = requests.Session()
    base_url = re.search('http.+.com', link).group()
    response = session.get(link)
    page_soup = BeautifulSoup(response.content, "lxml")
    scripts = page_soup.find_all("script", {"type": "text/javascript"})
    for script in scripts:
        if "getElementById('dlbutton')" in script.text:
            url_raw = re.search(r'= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);',
                                script.text).group('url')
            mathh = re.search(r'= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);',
                              script.text).group('math')
            dl_url = url_raw.replace(mathh, '"' + str(eval(mathh)) + '"')
            break
    dl_url = base_url + eval(dl_url)
    name = urllib.parse.unquote(dl_url.split('/')[-1])
    reply += f'[{name}]({dl_url})\n'
    return reply


def yandex_disk(url: str) -> str:
    """Yandex.Disk direct links generator"""
    reply = ''
    try:
        link = re.findall(r'\bhttps?://.*yadi\.sk\S+', url)[0]
    except IndexError:
        reply = "`No Yandex.Disk links found`\n"
        return reply
    api = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
    try:
        dl_url = requests.get(api.format(link)).json()['href']
        name = dl_url.split('filename=')[1].split('&disposition')[0]
        reply += f'[{name}]({dl_url})\n'
    except KeyError:
        reply += '`Error: File not found / Download limit reached`\n'
        return reply
    return reply


def mediafire(url: str) -> str:
    """MediaFire direct links generator"""
    try:
        link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
    except IndexError:
        reply = "`No MediaFire links found`\n"
        return reply
    reply = ''
    page = BeautifulSoup(requests.get(link).content, 'lxml')
    info = page.find('a', {'aria-label': 'Download file'})
    dl_url = info.get('href')
    size = re.findall(r'\(.*\)', info.text)[0]
    name = page.find('div', {'class': 'filename'}).text
    reply += f'[{name} {size}]({dl_url})\n'
    return reply


def sourceforge(url: str) -> str:
    """SourceForge direct links generator"""
    try:
        link = re.findall(r'\bhttps?://.*sourceforge\.net\S+', url)[0]
    except IndexError:
        reply = "`No SourceForge links found`\n"
        return reply
    file_path = re.findall(r'files(.*)/download', link)[0]
    reply = f"Mirrors for __{file_path.split('/')[-1]}__\n"
    project = re.findall(r'projects?/(.*?)/files', link)[0]
    mirrors = f'https://sourceforge.net/settings/mirror_choices?' \
              f'projectname={project}&filename={file_path}'
    page = BeautifulSoup(requests.get(mirrors).content, 'html.parser')
    info = page.find('ul', {'id': 'mirrorList'}).findAll('li')
    for mirror in info[1:]:
        name = re.findall(r'\((.*)\)', mirror.text.strip())[0]
        dl_url = f'https://{mirror["id"]}.dl.sourceforge.net/project/{project}/{file_path}'
        reply += f'[{name}]({dl_url}) '
    return reply


def osdn(url: str) -> str:
    """OSDN direct links generator"""
    osdn_link = 'https://osdn.net'
    try:
        link = re.findall(r'\bhttps?://.*osdn\.net\S+', url)[0]
    except IndexError:
        reply = "`No OSDN links found`\n"
        return reply
    page = BeautifulSoup(
        requests.get(link, allow_redirects=True).content, 'lxml')
    info = page.find('a', {'class': 'mirror_link'})
    link = urllib.parse.unquote(osdn_link + info['href'])
    reply = f"Mirrors for __{link.split('/')[-1]}__\n"
    mirrors = page.find('form', {'id': 'mirror-select-form'}).findAll('tr')
    for data in mirrors[1:]:
        mirror = data.find('input')['value']
        name = re.findall(r'\((.*)\)', data.findAll('td')[-1].text.strip())[0]
        dl_url = re.sub(r'm=(.*)&f', f'm={mirror}&f', link)
        reply += f'[{name}]({dl_url}) '
    return reply


def github(url: str) -> str:
    """GitHub direct links generator"""
    try:
        link = re.findall(r'\bhttps?://.*github\.com.*releases\S+', url)[0]
    except IndexError:
        reply = "`No GitHub Releases links found`\n"
        return reply
    reply = ''
    dl_url = ''
    download = requests.get(url, stream=True, allow_redirects=False)
    try:
        dl_url = download.headers["location"]
    except KeyError:
        reply += "`Error: Can't extract the link`\n"
    name = link.split('/')[-1]
    reply += f'[{name}]({dl_url}) '
    return reply


def androidfilehost(url: str) -> str:
    """AFH direct links generator"""
    try:
        link = re.findall(r'\bhttps?://.*androidfilehost.*fid.*\S+', url)[0]
    except IndexError:
        reply = "`No AFH links found`\n"
        return reply
    fid = re.findall(r'\?fid=(.*)', link)[0]
    session = requests.Session()
    user_agent = useragent()
    headers = {'user-agent': user_agent}
    res = session.get(link, headers=headers, allow_redirects=True)
    headers = {
        'origin': 'https://androidfilehost.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': user_agent,
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-mod-sbb-ctype': 'xhr',
        'accept': '*/*',
        'referer': f'https://androidfilehost.com/?fid={fid}',
        'authority': 'androidfilehost.com',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'submit': 'submit',
        'action': 'getdownloadmirrors',
        'fid': f'{fid}'
    }
    mirrors = None
    reply = ''
    error = "`Error: Can't find Mirrors for the link`\n"
    try:
        req = session.post(
            'https://androidfilehost.com/libs/otf/mirrors.otf.php',
            headers=headers,
            data=data,
            cookies=res.cookies)
        mirrors = req.json()['MIRRORS']
    except (json.decoder.JSONDecodeError, TypeError):
        reply += error
    if not mirrors:
        reply += error
        return reply
    for item in mirrors:
        name = item['name']
        dl_url = item['url']
        reply += f'[{name}]({dl_url}) '
    return reply


def useragent():
    """useragent random setter"""
    useragents = BeautifulSoup(
        requests.get(
            'https://developers.whatismybrowser.com/'
            'useragents/explore/operating_system_name/android/').content,
        'lxml').findAll('td', {'class': 'useragent'})
    user_agent = choice(useragents)
    return user_agent.text
