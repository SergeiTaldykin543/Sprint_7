import pytest
import requests
from urls.api_urls import ApiUrls
from data.order_data import OrderData


class TestOrderList:
    
    def test_get_orders_list_returns_orders(self):
        response = requests.get(ApiUrls.ORDERS)
        
        assert response.status_code == OrderData.STATUS_200
        response_data = response.json()
        assert 'orders' in response_data
        assert isinstance(response_data['orders'], list)