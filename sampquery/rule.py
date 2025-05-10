"""
In this module we storage the rules of the server
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from .utils import SAMPQuery_Utils


@dataclass
class SAMPQuery_Rule:
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
    def from_data(cls, data: bytes) -> tuple[SAMPQuery_Rule, bytes]:
        """
        Creates a rule from raw data

        :param bytes data: The raw data to parse into rule information
        :return tuple[SAMPQuery_Rule, bytes]: An instance of rule with the parsed data and the remaining data
        """
        name, data, _ = SAMPQuery_Utils.unpack_string(data, "B")
        value, data, encoding = SAMPQuery_Utils.unpack_string(data, "B")
        return cls(name=name, value=value, encoding=encoding), data


@dataclass
class SAMPQuery_RuleList:
    """
    Represents a list of the server rules

    :param list[SAMPQuery_Rule] rules: The list of rules
    """

    rules: list[SAMPQuery_Rule]

    @classmethod
    def from_data(cls, data: bytes) -> SAMPQuery_RuleList:
        """
        Creates an instance of SAMPQuery_RuleList from raw data

        :param bytes data: The raw data to parse into rule list information
        :return SAMPQuery_RuleList: An instance of SAMPQuery_RuleList with the parsed data
        """
        rcount = struct.unpack_from("<H", data)[0]
        data = data[2:]
        rules = []
        for _ in range(rcount):
            rule, data = SAMPQuery_Rule.from_data(data)
            rules.append(rule)
        assert not data
        return cls(rules=rules)

    def get(self, name: str) -> SAMPQuery_Rule | None:
        """
        Returns the rule with the given name

        :param str name: The name of the rule to get
        :return SAMPQuery_Rule | None: The rule with the given name or None if not found
        """
        for rule in self.rules:
            if rule.name == name:
                return rule
        return None
