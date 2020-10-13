"""
@name lipo
@file pchecker/lifecycle.py
@description lifecycle

@createtime Sat, 10 Oct 2020 15:43:30 +0800
"""
from enum import auto, Flag


class Lifecycle(Flag):
    Perbuild = auto()
    Building = auto()
    Inusing = auto()
    Destory = auto()
