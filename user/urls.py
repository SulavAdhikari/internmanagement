from django.urls import path
from .views import (
    CustomAuthToken,
    LoginAPIView,
    RegisterAPIView, 
    AllUserAPIView,
    UserAPIView,
    UserUpdateAPIView,)

app_name = 'user'
urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('login/',LoginAPIView.as_view()),
    path('register/',RegisterAPIView.as_view()),
    path('users/', AllUserAPIView.as_view()),
    path('user/<int:id>/',UserAPIView.as_view()),
    path('userupdate/<int:id>/',UserUpdateAPIView.as_view()),
]