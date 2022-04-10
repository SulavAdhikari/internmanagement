from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .extras import IsStaffUser, Tasks

from .serializers import (
    TaskSerializer,
    AddTaskSerializer,
    GetTaskSerializer
)
from .models import Task
# Create your views here.
class GetTaskAPIView(APIView, Tasks):
    permission_classes = (AllowAny, )
    serializer_class = GetTaskSerializer

    def get(self, request):
        tasks = self.fetch_tasks()
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data)

class TaskDetailAPIView(APIView, Tasks):
    permission_classes = (IsAuthenticated, )
    serializer_class = TaskSerializer

    def get(self, request, id):
        task = self.fetch_task(id)
        serializer = self.serializer_class(task)
        return Response(serializer.data)

class TaskAPIView(APIView, Tasks):
    permission_classes = (IsStaffUser, )
    serializer_class = TaskSerializer

    def put(self, request,id):
        task = self.fetch_task(id)
        request.data._mutable = True
        request.data['id'] = id
        serializer = self.serializer_class(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        task = self.fetch_task(id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddTaskAPIView(APIView):
    permission_clases = (IsStaffUser, )
    serializer_class = AddTaskSerializer

    def put(self, request):
        supervisor = request.user
        request.data._mutable = True
        data=request.data
        data['supervisor'] = supervisor.pk
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class CompleteTaskAPIView(APIView, Tasks):

    permission_classes = (IsAuthenticated, )

    def post(self, request, id):
        task = self.fetch_task(id)
        task.complete(request)
        return Response(status=status.HTTP_200_OK)
