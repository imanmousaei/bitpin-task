from decimal import Decimal
from typing import Optional

from django.conf import settings
from django.core.cache import cache


class CacheService:

    @staticmethod
    def get_decimal(key: str) -> Optional[Decimal]:
        """
        returns True if this key exists in cache
        """
        value = cache.get(key)

        if value is None:
            return None

        return Decimal(value)

    @staticmethod
    def set_decimal(key: str, value: Decimal):
        cache.set(key, str(value), timeout=settings.RATING_CACHE_TIMEOUT)
