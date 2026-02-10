"""
Error Definitions
Common errors and exceptions for the system
"""

class ShadowLinkException(Exception):
    """Base exception for ShadowLink system"""
    pass

class AgentNotFoundError(ShadowLinkException):
    """Raised when agent is not found"""
    pass

class AuthenticationError(ShadowLinkException):
    """Raised when authentication fails"""
    pass

class CommandExecutionError(ShadowLinkException):
    """Raised when command execution fails"""
    pass

class NetworkError(ShadowLinkException):
    """Raised when network communication fails"""
    pass

class TimeoutError(ShadowLinkException):
    """Raised when operation times out"""
    pass
