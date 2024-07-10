from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import WorkoutItem, WeightLog
from .forms import WorkoutForm, WeightLogForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
import json
from rest_framework import generics
from .models import FoodEntry
from .serializers import FoodEntrySerializer
from .forms import FoodEntryForm


def home(request):
    return render(request, "home.html")

@login_required
def workouts(request):
    items = WorkoutItem.objects.filter(user=request.user)
    for item in items:
        item.latest_weight = item.weight_logs.order_by('-date').first().weight if item.weight_logs.exists() else 'N/A'
    return render(request, "workouts.html", {"todos": items})

@login_required
def add_workout(request):
    if request.method == 'POST':
        todo_form = WorkoutForm(request.POST)
        weight_log_form = WeightLogForm(request.POST)
        if todo_form.is_valid() and weight_log_form.is_valid():
            todo = todo_form.save(commit=False)
            todo.user = request.user
            todo.save()
            weight_log = weight_log_form.save(commit=False)
            weight_log.todo = todo
            weight_log.save()
            return redirect('workouts')
    else:
        todo_form = WorkoutForm()
        weight_log_form = WeightLogForm()
    return render(request, 'add_workout.html', {'todo_form': todo_form, 'weight_log_form': weight_log_form})

@login_required
def edit_workout(request, pk):
    todo = get_object_or_404(WorkoutItem, pk=pk, user=request.user)
    if request.method == 'POST':
        todo_form = WorkoutForm(request.POST, instance=todo)
        weight_log_form = WeightLogForm(request.POST)
        if todo_form.is_valid() and weight_log_form.is_valid():
            todo_form.save()
            weight_log = weight_log_form.save(commit=False)
            weight_log.todo = todo
            weight_log.save()
            return redirect('workouts')
    else:
        todo_form = WorkoutForm(instance=todo)
        weight_log_form = WeightLogForm()
    return render(request, 'edit_workout.html', {'todo_form': todo_form, 'weight_log_form': weight_log_form})

@login_required
def delete_workout(request, pk):
    todo = get_object_or_404(WorkoutItem, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('workouts')
    return render(request, 'delete_workout.html', {'todo': todo})

@login_required
def progress_graph(request, pk):
    todo = get_object_or_404(WorkoutItem, pk=pk, user=request.user)
    weight_logs = todo.weight_logs.order_by('date')
    data = {
        "labels": [log.date.strftime("%Y-%m-%d") for log in weight_logs],
        "weights": [log.weight for log in weight_logs]
    }
    context = {
        "todo": todo,
        "data": json.dumps(data)
    }
    return render(request, "progress_graph.html", context)
def contact(request):
    return render(request, "contact.html")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('workouts')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
@login_required
def food_entries(request):
    if request.method == 'POST':
        form = FoodEntryForm(request.POST)
        if form.is_valid():
            food_entry = form.save(commit=False)
            food_entry.user = request.user
            food_entry.save()
            return redirect('food-entries')
    else:
        form = FoodEntryForm()

    food_entries = FoodEntry.objects.filter(user=request.user)
    
    total_calories = 0
    total_carbs = 0
    total_protein = 0
    total_fats  = 0
    for entry in food_entries:
        total_calories += entry.calories
        total_carbs += entry.carbs
        total_protein += entry.protein
        total_fats += entry.fats
    
    context = {
        'form': form,
        'food_entries': food_entries,
        'total_calories': total_calories,
        'total_carbs': total_carbs,
        'total_protein': total_protein,
        'total_fats': total_fats,
    }
    
    return render(request, 'food_entries.html', context)

@login_required
def edit_food(request, pk):
    item = get_object_or_404(FoodEntry, user=request.user, pk=pk)
    if request.method == 'POST':
        form = FoodEntryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('food-entries')
    else:
        form = FoodEntryForm(instance=item)
    return render(request, 'edit_food_entry.html', {'form': form})

@login_required
def delete_food(request, pk):
    item = get_object_or_404(FoodEntry, user=request.user, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('food-entries')
    return render(request, 'delete_food_entry.html', {'item': item})

#API for future use
class FoodEntryListCreate(generics.ListCreateAPIView):
    queryset = FoodEntry.objects.all()
    serializer_class = FoodEntrySerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FoodEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FoodEntry.objects.all()
    serializer_class = FoodEntrySerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
