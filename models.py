from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Table
from database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column



AuthorSong = Table('authorsong',
                    Base.metadata,
                    Column('authorId', ForeignKey('author.id'), primary_key=True),
                    Column('songId', ForeignKey('song.id'), primary_key=True)
                   )

class Author(Base):
    __tablename__ = 'author'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    songs: Mapped[list[Song]] = relationship(secondary=AuthorSong, back_populates='authors')

    def __repr__(self):
        return f'<Author: {self.name}>'

class Song(Base):
    __tablename__ = 'song'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    authors: Mapped[list[Author]] = relationship(secondary=AuthorSong, back_populates='songs')

    def __repr__(self):
        return f'<Title: {self.title}>'