"""
In this module we handle exceptions raised by the library
"""

from __future__ import annotations


class SAMPQuery_MissingRCON(Exception):
    """Raised when RCON password is missing"""
    pass


class SAMPQuery_InvalidRCON(Exception):
    """Raised when RCON password is invalid"""
    pass


class SAMPQuery_DisabledRCON(Exception):
    """Raised when RCON is disabled, the server is not using RCON"""
    pass


class SAMPQuery_InvalidPort(Exception):
    """Raised when port is invalid"""
    pass

class SAMPQuery_Timeout(Exception):
    """Raised when timeout is reached"""
    pass