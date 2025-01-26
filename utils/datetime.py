from datetime import datetime
from typing import Any, Optional

import pytz
from sqlalchemy import DateTime, TypeDecorator
from sqlalchemy.engine import Dialect

__all__ = ["Datetime"]

class Datetime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value: Optional[datetime], dialect: Dialect) -> Any:
        """
        Process a datetime value before binding it to a database parameter.

        Converts the datetime to UTC if it has timezone information and removes
        the timezone information before returning it.

        :param value: The datetime value to be processed. If None, no processing is done.
        :param dialect: The SQLAlchemy dialect in use.
        :return: The processed datetime value with timezone information removed, or None.
        """
        if value is not None:
            if value.tzinfo is not None and value.tzinfo != pytz.utc:
                value = value.astimezone(pytz.utc)
            value = value.replace(tzinfo=None)
        return value

    def process_result_value(self, value: Optional[datetime], dialect: Dialect) -> Any:
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
            return value.astimezone(pytz.utc).replace(tzinfo=pytz.utc)
        return value