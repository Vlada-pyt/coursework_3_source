import base64
import hashlib
import datetime
import jwt
import hmac
import calendar
from flask import abort
from flask import current_app

from project.constaints import JWT_ALGORITHM, JWT_SECRET, PWD_HASH_SALT, PWD_HASH_ITERATIONS



def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )

def compare_passwords(password_hash, other_password) -> bool:
    decoded_digest = base64.b64decode(password_hash)

    hash_digest = hashlib.pbkdf2_hmac(
        'sha256',
        other_password.encode(),
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    )
    return hmac.compare_digest(decoded_digest, hash_digest)

def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compose_passwords(password_hash, password):
    return password_hash == generate_password_hash(password)


def generate_tokens(email, password, password_hash=None, is_refresh=False):

    if email is None:
        raise abort(404)

    if not is_refresh:
        if not compare_passwords(other_password=password, password_hash=password_hash):
            abort(400)

    data = {
        "email": email,
        "password": password,
        }

    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {"access_token": access_token,
            "refresh_token": refresh_token}

def approve_refresh_token(refresh_token):
    data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=JWT_ALGORITHM)
    username = data.get("username")
    return generate_tokens(username, None, is_refresh=True)


def get_data_from_token(refresh_token):
    try:
        data = jwt.decode(jwt=refresh_token, key=current_app.config['SECRET_KEY'],
                          algorithms=[current_app.config['ALGORITHM']])
        return data
    except Exception:
        return None

