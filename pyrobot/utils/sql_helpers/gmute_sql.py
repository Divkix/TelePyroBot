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

def is_gmuted(sender_id):
    with INSERTION_LOCK:
        try:
            return SESSION.query(GMute).all()
        except:
            return None
        finally:
            SESSION.close()
        return


def gmute(sender):
    with INSERTION_LOCK:
        adder = GMute(str(sender))
        SESSION.add(adder)
        SESSION.commit()
    return


def ungmute(sender):
    with INSERTION_LOCK:
        rem = SESSION.query(GMute).get((str(sender)))
        if rem:
            SESSION.delete(rem)
            SESSION.commit()
        return