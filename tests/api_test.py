import uuid
from tests.fixtures import *

def test_user_registration(client):
    """Тест успешной регистрации пользователя"""
    username = f"user_{uuid.uuid4().hex[:8]}"

    response = client.post(
        "/register",
        json={"username": username, "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_user_login(client):
    """Тест успешного входа пользователя"""
    username = f"user_{uuid.uuid4().hex[:8]}"
    client.post("/register", json={"username": username, "password": "testpass"})

    response = client.post(
        "/login",
        json={"username": username, "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_create_note(client, auth_headers):
    """Тест создания заметки с проверкой всех полей"""
    unique_title = f"Note {uuid.uuid4().hex[:6]}"
    unique_body = f"Content {uuid.uuid4().hex[:6]}"

    note_data = {"title": unique_title, "body": unique_body}
    response = client.post("/notes", json=note_data, headers=auth_headers)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["title"] == unique_title
    assert response_data["body"] == unique_body
    assert "id" in response_data

def test_read_notes(client, auth_headers):
    """Тест получения списка заметок"""
    notes_to_create = 3

    for i in range(notes_to_create):
        note_data = {"title": f"Note {i}", "body": f"Content {i}"}
        client.post("/notes", json=note_data, headers=auth_headers)

    response = client.get("/notes", headers=auth_headers)
    assert response.status_code == 200

    notes = response.json()
    assert len(notes) == notes_to_create

    for note in notes:
        assert "id" in note
        assert "title" in note
        assert "body" in note
        assert "owner_id" in note

def test_read_single_note(client, auth_headers):
    """Тест получения конкретной заметки"""
    note_data = {"title": "Specific Note", "body": "Specific Content"}
    create_response = client.post("/notes", json=note_data, headers=auth_headers)
    note_id = create_response.json()["id"]

    response = client.get(f"/notes/{note_id}", headers=auth_headers)
    assert response.status_code == 200

    note = response.json()
    assert note["id"] == note_id
    assert note["title"] == "Specific Note"
    assert note["body"] == "Specific Content"

def test_full_user_cycle(client):
    """Тест полного цикла: регистрация, вход, создание, чтение"""
    username = f"user_{uuid.uuid4().hex[:8]}"
    reg_response = client.post(
        "/register",
        json={"username": username, "password": "testpass"}
    )
    assert reg_response.status_code == 200
    assert "access_token" in reg_response.json()

    login_response = client.post(
        "/login",
        json={"username": username, "password": "testpass"}
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    note_data = {"title": "Full Cycle Note", "body": "Created in full cycle test"}
    create_response = client.post("/notes", json=note_data, headers=headers)
    assert create_response.status_code == 200

    note = create_response.json()
    assert note["title"] == "Full Cycle Note"
    assert note["body"] == "Created in full cycle test"

    note_id = note["id"]
    get_response = client.get(f"/notes/{note_id}", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Full Cycle Note"
