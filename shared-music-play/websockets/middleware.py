from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            request_params = scope["query_string"].decode().split("&")
            request_params_dict = dict((param.split("=") for param in request_params))
            token_key = request_params_dict.get("token", None)
        except ValueError:
            token_key = None

        if token_key is None:
            scope["user"] = AnonymousUser()
        else:
            scope["user"] = await get_user(token_key)

        return await super().__call__(scope, receive, send)
