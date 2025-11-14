# common/result.py
from typing import Generic, TypeVar, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Define generic types for Result class
T = TypeVar("T")                    # Represents the success value type
E = TypeVar("E", bound=Exception)   # Represents the error value type
V = TypeVar("V")                    # New type variable for the return type of the bind function

# A generic Result class to encapsulate success and error outcomes
class Result(ABC, Generic[T, E]):
    """
    Abstract base class for Result type representing either success or failure.
    """
    @abstractmethod
    def and_then(self, func: Callable[[T], "Result[V, E]"]) -> "Result[V, E]":
        """
        Chain operations that return Results.
        If successful, apply the function to the value.
        If failed, propagate the failure.
        """
        pass
    
    @abstractmethod
    def map(self, func: Callable[[T], V]) -> "Result[V, E]":
        """
        Transform the success value without returning a Result.
        Automatically wraps the result in Success or Failure if an exception occurs.
        """
        pass
    
    @abstractmethod
    def get(self, default: T) -> T:
        """
        Get the value, or return default if failed.
        For Success, returns the wrapped value.
        For Failure, returns the default value.
        """
        pass
    
    @abstractmethod
    def or_try(self, func: Callable[[E], "Result[T, E]"]) -> "Result[T, E]":
        """
        Try an alternative function if failed.
        For Success, returns self without calling the function.
        For Failure, calls the function with the error to attempt recovery.
        """
        pass
    
    @abstractmethod
    def is_ok(self) -> bool:
        """Check if the result is successful."""
        pass

@dataclass(frozen=True)
class Success(Result[T, E]):
    """Represents a successful result, containing a value."""
    value: T

    def and_then(self, func: Callable[[T], Result[V, E]]) -> Result[V, E]:
        """
        If the result is a Success, apply the function to the value.
        This is the core of chaining operations.
        """
        return func(self.value)
    
    def map(self, func: Callable[[T], V]) -> Result[V, E]:
        """
        Transform the success value without returning a Result.
        Automatically wraps the result in Success or Failure if an exception occurs.
        """
        try:
            return Success(func(self.value))
        except Exception as e:
            return Failure(error=e)  # type: ignore
    
    def get(self, default: T) -> T:
        """
        Get the value, or return default if failed.
        For Success, always returns the wrapped value.
        """
        return self.value
    
    def or_try(self, func: Callable[[E], Result[T, E]]) -> Result[T, E]:
        """
        Try an alternative function if failed.
        For Success, returns self without calling the function.
        """
        return self
    
    def is_ok(self) -> bool:
        """Check if the result is successful."""
        return True

@dataclass(frozen=True)
class Failure(Result[T, E]):
    """Represents a failed result, containing an error."""
    error: E
    traceback_info: str | None = None

    def and_then(self, func: Callable[[T], Result[V, E]]) -> Result[V, E]:
        """
        If the result is a Failure, just pass the failure along,
        bypassing the function. The return signature must match Success.bind.
        """
        # The 'ignore' comment tells type checkers that we know 'self' doesn't
        # match the return type perfectly, but it's correct for this pattern.
        return self # type: ignore
    
    def map(self, func: Callable[[T], V]) -> Result[V, E]:
        """
        Propagate failure without applying the function.
        The transformation is skipped for Failure.
        """
        return self  # type: ignore
    
    def get(self, default: T) -> T:
        """
        Get the value, or return default if failed.
        For Failure, always returns the default value.
        """
        return default
    
    def or_try(self, func: Callable[[E], Result[T, E]]) -> Result[T, E]:
        """
        Try an alternative function if failed.
        For Failure, calls the function with the error to attempt recovery.
        """
        return func(self.error)
    
    def is_ok(self) -> bool:
        """Check if the result is successful."""
        return False
