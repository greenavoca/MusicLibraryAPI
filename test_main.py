import pytest
from fastapi.testclient import TestClient
from main import app
from database import engine
from models import Base


client = TestClient(app)

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

mock_data = {
    "author": "AuthorTest",
    "title": "TitleTest"
}

def test_create_song(test_db):
    response = client.post("/create-song/", json=mock_data)
    assert response.status_code == 201
    assert response.json() == {'Message': 'Song created!'}

def test_get_all_songs(test_db):
    mock = client.post("/create-song/", json=mock_data)
    response = client.get('/songs/')
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_find_title(test_db):
    mock = client.post("/create-song/", json=mock_data)
    response = client.get('/find-title/AuthorTest')
    assert response.status_code == 200

def test_find_title_not_in_db(test_db):
    response = client.get('/find-title/notindb')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Author not found!'}

def test_find_author(test_db):
    mock = client.post("/create-song/", json=mock_data)
    response = client.get('/find-author/TitleTest')
    assert response.status_code == 200

def test_find_author_not_in_db(test_db):
    response = client.get('/find-author/notindb')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Title not found!'}
