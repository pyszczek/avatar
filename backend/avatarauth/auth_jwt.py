import jwt

from django.conf import settings

JWT_SETTINGS = settings.AVATAR_APP['JWT']


def generate_jwt(sub: str, name: str, roles: list, secret_key: str, algorithm: str = JWT_SETTINGS['ALGORITHM']) -> str:
    payload = {
        'iss': JWT_SETTINGS['ISS'],
        'sub': sub,
        'name': name,
        'roles': roles,
    }

    return jwt.encode(payload, key=secret_key, algorithm=algorithm)


def decode_jwt(in_jwt: str, secret_key: str):
    try:
        received_message = jwt.decode(in_jwt, key=secret_key)
    except Exception as err:
        print(err)
        return None
    return received_message
