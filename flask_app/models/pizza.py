from datetime import datetime

from flask_app.config.mysqlconnection import connectToMySQL


class Pizza:
    db_name = "mvcuserpizzaaaa"

    def __init__(self, data):
        self.id = data.get("pizza_id")  # Use .get() method to handle missing keys gracefully
        self.method = data.get("method")
        self.size = data.get("size")
        self.crust = data.get("crust")
        self.quantity = data.get("quantity")
        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")  # You can handle the missing key here

    @classmethod
    def create(cls, data):
        query = "INSERT INTO pizzas (method, size, crust, quantity, user_id) VALUES (%(method)s, %(size)s, %(crust)s, %(quantity)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def getLastOrder(cls):
        query = "SELECT * FROM pizzas ORDER BY created_at DESC LIMIT 1;"
        result = connectToMySQL(cls.db_name).query_db(query)
        if result:
            return result[0]
        return False


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM pizzas;"
        results = connectToMySQL(cls.db_name).query_db(query)
        pizzas = []
        if results:
            for pizza in results:
                pizzas.append(pizza)
        return pizzas

    @classmethod
    def get_pizza_by_id(cls, data):
        query = "SELECT * FROM pizzas WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM pizzas where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def addTopping(cls, data):
        query = "INSERT INTO pizzatoppings (pizza_id, topping_id) VALUES (%(pizza_id)s, %(topping_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)