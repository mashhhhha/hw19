import base64
import calendar
import datetime
import hashlib
import hmac
from flask import abort
import jwt
from constants import ALGO, SECRET, PWD_HASH_ITERATIONS, PWD_HASH_SALT
from implemented import user_service


def generate_tokens(username, password, role, is_refresh=False):
    """ generating access and refresh tokens"""
    user = user_service.get_by_name(username)

    if user is None:
        raise abort(404)

    db_pass = user.password

    if not is_refresh:
        if not check_password(db_pass, password):
            raise abort(400)

    data = {
        'username': username,
        'password': password,
        'role': role
    }
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data['exp'] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, SECRET, algorithm=ALGO)

    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data['exp'] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, SECRET, algorithm=ALGO)

    return {'access_token': access_token,
            'refresh_token': refresh_token}


def check_password(db_hash, client_password):
    """checking entered password"""

    decoded_digest = base64.b64decode(db_hash)

    hash_digest = hashlib.pbkdf2_hmac(
        'sha256',
        client_password.encode('utf-8'),
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    )

    return hmac.compare_digest(decoded_digest, hash_digest)


def approve_refresh_token(refresh_token):
    """ generating a new pair of tokens"""
    try:
        data = jwt.decode(jwt=refresh_token, key=SECRET, algorithms=[ALGO])

    except Exception as e:
        return f'{e}', 401

    username = data.get('username')
    role = data.get('role')

    return generate_tokens(username, None, role, is_refresh=True)