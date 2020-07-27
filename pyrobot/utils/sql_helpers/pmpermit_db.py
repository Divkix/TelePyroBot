from sqlalchemy import Column, String
from pyrobot import BASE, SESSION
import threading


class WhitelistUsers(BASE):
    __tablename__ = "pmapprove"
    user_id = Column(String(14), primary_key=True)
    username = Column(String(15))

    def __init__(self, user_id, username):
        """initializing db"""
        self.user_id = user_id
        self.username = username
        
class ReqUsers(BASE):
    __tablename__ = "getpmapprove"
    user_id = Column(String(14), primary_key=True)
    username = Column(String(15))
    
    def __init__(self, user_id, username):
        """getting query from db for user and name"""
        self.user_id = user_id
        self.username = username
        
        
ReqUsers.__table__.create(checkfirst=True)
        
WhitelistUsers.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()

def set_whitelist(user_id, username):
    with INSERTION_LOCK:
        user = SESSION.query(WhitelistUsers).get(str(user_id))
        if not user:
            user = WhitelistUsers(str(user_id), str(username))
        else:
            user.username = str(username)
        
        SESSION.add(user)
        SESSION.commit()


def del_whitelist(user_id):

    with INSERTION_LOCK:
        user = SESSION.query(WhitelistUsers).get(str(user_id))
        if user:
            SESSION.delete(user)
            SESSION.commit()
        else:
            SESSION.close()
            return False


def get_whitelist(user_id):
    user = SESSION.query(WhitelistUsers).get(str(user_id))
    rep = ""
    if user:
        rep = str(user.username)
        
    SESSION.close()
    return rep