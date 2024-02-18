import jwt
from flask import current_app, request


def userdata_from_token(info: str):
    """Resolve the header of the request and return the user_id"""
    auth_header = request.headers.get("Authorization")
    _, token = auth_header.split(" ")

    try:
        payload = jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
        )
        data = payload[info]
        return data
    except jwt.ExpiredSignatureError:
        return "-1"
