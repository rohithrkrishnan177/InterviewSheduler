from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from .models import AvailableTime
from .mixin import DateOverlapMixin
from .serializers import AvailableTimeSerializer


class AvailableTimeViewSet(ModelViewSet):
    """
    Create APIVIew for the Available-time model
    """
    serializer_class = AvailableTimeSerializer
    queryset = AvailableTime.objects.all()


class ScheduleView(DateOverlapMixin, APIView):
    """
    APIView to get the available times for both interviewer and candidate
    """

    def get(self, request):
        interviewer = request.query_params.get('interviewer', None)
        candidate = request.query_params.get('candidate', None)
        if not interviewer or not candidate:
            return Response(
                {'error': "Both candidate and interviews id's are required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if interviewer == candidate:
            return Response(
                {'error': "Both candidate and interviews id's cannot be same"}, status=status.HTTP_400_BAD_REQUEST
            )
        data = self.get_overlaps(interviewer, candidate)
        return Response({'data': data}, status=status.HTTP_200_OK)
