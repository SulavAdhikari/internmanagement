
from django.urls import path
from .views import (
    AddAtendenceAPIView,

)

app_name = 'attendence'
urlpatterns = [
    path('attendence/',AddAtendenceAPIView.as_view())
]