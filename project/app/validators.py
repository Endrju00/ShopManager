from django.core.exceptions import ValidationError


def validate_phone_number(number):
    if not number.isdigit():
        raise ValidationError('Enter a valid phone number.')