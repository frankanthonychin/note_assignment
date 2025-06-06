from fastapi import FastAPI
from note_app.views import notes, tags

app = FastAPI()

app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])

if __name__ == "__main__":
    from uvicorn import run
    run("main:app", host="127.0.0.1", port=8000, reload=True)