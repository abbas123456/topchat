from django.db import models
from django.contrib.auth.models import User


class AuthenticationToken(models.Model):
    token_string = models.CharField(max_length=128)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.token_string)