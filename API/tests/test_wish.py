import pytest
import requests
import random
from conftest import BASE_URL

def test_create_wishlist_success(auth_token, setup_data):
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"name": f"{setup_data['wishlist']['name']}_{random.randint(10000,99999)}"}
    response = requests.post(f"{BASE_URL}/wishlists", json=data, headers=headers)
    assert response.status_code == 200
    wishlist = response.json()
    assert "id" in wishlist
    assert wishlist["name"] == data["name"]
    assert "owner_id" in wishlist

def test_create_wishlist_duplicate_name(auth_token, setup_data):
    headers = {"Authorization": f"Bearer {auth_token}"}
    name = f"{setup_data['wishlist']['name']}_{random.randint(10000,99999)}"
    data = {"name": name}
    # cria primeira vez
    requests.post(f"{BASE_URL}/wishlists", json=data, headers=headers)
    # cria segunda vez (deve dar conflito)
    response = requests.post(f"{BASE_URL}/wishlists", json=data, headers=headers)
    assert response.status_code == 409

def test_create_wishlist_no_auth():
    data = {"name": "unauth_list"}
    response = requests.post(f"{BASE_URL}/wishlists", json=data)
    assert response.status_code == 401
    assert "Not authenticated" in response.text

def test_create_wishlist_invalid_data(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/wishlists", json={}, headers=headers)
    assert response.status_code == 422
    assert "Missing name" in response.text

def test_get_all_wishlists_success(auth_token, wishlist_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{BASE_URL}/wishlists", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(w["id"] == wishlist_id for w in data)

def test_get_wishlists_empty(create_user):
    user = create_user()
    headers = {"Authorization": f"Bearer {user['token']}"}
    response = requests.get(f"{BASE_URL}/wishlists", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

def test_get_wishlists_no_auth():
    response = requests.get(f"{BASE_URL}/wishlists")
    assert response.status_code == 401
    assert "Not authenticated" in response.text
