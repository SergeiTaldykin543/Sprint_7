class CourierData:
    # Коды состояния
    STATUS_200 = 200
    STATUS_201 = 201
    STATUS_400 = 400
    STATUS_404 = 404
    STATUS_409 = 409
    
    # Успешный ответ
    CREATION_SUCCESS = {"ok": True}
    
    # Сообщения об ошибках
    INSUFFICIENT_DATA_CREATION = "Недостаточно данных для создания учетной записи"
    INSUFFICIENT_DATA_LOGIN = "Недостаточно данных для входа"


class CourierExamples:
    """Примеры данных из документации API"""
    CREATE_COURIER_EXAMPLE = {
        "login": "ninja",
        "password": "1234",
        "firstName": "saske"
    }
    
    LOGIN_COURIER_EXAMPLE = {
        "login": "ninja",
        "password": "1234"
    }