from django.contrib.auth.models import User
from django.db import models

class FacebookUser(models.Model):
    facebook_id = models.CharField(max_length=100, unique=True)
    contrib_user = models.OneToOneField(User,null=True,blank=True)
    contrib_password = models.CharField(max_length=100)
