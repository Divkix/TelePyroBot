import pickle
import threading
from sqlalchemy import Column, Integer, String, LargeBinary
from telepyrobot.db import BASE, SESSION


class gDriveCreds(BASE):
    __tablename__ = "gDrive"
    chat_id = Column(Integer, primary_key=True)
    credential_string = Column(LargeBinary)
    parent_id = Column(String)

    def __init__(self, chat_id):
        self.chat_id = chat_id


gDriveCreds.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def set_credential(chat_id, credential_string=None):
    with INSERTION_LOCK:
        saved_cred = SESSION.query(gDriveCreds).get(chat_id)
        if not saved_cred:
            saved_cred = gDriveCreds(chat_id)
            saved_cred.parent_id = "root"

        saved_cred.credential_string = pickle.dumps(credential_string)

        SESSION.add(saved_cred)
        SESSION.commit()


def set_parent_id(chat_id, parent_id="root"):
    with INSERTION_LOCK:
        saved_cred = SESSION.query(gDriveCreds).get(chat_id)
        if not saved_cred:
            saved_cred = gDriveCreds(chat_id)
            saved_cred.parent_id = parent_id
            SESSION.add(saved_cred)
        else:
            saved_cred.parent_id = parent_id
            SESSION.commit()

        SESSION.commit()


def get_credential(chat_id):
    with INSERTION_LOCK:
        saved_cred = SESSION.query(gDriveCreds).get(chat_id)
        creds = None
        if saved_cred is not None:
            creds = pickle.loads(saved_cred.credential_string)
        return creds


def get_parent_id(chat_id):
    with INSERTION_LOCK:
        saved_cred = SESSION.query(gDriveCreds).get(chat_id)
        if saved_cred:
            parent_id = saved_cred.parent_id if saved_cred.parent_id else "root"
        return parent_id


# Clear everything along with parent_id and credential code
def clear_credential(chat_id):
    with INSERTION_LOCK:
        saved_cred = SESSION.query(gDriveCreds).get(chat_id)
        if saved_cred:
            SESSION.delete(saved_cred)
            SESSION.commit()
