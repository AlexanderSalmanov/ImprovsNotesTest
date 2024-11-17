import logging

from django.core.cache import cache
from django.contrib.auth.models import User
from rest_framework.request import Request


logger = logging.getLogger(__name__)


class CacheInvalidationMixin:
    """Wrapper allowing basic cache invalidation for extended views.
    """
    @staticmethod
    def notes_cache_key(user: User) -> str:
        """Gets cache key for `Notes` model for specific user.
        
        :param `django.contrib.auth.models.User` user: User object
        :return: corresponding cache key
        :rtype: `str`
        """
        return f'user_{user.id}_notes_cache_key'

    def invalidate_cache(self, user: User) -> None:
        """Invalidates cache entry for the provided user.
        
        :param `django.contrib.auth.models.User` user: User object
        :rtype: `None`
        """
        cache_key = self.notes_cache_key(user)
        cache.delete(cache_key)
        logger.info(f"Cache invalidated for user {user.id}")