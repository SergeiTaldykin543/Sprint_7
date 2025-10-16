import requests
import random
import string
import allure
from urls.api_urls import ApiUrls


class CourierHelper:
    
    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def create_unique_courier():
        with allure.step('Генерация уникальных данных курьера'):
            login = f"ninja_{CourierHelper.generate_random_string(6)}"
            password = "1234"
            first_name = "saske"

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        with allure.step('Создание курьера в системе'):
            response = requests.post(ApiUrls.COURIER, data=payload)

        if response.status_code == 201:
            return login, password
        return None, None

    @staticmethod
    def login_courier(login, password):
        with allure.step(f'Авторизация курьера {login}'):
            payload = {
                "login": login,
                "password": password
            }
            return requests.post(ApiUrls.COURIER_LOGIN, data=payload)