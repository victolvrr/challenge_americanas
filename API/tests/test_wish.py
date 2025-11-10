import pytest
import requests
import random
from API.conftest import BASE_URL

# 14: Successfully Create a Wishlist
def test_create_wishlist_success(auth_token, setup_data):
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"name": f"{setup_data['wishlist']['name']}_{random.randint(10000,99999)}"}
    response = requests.post(f"{BASE_URL}/wishlists", json=data, headers=headers)
    assert response.status_code == 200
    wishlist = response.json()
    assert "id" in wishlist
    assert wishlist["name"] == data["name"]
    assert "owner_id" in wishlist

# 15: Create a Wishlist with a Duplicate Name
def test_create_wishlist_duplicate_name(auth_token, setup_data):
    headers = {"Authorization": f"Bearer {auth_token}"}
    name = f"{setup_data['wishlist']['name']}_{random.randint(10000,99999)}"
    data = {"name": name}
    first = requests.post(f"{BASE_URL}/wishlists", json=data, headers=headers)
    assert first.status_code == 200
    duplicate = requests.post(f"{BASE_URL}/wishlists", json=data, headers=headers)
    assert duplicate.status_code == 409
    assert "already exists" in duplicate.text.lower() or "duplicate" in duplicate.text.lower()

# 16: Create a Wishlist without Authentication
def test_create_wishlist_no_auth():
    data = {"name": "unauth_list"}
    response = requests.post(f"{BASE_URL}/wishlists", json=data)
    assert response.status_code == 401
    assert "not authenticated" in response.text.lower()

# 17: Create a Wishlist with Invalid Data
def test_create_wishlist_invalid_data(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/wishlists", json={}, headers=headers)
    assert response.status_code == 422
    assert "field required" in response.text.lower() or "missing" in response.text.lower()

# 18: Successfully Retrieve All Wishlists
def test_get_all_wishlists_success(auth_token, wishlist_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{BASE_URL}/wishlists", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(w["id"] == wishlist_id for w in data)

# 19: Retrieve Wishlists When None Exist
def test_get_wishlists_empty(create_user):
    user = create_user()
    headers = {"Authorization": f"Bearer {user['token']}"}
    response = requests.get(f"{BASE_URL}/wishlists", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

# 20: Retrieve Wishlists without Authentication
def test_get_wishlists_no_auth():
    response = requests.get(f"{BASE_URL}/wishlists")
    assert response.status_code == 401
    assert "not authenticated" in response.text.lower()
