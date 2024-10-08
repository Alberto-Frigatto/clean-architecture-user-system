from inspect import isclass, ismethod
from types import FunctionType, MethodType
from typing import Any, TypeVar

from fastapi import Depends

T = TypeVar('T', bound=Any)


class Di:
    _registrations: dict[type, tuple[type | Any, bool]] = {}
    _singletons: dict[type, Any] = {}

    @classmethod
    def map(
        cls, interface: type, *, to: type[T] | T | MethodType, singleton: bool = False
    ) -> None:
        cls._registrations[interface] = to, singleton

    @classmethod
    def inject(cls, interface: type[T]) -> T:
        return Depends(lambda: cls._resolve(interface))

    @classmethod
    def get_raw(cls, interface: type[T]) -> T:
        return cls._resolve(interface)

    @classmethod
    def _resolve(cls, interface: type[T]) -> T:
        implementation, is_singleton = cls._registrations.get(interface, (None, False))

        if not implementation:
            raise ValueError(f"{interface} não registrado")

        if is_singleton and (isclass(implementation) or ismethod(implementation)):
            if interface not in cls._singletons:
                cls._singletons[interface] = cls._create_instance(implementation)

            return cls._singletons[interface]

        return (
            cls._create_instance(implementation)
            if isclass(implementation) or ismethod(implementation)
            else implementation
        )

    @classmethod
    def _create_instance(cls, implementation: type[T] | MethodType) -> T:
        if isclass(implementation) and not cls._has_class_init_method(implementation):
            return implementation()

        constructor_params: dict[str, Any] = {}

        if isclass(implementation):
            constructor_params = implementation.__init__.__annotations__
        else:
            constructor_params = implementation.__annotations__

        constructor_params.pop('return', None)

        dependencies: list[type] = [
            cls._resolve(param_type) for _, param_type in constructor_params.items()
        ]

        return implementation(*dependencies)

    @classmethod
    def _has_class_init_method(cls, type_class: type[T]) -> bool:
        return isinstance(type_class.__init__, FunctionType)
