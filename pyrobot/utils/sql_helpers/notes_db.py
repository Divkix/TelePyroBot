import threading

from sqlalchemy import Column, UnicodeText, Integer

from pyrobot.utils.sql_helpers import BASE, SESSION
from pyrobot.utils.msg_types import Types


class Notes(BASE):
    __tablename__ = "self_notes"
    user_id = Column(Integer, primary_key=True)
    name = Column(UnicodeText, primary_key=True)
    value = Column(UnicodeText, nullable=False)
    msgtype = Column(Integer, default=Types.TEXT)
    file_id = Column(UnicodeText)
    file_ref = Column(UnicodeText)

    def __init__(self, user_id, name, value, msgtype, file_id, file_ref):
        """initializing db"""
        self.user_id = user_id
        self.name = name
        self.value = value
        self.msgtype = msgtype
        self.file_id = file_id
        self.file_ref = file_ref

    def __repr__(self):
        """get db message"""
        return "<Note %s>" % self.name


Notes.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()

SELF_NOTES = {}


# Types of message
# TEXT = 1
# DOCUMENT = 2
# PHOTO = 3
# VIDEO = 4
# STICKER = 5
# AUDIO = 6
# VOICE = 7
# VIDEO_NOTE = 8
# ANIMATION = 9
# ANIMATED_STICKER = 10
# CONTACT = 11


def save_note(user_id, note_name, note_data, msgtype, file_id=None, file_ref=None):
    global SELF_NOTES
    with INSERTION_LOCK:
        prev = SESSION.query(Notes).get((user_id, note_name))
        if prev:
            SESSION.delete(prev)
        note = Notes(user_id, note_name, note_data, msgtype=int(msgtype), file_id=file_id, file_ref=file_ref)
        SESSION.add(note)
        SESSION.commit()

        if not SELF_NOTES.get(user_id):
            SELF_NOTES[user_id] = {}
        SELF_NOTES[user_id][note_name] = {'value': note_data, 'type': msgtype, 'file_id': file_id, "file_ref"=file_ref}


def get_note(user_id, note_name):
    if not SELF_NOTES.get(user_id):
        SELF_NOTES[user_id] = {}
    return SELF_NOTES[user_id].get(note_name)


def get_all_notes(user_id):
    if not SELF_NOTES.get(user_id):
        SELF_NOTES[user_id] = {}
        return None
    allnotes = list(SELF_NOTES[user_id])
    allnotes.sort()
    return allnotes


def get_num_notes(user_id):
    try:
        num_notes = SESSION.query(Notes).count()
        return num_notes
    finally:
        SESSION.close()



def rm_note(user_id, note_name):
    global SELF_NOTES
    with INSERTION_LOCK:
        note = SESSION.query(Notes).get((user_id, note_name))
        if note:
            SESSION.delete(note)
            SESSION.commit()
            SELF_NOTES[user_id].pop(note_name)
            return True
        else:
            SESSION.close()
            return False


def __load_all_notes():
    global SELF_NOTES
    getall = SESSION.query(Notes).distinct().all()
    for x in getall:
        if not SELF_NOTES.get(x.user_id):
            SELF_NOTES[x.user_id] = {}
        SELF_NOTES[x.user_id][x.name] = {'value': x.value, 'type': x.msgtype, 'file_id': x.file_id, 'file_ref': x.file_ref}


__load_all_notes()
