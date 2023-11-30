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

def test_get_empty_list(test_db):
    response = client.get('/songs/')
    assert response.status_code == 200
    assert response.json() == {'Message': 'List is empty!'}

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

def test_update_author(test_db):
    mock = client.post("/create-song/", json=mock_data)
    response = client.put("/update-author/1", json={"new_name": "UpdateTest"})
    assert response.status_code == 202
    assert response.json() == {'Message': 'Author updated!'}

def test_update_author_not_exist(test_db):
    response = client.put("/update-author/1", json={"new_name": "UpdateTest"})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Author not found!'}

def test_update_author_with_same_data(test_db):
    mock = client.post("/create-song/", json=mock_data)
    response = client.put("/update-author/1", json={"new_name": "AuthorTest"})
    assert response.status_code == 403
    assert response.json() == {'detail': 'Cannot update with the same name!'}

def test_update_title(test_db):
    mock = client.post("/create-song/", json=mock_data)
    response = client.put("/update-title/1", json={"new_title": "UpdateTest"})
    assert response.status_code == 202
    assert response.json() == {'Message': 'Title updated!'}

def test_update_title_not_exist(test_db):
    response = client.put("/update-title/1", json={"new_title": "UpdateTest"})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Title not found!'}

def test_update_title_with_same_data(test_db):
    mock = client.post("/create-song/", json=mock_data)
    response = client.put("/update-title/1", json={"new_title": "TitleTest"})
    assert response.status_code == 403
    assert response.json() == {'detail': 'Cannot update with the same title!'}

def test_delete_song(test_db):
    mock = client.post("/create-song/", json=mock_data)
    response = client.delete(f'/delete-song/{mock_data['author']}/{mock_data['title']}')
    assert response.status_code == 200
    assert response.json() == {'Message': 'Song deleted!'}

def test_delete_song_not_in_db(test_db):
    response = client.delete(f'/delete-song/{mock_data['author']}/{mock_data['title']}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Song not found!'}

def test_delete_title_not_in_db(test_db):
    mock = client.post("/create-song/", json=mock_data)
    response = client.delete(f'/delete-song/{mock_data['author']}/notindb')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Song not found!'}