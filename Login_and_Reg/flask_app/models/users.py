from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    DB = 'validation_schema'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']


    @staticmethod
    def validate_user(NewUser):
        is_valid = True
        if len(NewUser['first_name']) < 2:
            flash('First name is required!')
            is_valid = False

        if len(NewUser['last_name']) < 2:
            flash('Last name is required!')
            is_valid = False

        if len(NewUser['email']) < 1:
            flash('Email is required!')
            is_valid = False
        if not EMAIL_REGEX.match(NewUser['email']):
            flash('Invalid email, please try again!')
            is_valid = False

        if len(NewUser['password']) < 8:
            flash('Password with 8 charcaters or more is required!')
            is_valid = False

        return is_valid


    @classmethod
    def CreateUser(cLs, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """
        result = connectToMySQL(cLs.DB).query_db(query, data)
        return result

        
    @classmethod
    def GetUserById(cLs, data):
        query = """
        SELECT * FROM users
        WHERE id = %(user_id)s;
        """
        result = connectToMySQL(cLs.DB).query_db(query, data)
        return cLs(result[0])


    @classmethod
    def GetUserByEmail(cLs, data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        result = connectToMySQL(cLs.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cLs(result[0])


   