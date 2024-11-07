from abc import ABC
from copy import deepcopy
from typing import Callable, Self

import pytest
from fastapi.params import Depends

from web.di import Di


@pytest.fixture(scope='function')
def di_container() -> type[Di]:
    return deepcopy(Di)


def test_when_map_an_interface_to_a_class_as_not_singleton_and_inject_it_the_ids_from_objects_are_not_equal(
    di_container: type[Di],
) -> None:
    class MyInterface(ABC):
        pass

    class MyClass(MyInterface):
        pass

    di_container.map(MyInterface, to=MyClass)

    result_1: Depends = di_container.inject(MyInterface)  # type: ignore
    dependency_1: Callable | None = result_1.dependency

    assert dependency_1 is not None
    assert isinstance(dependency_1(), MyClass)

    result_2: Depends = di_container.inject(MyInterface)  # type: ignore
    dependency_2: Callable | None = result_2.dependency

    assert dependency_2 is not None
    assert isinstance(dependency_2(), MyClass)

    assert id(dependency_1()) != id(dependency_2())


def test_when_map_an_interface_to_a_class_as_singleton_and_inject_it_the_ids_from_objects_are_equal(
    di_container: type[Di],
) -> None:
    class MyInterface(ABC):
        pass

    class MyClass(MyInterface):
        pass

    di_container.map(MyInterface, to=MyClass, singleton=True)

    result_1: Depends = di_container.inject(MyInterface)  # type: ignore
    dependency_1: Callable | None = result_1.dependency

    assert dependency_1 is not None
    assert isinstance(dependency_1(), MyClass)

    result_2: Depends = di_container.inject(MyInterface)  # type: ignore
    dependency_2: Callable | None = result_2.dependency

    assert dependency_2 is not None
    assert isinstance(dependency_2(), MyClass)

    assert id(dependency_1()) == id(dependency_2())


def test_when_map_an_interface_to_an_object_as_not_singleton_and_inject_it_the_ids_from_objects_are_equal(
    di_container: type[Di],
) -> None:
    class MyInterface(ABC):
        pass

    class MyClass(MyInterface):
        pass

    di_container.map(MyInterface, to=MyClass())

    result_1: Depends = di_container.inject(MyInterface)  # type: ignore
    dependency_1: Callable | None = result_1.dependency

    assert dependency_1 is not None
    assert isinstance(dependency_1(), MyClass)

    result_2: Depends = di_container.inject(MyInterface)  # type: ignore
    dependency_2: Callable | None = result_2.dependency

    assert dependency_2 is not None
    assert isinstance(dependency_2(), MyClass)

    assert id(dependency_1()) == id(dependency_2())


def test_when_map_an_interface_to_an_object_as_singleton_and_inject_it_the_ids_from_objects_are_equal(
    di_container: type[Di],
) -> None:
    class MyInterface(ABC):
        pass

    class MyClass(MyInterface):
        pass

    di_container.map(MyInterface, to=MyClass(), singleton=True)

    result_1: Depends = di_container.inject(MyInterface)  # type: ignore
    dependency_1: Callable | None = result_1.dependency

    assert dependency_1 is not None
    assert isinstance(dependency_1(), MyClass)

    result_2: Depends = di_container.inject(MyInterface)  # type: ignore
    dependency_2: Callable | None = result_2.dependency

    assert dependency_2 is not None
    assert isinstance(dependency_2(), MyClass)

    assert id(dependency_1()) == id(dependency_2())


def test_when_map_an_interface_to_a_method_as_not_singleton_and_inject_it_the_ids_from_objects_are_not_equal(
    di_container: type[Di],
) -> None:
    class MyInterface(ABC):
        pass

    class MyClass(MyInterface):
        pass

    class ClassWithMethod:
        @classmethod
        def method(cls) -> MyClass:
            return MyClass()

    di_container.map(MyInterface, to=ClassWithMethod.method)

    result_1: Depends = di_container.inject(MyInterface)  # type: ignore
    dependency_1: Callable | None = result_1.dependency

    assert dependency_1 is not None
    assert isinstance(dependency_1(), MyClass)

    result_2: Depends = di_container.inject(MyInterface)  # type: ignore
    dependency_2: Callable | None = result_2.dependency

    assert dependency_2 is not None
    assert isinstance(dependency_2(), MyClass)

    assert id(dependency_1()) != id(dependency_2())


def test_when_map_an_interface_to_a_method_as_singleton_and_inject_it_the_ids_from_objects_are_equal(
    di_container: type[Di],
) -> None:
    class MyInterface(ABC):
        pass

    class MyClass(MyInterface):
        pass

    class ClassWithMethod:
        @classmethod
        def method(cls) -> MyClass:
            return MyClass()

    di_container.map(MyInterface, to=ClassWithMethod.method, singleton=True)

    result_1: Depends = di_container.inject(MyInterface)  # type: ignore
    dependency_1: Callable | None = result_1.dependency

    assert dependency_1 is not None
    assert isinstance(dependency_1(), MyClass)

    result_2: Depends = di_container.inject(MyInterface)  # type: ignore
    dependency_2: Callable | None = result_2.dependency

    assert dependency_2 is not None
    assert isinstance(dependency_2(), MyClass)

    assert id(dependency_1()) == id(dependency_2())


