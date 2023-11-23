from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class SongBase(BaseModel):
    title: str
    author: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.post('/create-song/')
async def create_song(song: SongBase, db: db_dependency):
    q_author = db.query(models.Author).filter_by(name=song.author).first()
    q_title = db.query(models.Song).filter_by(title=song.title).first()
    if q_author is not None and q_title is not None:
        q_song = db.query(models.AuthorSong).filter_by(authorId=q_author.id, songId=q_title.id).first()
        if q_song is not None:
            raise HTTPException(403, detail='Already exists!')
    db_author = q_author
    if q_author is None:
        db_author = models.Author(name=song.author)
    db_title = q_title
    if q_title is None:
        db_title = models.Song(title=song.title)
    db_author.songs.append(db_title)
    db.add_all([db_author, db_title])
    db.commit()

@app.get('/songs/')
async def fetch_all_songs(db: db_dependency):
    q_songs = db.query(models.AuthorSong).all()
    if len(q_songs) == 0:
        return {'List is empty!'}
    songs_list = []
    for author_id, song_id in q_songs:
        author = db.query(models.Author).filter_by(id=author_id).first()
        song = db.query(models.Song).filter_by(id=song_id).first()
        songs_list.append({
            'author': author.name,
            'title': song.title})
    return {'song_list': songs_list}
