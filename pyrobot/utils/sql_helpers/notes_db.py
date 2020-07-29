import threading
from sqlalchemy import Column, String, Boolean, UnicodeText, Integer, func, distinct
from pyrobot.utils.sql_helpers import SESSION, BASE

class Notes(BASE):
    __tablename__ = "notes"
    owner_id = Column(Integer, primary_key=True)
    name = Column(UnicodeText, primary_key=True)
    d_message_id = Column(Integer)

    def __init__(self, owner_id, name, d_message_id):
        self.owner_id = owner_id  # ensure string
        self.name = name
        self.d_message_id = d_message_id

    def __repr__(self):
        return "<Note %s>" % self.name


Notes.__table__.create(checkfirst=True)

NOTES_INSERTION_LOCK = threading.RLock()


def add_note_to_db(owner_id, note_name, note_message_id):
    with NOTES_INSERTION_LOCK:
        prev = SESSION.query(Notes).get((str(owner_id), note_name))
        if prev:
            SESSION.delete(prev)
        note = Notes(owner_id, note_name, note_message_id)
        SESSION.add(note)
        SESSION.commit()


def get_note(owner_id, note_name):
    try:
        note_data = SESSION.query(Notes).get((owner_id, note_name))
        return note_data
    finally:
        SESSION.close()


def rm_note(owner_id, note_name):
    with NOTES_INSERTION_LOCK:
        note = SESSION.query(Notes).get((owner_id, note_name))
        if note:
            SESSION.delete(note)
            SESSION.commit()
            return True
        else:
            SESSION.close()
            return False


def get_all_notes(owner_id):
    try:
        all_notes = SESSION.query(Notes).filter(Notes.owner_id == owner_id).order_by(Notes.name.asc()).all()
        return all_notes
    finally:
        SESSION.close()


def num_notes():
    try:
        num_notes = SESSION.query(Notes).count()
        return num_notes
    finally:
        SESSION.close()
