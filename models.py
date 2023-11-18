from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Song(Base):
    __tablename__ = 'song'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class AuthorSong(Base):
    __tablename__ = 'authorsong'

    id = Column(Integer, primary_key=True, index=True)
    author = Column(ForeignKey('author.id'))
    song = Column(ForeignKey('song.id'))

