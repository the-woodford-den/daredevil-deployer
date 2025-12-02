"""Simple function for model serialization"""

from pydantic import AliasGenerator, ConfigDict


def _serialize(field_name):
    keys = field_name.split("_")
    new_field_name = keys[0] + "".join(x.title() for x in keys[1:])

    return new_field_name


def serializer():
    return ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=lambda field_name: (_serialize(field_name))
        )
    )
