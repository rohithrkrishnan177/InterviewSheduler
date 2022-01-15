from rest_framework.routers import DefaultRouter
from django.urls import include, path

from . import views

app_name = 'interviewapp'

# API urls declared here all URL's are prepended with 'api/v1/'
router = DefaultRouter()
router.register(r'Select-time-slot', views.AvailableTimeViewSet, basename='available-time')


urlpatterns = [
    path('', include(router.urls)),
    path('view-available-time/', views.ScheduleView.as_view(), name='schedule-time')
]

