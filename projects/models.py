import uuid
from xmlrpc.client import Boolean

from django.db import models
from django.forms import IntegerField
from django.urls import reverse
from users.models import Profile


class Project(models.Model):
    owner = models.ForeignKey(to=Profile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='project-images/', default='project-images/default.jpg')
    tags = models.ManyToManyField(to='Tag')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.id})

    @property
    def comments_count(self):
        return self.review_set.all().count()


class Vote(models.Model):
    VOTE_TYPE = (
        (1, 'Like'),
        (0, 'Dislike')
    )
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, null=True)
    vote = models.IntegerField(choices=VOTE_TYPE, null=True, blank=True)

    class Meta:
        unique_together = ('profile', 'project')
    
    def __str__(self):
        return f'{self.vote} -- {self.project.title} -- {self.profile.fullname}'


class Review(models.Model):
    owner = models.ForeignKey(to=Profile, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return f'{self.owner.fullname} --- {self.project}'

    class Meta:
        ordering = ('created',)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name
