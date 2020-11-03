"""
@name lipo
@file pchecker/lifecycle.py
@description lifecycle

@createtime Sat, 10 Oct 2020 15:43:30 +0800
"""
from enum import auto, Flag


class Lifecycle(Flag):
    Perbuild = auto()  # 预构建时检验
    Setting = auto()  # 设置时检验
    Inusing = auto()  # 使用时检验
    Destory = auto()  # 删除时检验
    Undefined = auto()
