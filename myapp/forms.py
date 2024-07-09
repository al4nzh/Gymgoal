from django import forms
from .models import WorkoutItem, WeightLog
from .models import FoodEntry
class WorkoutForm(forms.ModelForm):
    class Meta:
        model = WorkoutItem
        fields = ['title', 'reps', 'completed']

class WeightLogForm(forms.ModelForm):
    class Meta:
        model = WeightLog
        fields = ['date', 'weight']
    

class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry
        fields = ['name', 'calories', 'carbs', 'protein', 'fats']