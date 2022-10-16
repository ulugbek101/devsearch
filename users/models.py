import uuid

from django.urls import reverse
from django.db import models

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True)
    fullname = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True)
    bio = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True, default='user-images/user-default.png', upload_to='user-images/')
    location = models.CharField(max_length=200, null=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    social_stackoverflow = models.CharField(max_length=200, null=True, blank=True)
    social_website = models.CharField(max_length=200, null=True, blank=True)
    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    @property
    def unread_messages_count(self):
        unread_messages_count = self.messages.filter(is_read=False).count()
        return unread_messages_count if unread_messages_count > 0 else None

    def __str__(self):
        return f'{self.fullname} - {self.user}'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.id})

    # @property
    # def is_liked(self):
    #     if self.id in 
    #     return self.id in Project.objects.values_list('profile')
    # profile.id in project.vote_set.values_list('profile', flat=True)
    
    class Meta:
        ordering = ('created', 'fullname')


class Skill(models.Model):
    owner = models.ForeignKey(to=Profile, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    sender = models.ForeignKey(to=Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(to=Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    fullname = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # def __str__(self):
    #     return f'{self.recipient.fullname} : {self.subject}'

    class Meta:
        ordering = ['is_read', '-created']
