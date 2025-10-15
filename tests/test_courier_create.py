import pytest
import requests
import allure
from urls.api_urls import ApiUrls
from data.courier_data import CourierData
from data.locators import CourierLocators, ResponseLocators


class TestCourierCreate:
    
    def test_create_courier_success(self, create_unique_courier):
        with allure.step('Проверка успешного создания курьера'):
            login, password = create_unique_courier
            assert login is not None
            assert password is not None
    
    def test_create_duplicate_courier(self, create_unique_courier):
        login, password = create_unique_courier
        
        with allure.step('Попытка создания дубликата курьера'):
            payload = {
                CourierLocators.LOGIN_FIELD: login,
                CourierLocators.PASSWORD_FIELD: password,
                CourierLocators.FIRST_NAME_FIELD: "saske"
            }
            response = requests.post(ApiUrls.COURIER, data=payload)
        
        with allure.step('Проверка ошибки конфликта'):
            assert response.status_code == CourierData.STATUS_409
    
    @pytest.mark.parametrize('missing_field', [CourierLocators.LOGIN_FIELD, CourierLocators.PASSWORD_FIELD])
    def test_create_courier_missing_required_field(self, missing_field):
        import random
        import string
        
        with allure.step('Подготовка уникальных данных'):
            unique_login = f"test_{''.join(random.choices(string.ascii_lowercase, k=8))}"
        
        payload = {
            CourierLocators.LOGIN_FIELD: unique_login,
            CourierLocators.PASSWORD_FIELD: "test_pass",
            CourierLocators.FIRST_NAME_FIELD: "test_name"
        }
        del payload[missing_field]
        
        with allure.step(f'Создание курьера без поля {missing_field}'):
            response = requests.post(ApiUrls.COURIER, data=payload)
        
        with allure.step('Проверка ошибки валидации'):
            assert response.status_code == CourierData.STATUS_400
    
    def test_create_courier_returns_correct_code(self, create_unique_courier):
        with allure.step('Проверка кода ответа'):
            login, password = create_unique_courier
            assert login is not None
    
    def test_create_courier_success_response(self):
        import random
        import string
        
        with allure.step('Подготовка уникальных данных'):
            unique_login = f"test_{''.join(random.choices(string.ascii_lowercase, k=8))}"
        
        payload = {
            CourierLocators.LOGIN_FIELD: unique_login,
            CourierLocators.PASSWORD_FIELD: "1234",
            CourierLocators.FIRST_NAME_FIELD: "saske"
        }
        
        with allure.step('Создание курьера'):
            response = requests.post(ApiUrls.COURIER, data=payload)
        
        if response.status_code == CourierData.STATUS_201:
            with allure.step('Проверка успешного ответа'):
                assert response.json() == CourierData.CREATION_SUCCESS
            
            with allure.step('Очистка тестовых данных'):
                login_response = requests.post(ApiUrls.COURIER_LOGIN, data={
                    CourierLocators.LOGIN_FIELD: unique_login,
                    CourierLocators.PASSWORD_FIELD: "1234"})
                if login_response.status_code == 200:
                    courier_id = login_response.json()[ResponseLocators.ID_FIELD]
                    requests.delete(f"{ApiUrls.BASE_URL}/courier/{courier_id}")
    
    def test_create_courier_missing_field_error(self):
        import random
        import string
        
        with allure.step('Подготовка уникальных данных'):
            unique_login = f"test_{''.join(random.choices(string.ascii_lowercase, k=8))}"
        
        with allure.step('Тестирование отсутствия логина'):
            payload_without_login = {
                CourierLocators.PASSWORD_FIELD: "test_pass",
                CourierLocators.FIRST_NAME_FIELD: "test_name"
            }
            response = requests.post(ApiUrls.COURIER, data=payload_without_login)
            assert response.status_code == CourierData.STATUS_400
        
        with allure.step('Тестирование отсутствия пароля'):
            payload_without_password = {
                CourierLocators.LOGIN_FIELD: unique_login,
                CourierLocators.FIRST_NAME_FIELD: "test_name"
            }
            response = requests.post(ApiUrls.COURIER, data=payload_without_password)
            assert response.status_code == CourierData.STATUS_400
    
    def test_create_courier_duplicate_login_error(self, create_unique_courier):
        login, password = create_unique_courier
        
        with allure.step('Попытка создания курьера с существующим логином'):
            payload = {
                CourierLocators.LOGIN_FIELD: login,
                CourierLocators.PASSWORD_FIELD: "different_password",
                CourierLocators.FIRST_NAME_FIELD: "different_name"
            }
            response = requests.post(ApiUrls.COURIER, data=payload)
        
        with allure.step('Проверка ошибки дублирования'):
            assert response.status_code == CourierData.STATUS_409