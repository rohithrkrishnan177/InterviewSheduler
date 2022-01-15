from django.conf import settings
from django.utils import timezone


def check_overlapping(start_a, end_a, start_b, end_b):
    """
    function to check if 2 ranges A and B overlaps
    """
    if start_a <= end_b and end_a >= start_b:
        return True
    return False


def date_range_chunks(start, end, chunk=settings.MIN_INTERVIEW_DURATION):
    """
    func to split a date range into smaller range chunks, only complete chunks are returned
    """
    diff = (end - start).total_seconds() // chunk
    items = []
    start_time = start
    for i in range(int(diff)):
        end_time = start_time + timezone.timedelta(minutes=chunk)
        if end_time <= end:
            items.append((start_time, end_time))
            start_time = end_time
    return items
