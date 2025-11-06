import pytest
import requests
import random
from conftest import BASE_URL

# Scenario 35: Endpoints sem token
def test_endpoints_without_authentication(sample_wishlist_id, sample_product_id):
    endpoints = [
        ("POST", f"{BASE_URL}/wishlists", {"name": "Teste"}),
        ("GET", f"{BASE_URL}/wishlists", None),
        ("POST", f"{BASE_URL}/wishlists/{sample_wishlist_id}/products", {"Product": "Teste", "Price": "100", "delivery_estimate": "2 dias"}),
        ("GET", f"{BASE_URL}/wishlists/{sample_wishlist_id}/products", None),
        ("PUT", f"{BASE_URL}/products/{sample_product_id}", {"Price": "1999", "delivery_estimate": "2 dias"}),
        ("DELETE", f"{BASE_URL}/products/{sample_product_id}", None),
        ("PATCH", f"{BASE_URL}/products/{sample_product_id}/toggle", None)
    ]

    for method, url, body in endpoints:
        if method == "POST":
            r = requests.post(url, json=body)
        elif method == "GET":
            r = requests.get(url)
        elif method == "PUT":
            r = requests.put(url, json=body)
        elif method == "DELETE":
            r = requests.delete(url)
        elif method == "PATCH":
            r = requests.patch(url)
        else:
            continue

        # Aqui esperamos 401 ou 404, dependendo se o endpoint existe ou não
        assert r.status_code in [401, 404], f"{method} {url} não retornou 401/404"
        if r.status_code == 401:
            assert "Not authenticated" in r.text or "Unauthorized" in r.text

# Scenario 36: Endpoints com token inválido
def test_endpoints_with_invalid_token(sample_wishlist_id, sample_product_id):
    invalid_header = {"Authorization": "Bearer invalidtoken"}

    endpoints = [
        ("POST", f"{BASE_URL}/wishlists", {"name": "Teste"}),
        ("GET", f"{BASE_URL}/wishlists", None),
        ("POST", f"{BASE_URL}/wishlists/{sample_wishlist_id}/products", {"Product": "Teste", "Price": "100", "delivery_estimate": "2 dias"}),
        ("GET", f"{BASE_URL}/wishlists/{sample_wishlist_id}/products", None),
        ("PUT", f"{BASE_URL}/products/{sample_product_id}", {"Price": "1999", "delivery_estimate": "2 dias"}),
        ("DELETE", f"{BASE_URL}/products/{sample_product_id}", None),
        ("PATCH", f"{BASE_URL}/products/{sample_product_id}/toggle", None)
    ]

    for method, url, body in endpoints:
        if method == "POST":
            r = requests.post(url, headers=invalid_header, json=body)
        elif method == "GET":
            r = requests.get(url, headers=invalid_header)
        elif method == "PUT":
            r = requests.put(url, headers=invalid_header, json=body)
        elif method == "DELETE":
            r = requests.delete(url, headers=invalid_header)
        elif method == "PATCH":
            r = requests.patch(url, headers=invalid_header)
        else:
            continue

        assert r.status_code in [401, 404], f"{method} {url} não retornou 401/404"
        if r.status_code == 401:
            assert (
                "Could not validate credentials" in r.text
                or "Token has expired" in r.text
                or "Invalid token" in r.text
            )
