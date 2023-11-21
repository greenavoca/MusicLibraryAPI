from sqlalchemy import Column, ForeignKey, Integer, String, Table
from database import Base
from sqlalchemy.orm import relationship, query


AuthorSong = Table('authorsong',
                    Base.metadata,
                    Column('authorId', Integer, ForeignKey('author.id')),
                    Column('songId', Integer, ForeignKey('song.id'))
                   )

class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    songs = relationship('Song', secondary=AuthorSong, backref='Author')

class Song(Base):
    __tablename__ = 'song'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    authors = relationship('Author', secondary=AuthorSong, backref='Song')


