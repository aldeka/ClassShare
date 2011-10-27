from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class ISchooler(User):
    is_current_student = models.BooleanField(default=True)

class Review(models.Model):
    author = models.ForeignKey(ISchooler, blank=True, null=True, on_delete=models.SET_NULL)
    content = models.TextField(blank=True,null=True)
    is_anonymous = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
