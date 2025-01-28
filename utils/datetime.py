from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import DateTime, TypeDecorator
from sqlalchemy.engine import Dialect

__all__ = ["Datetime"]

class Datetime(TypeDecorator):
    """
    A SQLAlchemy TypeDecorator for handling datetime values with timezone information.
    Ensures that datetime values are stored in UTC and retrieved with UTC timezone information.
    """
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value: Optional[datetime], dialect: Dialect) -> Optional[datetime]:
        """
        Process a datetime value before binding it to a database parameter.

        Converts the datetime to UTC if it has timezone information and removes
        the timezone information before returning it.

        :param value: The datetime value to be processed. If None, no processing is done.
        :param dialect: The SQLAlchemy dialect in use.
        :return: The processed datetime value with timezone information removed, or None.
        """
        if value is not None:
            if value.tzinfo is not None and value.tzinfo != timezone.utc:
                value = value.astimezone(timezone.utc)
            value = value.replace(tzinfo=None)
        return value

    def process_result_value(self, value: Optional[datetime], dialect: Dialect) -> Optional[datetime]:
        """
        Process a datetime value when fetching it from a database result.

        Converts the datetime to UTC if it has timezone information and assigns
        the timezone information to the datetime object. If no timezone information
        is present, it is assumed to be UTC and the datetime object will have
        timezone information.

        :param value: The datetime value to be processed. If None, no processing is done.
        :param dialect: The SQLAlchemy dialect in use.
        :return: The processed datetime value with timezone information, or None.
        """
        if value is not None:
            return value.replace(tzinfo=timezone.utc)
        return value


    def __repr__(self) -> str:
        """
        Return a string representation of the Datetime object.

        :return: A string representation showing the implementation type.
        """
        return f"<Datetime(impl={self.impl})>"