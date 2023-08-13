from requests import Session
from http import HTTPStatus
import pytest

AUTH_API = 'http://localhost:5000/api'
TRACKER_API = 'http://localhost:5001/api'
session = Session()


def get_headers(data: dict = None):
    if not data:
        data = {"username": "Popug", "password": "12345"}
    r = session.post(f"{AUTH_API}/auth", json=data)
    access_token = r.json()["accessToken"]
    return {'Authorization': f'Bearer {access_token}'}


@pytest.mark.auth
def test_create_popug():
    data = {
        "username": "Popug",
        "password": "12345",
        "email": "popug@popug.io",
        'role': 'developer',
    }

    r = session.post(f"{AUTH_API}/user", json=data)
    assert r.status_code == HTTPStatus.OK


@pytest.mark.auth
def test_login_popug():
    data = {
        "username": "Popug",
        "password": "12345",
    }
    r = session.post(f"{AUTH_API}/auth", json=data)
    assert r.status_code == HTTPStatus.OK


@pytest.mark.tracker
def test_create_task():
    headers = get_headers()
    task = {"description": 'Very important task!!!!!'}
    r = session.post(f"{TRACKER_API}/task", json=task, headers=headers)
    assert r.status_code == HTTPStatus.CREATED
    print(r.json())


@pytest.mark.tracker
def test_reassigned_task():
    headers = get_headers()
    r = session.post(f"{TRACKER_API}/reassign", headers=headers)
    assert r.status_code == HTTPStatus.OK


@pytest.mark.tracker
def test_reassigned_no_auth_task():
    r = session.post(f"{TRACKER_API}/reassign")
    assert r.status_code == HTTPStatus.UNAUTHORIZED
