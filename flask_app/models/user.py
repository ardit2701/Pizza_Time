import re

from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
PASWORD_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class User:
    db_name = "mvcuserpizzaaaa"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.address = data["address"]
        self.city = data["city"]
        self.state = data["state"]
        self.password = data["password"]
        self.confirm_password = data["confirm_password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.phone_number = data["phone_number"]

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users where email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users where user_id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, address, city, state, password, confirm_password, phone_number) VALUES (%(first_name)s, %(last_name)s, %(email)s,%(address)s,%(city)s,%(state)s, %(password)s, %(confirm_password)s, %(phone_number)s );"
        return connectToMySQL(cls.db_name).query_db(query, data)

    #@classmethod
    #def update(cls, data):
    #    query = "UPDATE users set first_name = %(first_name)s, last_name = %(last_name)s WHERE id = %(id)s;"
    #    return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email address!", "emailLogin")
            is_valid = False
        if len(user["password"]) < 1:
            flash("Password is required!", "passwordLogin")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_userRegister(user):
        is_valid = True
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email address!", "emailRegister")
            is_valid = False
        if len(user["password"]) < 1:
            flash("Password is required!", "passwordRegister")
            is_valid = False
        if user["password"] != user["confirm_password"]:
            flash("Passwords do not match!", "confirm_passwordRegister")
            is_valid = False
        if len(user["first_name"]) < 1:
            flash("First name is required!", "nameRegister")
            is_valid = False
        if len(user["last_name"]) < 1:
            flash("Last name is required!", "last_nameRegister")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_userUpdate(user):
        is_valid = True
        if len(user["first_name"]) < 1:
            flash("First name is required!", "nameRegister")
            is_valid = False
        if len(user["last_name"]) < 1:
            flash("Last name is required!", "last_nameRegister")
            is_valid = False
        return is_valid
    
    @staticmethod
    def update_profile(data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s"
        if "email" in data:
            query += ", email = %(email)s"
        if "address" in data:
            query += ", address = %(address)s"
        if "city" in data:
            query += ", city = %(city)s"
        if "state" in data:
            query += ", state = %(state)s"
        if "phone_number" in data:
            query += ", phone_number = %(phone_number)s"    
        query += " WHERE user_id = %(id)s;"
        return connectToMySQL(User.db_name).query_db(query, data)
    
    @classmethod
    def createPayment(cls,data):
        query = "INSERT INTO payments (ammount, status, member_id) VALUES (%(ammount)s, %(status)s, %(member_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_allUserPayments(cls, data):
        query = "SELECT * FROM payments where member_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        payments = []
        if results:
            for pay in results:
                payments.append(pay)
        return payments
        