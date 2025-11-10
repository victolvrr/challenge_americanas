import pytest
import requests
from API.conftest import BASE_URL

# 21: Successfully Add a Product to a Wishlist
def test_add_product_success(auth_token, setup_data, wishlist_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = setup_data["products"][0]
    response = requests.post(f"{BASE_URL}/wishlists/{wishlist_id}/products", headers=headers, json=data)
    assert response.status_code == 200
    product = response.json()
    assert "id" in product
    assert product.get("purchased", False) is False

# 22: Add a Product to a Non-Existent Wishlist
def test_add_product_to_nonexistent_wishlist(auth_token, setup_data):
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = setup_data["products"][0]
    response = requests.post(f"{BASE_URL}/wishlists/999999/products", headers=headers, json=data)
    assert response.status_code == 404
    assert "Wishlist not found" in response.text

# 23: Add a Product to Another User's Wishlist
def test_add_product_to_other_user_wishlist(auth_token_user_b, setup_data, other_user_wishlist_id):
    headers = {"Authorization": f"Bearer {auth_token_user_b}"}
    data = setup_data["products"][0]
    response = requests.post(f"{BASE_URL}/wishlists/{other_user_wishlist_id}/products", headers=headers, json=data)
    assert response.status_code == 404
    assert "not found" in response.text.lower() or "wishlist" in response.text.lower()

# 24: Add a Product with Incomplete Data
def test_add_product_incomplete_data(auth_token, wishlist_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/wishlists/{wishlist_id}/products", headers=headers, json={"Price": "100.00"})
    assert response.status_code == 422
    assert "field required" in response.text or "Missing" in response.text

# 25: Successfully Retrieve Products from a Wishlist
def test_get_products_from_wishlist(auth_token, wishlist_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{BASE_URL}/wishlists/{wishlist_id}/products", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# 26: Retrieve Products and Filter by Name
def test_get_products_filter_by_name(auth_token, wishlist_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{BASE_URL}/wishlists/{wishlist_id}/products?Product=iPhone", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert all("iPhone" in p.get("Product", "") for p in data)

# Retrieve Products and Filter by is_purchased Status
def test_get_products_filter_purchased(auth_token, wishlist_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{BASE_URL}/wishlists/{wishlist_id}/products?is_purchased=true", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert all(p.get("is_purchased", False) is True for p in data)

# 28: List Products from Another User's Wishlist
def test_get_products_from_other_user_wishlist(auth_token_user_b, other_user_wishlist_id):
    headers = {"Authorization": f"Bearer {auth_token_user_b}"}
    response = requests.get(f"{BASE_URL}/wishlists/{other_user_wishlist_id}/products", headers=headers)
    assert response.status_code == 404
    assert "not found" in response.text.lower() or "wishlist" in response.text.lower()

# 29: Successfully Update a Product
def test_update_product_success(auth_token, setup_data, wishlist_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    product_data = setup_data["products"][1]
    created = requests.post(f"{BASE_URL}/wishlists/{wishlist_id}/products", headers=headers, json=product_data).json()
    pid = created.get("id")
    assert pid is not None

    update_data = {"Price": "2999,00"}
    response = requests.put(f"{BASE_URL}/products/{pid}", headers=headers, json=update_data)
    assert response.status_code == 200
    updated = response.json()
    assert updated.get("Price") == "2999,00"

# 30: Update a Product That Doesn't Exist
def test_update_nonexistent_product(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.put(f"{BASE_URL}/products/999999", headers=headers, json={"Price": "10.00"})
    assert response.status_code == 404

# 31: Update Another User's Product
def test_update_other_user_product(auth_token_user_b, other_user_product_id):
    headers = {"Authorization": f"Bearer {auth_token_user_b}"}
    update_data = {"Price": "1500.00"}
    response = requests.put(f"{BASE_URL}/products/{other_user_product_id}", headers=headers, json=update_data)
    assert response.status_code == 404
    assert "not found" in response.text.lower() or "product" in response.text.lower()

# 32: Successfully Delete a Product
def test_delete_product_success(auth_token, setup_data, wishlist_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    product_data = setup_data["products"][0]
    created = requests.post(f"{BASE_URL}/wishlists/{wishlist_id}/products", headers=headers, json=product_data).json()
    pid = created.get("id")
    assert pid is not None

    response = requests.delete(f"{BASE_URL}/products/{pid}", headers=headers)
    assert response.status_code == 204

# 33: Delete a Product That Doesn't Exist
def test_delete_nonexistent_product(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.delete(f"{BASE_URL}/products/999999", headers=headers)
    assert response.status_code == 404

# 34: Delete Another User's Product
def test_delete_other_user_product(auth_token_user_b, other_user_product_id):
    headers = {"Authorization": f"Bearer {auth_token_user_b}"}
    response = requests.delete(f"{BASE_URL}/products/{other_user_product_id}", headers=headers)
    assert response.status_code == 404
    assert "not found" in response.text.lower() or "product" in response.text.lower()