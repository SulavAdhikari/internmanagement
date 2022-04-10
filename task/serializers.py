from importlib.resources import read_binary
from pyexpat import model
from rest_framework import serializers 

from .models import Task
from user.models import User, UserProfile 

class GetTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields= ['id','title','description','intern','isCompleted','supervisor']


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True)
    intern = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=User.objects.all())
    isCompleted = serializers.BooleanField(required=False, allow_null=True)
    supervisor = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=User.objects.all())
    
    class Meta:
        model = Task
        fields= ['id','title','description','intern','isCompleted','supervisor']     
    def validate(self, data):
        intern = data.get('intern')

        if intern:
            if intern.is_staff:
                raise serializers.ValidationError(
                    {
                        'validationError':'Cannot assin to supervisor'
                    }
                )

class AddTaskSerializer(serializers.ModelSerializer):
    #id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Task
        fields= ['id','title','description','intern','isCompleted', 'supervisor']

    def validate(self, data):
        intern = data.get('intern')
        supervisor = data.get('supervisor')
        
        if intern is None:
            raise serializers.ValidationError(
                {
                    'ValidationError':'Inter is requred to assign a task.'
                }
            )
        if supervisor is None:
            raise serializers.ValidationError(
                {
                    'ValidationError':'Supervisor is requred to assign a task.'
                }
            )
        internobj = User.objects.filter(id=intern.pk).first()
        supervisorobj = User.objects.filter(id=supervisor.pk).first()
        if not supervisor:
            raise serializers.ValidationError(
                {
                    'ValidationError':'No supervisor with such id.'
                }
            )
        if not internobj:
            raise serializers.ValidationError(
                {
                    'ValidationError':'No intern with such id.'
                }
            )

        internprofile = UserProfile.objects.filter(user=internobj).first()
        if internprofile.isSupervisor:
            raise serializers.ValidationError(
                {
                    'ValidationError':'Cannot assign task to a supervisor.'
                }
            )
        return data
        