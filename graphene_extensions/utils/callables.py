import inspect
import typing


def get_property_names(obj: object) -> typing.Set[str]:
    return {name for name, member in inspect.getmembers(obj) if isinstance(member, property)}


def get_method_names(obj: object) -> typing.Set[str]:
    return {name for name, member in inspect.getmembers(obj) if inspect.isfunction(member)}
