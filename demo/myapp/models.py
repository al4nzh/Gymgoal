from django.db import models

class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    reps = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class WeightLog(models.Model):
    todo = models.ForeignKey(TodoItem, on_delete=models.CASCADE, related_name='weight_logs')
    date = models.DateField()
    weight = models.FloatField()

    def __str__(self):
        return f"{self.todo.title} - {self.date} - {self.weight}"
