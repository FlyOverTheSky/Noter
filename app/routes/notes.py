from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.crud import *
from app.auth import get_current_user
from app.models.user import UserModel
from app.utils.logger import log_action

router = APIRouter()

# User endpoints
@router.post("/notes", response_model=NoteResponse)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    new_note = create_note_db(db, note, current_user.id)

    log_action("create_note", current_user.username, new_note.id)

    return new_note

@router.get("/notes", response_model=list[NoteResponse])
def read_notes(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    notes = get_user_notes_db(db, current_user.id)

    log_action("get_notes", current_user.username)

    return notes

@router.get("/notes/{note_id}", response_model=NoteResponse)
def read_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    note = get_note_db(db, note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    log_action("get_note", current_user.username, note_id)

    return note

@router.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    updated_note = update_note_db(db, note_id, note, current_user.id)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")

    log_action("update_note", current_user.username, note_id)

    return updated_note

@router.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not delete_note_db(db, note_id, current_user.id):
        raise HTTPException(status_code=404, detail="Note not found")

    log_action("delete_note", current_user.username, note_id)

    return {"message": "Note deleted"}

# Admin endpoints
@router.post("/admin/notes/{note_id}/restore", response_model=NoteResponse)
def restore_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):

    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    restored_note = restore_note_db(db, note_id)
    if not restored_note:
        raise HTTPException(status_code=404, detail="Note not found")

    log_action("restore_note", current_user.username, note_id)

    return restored_note

@router.get("/admin/notes", response_model=list[NoteResponse])
def get_all_notes(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    notes = get_all_notes_db(db)

    log_action("get_all_notes", current_user.username)

    return notes

@router.get("/admin/users/{user_id}/notes", response_model=list[NoteResponse])
def get_user_notes_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    notes = get_user_notes_admin_db(db, user_id)

    log_action("get_user_notes_admin", current_user.username, user_id=user_id)

    return notes
