from django.db import models

class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    weight = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)
