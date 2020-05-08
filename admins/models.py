from django.db import models
from django.contrib.auth.models import User , Group


# Create your models here.
class adminlevel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, null=False, blank=False)
    is_accept = models.BooleanField(default=False)
    is_reject = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name


class publish(models.Model):
    user = models.ForeignKey(adminlevel, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    is_accept = models.BooleanField(default=False)
    file = models.FileField(default=None)
