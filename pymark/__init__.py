from ._pymark import convert
import ctypes
import os
from pathlib import Path


__all__ = ("convert",)


lib_dir = Path(__file__).parent
lib_path = lib_dir / "libcmark.so"

ctypes.CDLL(str(lib_path))
