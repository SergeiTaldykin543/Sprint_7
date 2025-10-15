import requests
import random
import string
import allure
from urls.api_urls import ApiUrls


class CourierHelper:
    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    def create_unique_courier(self):
        with allure.step('Генерация уникальных данных курьера'):
            login = f"ninja_{self.generate_random_string(6)}"
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

    def login_courier(self, login, password):
        with allure.step(f'Авторизация курьера {login}'):
            payload = {
                "login": login,
                "password": password
            }
            return requests.post(ApiUrls.COURIER_LOGIN, data=payload)