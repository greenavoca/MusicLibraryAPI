# MusicLibraryAPI

An Application Programming Interface built with fastAPI and SQLAlchemy,
connected with postgresql database.

## Features / Endpoints:
* create song -> /create-song/
* read all songs -> /songs/
* find by author/title -> /find-title/author_name or /find-author/title_name
* update data -> /update-author/author_id or /update-title/title_id
* delete data -> /delete-song/author/title


## How to run:
* clone this repo
* run 'pip install -r requirements.txt'
* create environment variable DB_URL with db credentials
* run 'uvicorn main:app --reload'