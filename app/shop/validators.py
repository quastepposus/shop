from django.core.exceptions import ValidationError


def more_than_zero(count):
    if count <= 0:
        return ValidationError('count must be more than 0')