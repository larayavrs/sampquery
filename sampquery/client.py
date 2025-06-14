"""
This module is used to interact with a given game server
"""

from __future__ import annotations

import trio
import typing as tp

from dataclasses import dataclass, field
from random import getrandbits

from .utils import SAMPQuery_Utils
from .server import SAMPQuery_Server
from .player import SAMPQuery_PlayerList
from .rule import SAMPQuery_RuleList

from .exceptions import ( 
    SAMPQuery_TooManyPlayers, 
    SAMPQuery_DisabledRCON, 
    SAMPQuery_InvalidRCON 
)


@dataclass
class SAMPQuery_Client:
    """
    This class is used for interact with a SA:MP/OMP server.

    :param str ip: The IP of the server
    :param int port: The port of the server
    :param str rcon_password: The rcon password of the server
    :param bytes prefix: The prefix needed for the queries
    """

    ip: str
    port: int
    rcon_password: str | None = field(default=None, repr=False)
    prefix: bytes | None = field(default=None, repr=False)
    __socket: trio.socket.SocketType | None = field(default=None, repr=False)

    async def __connect(self) -> None:
        """Connect to the server and save the prefix needed for the queries."""
        family, type, proto, _, (ip, *_) = (await trio.socket.getaddrinfo(
            self.ip,
            self.port,
            family=trio.socket.AF_INET,
            proto=trio.socket.IPPROTO_UDP
        ))[0]
        self.ip = ip
        self.__socket = _socket = trio.socket.socket(family, type, proto)
        await _socket.connect((self.ip, self.port))
        self.prefix = (
            b"SAMP" + trio.socket.inet_aton(self.ip) + self.port.to_bytes(2, "little")
        )

    async def __send(self, opcode: bytes, payload: bytes = b"") -> None:
        """
        Send a packet to the server.

        :param bytes opcode: The opcode of the packet
        :param bytes payload: The payload of the packet
        """
        if not self.__socket:
            await self.__connect()
        assert self.__socket and self.prefix
        await self.__socket.send(self.prefix + opcode + payload)

    async def __receive(self, header: tp.Optional[bytes] = b"") -> bytes:
        """
        Receive a query from the server.

        :param bytes header: The header of the packet to receive
        :return bytes: The packet received
        :raises TimeoutError: If the server does not respond within the timeout period.
        """
        assert self.__socket
        try:
            with trio.move_on_after(20):  # TODO: verify if this is enough for longer queries
                while True:
                    data = await self.__socket.recv(4096)  # 4096 bytes per packet
                    if data.startswith(header):
                        return data[len(header):]
            raise TimeoutError("The server did not respond within the timeout period.")
        except TimeoutError as e:
            raise TimeoutError(
                f"Failed to receive data from the server. Reason: {str(e)}"
            ) from e

    async def __ping(self) -> float:
        """
        Simply sends a ping packet to the server and returns the time it took to receive the packet

        :return float: The time it took to receive the packet
        """
        payload = getrandbits(32).to_bytes(4, "little")
        starttime = trio.current_time()
        await self.__send(b"p", payload)
        assert self.prefix
        data = await self.__receive(header=self.prefix + b"p" + payload)
        assert not data
        return trio.current_time() - starttime

    async def __is_omp(self) -> bool:
        """
        This method is used to check if the server is OpenMP server or not

        :return bool: True if the server is OpenMP server, False otherwise
        """
        ping = await self.__ping()
        payload = getrandbits(32).to_bytes(4, "little")
        with trio.move_on_after(SAMPQuery_Utils.MAX_LATENCY_VARIABILITY * ping):
            await self.__send(b"o", payload)
            assert self.prefix
            data = await self.__receive(header=self.prefix + b"o" + payload)
            assert not data
            return True
        return False

    async def info(self) -> SAMPQuery_Server:
        """
        This method is used to get the server information

        :return SAMPQuery_Server: The server information
        """
        await self.__send(b"i")
        assert self.prefix
        data = await self.__receive(header=self.prefix + b"i")
        return SAMPQuery_Server.from_data(data)

    async def players(self) -> SAMPQuery_PlayerList:
        """
        This method is used to get the player list.

        :return SAMPQuery_PlayerList: The player list.
        :raises SAMPQuery_TooManyPlayers: If the server has too many connected players.
        :raises TimeoutError: If the server does not respond in time.
        """
        server_info = await self.info()
        if server_info.players > 100:  # maximum limit according to SA:MP documentation
            raise SAMPQuery_TooManyPlayers(
                f"Server has too many players ({server_info.players}) and cannot retrieve the player list."
            )
        await self.__send(b"c")
        assert self.prefix
        try:
            data = await self.__receive(header=self.prefix + b"c")
            return SAMPQuery_PlayerList.from_data(data)
        except TimeoutError as e:
            raise TimeoutError(
                "Failed to retrieve player list due to a timeout. The server may be unresponsive."
            ) from e
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {str(e)}") from e

    async def rules(self) -> SAMPQuery_RuleList:
        """
        This method is used to get the rules list

        :return SAMPQuery_RuleList: The rules list
        """
        await self.__send(b"r")
        assert self.prefix
        data = await self.__receive(header=self.prefix + b"r")
        return SAMPQuery_RuleList.from_data(data)

    async def detailed_players(self) -> SAMPQuery_PlayerList:
        """
        This method is used to get the detailed player list.

        :return SAMPQuery_PlayerList: The detailed player list.
        :raises SAMPQuery_TooManyPlayers: If the server has too many connected players.
        :raises TimeoutError: If the server does not respond in time.
        """
        server_info = await self.info()
        if server_info.players > 100:
            raise SAMPQuery_TooManyPlayers(
                f"Server has too many players ({server_info.players}) and cannot retrieve the detailed player list."
            )
        # yeah, if the player count is within the limit, proceed with the query
        await self.__send(b"d")
        assert self.prefix
        try:
            data = await self.__receive(header=self.prefix + b"d")
            return SAMPQuery_PlayerList.from_detailed_data(data)
        except TimeoutError as e:
            raise TimeoutError(
                "Failed to retrieve detailed player list due to a timeout. The server may be unresponsive."
            ) from e
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {str(e)}") from e
        
    async def lagcomp(self) -> str:
        """
        This method determines whether the server uses lagshot or skinshot based on the 'lagcomp' rule.

        :return str: "skinshot" if lagcomp is On, "lagshot" if lagcomp is Off.
        :raises ValueError: If the 'lagcomp' rule is not found.
        """
        server_rules = await self.rules()
        lagcomp_rule = server_rules.get("lagcomp")
        if lagcomp_rule is None:
            raise ValueError("The 'lagcomp' rule is not available on this server.")
        if lagcomp_rule.value.lower() == "on":
            return "skinshot"
        elif lagcomp_rule.value.lower() == "off":
            return "lagshot"
        else:
            raise ValueError(f"Unexpected value for 'lagcomp': {lagcomp_rule.value}")
        
    async def rcon(self, command: str) -> str:
        """
        This method is used to execute a command on the server using RCON.

        :param str command: The command to execute.
        :return str: The response from the server.

        :raises SAMPQuery_DisabledRCON: If the RCON password is missing or disabled.
        :raises SAMPQuery_InvalidRCON: If the RCON password is invalid.
        """
        if not self.rcon_password:
            raise SAMPQuery_DisabledRCON(
                "RCON password is missing. Please provide a valid RCON password."
            )
        ping = await self.__ping()
        payload = (
            getrandbits(32).to_bytes(4, "little") 
            + self.rcon_password.encode() 
            + command.encode()
        )
        await self.__send(b"x", payload) # 0x78 packet for RCON purposes
        assert self.prefix
        try:
            with trio.move_on_after(
                SAMPQuery_Utils.MAX_LATENCY_VARIABILITY * ping
            ) as cancel_scope:
                while True:
                    start = trio.current_time()
                    data = await self.__receive(header=self.prefix + b"x" + payload)
                    receive_duraton = trio.current_time() - start
                    line, data, _ = SAMPQuery_Utils.unpack_string(data, 'H')
                    assert not data
                    response = line + '\n'
                    cancel_scope.deadline += receive_duraton
            if not response:
                raise SAMPQuery_DisabledRCON(
                    "RCON password is missing. Please provide a valid RCON password."
                )
            if response.startswith(b"Invalid RCON password"):
                raise SAMPQuery_InvalidRCON(
                    "Invalid RCON password. Please check your RCON password."
                )
            return response[:-1].decode("utf-8")
        except TimeoutError as e:
            raise TimeoutError(
                "Failed to retrieve RCON response due to a timeout. The server may be unresponsive."
            ) from e

    async def ping_history(self, samples: int = 5, interval: float = 1.0) -> list[float]:
        """
        Perform multiple ping measurements to the server and return a list with the results.

        :param samples: Number of measurements to perform.
        :param interval: Interval in seconds between each measurement.
        :return: List of ping times (in seconds).
        """
        results = []
        for _ in range(samples):
            ping = await self.__ping()
            results.append(ping)
            if _ < samples - 1:
                await trio.sleep(interval)
        return results

    async def server_version(self) -> str:
        """
        Retrieve the server version.

        :return str: The server version.
        """
        info = await self.info()
        return getattr(
            info, "version", "Unknown"
        )

    async def players_with_score(self, min_score: int = 0) -> list:
        """
        Returns a list of players whose score is greater than or equal to min_score.

        :param min_score: Minimum required score.
        :return: List of players that meet the criteria.
        """
        players = await self.detailed_players()
        return [p for p in players if getattr(p, "score", 0) >= min_score]

    async def free_slots(self) -> int:
        """
        Returns the number of free slots on the server.

        :return: Number of free slots.
        """
        info = await self.info()
        return getattr(info, "max_players", 0) - getattr(info, "players", 0)