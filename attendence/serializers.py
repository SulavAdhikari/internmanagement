from rest_framework import serializers
from datetime import date

from .models import Attendence
from user.models import User
class AttendenceAddSerializer(serializers.ModelSerializer):
    date = serializers.DateField(read_only=True)
    intern = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model=Attendence
        fields = ['date','intern']
    
    def validate(self, data):
        intern = self.context.get('intern')
        if intern.role != 'intern':
            raise serializers.ValidationError({
                'validationError':'Invalid user'
            })
        today = str(date.today())
        obj = Attendence.objects.filter(intern=intern,date=today).first()
        if obj:
            raise serializers.ValidationError({
                'validationError':"Already attended for today's date"
            })
        data['intern']=intern
        return data

    def create(self, validated_data):
        intern = validated_data.get('intern')
        obj = Attendence(intern=intern)
        obj.save()
        super().create(validated_data=validated_data)
