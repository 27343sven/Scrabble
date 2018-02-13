import sys
from cx_Freeze import setup, Executable

setup(
    name = "Scrabble",
    version = "1.0",
    description = "Kan je niet lezen?",
    executables = [Executable("control.py")])
