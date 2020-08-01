from sqlalchemy import Column, String, Integer
from pyrobot.utils.sql_helpers import BASE, SESSION
import threading


class WhitelistUsers(BASE):
    __tablename__ = "pmapprove"
    user_id = Column(Integer, primary_key=True)
    boolvalue = Column(String)
    msg_id = Column(Integer)

    def __init__(self, user_id, boolvalue, msg_id=0):
        """initializing db"""
        self.user_id = user_id
        self.boolvalue = boolvalue
        self.msg_id = msg_id


WhitelistUsers.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()

def set_whitelist(user_id, boolvalue):
    with INSERTION_LOCK:
        user = SESSION.query(WhitelistUsers).get(user_id)
        if not user:
            user = WhitelistUsers(user_id, boolvalue, msg_id)
        else:
            user.boolvalue = str(boolvalue)
        SESSION.add(user)
        SESSION.commit()
    return user_id, msg_id


def set_last_msg_id(user_id, msg_id):
    with INSERTION_LOCK:
        user = SESSION.query(WhitelistUsers).get(user_id)
        if not user:
            user = WhitelistUsers(user_id, str(False), msg_id)
        else:
            user.msg_id = msg_id
        SESSION.merge(user)
        SESSION.commit()
    return


def get_msg_id(user_id):
    user = SESSION.query(WhitelistUsers).get(str(user_id))
    msg_id = None
    if user:
        msg_id = user.msg_id
    SESSION.close()
    return msg_id


def del_whitelist(user_id):
    with INSERTION_LOCK:
        user = SESSION.query(WhitelistUsers).get(user_id)
        if user:
            SESSION.delete(user)
            SESSION.commit()
        else:
            SESSION.close()
            return False


def get_whitelist(user_id):
    user = SESSION.query(WhitelistUsers).get(user_id)
    rep = ""
    if user:
        rep = str(user.boolvalue)
    SESSION.close()
    return rep