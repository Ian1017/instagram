from django.db import models
import datetime as dt

# Create your models here.
class Editor(models.Model):
    first_name = models.CharField(max_length =30)
    last_name = models.CharField(max_length =30)
    email = models.EmailField()

    def __str__(self):
        return self.first_name
    class Meta:
        ordering = ['first_name']
    def save_editor(self):
        self.save()

class tags(models.Model):
    name = models.CharField(max_length= 20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags' 

class Profile(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    editor = models.ForeignKey(Editor)
    profile_image = models.ImageField(upload_to = 'profile')
    bio = models.TextField()

class NewsletterRecipients(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField() 