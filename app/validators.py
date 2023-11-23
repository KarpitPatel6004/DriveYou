from django.core.exceptions import ValidationError

def validate_mobile_number(value):
    if len(value) != 10 or not value.isdigit():
        raise ValidationError("Invalid mobile number. It should be 10 digits.")