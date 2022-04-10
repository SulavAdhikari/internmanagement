from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        from .models import UserProfile

    
        return user
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username=username, password=password, **extra_fields)

    def create_staffuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Staffuser must have is_superuser=True.')
    
        return self.create_user(username=username, password=password,**extra_fields)
