"""Simple function for model serialization"""


def serialize(field_name):
    keys = field_name.split("_")
    new_field_name = keys[0] + "".join(x.title() for x in keys[1:])

    return new_field_name
