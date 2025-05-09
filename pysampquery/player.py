"""
This module is used to handle the players information data from the server
"""

from __future__ import annotations

from dataclasses import dataclass
from .utils import PySAMPQuery_Utils

import struct


@dataclass
class PySAMPQuery_Player:
    """
    Class to represent a player into the server

    :param str name: The name of the player
    :param int score: The score of the player
    """

    name: str
    score: int

    @classmethod
    def from_data(cls, data: bytes) -> tuple[PySAMPQuery_Player, bytes]:
        """
        Creates an instance of PySAMPQuery_Player from raw data

        :param bytes data: The raw data to parse into player information
        :return tuple[PySAMPQuery_Player, bytes]: An instance of PySAMPQuery_Player with the parsed data and the remaining data
        """
        name, data, _ = PySAMPQuery_Utils.unpack_string(data, "B")
        score = struct.unpack_from("<i", data)[0]
        data = data[4:]
        return cls(name=name, score=score), data


@dataclass
class PySAMPQuery_PlayerList:
    """
    Class to represent a list of players into the server

    :param list[PySAMPQuery_Player] players: The list of players
    """

    players: list[PySAMPQuery_Player]

    @classmethod
    def from_data(cls, data: bytes) -> PySAMPQuery_PlayerList:
        """
        Creates an instance of PySAMPQuery_PlayerList from raw data

        :param bytes data: The raw data to parse into player list information
        :return PySAMPQuery_PlayerList: An instance of PySAMPQuery_PlayerList with the parsed data
        """
        pcount = struct.unpack_from("<H", data)[0]
        data = data[2:]
        players = []
        for _ in range(pcount):
            player, data = PySAMPQuery_Player.from_data(data)
            players.append(player)
        assert not data
        return cls(players=players)
