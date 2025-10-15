import pytest
import requests
import allure
from helpers.courier import CourierHelper
from urls.api_urls import ApiUrls


@pytest.fixture
def courier_helper():
    return CourierHelper()


@pytest.fixture
def create_unique_courier(courier_helper):
    login, password = courier_helper.create_unique_courier()
    
    if not login:
        pytest.skip("Не удалось создать курьера для теста")
    
    yield login, password
    
    with allure.step('Удаление тестового курьера'):
        login_response = courier_helper.login_courier(login, password)
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
            requests.delete(f"{ApiUrls.BASE_URL}/courier/{courier_id}")

