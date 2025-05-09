"""
In this module we storage the rules of the server
"""

from __future__ import annotations
from dataclasses import dataclass
from .utils import PySAMPQuery_Utils


@dataclass
class PySAMPQuery_Rule:
    """
    Class Rule represents the server rule

    :param str name: The name of the rule
    :param str value: The value of the rule
    :param str encoding: The encoding of the rule
    """

    name: str
    value: str
    encoding: str

    @classmethod
    def from_data(cls, data: bytes) -> tuple[PySAMPQuery_Rule, bytes]:
        """
        Creates a rule from raw data

        :param bytes data: The raw data to parse into rule information
        :return tuple[PySAMPQuery_Rule, bytes]: An instance of rule with the parsed data and the remaining data
        """
        name, data, _ = PySAMPQuery_Utils.unpack_string(data, "B")
        value, data, encoding = PySAMPQuery_Utils.unpack_string(data, "B")
        return cls(name=name, value=value, encoding=encoding), data
