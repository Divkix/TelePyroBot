from pyrobot.utils.sql_helpers import SESSION, BASE
from sqlalchemy import Column, String, UnicodeText
import threading


class GMute(BASE):
    __tablename__ = "gmute"
    sender = Column(String(14), primary_key=True)

    def __init__(self, sender):
        self.sender = str(sender)


GMute.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()

GMUTE_USERS = []

def is_gmuted(sender_id):
    Global GMUTE_USERS
    with INSERTION_LOCK:
        try:
            if sender_id in GMUTE_USERS:
            return True
        except:
            return None
        finally:
            SESSION.close()
        return


def gmute(sender):
    Global GMUTE_USERS
    with INSERTION_LOCK:
        adder = GMute(str(sender))
        GMUTE_USERS.append(str(sender))
        SESSION.add(adder)
        SESSION.commit()
    return


def ungmute(sender):
    Global GMUTE_USERS
    with INSERTION_LOCK:
        rem = SESSION.query(GMute).get((str(sender)))
        if rem:
            GMUTE_USERS.remove(sender)
            SESSION.delete(rem)
            SESSION.commit()
        return


def __load_all_gmute_users():
    Global GMUTE_USERS
    getall = SESSION.query(GMute).all()
    for x in getall:
        GMUTE_USERS.append(x)
    return

# Load All GMute Users
__load_all_gmute_users()
