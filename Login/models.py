from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class ProfileManager(BaseUserManager):

    def create_user(self,username,password,email,name):
        if not username or not email or not name:
            raise ValueError('Username can not be null')
        normal_email = self.normalize_email(email)
        user = self.model(username=username,name=name,email=normal_email)
        user.set_password(password)
        user.save(using=self.db)

    def create_superuser(self,username,password,email,name):
        if not username or not email or not name:
            raise ValueError('Fields are required')
        normal_email = self.normalize_email(email)
        user = self.model(username=username,name=name,email=normal_email)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self.db)


class Profile(AbstractBaseUser,PermissionsMixin):

    username = models.CharField(unique=True,max_length=50)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects  = ProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS =['name','email']

    def __str__(self):
        return self.username
