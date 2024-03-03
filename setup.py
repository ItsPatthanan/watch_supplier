import  sys
import os
from cx_Freeze import setup, Executable

files = ['favicon.ico']

target = Executable(
   script="main.py",
   base="Win32GUI",
   icon="favicon.ico"
   )

setup(
    name = "Watch Project",
    version = "1.0",
    description = "OS_GUI",
    author = "JP-H0ShiYoMi",
    options = {"build_exe": {"include_files" : files}},
    executables = [target]
)