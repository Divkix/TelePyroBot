from pyrogram import Filters

from pyrobot import (
    SUDO_USERS,
    OWNER_ID
)

def f_sudo_filter(f, m):
    return bool(
        m.from_user.id in SUDO_USERS
        or m.from_user.id == OWNER_ID
    )

sudo_filter = Filters.create(
    func=f_sudo_filter,
    name="SudoFilter"
)