from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=255, default='null', blank=True, null=True)
    contact = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.user.get_username())


def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_profile, sender=User)