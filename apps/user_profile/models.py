from dynamic_filenames import FilePattern
from stdimage.models import StdImageField

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser


class UserProfile (AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=100, unique=True, blank=False, null=False)
    username = models.CharField(max_length=20, unique=False, blank=False, null=False)
    first_name = models.CharField(max_length=20, unique=False, blank=False)
    last_name = models.CharField(max_length=20, unique=False, blank=False)
    avatar = StdImageField(upload_to=FilePattern(filename_pattern='user_profiles/{uuid:base32}{ext}'), variations={
        'normal': {"width": 200, "height": 200, "crop": True},
        'small': {"width": 50, "height": 50, "crop": True},
    }, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profiles', on_delete=models.CASCADE, null=True)
    last_activity = models.DateTimeField()
