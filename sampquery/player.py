"""
This module is used to handle the players information data from the server
"""

from __future__ import annotations

from dataclasses import dataclass
from .utils import SAMPQuery_Utils

import struct


@dataclass
class SAMPQuery_Player:
    """
    Class to represent a player into the server

    :param str name: The name of the player
    :param int score: The score of the player
    """

    name: str
    score: int

    @classmethod
    def from_data(cls, data: bytes) -> tuple[SAMPQuery_Player, bytes]:
        """
        Creates an instance of SAMPQuery_Player from raw data

        :param bytes data: The raw data to parse into player information
        :return tuple[SAMPQuery_Player, bytes]: An instance of SAMPQuery_Player with the parsed data and the remaining data
        """
        name, data, _ = SAMPQuery_Utils.unpack_string(data, "B")
        score = struct.unpack_from("<i", data)[0]
        data = data[4:]
        return cls(name=name, score=score), data


@dataclass
class SAMPQuery_PlayerList:
    """
    Class to represent a list of players into the server

    :param list[SAMPQuery_Player] players: The list of players
    """

    players: list[SAMPQuery_Player]

    @classmethod
    def from_data(cls, data: bytes) -> SAMPQuery_PlayerList:
        """
        Creates an instance of SAMPQuery_PlayerList from raw data

        :param bytes data: The raw data to parse into player list information
        :return SAMPQuery_PlayerList: An instance of SAMPQuery_PlayerList with the parsed data
        """
        pcount = struct.unpack_from("<H", data)[0]
        data = data[2:]
        players = []
        for _ in range(pcount):
            player, data = SAMPQuery_Player.from_data(data)
            players.append(player)
        assert not data
        return cls(players=players)
