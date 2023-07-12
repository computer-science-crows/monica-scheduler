from app.user import get_user, set_user
from domain.user import User

class Auth:

    def __init__(self) -> None:
        pass

    def sign_up(alias, full_name, password):

        user = get_user(alias)

        if user != None:
            print(f"Cannot sign up because a user with the same alias already exists.")
            return False
        
        user = User(alias, full_name, password)
        set_user(user)

        return True


    def log_in(alias, password):

        user = get_user(alias)

        if user == None:
            print(f"There is no user with the alias {alias}.")
            return False
        
        if user.password != password:
            print(f"Incorrect password.")
            return False
        
        user.logged()
        set_user(user)

        return True


        

        