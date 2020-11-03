"""
@name lipo
@file pchecker/annotation.py
@description annotation

@createtime Sat, 10 Oct 2020 15:47:52 +0800
"""
from pchecker.exception import CheckParameterError


class AnnotationMeta(type):
    def __add__(cls, right):
        source = cls()
        return source + right


class Annotation(metaclass=AnnotationMeta):
    """
    注解描述
    """
    source = None
    target = None

    def __add__(self, right):
        if isinstance(right, AnnotationMeta):
            # 初始化annotation
            right = right()

        # 设置目标target
        self.target = right
        right.source = self
        return right

    def __call__(self, value):
        """
        执行注解链路检查
        """
        if self.source:
            value = self.source(value)

        return self.check(value)


class IsInstance(Annotation):
    def __init__(self, _type=int):
        self._type = _type

    def check(self, value):
        if isinstance(value, self._type):
            return value
        else:
            raise CheckParameterError()


class Destory(Annotation):
    """
    参数弃置标志
    """
