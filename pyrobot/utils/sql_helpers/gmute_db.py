from pyrobot.utils.sql_helpers import SESSION, BASE
from sqlalchemy import Column, Integer
import threading

class GMute(BASE):
    __tablename__ = "gmute"
    sender = Column(Integer, primary_key=True)

    def __init__(self, sender):
        self.sender = str(sender)


GMute.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()

GMUTE_USERS = []

def is_gmuted(sender_id):
    global GMUTE_USERS
    with INSERTION_LOCK:
        try:
            if sender_id in GMUTE_USERS:
                return True
            else:
                return None
        finally:
            SESSION.close()
        return


def gmute(sender):
    global GMUTE_USERS
    with INSERTION_LOCK:
        adder = GMute(sender)
        GMUTE_USERS.append(sender)
        SESSION.add(adder)
        SESSION.commit()
    return


def ungmute(sender):
    global GMUTE_USERS
    with INSERTION_LOCK:
        rem = SESSION.query(GMute).get(sender)
        if rem:
            GMUTE_USERS.remove(sender)
            SESSION.delete(rem)
            SESSION.commit()
        return

def get_gmute_users():
    return GMUTE_USERS


def __load_all_gmute_users():
    global GMUTE_USERS
    getall = SESSION.query(GMute).all()
    for x in getall:
        GMUTE_USERS.append(x)
    return

# Load All GMute Users
__load_all_gmute_users()
