from sqlalchemy import Column, String, Integer
from pyrobot.utils.sql_helpers import BASE, SESSION
import threading


class PMTable(BASE):
    __tablename__ = "pmapprove"
    user_id = Column(Integer, primary_key=True)
    boolvalue = Column(String)
    msg_id = Column(Integer)

    def __init__(self, user_id, boolvalue, msg_id):
        """initializing db"""
        self.user_id = user_id
        self.boolvalue = boolvalue
        self.msg_id = msg_id


PMTable.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()

def set_whitelist(user_id, boolvalue):
    with INSERTION_LOCK:
        user = SESSION.query(PMTable).get(user_id)
        try:
            if not user:
                user = PMTable(user_id, boolvalue, msg_id)
            else:
                user.boolvalue = str(boolvalue)
            SESSION.add(user)
            SESSION.commit()
        finally:
            SESSION.close()
    return user_id, msg_id


def set_last_msg_id(user_id, msg_id):
    with INSERTION_LOCK:
        user = SESSION.query(PMTable).get(user_id)
        if not user:
            user = PMTable(user_id, str(False), msg_id)
        else:
            user.msg_id = msg_id
        SESSION.merge(user)
        SESSION.commit()
    return


def del_whitelist(user_id):
    with INSERTION_LOCK:
        user = SESSION.query(PMTable).get(user_id)
        try:
            if user:
                SESSION.delete(user)
                SESSION.commit()
        finally:
            SESSION.close()
        return False

def get_msg_id(user_id):
    user = SESSION.query(PMTable).get(str(user_id))
    msg_id = None
    if user:
        msg_id = user.msg_id
    SESSION.close()
    return msg_id


def get_whitelist(user_id):
    user = SESSION.query(PMTable).get(user_id)
    rep = ""
    if user:
        rep = str(user.boolvalue)
    SESSION.close()
    return rep