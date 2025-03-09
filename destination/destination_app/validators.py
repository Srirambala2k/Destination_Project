from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
import re

def validate_email(value):
    validator = EmailValidator()
    try:
        validator(value)
    except ValidationError:
        raise ValidationError("Invalid email address.")

def validate_website(value):
    if not re.match(r'^(https?://)?(www\.)?([a-zA-Z0-9]+(\.[a-zA-Z]{2,})+)$', value):
        raise ValidationError("Invalid website URL.")