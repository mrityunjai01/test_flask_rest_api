from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate(username, password):
    """
    Function called when /auth is reached
    :param username:
    :param password:
    :return: A user if authentication successful, none otherewise
    """
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user
def identity(payload):
    """
    Function that is called when a user has already authenticated & flask JWT verified that their authorization header is correct
    :param payload: a dictionary with 'identity' key
    :return: a UserModel object
    """
    id = payload['identity']
    return UserModel.find_by_id(id)