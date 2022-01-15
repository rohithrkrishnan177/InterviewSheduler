from django.conf import settings
from django.utils import timezone
from django.db.models import Q

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import AvailableTime


class AvailableTimeSerializer(ModelSerializer):
    # TODO implement once auth flow is complete
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = AvailableTime
        fields = '__all__'


    def validate(self, attrs):
        """
        All validations for Available Time API's
        """
        end_time = attrs['end_time']
        start_time = attrs['start_time']
        user = attrs['user']

        if end_time < start_time + timezone.timedelta(minutes=settings.MIN_INTERVIEW_DURATION):
            raise serializers.ValidationError('End time should be at least interview duration '
                                              'time greater than start time')
        # check if the slot is not overlapping with other slots for the same user
        avb_times = AvailableTime.objects.filter(user_id=user).filter(Q(start_time__lt=end_time) & Q(end_time__gt=start_time))

        if avb_times.exists():
            raise serializers.ValidationError('Cannot create overlapping Available times')
        return attrs
