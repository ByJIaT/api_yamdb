import datetime as dt

from django.core.exceptions import ValidationError


def validate_actuality_year(value):
    if value > dt.datetime.now().year:
        raise ValidationError(
            '%(value)s год больше чем текущий год',
            params={'value': value},
        )
