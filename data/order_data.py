class OrderTestData:
    @staticmethod
    def get_base_order_data():
        return {
            "firstName": "Сергей",
            "lastName": "Талдыкин",
            "address": "ул. Есенина, д. 1",
            "metroStation": "1",
            "phone": "+79991234567",
            "rentTime": 3,
            "deliveryDate": "2025-10-14",
            "comment": "Тестовый заказ"
        }
    
    @staticmethod
    def get_order_with_colors(colors):
        data = OrderTestData.get_base_order_data()
        if colors:
            data["color"] = colors
        return data
    
    @staticmethod
    def get_color_combinations():
        return [
            (["BLACK"], "один цвет BLACK"),
            (["GREY"], "один цвет GREY"), 
            (["BLACK", "GREY"], "оба цвета"),
            ([], "без цвета")
        ]