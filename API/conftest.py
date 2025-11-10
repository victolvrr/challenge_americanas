import pytest
import requests
import json
import random

BASE_URL = "http://127.0.0.1:8000/"

@pytest.fixture(scope="session")
def setup_data():
    with open("API/setup.json", "r") as f:
        return json.load(f)

# Criação de usuários e tokens
@pytest.fixture
def create_user():
    def _create_user():
        email = f"user{random.randint(10000,99999)}@example.com"
        username = f"user{random.randint(10000,99999)}"
        password = "Senha123!"
        payload = {"username": username, "email": email, "password": password}
        requests.post(f"{BASE_URL}/auth/register", json=payload)
        login = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        token = login.json().get("access_token")
        return {"token": token, "email": email, "password": password}
    return _create_user

@pytest.fixture
def auth_token(create_user):
    user = create_user()
    return user["token"]

@pytest.fixture
def second_user_token(create_user):
    user = create_user()
    return user["token"]

# Criação de wishlists e produtos
@pytest.fixture
def wishlist_id(auth_token, setup_data):
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"name": f"{setup_data['wishlist']['name']}_{random.randint(10000,99999)}"}
    response = requests.post(f"{BASE_URL}/wishlists", headers=headers, json=data)
    assert response.status_code == 200, f"Falha ao criar wishlist: {response.text}"
    return response.json()["id"]

@pytest.fixture
def sample_wishlist_id(auth_token, setup_data):
    # Wishlist temporária para testes sem auth
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"name": f"temp_{setup_data['wishlist']['name']}_{random.randint(1000,9999)}"}
    response = requests.post(f"{BASE_URL}/wishlists", headers=headers, json=data)
    assert response.status_code == 200, f"Falha ao criar wishlist temporária: {response.text}"
    return response.json()["id"]

@pytest.fixture
def sample_product_id(auth_token, sample_wishlist_id):
    # Produto temporário para testes sem auth
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {
        "Product": f"Temp Product {random.randint(1000,9999)}",
        "Price": "100.00",
        "Zipcode": "00000000",
        "delivery_estimate": "5 dias úteis",
        "shipping_fee": "20.00"
    }
    response = requests.post(f"{BASE_URL}/wishlists/{sample_wishlist_id}/products", headers=headers, json=data)
    assert response.status_code == 200, f"Falha ao criar produto temporário: {response.text}"
    return response.json().get("id")

# Fixtures para cenários de acesso indevido (outro usuário)
@pytest.fixture
def auth_token_user_a(create_user):
    # Token do usuário A
    return create_user()["token"]

@pytest.fixture
def auth_token_user_b(create_user):
    # Token do usuário B
    return create_user()["token"]

@pytest.fixture
def other_user_wishlist_id(auth_token_user_a, setup_data):
    # Wishlist criada pelo usuário A (será usada pra testes com o usuário B)
    headers = {"Authorization": f"Bearer {auth_token_user_a}"}
    data = {"name": f"wishlist_userA_{random.randint(1000,9999)}"}
    response = requests.post(f"{BASE_URL}/wishlists", headers=headers, json=data)
    assert response.status_code == 200, f"Falha ao criar wishlist de outro usuário: {response.text}"
    return response.json()["id"]

@pytest.fixture
def other_user_product_id(auth_token_user_a, other_user_wishlist_id):
    # Produto criado pelo usuário A, usado nos testes do usuário B
    headers = {"Authorization": f"Bearer {auth_token_user_a}"}
    data = {
        "Product": f"Produto UserA {random.randint(1000,9999)}",
        "Price": "250.00",
        "Zipcode": "11111111",
        "delivery_estimate": "7 dias úteis",
        "shipping_fee": "15.00"
    }
    response = requests.post(f"{BASE_URL}/wishlists/{other_user_wishlist_id}/products", headers=headers, json=data)
    assert response.status_code == 200, f"Falha ao criar produto de outro usuário: {response.text}"
    return response.json()["id"]
