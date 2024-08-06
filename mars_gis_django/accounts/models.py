from django.contrib.auth.models import UserManager, AbstractUser
from django.contrib.gis.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password

class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        # create_user と create_superuser の共通処理
        if not email:
            raise ValueError('email must be set')
        if not username:
            raise ValueError('username must be set')

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email=None, password=None, **extra_fields):

        if not email:
            raise ValueError('email must be set')
        if not username:
            raise ValueError('username must be set')

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, password, **extra_fields)
    

class CustomUser(AbstractUser):
    objects = CustomUserManager()

    def __str__(self):
        return self.username
    

class Project(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=255, null=False, blank=False)
    admin = models.ManyToManyField(CustomUser,related_name='project_admin')
    member = models.ManyToManyField(CustomUser, related_name='project_member')

    def __str__(self):
        return self.name
    
