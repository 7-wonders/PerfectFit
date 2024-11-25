from flask import Response


class Cookie:
    @staticmethod
    def save(response: Response, key: str, value: str, expiration: int):
        response.set_cookie(
            key,
            value,
            httponly=True,
            secure=True,
            samesite='LAX',
            expires=expiration
        )

    @staticmethod
    def delete(response: Response, key: str):
        response.delete_cookie(key)
