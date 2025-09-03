from sqlalchemy import select
from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Пользователи
def get_user_by_username(db: Session, username: str):
    return db.execute(select(models.User).where(models.User.username == username)).scalar_one_or_none()

def create_user(db: Session, user_in: schemas.UserCreate):
    hashed_password = pwd_context.hash(user_in.password)
    db_user = models.User(username=user_in.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

# Заметки
def create_note(db: Session, note_in: schemas.NoteCreate, owner_id: int):
    note = models.Note(**note_in.dict(), owner_id=owner_id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_notes_by_user(db: Session, owner_id: int):
    return db.execute(select(models.Note).where(models.Note.owner_id == owner_id)).scalars().all()

def get_note_by_id(db: Session, note_id: int, owner_id: int):
    return db.execute(
        select(models.Note).where(models.Note.id == note_id, models.Note.owner_id == owner_id)
    ).scalar_one_or_none()

def delete_note(db: Session, note: models.Note):
    db.delete(note)
    db.commit()

def update_note(db: Session, note: models.Note, note_in: schemas.NoteCreate):
    for var, value in note_in.dict().items():
        setattr(note, var, value)
    db.commit()
    db.refresh(note)
    return note
