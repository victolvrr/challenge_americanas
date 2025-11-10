import pytest
import requests
import random
from API.conftest import BASE_URL

# SCENARIO 8 - Successful User Registration
def test_register_success():
    email = f"testuser{random.randint(1000,9999)}@example.com"
    payload = {"username": f"user{random.randint(1000,9999)}","email": email,"password": "password123"}
    r = requests.post(f"{BASE_URL}/auth/register", json=payload)
    print(r.json())
    assert r.status_code == 200
    assert r.json()["email"] == email

# SCENARIO 9 - User Registration with Existing Email
def test_register_existing_email():
    payload = {"username": "projeto","email": "projeto@example.com","password": "Senha123!"}
    r = requests.post(f"{BASE_URL}/auth/register", json=payload)
    print(r.json())
    assert r.status_code == 400
    assert "already registered" in r.json().get("detail", "").lower()

# SCENARIO 10 - User Registration with Invalid Data
    # Email inválido
    payload_invalid_email = {"username": "user_invalid","email": "not-an-email","password": "password123"}
    r1 = requests.post(f"{BASE_URL}/auth/register", json=payload_invalid_email)
    print(r1.json())
    assert r1.status_code == 422
    # Sem password
    payload_missing_password = {"username": "user_missing","email": f"user{random.randint(1000,9999)}@example.com"}
    r2 = requests.post(f"{BASE_URL}/auth/register", json=payload_missing_password)
    print(r2.json())
    assert r2.status_code == 422

# SCENARIO 11 - User Login with Valid Credentials
def test_login_success(setup_data):
    payload = {"email": "projeto@example.com","password": "Senha123!"}
    r = requests.post(f"{BASE_URL}/auth/login", json=payload)
    print(r.json())
    assert r.status_code == 200
    assert "access_token" in r.json()

# SCENARIO 12 - User Login with Wrong Password
def test_login_wrong_password(setup_data):
    payload = {"email": "projeto@example.com","password": "Errada123"}
    r = requests.post(f"{BASE_URL}/auth/login", json=payload)
    print(r.json())
    assert r.status_code == 401
    assert "incorrect" in r.json().get("detail", "").lower()

# SCENARIO 13 - User Login with Nonexistent Email
def test_login_nonexistent_user():
    payload = {"email": "naoexiste@example.com","password": "abc123"}
    r = requests.post(f"{BASE_URL}/auth/login", json=payload)
    print(r.json())
    assert r.status_code == 401
    assert "incorrect" in r.json().get("detail", "").lower()
