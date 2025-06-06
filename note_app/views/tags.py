from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from note_app import models, schemas
from note_app.database import SessionLocal
from typing import List

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get list of all tags
@router.get("/", response_model=List[schemas.TagBase])
def get_tags(db: Session = Depends(get_db)):
    return db.query(models.Tag).all()


# Get a specific tag and all notes that use it
@router.get("/{tag_name}", response_model=schemas.TagWithNotes)
def get_tag_with_notes(tag_name: str, db: Session = Depends(get_db)):
    tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    notes_out = []
    for note in tag.notes:
        notes_out.append(
            schemas.NoteOut(
                id=note.id,
                title=note.title,
                description=note.description,
                tags=[t.name for t in note.tags]
            )
        )

    return schemas.TagWithNotes(
        id=tag.id,
        name=tag.name,
        notes=notes_out
    )
