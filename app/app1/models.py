from django.db import models


# Create your models here.
class Users(models.Model):
    email = models.EmailField(unique=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email
