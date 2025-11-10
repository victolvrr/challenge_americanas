import pytest
import requests

BASE_URL = "http://127.0.0.1:8000/"

# Scenario 35: Accessing Endpoint without Authentication Token
def test_endpoints_without_authentication(sample_wishlist_id, sample_product_id):
    endpoints = [
        ("POST", f"{BASE_URL}/wishlists", {"name": "Wishlist Sem Token"}),
        ("GET", f"{BASE_URL}/wishlists", None),
        ("POST", f"{BASE_URL}/wishlists/{sample_wishlist_id}/products", {"Product": "Sem Token", "Price": "100", "Zipcode": "00000000"}),
        ("GET", f"{BASE_URL}/wishlists/{sample_wishlist_id}/products", None),
        ("PUT", f"{BASE_URL}/products/{sample_product_id}", {"Price": "200"}),
        ("DELETE", f"{BASE_URL}/products/{sample_product_id}", None),
        # ("PATCH", f"{BASE_URL}/products/{sample_product_id}/toggle", None),
    ]

    for method, url, payload in endpoints:
        response = requests.request(method, url, json=payload)
        assert response.status_code in [401, 403], f"{url} deveria recusar sem token, mas retornou {response.status_code}: {response.text}"
        assert "not authenticated" in response.text.lower()

# Scenario 36: Accessing Endpoint with Invalid Token
def test_endpoints_with_invalid_token(sample_wishlist_id, sample_product_id):
    headers = {"Authorization": "Bearer INVALID_TOKEN"}
    endpoints = [
        ("POST", f"{BASE_URL}/wishlists", {"name": "Wishlist Invalida"}),
        ("GET", f"{BASE_URL}/wishlists", None),
        ("POST", f"{BASE_URL}/wishlists/{sample_wishlist_id}/products", {"Product": "Produto Inválido", "Price": "123", "Zipcode": "00000000"}),
        ("GET", f"{BASE_URL}/wishlists/{sample_wishlist_id}/products", None),
        ("PUT", f"{BASE_URL}/products/{sample_product_id}", {"Price": "999"}),
        ("DELETE", f"{BASE_URL}/products/{sample_product_id}", None),
        # ("PATCH", f"{BASE_URL}/products/{sample_product_id}/toggle", None),
    ]

    for method, url, payload in endpoints:
        response = requests.request(method, url, headers=headers, json=payload)
        assert response.status_code in [401, 403], f"{url} deveria recusar com token inválido, mas retornou {response.status_code}: {response.text}"
        assert "could not validate" in response.text.lower() or "expired" in response.text.lower()