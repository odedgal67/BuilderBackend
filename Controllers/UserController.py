from singleton_decorator import singleton
from Utils.Exceptions import *
from Utils.PasswordHasher import *
from User import User
import string
import re

@singleton
class UserController:

    def __init__(self):
        self.users = dict(User) # Dict of all registered usernames and their user instance
    

    


    # ==================================API Methods==================================

    def register(self, username:str, password:str, id:str):
        if not _is_username_legal(username):
            raise IllegalUsernameException(username)
        
        if _is_username_exist(username):
            raise UsernameDoesntExistException(username)
        
        if _is_password_legal(password):
            raise IllegalPasswordException()
        
        # Create new user instance
        new_user = User(username=username, password=password ,id=id)
        # Add new user to users dict
        self.users[username] = new_user


    def login(self, username:str, password:str) -> bool:
        if not _is_username_exist(username):
            raise UsernameDoesntExistException(username)
        
        current_user : User = self.users[username]
        if not current_user.is_correct_password(password):
            raise IncorrectPasswordException()
        
        current_user.login()


# ================================Internal methods================================

def _is_username_exist(self, username:string) -> bool:
    registered_users_dict : dict = self.user_controller.users    
    return username in registered_users_dict.keys()


def _is_username_legal(self, username:str) -> bool:
    if len(username) < 3:
        return False
    if string.whitespace(username):
        return False
    return True
        

def _is_password_legal(password:str) -> bool:
    if len(password) < 6: # Too short
        return False
    if string.whitespace(password): # All whitespaces
        return False  
    if not re.search("[0,9]", password): # No digits
        return False
    if not re.search("[a,z]", password): # No small letters
        return False    
    if not re.search("[A,Z]", password): # No capital letters
        return False
    return True