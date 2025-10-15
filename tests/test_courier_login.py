import pytest
import requests
import allure
from urls.api_urls import ApiUrls
from data.courier_data import CourierData
from data.locators import CourierLocators, ResponseLocators


class TestCourierLogin:
    
    def test_login_courier_success(self, create_unique_courier):
        login, password = create_unique_courier
        
        with allure.step('Авторизация курьера'):
            response = requests.post(ApiUrls.COURIER_LOGIN, data={
                CourierLocators.LOGIN_FIELD: login,
                CourierLocators.PASSWORD_FIELD: password})
        
        with allure.step('Проверка успешной авторизации'):
            assert response.status_code == CourierData.STATUS_200
    
    def test_login_courier_requires_all_fields(self):
        with allure.step('Попытка авторизации без пароля'):
            response = requests.post(ApiUrls.COURIER_LOGIN, data={
                CourierLocators.LOGIN_FIELD: "test"})
        
        with allure.step('Проверка что ответ не успешный'):
            assert response.status_code != CourierData.STATUS_200
    
    def test_login_courier_wrong_credentials(self, create_unique_courier):
        login, password = create_unique_courier
        
        with allure.step('Попытка авторизации с неправильным паролем'):
            response = requests.post(ApiUrls.COURIER_LOGIN, data={
                CourierLocators.LOGIN_FIELD: login,
                CourierLocators.PASSWORD_FIELD: "wrong_password"})
            assert response.status_code == CourierData.STATUS_404
        
        with allure.step('Попытка авторизации с неправильным логином'):
            response = requests.post(ApiUrls.COURIER_LOGIN, data={
                CourierLocators.LOGIN_FIELD: "wrong_login",
                CourierLocators.PASSWORD_FIELD: password})
            assert response.status_code == CourierData.STATUS_404
    
    @pytest.mark.parametrize('missing_field', [CourierLocators.LOGIN_FIELD, CourierLocators.PASSWORD_FIELD])
    def test_login_courier_missing_field_error(self, missing_field):
        with allure.step(f'Подготовка данных без поля {missing_field}'):
            payload = {
                CourierLocators.LOGIN_FIELD: "test",
                CourierLocators.PASSWORD_FIELD: "test"
            }
            del payload[missing_field]
        
        with allure.step('Попытка авторизации'):
            response = requests.post(ApiUrls.COURIER_LOGIN, data=payload)
        
        with allure.step('Проверка что ответ не успешный'):
            assert response.status_code != CourierData.STATUS_200
    
    def test_login_nonexistent_courier_error(self):
        with allure.step('Попытка авторизации несуществующего курьера'):
            response = requests.post(ApiUrls.COURIER_LOGIN, data={
                CourierLocators.LOGIN_FIELD: "nonexistent_user_123",
                CourierLocators.PASSWORD_FIELD: "nonexistent_password"})
        
        with allure.step('Проверка ошибки'):
            assert response.status_code == CourierData.STATUS_404
    
    def test_login_courier_returns_id(self, create_unique_courier):
        login, password = create_unique_courier
        
        with allure.step('Авторизация курьера'):
            response = requests.post(ApiUrls.COURIER_LOGIN, data={
                CourierLocators.LOGIN_FIELD: login,
                CourierLocators.PASSWORD_FIELD: password})
        
        with allure.step('Проверка наличия ID в ответе'):
            assert response.status_code == CourierData.STATUS_200
            assert ResponseLocators.ID_FIELD in response.json()