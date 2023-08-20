import random
import time
from http import HTTPStatus

import pytest
from requests import Session

AUTH_API = 'http://localhost:5000/api'
TRACKER_API = 'http://localhost:5001/api'
session = Session()

POPUG = {
    "username": f"Popug_{random.randint(1, 1000)}",
    "password": "12345",
    "email": f"popug_{random.randint(1, 1000)}@popug.io",
    'role': 'developer',
}


def get_headers(data: dict = None):
    if not data:
        data = {
            "username": POPUG["username"],
            "password": POPUG["password"]
        }
    r = session.post(f"{AUTH_API}/auth", json=data)
    access_token = r.json()["accessToken"]
    return {'Authorization': f'Bearer {access_token}'}


@pytest.mark.auth
def test_create_popug():
    r = session.post(f"{AUTH_API}/user", json=POPUG)
    assert r.status_code == HTTPStatus.OK


@pytest.mark.auth
def test_login_popug():
    data = {
        "username": POPUG["username"],
        "password": POPUG["password"]
    }
    r = session.post(f"{AUTH_API}/auth", json=data)
    assert r.status_code == HTTPStatus.OK


@pytest.mark.stream
def test_stream_user():
    data = {
        "username": f"Popug_{random.randint(1, 1000)}",
        "password": "12345",
        "email": f"popug_{random.randint(1, 1000)}@popug.io",
        'role': 'developer',
    }

    r = session.post(f"{AUTH_API}/user", json=data)
    assert r.status_code == HTTPStatus.OK

    access_token = r.json()["accessToken"]
    headers = {'Authorization': f'Bearer {access_token}'}
    r = session.get(f"{AUTH_API}/user", headers=headers)
    assert r.status_code == HTTPStatus.OK

    time.sleep(1)
    user_id = r.json().get('publicId')
    print(r.json())
    r = session.get(f"{TRACKER_API}/user/{user_id}", headers=headers)
    assert r.status_code == HTTPStatus.OK
    print(r.json())


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



