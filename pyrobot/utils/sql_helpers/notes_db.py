import threading
from sqlalchemy import Column, String, Boolean, UnicodeText, Integer, func, distinct
from pyrobot.utils.sql_helpers import SESSION, BASE


class Notes(BASE):
    __tablename__ = "notes"
    name = Column(UnicodeText, primary_key=True)
    d_message_id = Column(String)

    def __init__(self, name, d_message_id):
        self.name = name
        self.d_message_id = d_message_id

    def __repr__(self):
        return "<Note %s>" % self.name


Notes.__table__.create(checkfirst=True)

NOTES_INSERTION_LOCK = threading.RLock()


def add_note_to_db(note_name, note_message_id):
    with NOTES_INSERTION_LOCK:
        prev_note = SESSION.query(Notes).get(note_name)
        if prev_note:
            SESSION.delete(prev)
        note = Notes(note_name, note_message_id)
        SESSION.add(note)
        SESSION.commit()


def get_note(note_name):
    try:
        note = SESSION.query(Notes).get(note_name)
        return note
    finally:
        SESSION.close()


def rm_note(note_name):
    with NOTES_INSERTION_LOCK:
        note = SESSION.query(Notes).get(note_name)
        if note:
            SESSION.delete(note)
            SESSION.commit()
            return True
        else:
            SESSION.close()
            return False


def get_all_chat_notes():
    try:
        all_notes = SESSION.query(Notes).order_by(Notes.name.asc()).all()
        return all_notes
    finally:
        SESSION.close()


def num_notes():
    try:
        notes_count = SESSION.query(Notes).count()
        return notes_count
    finally:
        SESSION.close()
