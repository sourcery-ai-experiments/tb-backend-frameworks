from logging import Logger
from functools import wraps
from typing import Callable
from botocore.exceptions import ClientError, ParamValidationError

def catch_exceptions(func: Callable) -> Callable:
    """ 
    Decorator that wraps a method and catches exceptions, logging them.
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        self = args[0]
        logger = self.logger
        method_name = func.__name__
        try:
            logger.debug(f"Attempting to {method_name} with args: {args[1:]}, kwargs: {kwargs}")
            result = func(*args, **kwargs)
            logger.debug(f"Successfully completed {method_name} with result: {result}")
            return result
        except ClientError as e:
            logger.error(f"ClientError during {method_name} with args: {args[1:]}, kwargs: {kwargs}, error: {e}")
            raise
        except ValueError as ve:
            logger.error(f"ValueError during {method_name} with args: {args[1:]}, kwargs: {kwargs}, error: {ve}")
            raise
        except ParamValidationError as pve:
            logger.error(f"ParamValidationError during {method_name} with args: {args[1:]}, kwargs: {kwargs}, error: {pve}")
            raise
    return decorator