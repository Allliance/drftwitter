from django.db import models
import datetime


class User(models.Model):
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False)
    username = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.date_modified = datetime.date.today()
        super(User, self).save(*args, **kwargs)


class Twit(models.Model):
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now_add=True)
    text = models.TextField(max_length=100, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date_created']

    def save(self, *args, **kwargs):
        self.date_modified = datetime.date.today()
        super(Twit, self).save(*args, **kwargs)


class Comment(models.Model):
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now_add=True)
    twit = models.ForeignKey(Twit, on_delete=models.CASCADE)
    text = models.TextField(max_length=50, blank=False)

    class Meta:
        ordering = ['date_created']

    def save(self, *args, **kwargs):
        self.date_modified = datetime.date.today()
        super(Comment, self).save(*args, **kwargs)

