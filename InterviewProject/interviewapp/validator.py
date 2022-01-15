from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

"""
Utils file to save common validators
"""


def val_future_time(value):
    """
    function to check if the current value is in a future time
    """
    today = timezone.now()
    if value < today:
        raise ValidationError('Datetime should be a future Date and time')


def val_future_end_time(value):
    """
    check for validations in end time by adding min interview duration
    ie, end time should be a time grater than now() + min duration
    """
    today = timezone.now() + timezone.timedelta(minutes=settings.MIN_INTERVIEW_DURATION)
    if value < today:
        raise ValidationError(f'Datetime should be atleast {settings.MIN_INTERVIEW_DURATION} min after current Date and time')

