import pytest
import requests
from urls.api_urls import ApiUrls
from data.order_data import OrderData, OrderTestData


class TestOrderCreate:
    
    @pytest.mark.parametrize('colors, description', [
        (["BLACK"], "один цвет BLACK"),
        (["GREY"], "один цвет GREY"), 
        (["BLACK", "GREY"], "оба цвета"),
        ([], "без цвета")])
    
    def test_create_order_with_different_colors(self, colors, description):
        payload = OrderTestData.get_order_with_colors(colors)
        
        response = requests.post(ApiUrls.ORDERS, json=payload)
        
        assert response.status_code == OrderData.STATUS_201
        assert 'track' in response.json()
    
    def test_create_order_response_contains_track(self):
        payload = OrderTestData.get_base_order_data()
        
        response = requests.post(ApiUrls.ORDERS, json=payload)
        
        assert response.status_code == OrderData.STATUS_201
        response_data = response.json()
        assert 'track' in response_data
        assert isinstance(response_data['track'], int)