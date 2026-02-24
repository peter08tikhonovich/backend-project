from schemas import NoteInput
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm.exc import UnmappedInstanceError
from model.database import DBSession
from model import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
	"http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/notes")
def read_notes():
    db = DBSession()
    try:
        notes = db.query(models.Note).all()
    finally:
        db.close()
    return notes



@app.post("/note")

def create_note(note: NoteInput):
    db = DBSession()
    try:
        if len(note.title) == 0 and len(note.note_body) == 0:
            raise HTTPException(status_code=400, detail="Title and body cannot be empty")

        new_note = models.Note(title=note.title, note_body=note.note_body)

        db.add(new_note)
        db.commit()
        db.refresh(new_note)
    finally:
        db.close()
    return new_note


@app.put("/note/{id}")
def update_note(id: int, updated_note: NoteInput):
    if len(updated_note.title) == 0 and len(updated_note.note_body) == 0:
        raise HTTPException(status_code=400, detail="Title and body cannot be empty")

    db = DBSession()
    try:
        note = db.query(models.Note).filter(models.Note.id == id).first()
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")

        note.title = updated_note.title
        note.note_body = updated_note.note_body
        db.commit()
        db.refresh(note)
    finally:
        db.close()

    return note




@app.delete("/note/{id}")
def delete_note(id: int):
    db = DBSession()
    try:
        note = db.query(models.Note).filter(models.Note.id == id).first()
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")

        db.delete(note)
        db.commit()
    finally:
        db.close()

    return {"status": "success"}
