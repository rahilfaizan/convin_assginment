from django.db import models

# Create your models here.

from django.db import models

# Create your models here.


class users(models.Model):
    Name = models.CharField(max_length=500)


class accounts(models.Model):
    Name = models.CharField(max_length=500)


class contacts(models.Model):
    Name = models.CharField(max_length=500)