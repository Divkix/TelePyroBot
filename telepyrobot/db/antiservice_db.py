from sqlalchemy import Column, String, Boolean
from telepyrobot.db import BASE, SESSION


class AntiService(BASE):
    __tablename__ = "antiservice"
    chat_id = Column(String(14), primary_key=True)
    is_enabled = Column(Boolean, default=False)

    def __init__(self, chat_id, is_enabled):
        """initializing db"""
        self.chat_id = str(chat_id)
        self.is_enabled = is_enabled

    def __repr__(self):
        """chat message for db"""
        stat = "Enabled" if self.is_enabled else "Disabled"
        return f"<{stat} {self.chat_id}>"


AntiService.__table__.create(checkfirst=True)

ANTISERVICE_CHATS = []


def enable_antiservice(chat_id, vbool: True):
    try:
        enabled = SESSION.query(AntiService).get(str(chat_id))
        if enabled:
            SESSION.delete(enabled)
        enabled = AntiService(chat_id, vbool)
        SESSION.add(enabled)
        SESSION.commit()
    finally:
        SESSION.close()


def disable_antiservice(chat_id, vbool: False):
    try:
        enabled = SESSION.query(AntiService).get(str(chat_id))
        if enabled:
            SESSION.delete(enabled)
        enabled = AntiService(chat_id, vbool)
        SESSION.add(enabled)
        SESSION.commit()
    finally:
        SESSION.close()


def get_antiservice(chat_id):
    try:
        x = SESSION.query(AntiService).get(str(chat_id))
        if x.is_enabled:
            return True
        else:
            return False
    finally:
        SESSION.close()


def __load_mychats():
    global ANTISERVICE_CHATS
    try:
        ANTISERVICE_CHATS = []
        qall = SESSION.query(AntiService).all()
        for x in qall:
            if x.is_enabled:
                ANTISERVICE_CHATS.append(x.chat_id)
    finally:
        SESSION.close()


__load_mychats()
