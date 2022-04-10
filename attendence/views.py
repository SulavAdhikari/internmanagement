from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from user import serializers

from .serializers import AttendenceAddSerializer
# Create your views here.

class AddAtendenceAPIView(APIView):
    serializer_class = AttendenceAddSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        user = request.user
        context = {'intern':user}
        serializer = self.serializer_class(data = request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        