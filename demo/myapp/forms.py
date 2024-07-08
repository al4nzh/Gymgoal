from django import forms
from .models import TodoItem, WeightLog
from .models import FoodEntry
class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title', 'reps', 'completed']

class WeightLogForm(forms.ModelForm):
    class Meta:
        model = WeightLog
        fields = ['date', 'weight']
    

class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry
        fields = ['name', 'calories', 'carbs', 'protein', 'fats']