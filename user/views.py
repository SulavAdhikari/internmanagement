from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from .serializers import  (
    LoginSerializer,
    RegisterSerializer,
    AllUserSerializer,
    UserUpdateSerializer,
    
    )
from .models import User

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

class LoginAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

class RegisterAPIView(APIView):

    permission_classes = (IsAdminUser, )
    serializer_class = RegisterSerializer

    def post(self,request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class AllUserAPIView(APIView):
    serializer_class = AllUserSerializer
    permission_classes = (IsAuthenticated, )
    
    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

class UserAPIView(APIView):
    serializer_class= AllUserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

class UserUpdateAPIView(APIView):
    
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAdminUser, )

    def put(self, request, id):
        print('id:',str(id))
        context = {
            'id':id,
        }
        data = request.data
        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        user = User.objects.filter(id=id).first()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
