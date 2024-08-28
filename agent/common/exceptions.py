class FirewallAgentException(Exception):
    """Base exception for FirewallAgent"""
    pass

class ConfigurationError(FirewallAgentException):
    """Raised when there's an error in the configuration"""
    pass

class NetworkError(FirewallAgentException):
    """Raised when there's a network-related error"""
    pass

class DatabaseError(FirewallAgentException):
    """Raised when there's a database-related error"""
    pass

# Add more custom exceptions as needed