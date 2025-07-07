from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.models.note import NoteModel

def get_user_db(db: Session, username: str):
    return db.query(UserModel).where(UserModel.username == username, UserModel.is_deleted == False).first()

def create_user_db(db: Session, user_data):
    db_user = UserModel(**user_data.dict())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def update_user_role_db(db: Session, username: str):
    user = get_user_db(db=db, username=username)

    setattr(user, "role", "Admin")

    db.commit()
    db.refresh(user)

    return user

def create_note_db(db: Session, note_data, user_id: int):
    db_note = NoteModel(**note_data.dict(), owner_id=user_id)

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note

def get_user_notes_db(db: Session, user_id: int):
    return db.query(NoteModel).filter(NoteModel.owner_id == user_id, NoteModel.is_deleted == False).all()

def get_note_db(db: Session, note_id: int, user_id: int):
    note = db.query(NoteModel).filter(
        NoteModel.id == note_id, 
        NoteModel.owner_id == user_id,
        NoteModel.is_deleted == False
    ).first()

    return note

def update_note_db(db: Session, note_id: int, note_data, user_id: int):
    note = get_note_db(db, note_id, user_id)
    if note:
        for key, value in note_data.dict().items():
            setattr(note, key, value)
        db.commit()
        db.refresh(note)
    return note

def delete_note_db(db: Session, note_id: int, user_id: int):
    note = get_note_db(db, note_id, user_id)
    if note:
        note.is_deleted = True
        db.commit()
        return True
    return False

# Admin functions
def restore_note_db(db: Session, note_id: int):
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if note:
        note.is_deleted = False
        db.commit()
        return note
    return None

def get_all_notes_db(db: Session):
    return db.query(NoteModel).filter(NoteModel.is_deleted == False).all()

def get_user_notes_admin_db(db: Session, user_id: int):
    return db.query(NoteModel).filter(NoteModel.owner_id == user_id, NoteModel.is_deleted == False).all()
