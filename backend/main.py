from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Note(BaseModel):
    title: str
    content: str

def load_notes():
    if os.path.exists("notes.json"):
        with open("notes.json", "r") as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open("notes.json", "w") as f:
        json.dump(notes, f)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("frontend/index.html", "r") as f:
        return f.read()

@app.get("/notes")
async def get_notes():
    return load_notes()

@app.post("/notes")
async def create_note(note: Note):
    notes = load_notes()
    notes.append(note.dict())
    save_notes(notes)
    return note

@app.delete("/notes/{title}")
async def delete_note(title: str):
    notes = load_notes()
    notes = [note for note in notes if note["title"] != title]  # Remove the note with the specified title
    save_notes(notes)
    return {"message": "Note deleted successfully"}
