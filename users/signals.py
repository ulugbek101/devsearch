from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from users.models import Profile



@receiver(post_save, sender=User)
def profile_creation(sender, created, instance, **kwargs):
    if created:
        profile = Profile.objects.create(
            user=instance,
            fullname=f"{instance.first_name} {instance.last_name}",
            username=instance.username,
            email=instance.email
        )
        profile.save()
        
        subject = 'Welcome to Dev-Search'
        message = 'We are glad you are here !'
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [profile.email],
                fail_silently=False
            )
        except:
            pass

@receiver(post_delete, sender=Profile)
def profile_deletion(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


def user_update(sender, instance, created, **kwargs):
    if not created:
        profile = instance
        user = profile.user

        user.username = profile.username
        user.full_name = profile
        user.email = profile.email
        user.save()


post_save.connect(user_update, sender=Profile)
