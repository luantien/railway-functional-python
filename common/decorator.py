import traceback
from functools import wraps
from typing import Callable, Type, TypeVar, ParamSpec

from common.result import Result, Success, Failure


# ParamSpec captures the parameter signature of the decorated function
P = ParamSpec('P')
# TypeVar captures the return type of the decorated function
R = TypeVar('R')


def railway_handler(*exception_types: Type[Exception]) -> Callable[[Callable[P, R]], Callable[P, Result[R, Exception]]]:
    """
    A decorator factory that creates a decorator to handle specified exceptions
    and wrap the function's result in a Success or Failure object.
    
    If no exception types are specified, catches all exceptions.
    """
    # Default to catching all Exceptions if none specified
    exceptions_to_catch = exception_types if exception_types else (Exception,)
    
    def decorator(func: Callable[P, R]) -> Callable[P, Result[R, Exception]]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[R, Exception]:
            try:
                result_value = func(*args, **kwargs)
                # Check if the result is already a Result type
                if isinstance(result_value, Result):
                    # Flatten: if function returns Result, don't wrap it again
                    return result_value
                # Otherwise, wrap in Success
                return Success(result_value)
            except exceptions_to_catch as e:
                trace_string = traceback.format_exc()
                return Failure(error=e, traceback_info=trace_string)
        return wrapper
    return decorator
