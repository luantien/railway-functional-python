# monitoring/exceptions.py

class DataException(Exception):
    """Base class for exceptions in this module."""
    pass

class ServerException(Exception):
    """Exception raised for server-related errors."""
    pass

class ClientException(Exception):
    """Exception raised for client-related errors."""
    pass
