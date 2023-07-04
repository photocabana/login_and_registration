from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# The above is used when we do login registration, be sure to install flask-bcrypt: pipenv install flask-bcrypt


class User:
    db = "login_and_registration" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # What changes need to be made above for this project?
        #What needs to be added her for class association?




    # Login


    @staticmethod
    def login(data):
        profile_user = User.get_user_by_email(data['email'])
        if profile_user:
            if bcrypt.check_password_hash(profile_user.password, data['password']):
                session['user_id'] = profile_user.id
                session['user_name'] = f'{profile_user.first_name} {profile_user.last_name}'
                return True
        flash('Something has went wrong! Could be email or password..')
        return False



    # Create Users Models


    @classmethod
    def create_user(cls, user_info):
        if not cls.validate_user_data(user_info):
            return False
        user_info = user_info.copy()
        user_info['password'] = bcrypt.generate_password_hash(user_info['password'])
        query = """
        INSERT INTO users 
        (first_name, last_name, email, password)
        VALUES 
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query, user_info)
        session['user_id'] = user_id
        session['user_name'] = f'{user_info["first_name"]} {user_info["last_name"]}'
        return user_id
    

    # Read Users Models

    @classmethod
    def get_user_by_id(cls, user_id):
        data = { 'id' : user_id }
        query = """
        SELECT *
        FROM users
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])


    @classmethod
    def get_user_by_email(cls, email):
        data = { 'email' : email }
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return cls(result[0])
        return False


    @classmethod
    def get_all_users(cls):
        query = """
        SELECT * 
        FROM users
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users


    # Update Users Models



    # Delete Users Models
    






    # Helper Methods
    
    @staticmethod
    def validate_user_data(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 2 :
            flash('Your first name must contain at least two character. Try Again!')
            is_valid = False
        if len(data['last_name']) < 2 :
            flash('Your last name must contain at least two characters. Try Again!')
            is_valid = False
        if 'id' not in data:  #Congrats it's a new user
            if len(data['password']) < 8 :
                flash('Your password must be at least 8 characters long. Try Again!')
                is_valid = False
            if data['password'] != data['confirm_password'] :
                flash('Your password no matchy, no worky! Try Again!')
                is_valid = False
        if 'id' not in data or data['email'] != User.get_user_by_id(data['id']).email :
            if not EMAIL_REGEX.match(data['email']): 
                flash("Please try a valid email address next time.")
                is_valid = False
            if User.get_user_by_email(data['email']):
                flash('That email is taken')
                is_valid = False
        return is_valid





    # @staticmethod
    # def parse_user_data(data):
    #     parsed_data = {
    #         'email' : data['email'],
    #         'first_name' : data['first_name'],
    #         'last_name' : data['last_name'],
    #         'password' : bcrypt.generate_password_hash(data['password'])
    #     }
    #     print('!!!!!!!!!!!!!!!!!!!!', parsed_data)
    #     return(parsed_data)
    
    
    
    
    # cls.parse_user_data(user_info)