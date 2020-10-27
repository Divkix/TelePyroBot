import os


class Config:
    LOGGER = True
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH", None)
    STRING_SESSION = os.environ.get("STRING_SESSION", None)
    MAX_MESSAGE_LENGTH = 4096
    COMMAND_HAND_LER = os.environ.get("COMMAND_HAND_LER", ".")
    TMP_DOWNLOAD_DIRECTORY = os.environ.get(
        "TMP_DOWNLOAD_DIRECTORY", "telepyrobot/downloads"
    )
    OFFICIAL_UPSTREAM_REPO = os.environ.get(
        "OFFICIAL_UPSTREAM_REPO", "https://github.com/SkuzzyxD/TelePyroBot.git"
    )
    DATABASE_URL = os.environ.get("DATABASE_URL", None)
    G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
    G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
    OWNER_ID = int(os.environ.get("OWNER_ID", "716243352"))
    SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
    TG_MAX_SELECT_LEN = int(os.environ.get("TG_MAX_SELECT_LEN", "100"))
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    OWNER_NAME = os.environ.get("OWNER_NAME", "Skuzzy xD")
    PRIVATE_GROUP_ID = int(os.environ.get("PRIVATE_GROUP_ID", -100))
    PM_PERMIT = bool(os.environ.get("PM_PERMIT", False))
    REMBG_API_KEY = os.environ.get("REMBG_API_KEY", None)


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
