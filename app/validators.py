import pytz
from datetime import datetime
from django.core.exceptions import ValidationError

utc=pytz.UTC

def validate_mobile_number(value):
    if len(value) != 10 or not value.isdigit():
        raise ValidationError("Invalid mobile number. It should be 10 digits.")
    
def validate_date_travel_date(date):
    if date.replace(tzinfo=utc) < datetime.now().replace(tzinfo=utc):
        raise ValidationError("Date cannot be in the past")