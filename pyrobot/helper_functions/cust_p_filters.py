#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pyrogram import Filters

from pyrobot import (
    SUDO_USERS,
    OWNER_ID
)


SUDOUSERS = SUDO_USERS + OWNER_ID

def f_sudo_filter(f, m):
    return bool(
        m.from_user.id in SUDOUSERS
    )

def f_owner_filter(f,m):
    return bool(
        m.from_user.id == OWNER_ID
    )


sudo_filter = Filters.create(
    func=f_sudo_filter,
    name="SudoFilter"
)

owner_filter = Filters.create(
    func=f_owner_filter,
    name="OwnerFilter"
)
