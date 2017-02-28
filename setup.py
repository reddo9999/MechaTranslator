import sys
from cx_Freeze import setup, Executable
setup(
    name = "MechaTranslator",
    version = "0.2.5",
    description = "MechaTranslator for RPG Maker Trans",
    executables = [Executable(script = "MechaTranslator.py", base = "Console")])