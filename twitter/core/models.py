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
