from rest_framework import serializers 
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .models import User, UserProfile

class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username is None:
            raise serializers.ValidationError(
                {
                    'validationError': 'An username is required to log in.',
                }
            )
        
        if password is None:
            raise serializers.ValidationError(
                {
                    'validationError': 'A password is required to log in.'
                }
            )
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise serializers.ValidationError(
                {
                    'validationError':'Email or password did not match.'
                }
            )

        token, created = Token.objects.get_or_create(user=user)
        return {
            'token':token.key,
            'id':user.pk,
            'username':user.username
        }

class RegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model = User
        fields = ['id','username','password','token',]

    def validate(self, data):
        username = data['username']
        if User.objects.filter(username=username):
            raise serializers.ValidationError(
                {
                    'validationError':'Username already in use.'
                }
            )

        return data
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        
class AllUserSerializer(serializers.ModelSerializer):   
    class Meta:
        model = User
        fields = ['id','username','role']

class UserUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    role = serializers.CharField(max_length=10)
    username = serializers.CharField(max_length=100, required=False,allow_null=True)

    class Meta:
        model = User
        fields = ['id','role','username']

    def validate(self, data):
        role = data.get('role')
        id = self.context.get('id')
        user = User.objects.filter(id=id).first()
        if user is None:
            raise serializers.ValidationError({
                'valdationError': 'Invalid user id.'
            })
        
        if role:
            if role != 'intern' and role != 'supervisor':
                raise serializers.ValidationError({
                    'valdationError': 'Invalid role type.'
                })
            
        data['id']=id
        return data

    def create(self, validated_data):
        role = validated_data['role']
        id = validated_data['id']
        user = User.objects.filter(id=id).first()
        if role == 'intern':
            userprofile = UserProfile.objects.filter(user=user).first()
            userprofile.isIntern = True
            userprofile.isSupervisor = False
            user.is_staff = False
            user.is_admin = False
            userprofile.save()
            user.save()
        if role == 'supervisor':
            userprofile = UserProfile.objects.filter(user=user).first()
            userprofile.isIntern = False
            userprofile.isSupervisor = True
            user.is_staff = True
            userprofile.save()
            user.save()
        return user