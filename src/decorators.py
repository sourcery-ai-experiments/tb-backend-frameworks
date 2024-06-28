from logging import Logger
from functools import wraps
from typing import Callable
from botocore.exceptions import ClientError

def catch_exceptions(func: Callable) -> Callable:
    """ 
    Function for creating a decorator that wraps a method and runs it with inside a try, except block with logging
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        self = args[0]  # The first argument to the instance method will always be 'self'
        logger = self.logger
        method_name = func.__name__
        try:
            logger.debug(f"Attempting to {method_name} with args: {args[1:]}, kwargs: {kwargs}")
            result = func(*args, **kwargs)
            logger.debug(f"Successfully completed {method_name} with result: {result}")
            return result
        except ClientError as e:
            logger.error(f"Error during {method_name} with args: {args[1:]}, kwargs: {kwargs}, error: {e}")
            raise  # Re-raise the exception after logging it
    return decorator