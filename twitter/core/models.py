from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=False, unique=True)
    name = models.CharField(max_length=100, blank=False)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = None
    REQUIRED_FIELDS = ['name']

    def save(self, *args, **kwargs):
        self.date_modified = datetime.date.today()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Twit(models.Model):
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now_add=True)
    text = models.TextField(max_length=100, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

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
    twit = models.ForeignKey(Twit, on_delete=models.CASCADE, blank=False, null=False)
    text = models.TextField(max_length=50, blank=False)

    class Meta:
        ordering = ['date_created']

    def save(self, *args, **kwargs):
        self.date_modified = datetime.date.today()
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return self.text
