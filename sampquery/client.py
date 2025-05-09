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
        """
        assert self.__socket
        with trio.move_on_after(10):  # Timeout after 10 seconds
            while True:
                data = await self.__socket.recv(4096)  # 4096 bytes per packet
                if data.startswith(header):
                    return data[len(header) :]
        raise TimeoutError

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
        This method is used to get the player list

        :return SAMPQuery_PlayerList: The player list
        """
        await self.__send(b"c")
        assert self.prefix
        data = await self.__receive(header=self.prefix + b"c")
        return SAMPQuery_PlayerList.from_data(data)

    async def rules(self) -> SAMPQuery_RuleList:
        """
        This method is used to get the rules list

        :return SAMPQuery_RuleList: The rules list
        """
        await self.__send(b"r")
        assert self.prefix
        data = await self.__receive(header=self.prefix + b"r")
        return SAMPQuery_RuleList.from_data(data)
