from django.urls import path
from .views import (
    AddTaskAPIView,
    GetTaskAPIView,
    CompleteTaskAPIView,
    TaskAPIView,
    TaskDetailAPIView,

)

app_name = 'task'
urlpatterns = [
    path('assign/',AddTaskAPIView.as_view()),
    path('tasks/',GetTaskAPIView.as_view()),
    path('complete/<int:id>/',CompleteTaskAPIView.as_view()),
    path('task/<int:id>/', TaskDetailAPIView.as_view()),
    path('taskupdate/<int:id>/', TaskAPIView.as_view()),
    
]