from re import U
from sys import intern
from django.db import models
from user.models import User

# Create your models here.
class Task(models.Model):
    supervisor = models.OneToOneField(User,related_name="supervisor", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    intern = models.OneToOneField(User,related_name="intern", on_delete=models.CASCADE)
    isCompleted = models.BooleanField(default=False)

    def complete(self, request):
        if request.user.id == self.intern.id or request.user.isStaff:
            self.isCompleted = True
            self.save()

    