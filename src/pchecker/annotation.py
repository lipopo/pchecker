"""
@name lipo
@file pchecker/annotation.py
@description annotation

@createtime Sat, 10 Oct 2020 15:47:52 +0800
"""
class AnnotationMeta(type):
    def __add__(cls, right):
        source = cls()
        return source + right


class Annotation(metaclass=AnnotationMeta):
    source = None
    target = None

    def __add__(self, right):
        if isinstance(right, AnnotationMeta):
            right = right()
        self.target = right
        right.source = self
        return right

    def __call__(self):
        if self.source:
            self.source()
        self.run()
