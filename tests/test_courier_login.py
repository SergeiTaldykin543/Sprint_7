import pytest
import requests
import allure
from urls.api_urls import ApiUrls
from data.courier_data import CourierData
from data.locators import CourierLocators, ResponseLocators


class TestCourierLogin:
    
    @allure.title("Успешная авторизация курьера")
    def test_login_courier_success(self, create_unique_courier):
        login, password = create_unique_courier
        
        response = requests.post(ApiUrls.COURIER_LOGIN, data={
            CourierLocators.LOGIN_FIELD: login,
            CourierLocators.PASSWORD_FIELD: password})
        
        assert response.status_code == CourierData.STATUS_200
    
    @allure.title("Авторизация без пароля")
    def test_login_courier_requires_all_fields(self):
        response = requests.post(ApiUrls.COURIER_LOGIN, data={
            CourierLocators.LOGIN_FIELD: "test"})
        
        assert response.status_code != CourierData.STATUS_200
    
    @allure.title("Авторизация с неверными учетными данными")
    def test_login_courier_wrong_credentials(self, create_unique_courier):
        login, password = create_unique_courier
        
        response = requests.post(ApiUrls.COURIER_LOGIN, data={
            CourierLocators.LOGIN_FIELD: login,
            CourierLocators.PASSWORD_FIELD: "wrong_password"})
        assert response.status_code == CourierData.STATUS_404
        
        response = requests.post(ApiUrls.COURIER_LOGIN, data={
            CourierLocators.LOGIN_FIELD: "wrong_login",
            CourierLocators.PASSWORD_FIELD: password})
        assert response.status_code == CourierData.STATUS_404
    
    @allure.title("Авторизация без обязательного поля: {missing_field}")
    @pytest.mark.parametrize('missing_field', [CourierLocators.LOGIN_FIELD, CourierLocators.PASSWORD_FIELD])
    def test_login_courier_missing_field_error(self, missing_field):
        payload = {
            CourierLocators.LOGIN_FIELD: "test",
            CourierLocators.PASSWORD_FIELD: "test"
        }
        del payload[missing_field]
        
        response = requests.post(ApiUrls.COURIER_LOGIN, data=payload)
        assert response.status_code != CourierData.STATUS_200
    
    @allure.title("Авторизация несуществующего курьера")
    def test_login_nonexistent_courier_error(self):
        response = requests.post(ApiUrls.COURIER_LOGIN, data={
            CourierLocators.LOGIN_FIELD: "nonexistent_user_123",
            CourierLocators.PASSWORD_FIELD: "nonexistent_password"})
        
        assert response.status_code == CourierData.STATUS_404
    
    @allure.title("Проверка наличия ID в ответе при авторизации")
    def test_login_courier_returns_id(self, create_unique_courier):
        login, password = create_unique_courier
        
        response = requests.post(ApiUrls.COURIER_LOGIN, data={
            CourierLocators.LOGIN_FIELD: login,
            CourierLocators.PASSWORD_FIELD: password})
        
        assert response.status_code == CourierData.STATUS_200
        assert ResponseLocators.ID_FIELD in response.json()