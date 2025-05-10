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
    :param int player_id: The ID of the player
    :param int score: The score of the player
    :param int ping: The ping of the player
    """

    name: str
    player_id: int
    score: int
    ping: int

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
        return cls(name=name, player_id=0, score=score, ping=0), data

    @classmethod
    def from_detailed_data(cls, data: bytes) -> tuple[SAMPQuery_Player, bytes]:
        """
        Creates an instance of SAMPQuery_Player from detailed player data (opcode 'd').

        :param bytes data: The raw data to parse into player information.
        :return tuple[SAMPQuery_Player, bytes]: An instance of SAMPQuery_Player with the parsed data and the remaining data.
        """
        if len(data) < 10:
            raise ValueError("Insufficient data to unpack detailed player information.")

        name, data, _ = SAMPQuery_Utils.unpack_string(data, "B")
        player_id, score, ping = struct.unpack_from("<Bii", data)
        data = data[9:]
        return cls(name=name, player_id=player_id, score=score, ping=ping), data


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

    @classmethod
    def from_detailed_data(cls, data: bytes) -> SAMPQuery_PlayerList:
        """
        Parses the raw data into a list of players with detailed information.

        :param bytes data: The raw data to parse.
        :return SAMPQuery_PlayerList: A list of players parsed from the data.
        """
        if not data:
            return cls(players=[])

        num_clients = struct.unpack_from("<H", data, 0)[0]
        offset = 2

        players = []
        for _ in range(num_clients):
            if offset >= len(data):
                print(f"Warning: Incomplete data for player {_ + 1}/{num_clients}.")
                break

            player_id = struct.unpack_from("<B", data, offset)[0]
            offset += 1

            name, offset = SAMPQuery_Utils.unpack_string_with_offset(data, offset, "B")

            if offset + 4 > len(data):
                print(f"Warning: Incomplete score data for player {name}.")
                break
            score = struct.unpack_from("<i", data, offset)[0]
            offset += 4

            if offset + 4 > len(data):
                print(f"Warning: Incomplete ping data for player {name}.")
                break
            ping = struct.unpack_from("<i", data, offset)[0]
            offset += 4

            player = SAMPQuery_Player(name=name, player_id=player_id, score=score, ping=ping)
            players.append(player)

        return cls(players=players)