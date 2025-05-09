"""
This module is used for utility functions used by the library in another modules
"""

from __future__ import annotations

import struct
import cchardet as chdet
import typing as tp

class PySAMPQuery_Utils:
    """
    This class is used for utility functions used by the library in another modules
    """

    MAX_LATENCY_VARIABILITY = 5 # the ratio between the latency in max/min can't be higher than this

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
        raise UnicodeEncodeError('cp1252', string, 0, len(string), 'The string can\'t be encoded')
    
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
        fmt = f'<{len_type}'
        return struct.pack(fmt, len(string)) + PySAMPQuery_Utils.encode_codepage(string)
    
    def unpack_string(data: bytes, len_type: str) -> tuple[str, bytes, str]:
        """
        Unpack a string from bytes with a length prefix.

        :param bytes data: The data to unpack.
        :param str len_type: The format specifier for the length prefix.
        :return: The unpacked string, the remaining data, and the detected
                encoding.
        :rtype: tuple[str, bytes]
        """
        format = f'<{len_type}'
        size = struct.calcsize(format)
        str_len, data = *struct.unpack_from(format, data), data[size:] # we get the length and the rest of the data as a tuple :)
        string, data = data[:str_len], data[str_len:]
        encoding = chdet.detect(string)['encoding'] or 'ascii'
        return string.decode(encoding), data, encoding
    
class PySAMPQuery_Encodings(tp.TypedDict):
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