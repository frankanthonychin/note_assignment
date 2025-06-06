from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from note_app import models, schemas
from note_app.database import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get all notes
@router.get("/", response_model=List[schemas.NoteOut])
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(models.Note).all()
    result = []
    for note in notes:
        result.append(
            schemas.NoteOut(
                id=note.id,
                title=note.title,
                description=note.description,
                tags=[tag.name for tag in note.tags]
            )
        )
    return result


# Create a new note
@router.post("/", response_model=schemas.NoteOut)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_tags = []
    for tag_name in note.tags:
        tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
        if not tag:
            tag = models.Tag(name=tag_name)
        db_tags.append(tag)

    db_note = models.Note(
        title=note.title,
        description=note.description,
        tags=db_tags
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return schemas.NoteOut(
        id=db_note.id,
        title=db_note.title,
        description=db_note.description,
        tags=[tag.name for tag in db_note.tags]
    )


# Update an existing note
@router.put("/{note_id}", response_model=schemas.NoteOut)
def update_note(note_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    db_tags = []
    for tag_name in note.tags:
        tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
        if not tag:
            tag = models.Tag(name=tag_name)
        db_tags.append(tag)

    db_note.title = note.title
    db_note.description = note.description
    db_note.tags = db_tags

    db.commit()
    db.refresh(db_note)

    return schemas.NoteOut(
        id=db_note.id,
        title=db_note.title,
        description=db_note.description,
        tags=[tag.name for tag in db_note.tags]
    )


# Delete a note
@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    return {"message": f"Note with id {note_id} deleted successfully"}
