import redis

from django.conf import settings
from django.contrib.auth.models import User

from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])

class RedisJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> tuple[User, str]:
        """Overrides default `rest_framework_simplejwt.authentication.JWTAuthentication.authenticate`
        behavior, raising `rest_framework.exceptions.AuthenticationFailed` if the current JWT token 
        was not found in Redis cache.
        
        :param `rest_framework.request.Request` request: current HTTP request
        :return: User, associated with the current request, and their access token
        :rtype: `tuple[django.conf.settings.AUTH_USER_MODEL, str]`
        """
        validated_token = super().authenticate(request)
        if validated_token is None:
            return None

        user, token = validated_token

        if not redis_client.exists(f"jwt:{token}"):
            raise AuthenticationFailed("Token is invalid or has been revoked.")
        
        return user, token
