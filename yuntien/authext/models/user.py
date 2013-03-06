_current_user = None

def get_current_user():
    return _current_user

def set_current_user(user):
    global _current_user
    _current_user = user
