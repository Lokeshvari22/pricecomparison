import pytest
from django.urls import reverse
from django.test import Client
from unittest.mock import patch

@pytest.mark.django_db
class TestSearchCompareViews:
    def setup_method(self):
        self.client = Client()

    @patch('home.views.extract_product_data')
    @patch('home.views.compare_clothing_products')
    def test_search_clothes_valid(self, mock_compare, mock_extract):
        mock_extract.return_value = [{'name': 'Red T-shirt', 'price': '499'}]
        mock_compare.return_value = [{'name': 'Red T-shirt', 'match': True}]

        response = self.client.post(reverse('search'), {
            'category': 'clothes',
            'search': 'tshirt'
        })

        assert response.status_code == 200
        assert 'matches' in response.context
        assert 'products1' in response.context
        assert 'products2' in response.context
        assert response.templates[0].name == 'search.html'

    @patch('home.views.extract_product_data')
    def test_search_mobiles_valid(self, mock_extract):
        mock_extract.return_value = [{'name': 'iPhone', 'price': '79999'}]

        response = self.client.post(reverse('search'), {
            'category': 'mobiles',
            'brand1': 'apple',
            'brand2': 'apple'
        })

        assert response.status_code == 200
        assert 'products1' in response.context
        assert 'products2' in response.context
        assert response.templates[0].name == 'select_compare.html'

    def test_search_invalid_input(self):
        response = self.client.post(reverse('search'), {
            'category': 'unknown'
        })
        assert response.status_code == 200
        assert response.templates[0].name == 'Prnotfound.html'

    def test_compare_post_valid(self):
        response = self.client.post(reverse('compare'), {
            'category': 'mobiles',
            'selected_products': [
                "Phone#FIELD#img.jpg#FIELD#50000#FIELD#4.5#FIELD#8.0#FIELD#9.0#FIELD#9.5#FIELD#RAM<br>Camera#FIELD#link1",
                "Phone#FIELD#img2.jpg#FIELD#45000#FIELD#4.2#FIELD#7.5#FIELD#8.0#FIELD#8.5#FIELD#Battery<br>Design#FIELD#link2",
            ]
        })

        assert response.status_code == 200
        assert 'products' in response.context
        assert response.templates[0].name == 'comparison_table.html'
        assert len(response.context['products']) == 2

    def test_compare_invalid_post(self):
        response = self.client.post(reverse('compare'), {
            'category': 'mobiles',
            'selected_products': ['invalid-data']
        })

        assert response.status_code == 200
        assert response.templates[0].name == 'comparison_table.html' or 'Prnotfound.html' in [t.name for t in response.templates]
