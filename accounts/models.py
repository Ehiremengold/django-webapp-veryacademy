from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(default="default.png", upload_to="profile_pics")
    contact = models.CharField(max_length=13, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=200,  null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs["created"]:
        profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


