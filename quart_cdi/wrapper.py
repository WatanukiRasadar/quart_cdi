from typing import Any


class Wrapper:

    def __init__(self, klz, container):
        self.klz = klz
        self.container = container

    def __getattribute__(self, name: str) -> Any:
        klz = super().__getattribute__('klz')
        container = super().__getattribute__('container')

        if not hasattr(container, klz.__name__):
            setattr(container, klz.__name__, klz())
        return getattr(getattr(container, klz.__name__), name)
