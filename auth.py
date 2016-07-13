from functools import wraps
from flask import request, Response
from models import Users
from database import session


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    user = session.query(Users).filter_by(name=username).first()
    return username == user.name  and password ==  user.password

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def requires_manager(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        user = session.query(Users).filter_by(name=auth.username).first()
        if user.privilegies == 0:
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def requires_boss(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        user = session.query(Users).filter_by(name=auth.username).first()
        if user.privilegies == 0 or user.privilegies == 1:
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        user = session.query(Users).filter_by(name=auth.username).first()
        if user.privilegies == 0 or user.privilegies == 1 or user.privilegies == 2:
            return authenticate()
        return f(*args, **kwargs)
    return decorated