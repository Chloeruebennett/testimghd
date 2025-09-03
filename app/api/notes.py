from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db
from app import schemas, crud, models

router = APIRouter()

@router.post("/", response_model=schemas.NoteRead)
async def create_note_endpoint(note_in: schemas.NoteCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    note = crud.create_note(db, note_in, owner_id=current_user.id)
    return note

@router.get("/", response_model=list[schemas.NoteRead])
async def read_notes(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    notes = crud.get_notes_by_user(db, owner_id=current_user.id)
    return notes

@router.get("/{note_id}", response_model=schemas.NoteRead)
async def read_note(note_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    note = crud.get_note_by_id(db, note_id, owner_id=current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete("/{note_id}")
async def delete_note_endpoint(note_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    note = crud.get_note_by_id(db, note_id, owner_id=current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    crud.delete_note(db, note)
    return {"detail": "Note deleted"}

@router.put("/{note_id}", response_model=schemas.NoteRead)
async def update_note_endpoint(note_id: int, note_in: schemas.NoteCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    note = crud.get_note_by_id(db, note_id, owner_id=current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    updated_note = crud.update_note(db, note, note_in)
    return updated_note
