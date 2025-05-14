"""
This module is used for utility functions used by the library in another modules
"""

from __future__ import annotations

import struct
import cchardet as chdet
import typing as tp


class SAMPQuery_Utils:
    """
    This class is used for utility functions used by the library in another modules
    """

    MAX_LATENCY_VARIABILITY = (
        5  # the ratio between the latency in max/min can't be higher than this
    )

    @staticmethod
    def encode_codepage(string: str) -> bytes:
        """
        Encode the given string into bytes for the first posible codepage

        :param string: The string to encode
        :type string: str
        :return: The encoded string
        :rtype: bytes
        :raises UnicodeEncodeError: If the string can't be encoded
        """
        for cp in range(1250, 1259):
            try:
                return string.encode(f"cp{cp}")
            except UnicodeEncodeError:
                continue
        raise UnicodeEncodeError(
            "cp1252", string, 0, len(string), "The string can't be encoded"
        )

    @staticmethod
    def pack_string(string: str, len_type: str) -> bytes:
        """
        Pack a string into bytes

        :param string: The string to pack
        :type string: str
        :param len_type: The length type
        :type len_type: str
        :return: The packed string
        :rtype: bytes
        """
        fmt = f"<{len_type}"
        return struct.pack(fmt, len(string)) + SAMPQuery_Utils.encode_codepage(string)

    @staticmethod
    def unpack_string(data: bytes, len_type: str) -> tuple[str, bytes, str]:
        """
        Unpack a string from bytes with a length prefix.

        :param bytes data: The data to unpack.
        :param str len_type: The format specifier for the length prefix.
        :return: The unpacked string, the remaining data, and the detected
                encoding.
        :rtype: tuple[str, bytes]
        """
        format = f"<{len_type}"
        size = struct.calcsize(format)
        str_len, data = (
            *struct.unpack_from(format, data),
            data[size:],
        )  # we get the length and the rest of the data as a tuple :)
        string, data = data[:str_len], data[str_len:]
        encoding = chdet.detect(string)["encoding"] or "ascii"
        return string.decode(encoding), data, encoding

    @staticmethod
    def unpack_string_with_offset(data: bytes, offset: int, length_format: str) -> tuple[str, int]:
        """
        Unpacks a string from the given data starting at the specified offset.

        :param bytes data: The raw data to parse.
        :param int offset: The current offset in the data.
        :param str length_format: The format of the length prefix (e.g., "B" for 1 byte).
        :return tuple[str, int]: The unpacked string and the new offset.
        """
        if offset >= len(data):
            raise ValueError("Offset exceeds data length.")
        length = struct.unpack_from(length_format, data, offset)[0]
        offset += struct.calcsize(length_format)
        if offset + length > len(data):
            raise ValueError("String data exceeds buffer length.")
        string = data[offset:offset + length].decode("utf-8")
        offset += length
        return string, offset

class SAMPQuery_Constants:
    """
    This class is used for constants used by the library in another modules
    """

    MAX_PLAYER_NAME_LENGTH = 32
    """The maximum length of a player name"""

    MENU_COMMANDS = ["players", "rules", "info", "lagcomp", "exit"]
    """List of menu commands"""


class SAMPQuery_Encodings(tp.TypedDict):
    """
    Encoding class information

    NOTE: I dont know if this is the best place to put this class

    :param str name: The name of the encoding
    :param str gamemode: The gamemode of the encoding
    :param str language: The language of the encoding
    """

    name: str
    gamemode: str
    language: str
