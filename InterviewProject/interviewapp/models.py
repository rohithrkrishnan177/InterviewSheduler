from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from django_extensions.db.models import TimeStampedModel

from .validator import (val_future_time, val_future_end_time)
# Create your models here.
class User(AbstractUser):
    """
    User model to save the details of both the interview and candidate.
    """
    CANDIDATE = 'candidate'
    INTERVIEWER = 'interviewer'

    USER_TYPES = (
        (CANDIDATE, _('Candidate')),
        (INTERVIEWER, _('Interviewer')),
    )

    user_type = models.CharField(_("User Type"), max_length=125, choices=USER_TYPES, default=INTERVIEWER)


class AvailableTime(TimeStampedModel):
    """
    Model to save the available times of a user
    Validations:
    No user can have overlapping times.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='available_time', on_delete=models.CASCADE)
    start_time = models.DateTimeField(
        validators=[val_future_time],
        help_text=f"Time should be at least {settings.MIN_AVAILABLE_TIME_NOTICE} mins before current time"
    )
    end_time = models.DateTimeField(
        validators=[val_future_end_time],
        help_text=f"Time should atleast {settings.MIN_AVAILABLE_TIME_NOTICE} minutes from start time"
    )

    def __str__(self):
        return f'{self.user} - {self.start_time.date()}'

    def clean(self):
        cleaned_data = super(AvailableTime, self).clean()
        # check if the end date is at least greater than end_time + min_duration
        end_time = cleaned_data['end_date']
        start_time = cleaned_data['start_time']

        if start_time + timezone.timedelta(minutes=settings.MIN_INTERVIEW_DURATION) < end_time:
            raise ValidationError('End time should be at least interview duration time greater than start time')