def test_inject_a_dependency_with_sub_dependencies(
    di_container: type[Di],
) -> None:
    class MyInterface(ABC):
        pass

    class InnerDependency:
        @classmethod
        def method(cls) -> Self:
            return cls()

    class OuterDependency:
        def __init__(self, inner_dependency: InnerDependency) -> None:
            self.inner_dependency: InnerDependency = inner_dependency

    class MyClass(MyInterface):
        def __init__(self, outer_dependency: OuterDependency) -> None:
            self.outer_dependency: OuterDependency = outer_dependency

    di_container.map(MyInterface, to=MyClass)
    di_container.map(OuterDependency, to=OuterDependency)
    di_container.map(InnerDependency, to=InnerDependency.method)

    result: Depends = di_container.inject(MyInterface)  # type: ignore
    dependency: Callable | None = result.dependency

    assert dependency is not None
    assert isinstance((dependency_obj := dependency()), MyClass)
    assert isinstance(dependency_obj.outer_dependency, OuterDependency)
    assert isinstance(dependency_obj.outer_dependency.inner_dependency, InnerDependency)


def test_when_map_an_interface_to_a_class_as_not_singleton_and_get_raw_it_the_ids_from_objects_are_not_equal(
    di_container: type[Di],
) -> None:
    class MyInterface(ABC):
        pass

    class MyClass(MyInterface):
        pass

    di_container.map(MyInterface, to=MyClass)

    result_1: MyInterface = di_container.get_raw(MyInterface)

    assert isinstance(result_1, MyClass)

    result_2: MyInterface = di_container.get_raw(MyInterface)

    assert isinstance(result_2, MyClass)

    assert id(result_1) != id(result_2)


def test_when_map_an_interface_to_a_class_as_singleton_and_get_raw_it_the_ids_from_objects_are_equal(
    di_container: type[Di],
) -> None:
    class MyInterface(ABC):
        pass

    class MyClass(MyInterface):
        pass

    di_container.map(MyInterface, to=MyClass, singleton=True)

    result_1: MyInterface = di_container.get_raw(MyInterface)

    assert isinstance(result_1, MyClass)

    result_2: MyInterface = di_container.get_raw(MyInterface)

    assert isinstance(result_2, MyClass)

    assert id(result_1) == id(result_2)


def test_when_map_an_interface_to_an_object_as_not_singleton_and_get_raw_it_the_ids_from_objects_are_equal(
    di_container: type[Di],
) -> None:
    class MyInterface(ABC):
        pass

    class MyClass(MyInterface):
        pass

    di_container.map(MyInterface, to=MyClass())

    result_1: MyInterface = di_container.get_raw(MyInterface)

    assert isinstance(result_1, MyClass)

    result_2: MyInterface = di_container.get_raw(MyInterface)

    assert isinstance(result_2, MyClass)

    assert id(result_1) == id(result_2)


def test_when_map_an_interface_to_an_object_as_singleton_and_get_raw_it_the_ids_from_objects_are_equal(
    di_container: type[Di],
) -> None:
    class MyInterface(ABC):
        pass

    class MyClass(MyInterface):
        pass

    di_container.map(MyInterface, to=MyClass(), singleton=True)

    result_1: MyInterface = di_container.get_raw(MyInterface)

    assert isinstance(result_1, MyClass)

    result_2: MyInterface = di_container.get_raw(MyInterface)

    assert isinstance(result_2, MyClass)

    assert id(result_1) == id(result_2)


def test_when_map_an_interface_to_a_method_as_not_singleton_and_get_raw_it_the_ids_from_objects_are_not_equal(
    di_container: type[Di],
) -> None:
    class MyInterface(ABC):
        pass

    class MyClass(MyInterface):
        pass

    class ClassWithMethod:
        @classmethod
        def method(cls) -> MyClass:
            return MyClass()

    di_container.map(MyInterface, to=ClassWithMethod.method)

    result_1: MyInterface = di_container.get_raw(MyInterface)

    assert isinstance(result_1, MyClass)

    result_2: MyInterface = di_container.get_raw(MyInterface)

    assert isinstance(result_2, MyClass)

    assert id(result_1) != id(result_2)


def test_when_map_an_interface_to_a_method_as_singleton_and_get_raw_it_the_ids_from_objects_are_equal(
    di_container: type[Di],
) -> None:
    class MyInterface(ABC):
        pass

    class MyClass(MyInterface):
        pass

    class ClassWithMethod:
        @classmethod
        def method(cls) -> MyClass:
            return MyClass()

    di_container.map(MyInterface, to=ClassWithMethod.method, singleton=True)

    result_1: MyInterface = di_container.get_raw(MyInterface)

    assert isinstance(result_1, MyClass)

    result_2: MyInterface = di_container.get_raw(MyInterface)

    assert isinstance(result_2, MyClass)

    assert id(result_1) == id(result_2)


def test_get_raw_a_dependency_with_sub_dependencies(
    di_container: type[Di],
) -> None:
    class MyInterface(ABC):
        pass

    class InnerDependency:
        @classmethod
        def method(cls) -> Self:
            return cls()

    class OuterDependency:
        def __init__(self, inner_dependency: InnerDependency) -> None:
            self.inner_dependency: InnerDependency = inner_dependency

    class MyClass(MyInterface):
        def __init__(self, outer_dependency: OuterDependency) -> None:
            self.outer_dependency: OuterDependency = outer_dependency

    di_container.map(MyInterface, to=MyClass)
    di_container.map(OuterDependency, to=OuterDependency)
    di_container.map(InnerDependency, to=InnerDependency.method)

    result: MyInterface = di_container.get_raw(MyInterface)

    assert isinstance(result, MyClass)
    assert isinstance(result.outer_dependency, OuterDependency)
    assert isinstance(result.outer_dependency.inner_dependency, InnerDependency)


def test_when_try_to_inject_a_not_mapped_dependency_raises_ValueError(
    di_container: type[Di],
) -> None:
    class MyInterface(ABC):
        pass

    with pytest.raises(ValueError):
        di_container.get_raw(MyInterface)
