"""
In this module we handle exceptions raised by the library
"""

from __future__ import annotations


class PySAMPQuery_MissingRCON(Exception):
    """Raised when RCON password is missing"""

    pass


class PySAMPQuery_InvalidRCON(Exception):
    """Raised when RCON password is invalid"""

    pass


class PySAMPQuery_DisabledRCON(Exception):
    """Raised when RCON is disabled, the server is not using RCON"""

    pass


class PySAMPQuery_InvalidPort(Exception):
    """Raised when port is invalid"""

    pass
