import pytest
import requests
import allure
from urls.api_urls import ApiUrls
from data.order_data import OrderData
from data.locators import ResponseLocators


class TestOrderList:
    
    @allure.title("Получение списка заказов")
    def test_get_orders_list_returns_orders(self):
        response = requests.get(ApiUrls.ORDERS)
        
        assert response.status_code == OrderData.STATUS_200
        response_data = response.json()
        assert ResponseLocators.ORDERS_FIELD in response_data
        assert isinstance(response_data[ResponseLocators.ORDERS_FIELD], list)