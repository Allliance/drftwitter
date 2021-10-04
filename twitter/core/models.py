from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime


class UserManager(BaseUserManager):
    def create_user(self, username, name, password=None):
        if not username:
            raise ValueError("Users must have username")
        if not name:
            raise ValueError("Users must have name")
        user = self.model(username=username,
                          name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, password=None):
        user = self.create_user(username=username, name=name, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, blank=False, unique=True)
    name = models.CharField(max_length=100, blank=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    date_modified = models.DateTimeField(verbose_name='date modified', auto_now_add=True)
    last_login = models.DateField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = None
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        self.date_modified = datetime.datetime.today()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Twit(models.Model):
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now_add=True)
    text = models.TextField(max_length=100, blank=False)
    user = models.ForeignKey(User, related_name='twits', on_delete=models.CASCADE)

    class Meta:
        ordering = ['date_created']

    def save(self, *args, **kwargs):
        self.date_modified = datetime.date.today()
        super(Twit, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id) + " : " + str(self.text)


class Comment(models.Model):
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now_add=True)
    twit = models.ForeignKey(Twit, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=50, blank=False)

    class Meta:
        ordering = ['date_created']

    def save(self, *args, **kwargs):
        self.date_modified = datetime.date.today()
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return self.text
