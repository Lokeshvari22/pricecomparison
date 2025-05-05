import pytest
from django.test import Client
from unittest.mock import patch

@pytest.mark.django_db
@patch("home.views.extract_product_data")
def test_search_integration_mobiles(mock_extract):
    # Mock return for both brands
    mock_extract.side_effect = [
        [{'name': 'Galaxy S24', 'price': 79999}],  # Samsung products
        [{'name': 'iPhone 14', 'price': 89999}]    # Apple products
    ]

    client = Client()
    response = client.post("/search", {
        "category": "mobiles",
        "brand1": "samsung",
        "brand2": "apple"
    })

    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "Galaxy S24" in content
    assert "iPhone 14" in content
    assert "Samsung" in content or "samsung" in content
    assert "Apple" in content or "apple" in content
