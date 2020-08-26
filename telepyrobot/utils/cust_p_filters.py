from pyrogram import filters
from telepyrobot import SUDO_USERS, OWNER_ID


def f_sudo_filter(_, __, m):
    return bool(m.from_user.id in SUDO_USERS or m.from_user.id == OWNER_ID)


sudo_filter = filters.create(f_sudo_filter)
