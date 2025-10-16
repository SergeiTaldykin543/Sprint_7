import pytest
import requests
import allure
from urls.api_urls import ApiUrls
from data.courier_data import CourierData
from data.locators import CourierLocators, ResponseLocators
from data.test_data import TestDataGenerator


class TestCourierCreate:
    
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, create_unique_courier):
        login, password = create_unique_courier
        assert login is not None
        assert password is not None
    
    @allure.title("Создание дубликата курьера")
    def test_create_duplicate_courier(self, create_unique_courier):
        login, password = create_unique_courier
        
        payload = {
            CourierLocators.LOGIN_FIELD: login,
            CourierLocators.PASSWORD_FIELD: password,
            CourierLocators.FIRST_NAME_FIELD: "saske"
        }
        response = requests.post(ApiUrls.COURIER, data=payload)
        
        assert response.status_code == CourierData.STATUS_409
    
    @allure.title("Создание курьера без обязательного поля: {missing_field}")
    @pytest.mark.parametrize('missing_field', [CourierLocators.LOGIN_FIELD, CourierLocators.PASSWORD_FIELD])
    def test_create_courier_missing_required_field(self, missing_field):
        unique_login = TestDataGenerator.generate_unique_login()
        
        payload = {
            CourierLocators.LOGIN_FIELD: unique_login,
            CourierLocators.PASSWORD_FIELD: "test_pass",
            CourierLocators.FIRST_NAME_FIELD: "test_name"
        }
        del payload[missing_field]
        
        response = requests.post(ApiUrls.COURIER, data=payload)
        assert response.status_code == CourierData.STATUS_400
    
    @allure.title("Проверка кода ответа при создании курьера")
    def test_create_courier_returns_correct_code(self, create_unique_courier):
        login, password = create_unique_courier
        assert login is not None
    
    @allure.title("Проверка успешного ответа при создании курьера")
    def test_create_courier_success_response(self):
        unique_login = TestDataGenerator.generate_unique_login()
        
        payload = {
            CourierLocators.LOGIN_FIELD: unique_login,
            CourierLocators.PASSWORD_FIELD: "1234",
            CourierLocators.FIRST_NAME_FIELD: "saske"
        }
        
        response = requests.post(ApiUrls.COURIER, data=payload)
        
        assert response.status_code == CourierData.STATUS_201
        assert response.json() == CourierData.CREATION_SUCCESS
        
        with allure.step('Очистка тестовых данных'):
            login_response = requests.post(ApiUrls.COURIER_LOGIN, data={
                CourierLocators.LOGIN_FIELD: unique_login,
                CourierLocators.PASSWORD_FIELD: "1234"})
            
            assert login_response.status_code == CourierData.STATUS_200
            
            courier_id = login_response.json()[ResponseLocators.ID_FIELD]
            delete_response = requests.delete(f"{ApiUrls.BASE_URL}/courier/{courier_id}")
            assert delete_response.status_code == CourierData.STATUS_200
    
    @allure.title("Создание курьера с дублирующимся логином")
    def test_create_courier_duplicate_login_error(self, create_unique_courier):
        login, password = create_unique_courier
        
        payload = {
            CourierLocators.LOGIN_FIELD: login,
            CourierLocators.PASSWORD_FIELD: "different_password",
            CourierLocators.FIRST_NAME_FIELD: "different_name"
        }
        response = requests.post(ApiUrls.COURIER, data=payload)
        
        assert response.status_code == CourierData.STATUS_409