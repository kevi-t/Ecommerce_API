import re
from rest_framework import serializers


def normalize_kenyan_phone_number(value):
    value = re.sub(r"\D", "", value)

    if value.startswith("07") and len(value) == 10:
        return f"+254{value[1:]}"
    if value.startswith("254") and len(value) == 12:
        return f"+{value}"

    raise serializers.ValidationError(
        "Phone number must be a valid Kenyan number, e.g. 0722123456."
    )