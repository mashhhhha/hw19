import jwt
from constants import SECRET, ALGO
from flask import request, abort


def auth_required(func):
    """checking user's authorization"""
    def wrapper(*args, **kwargs):

        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']

        token = data.split('Bearer ')[-1]

        try:
            jwt.decode(token, SECRET, algorithms=[ALGO])

        except Exception as e:
            print('JWT Decode Exception', e)
            abort(401)

        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    """checking user's role"""
    def wrapper(*args, **kwargs):

        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']

        token = data.split('Bearer ')[-1]

        try:
            decoded_token = jwt.decode(token, SECRET, algorithms=[ALGO])

            if decoded_token['role'] != 'admin':
                abort(403)

        except Exception as e:
            print('JWT Decode Exception', e)
            abort(401)

        return func(*args, **kwargs)
    return wrapper