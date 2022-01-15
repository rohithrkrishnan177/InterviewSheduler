from django.conf import settings
from django.utils import timezone

from .models import AvailableTime
from .utils import date_range_chunks


class DateOverlapMixin:
    """
    Mixin to calc to the overlappes and return a dict of overlaps
    available_slots: list of date ranges with interview length duration
    available times: list of all available times for the user and candidate
    """

    def get_overlaps(self, interviewer, candidate):
        result_qs = AvailableTime.objects.filter(
            end_time__gte=timezone.now() + timezone.timedelta(minutes=settings.MIN_INTERVIEW_DURATION),
            user_id__in=[interviewer, candidate]
        )
        # get interviewer items
        intvr_qs = result_qs.filter(user_id=interviewer)
        cand_qs = result_qs.filter(user_id=candidate)
        date_ranges = []
        date_chunks = []

        # TODO change logic from for loops to query
        for inv_item in intvr_qs:
            st_time = inv_item.start_time + timezone.timedelta(minutes=settings.MIN_INTERVIEW_DURATION)
            end_time = inv_item.end_time - timezone.timedelta(minutes=settings.MIN_INTERVIEW_DURATION)
            cand_qs.filter(end_time__gte=st_time, start_time__lte=end_time)
            for can_item in cand_qs:
                overlap = self.find_overlap(inv_item.start_time, inv_item.end_time, can_item)
                if overlap:
                    date_ranges.append(overlap)
                    date_chunks.extend(date_range_chunks(overlap[0], overlap[1]))

        return {'available_slots': date_chunks, 'available_times': date_ranges}

    def find_overlap(self, st_time, end_time, obj):
        """
        find if a given range overlaps with start-end times of an object
        """
        latest_start = max(st_time, obj.start_time)
        earliest_end = min(end_time, obj.end_time)
        delta = (earliest_end - latest_start).total_seconds() / 60.0
        # check if the delta is greater than min interview duration or else return False
        if delta >= settings.MIN_INTERVIEW_DURATION:
            return [latest_start, earliest_end]
        return False
