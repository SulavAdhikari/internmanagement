from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    
    USERNAME_FIELDS = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @property
    def role(self):
        from .models import UserProfile
        userprof = UserProfile.objects.filter(user=self).first()
        if userprof.isIntern:
            return 'intern'
        if userprof.isSupervisor:
            return 'supervisor'
        return None


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isIntern = models.BooleanField()
    isSupervisor = models.BooleanField()

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        if user.is_staff == True:
            userprofile = UserProfile.objects.create(user=user, isIntern=False, isSupervisor=True)
        
        else:
            userprofile = UserProfile.objects.create(user=user, isIntern=True, isSupervisor=False)

post_save.connect(create_profile, sender=User)