from django.db import models
from datetime import date
from user.models import User
# Create your models here.

class Attendence(models.Model):
    intern = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today())