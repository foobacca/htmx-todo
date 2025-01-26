from django.db import models

from .querysets import TodoQuerySet

# Create your models here.

class TodoItem(models.Model):
    title = models.CharField(max_length=200, unique=True)
    text = models.TextField()

    objects = TodoQuerySet.as_manager()

    class Meta:
        ordering = ["id"]
