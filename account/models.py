from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyUser(AbstractUser):

    email = models.EmailField(_("email address"), unique=True)


class Profile(models.Model):
    user = models.OneToOneField(
        MyUser, on_delete=models.CASCADE, related_name="profile"
    )

    cellphone = models.CharField(max_length=15, blank=True)
    tice = models.CharField(max_length=15, blank=True)
    age = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    objects = models.Manager()
