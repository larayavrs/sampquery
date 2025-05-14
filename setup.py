import sys

from sampquery import __name__, __version__, __author__
from cx_Freeze import setup, Executable

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    description="SAMP Query ― better GTA SA:MP query client.",
    executables=[
        Executable(
            "main.py",
            copyright=f"Copyright (C) {__author__}",
            icon="assets/logo.ico",
            target_name="sampquery",
            shortcut_name="SAMPQuery",
        )
    ]
)