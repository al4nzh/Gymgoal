from django import forms
from .models import TodoItem, WeightLog

class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title', 'reps', 'completed']

class WeightLogForm(forms.ModelForm):
    class Meta:
        model = WeightLog
        fields = ['date', 'weight']