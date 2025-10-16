import pytest
import requests
import allure
from urls.api_urls import ApiUrls
from data.order_data import OrderData, OrderTestData
from data.locators import ResponseLocators


class TestOrderCreate:
    
    @allure.title("Создание заказа с разными цветами: {description}")
    @pytest.mark.parametrize('colors, description', OrderTestData.get_color_combinations())  # ✅ данные из дата-модуля
    def test_create_order_with_different_colors(self, colors, description):
        payload = OrderTestData.get_order_with_colors(colors)
        
        response = requests.post(ApiUrls.ORDERS, json=payload)
        
        assert response.status_code == OrderData.STATUS_201
        response_data = response.json()
        assert ResponseLocators.TRACK_FIELD in response_data
        
        track = response_data[ResponseLocators.TRACK_FIELD]
        requests.put(f"{ApiUrls.ORDERS}/cancel", json={"track": track})
    
    @allure.title("Проверка наличия track в ответе при создании заказа")
    def test_create_order_response_contains_track(self):
        payload = OrderTestData.get_base_order_data()
        
        response = requests.post(ApiUrls.ORDERS, json=payload)
        
        assert response.status_code == OrderData.STATUS_201
        response_data = response.json()
        assert ResponseLocators.TRACK_FIELD in response_data
        assert isinstance(response_data[ResponseLocators.TRACK_FIELD], int)
        
        track = response_data[ResponseLocators.TRACK_FIELD]
        requests.put(f"{ApiUrls.ORDERS}/cancel", json={"track": track})