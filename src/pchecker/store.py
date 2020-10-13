from typing import Any, Union


class Store:

    def load(self, origin: str) -> Union[Any, None]:
        entry_list = origin.split(".")

        try:
            field = self.__getattribute__(entry_list[0])
        except AttributeError:
            # XXX: 实现形式不好,应该做些什么
            field = {}

        for entry in entry_list[1:]:
            field = (field or {}).get(entry, {})

        return field or None
