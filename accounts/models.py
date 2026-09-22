from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
