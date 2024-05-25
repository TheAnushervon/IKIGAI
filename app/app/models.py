from django.db import models


class MyModel(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.id
