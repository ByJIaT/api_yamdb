from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RangeValueValidator:
    message = _('number must be between 1 and 10')

    def __init__(self, field):
        self.field = field

    def __call__(self, *args, **kwargs):
        if not 1 <= self.field <= 10:
            raise ValidationError(self.message)
