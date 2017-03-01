import sys
from lib.classes import version
from cx_Freeze import setup, Executable
setup(
    name = "MechaTranslator",
    version = version.version,
    description = "MechaTranslator for RPG Maker Trans",
    executables = [Executable(script = "MechaTranslator.py", base = "Console")])