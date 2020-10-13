"""
@name lipo
@file pchecker/field.py
@description field

@createtime Sat, 10 Oct 2020 17:33:51 +0800
"""
from functools import wraps
from typing import Union, List


class MetaField(type):
    def __call__(cls, *args, **kwargs):
        if args and callable(args[0]):
            ins = super().__call__()
            return ins(args[0])
        else:
            ins = super().__call__(*args, **kwargs)
            return ins


class Field(metaclass=MetaField):
    func = None
    name = None
    store_loaded = False
    multi_origin = False
    origin_loaded = None

    def __init__(
        self,
        origin: Union[None, str, List[str]]=None,
        default_value=None,
        setter=None,
        store=None
    ):
        """
        Field实体类

        @show
            class A(Param):
                a = Field()

                @Field()
                def b(self, default_value):
                    ...

        @parameter origin 数据源点 支持列表形式的多源点
        @parameter default_value 数据默认值
        @parameter setter 数据设置方法
        @parameter store List[Store] 存储空间
        """
        self.origin = origin
        if isinstance(self.origin, list):
            self.multi_origin = True
        self.default_value = default_value
        self.setter = setter
        self.store = store

    def __call__(self, func, load_name=True):
        name = func.__name__
        if self.name is None and load_name:
            self.name = name
        self.func = func
        return self

    def __repr__(self):
        return f"<field {self.origin}={self.default_value} at {hex(id(self))}>"

    def build_property(self):
        @wraps(self.func)
        def get_field(ins):
            # 获取唯一的数据源头field
            ognfield = ins.fields.get(str(self.origin))
            if ognfield.store is not None and not ognfield.store_loaded:
                origins = ognfield.origin
                if not ognfield.multi_origin:
                    origins = [origins]
                for origin in origins:
                    for store in ognfield.store:
                        _value = store.load(origin)
                        if _value is not None:
                            # NOTE: 为了保证设置的默认值生效，所以采用该机制
                            ognfield.default_value = _value
                            # 设置生效的origin
                            ognfield.origin_loaded = origin
                            break
                ognfield.store_loaded = True

            # 生成数据
            if self.multi_origin:
                value = self.func(ins, ognfield.default_value, origin=ognfield.origin_loaded)
            else:
                value = self.func(ins, ognfield.default_value)

            return value

        def set_field(ins, value):
            # 获取唯一的数据元购
            ognfield = ins.fields.get(str(self.origin))
            # 设置默认value，如果存在setter,则执行setter流程
            if callable(self.setter):
                value = self.setter(ins, value)
            ognfield.default_value = value

        default_property = property(get_field, set_field)
        return default_property

    @classmethod
    def build(cls, wrap_field):
        field = cls(
            wrap_field.origin,
            wrap_field.default_value,
            wrap_field.setter,
            wrap_field.store
        )(wrap_field.func, False)
        return field

    def load(self, data):
        origins = self.origin
        if isinstance(self.origin, str):
            origins = [origins]
        _value = None
        for origin in origins:
            for store in (self.store or []):
                _value = store.load(origin)
                if _value is not None:
                    self.store_loaded = True
                    break

            if (_value or data.get(origin)) is not None:
                _value = (_value or data.get(origin))
                self.origin_loaded = origin
                self.store_loaded = True
                break
        else:
            self.store_loaded = False

        self.default_value = _value or self.default_value


def FieldFactory(
        factory_func,
        origin=None,
        default_value=None,
        setter=None,
        store=None
    ):
    """
    Field工厂函数

    @show
        class A(Param):
            def get_a(self, default_value):
                ...

            a = FieldFactory(get_a)

    @param factory_func 工厂函数 required!
    """
    field = Field(origin, default_value, setter, store)(factory_func, False)
    return field
