"""
@name lipo
@file pchecker/param.py
@description param

@createtime Tue, 13 Oct 2020 09:31:39 +0800
"""
from pchecker.field import Field, FieldFactory


class MetaParam(type):
    def __new__(cls, cls_name, cls_bases, cls_dict):
        """
        类构建流程

        @intent
            - 构建named_fields，囊括所有已构建的field
        """
        base_name_fields = []
        for base in cls_bases:
            if hasattr(base, "named_fields"):
                base_name_fields.extend(base.named_fields)

        named_fields = base_name_fields + cls_dict.get("named_fields", [])
        for n, v in cls_dict.items():
            if isinstance(v, Field):
                # setup named field
                if v.origin is None:
                    v.origin = n

                if v.name is None:
                    v.name = n

                if v.func is None:
                    def func(ins, default_value, origin=None):
                        return default_value

                    v.func = func
                named_fields.append((n, v))
        new_cls = super().__new__(cls, cls_name, cls_bases, cls_dict)
        new_cls.named_fields = named_fields
        return new_cls

    def __call__(cls, *args, **kwargs):
        """
        实例生成流程

        @intent
            - 构建所有的属性接口
            - 构建属性接口对接的所有的Field
        """
        fields = {}
        for name, wrap_field in cls.named_fields:
            origin = wrap_field.origin
            # 属性克隆
            default_property = wrap_field.build_property()
            setattr(cls, name, default_property)

            if str(origin) not in fields:
                # create origin field
                fields[str(origin)] = Field.build(wrap_field)

        instance = super().__call__(cls, *args, **kwargs)
        # 挂载到instance中
        instance.fields = fields
        instance.build(**kwargs)
        return instance


class Param(metaclass=MetaParam):

    def __init__(self, *args, **kwargs):
        ...

    def build(self, **kwargs):
        # NOTE: 只支持具名参数
        # 源数据转载
        for field in self.fields.values():
            field.load(kwargs)

    def load(self, data):
        self.build(**data)

    def reload(self, name=None):
        # 重新加载store数据
        for field in self.fields.value():
            if name is None or field.name == name:
                field.store_loaded = False
