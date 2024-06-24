from django.shortcuts import render, get_object_or_404, redirect
from .models import TodoItem, WeightLog
from .forms import TodoForm, WeightLogForm
import json 
def home(request):
    return render(request, "home.html")

def todos(request):
    items = TodoItem.objects.all()
    for item in items:
        item.latest_weight = item.weight_logs.order_by('-date').first().weight if item.weight_logs.exists() else 'N/A'
    return render(request, "todos.html", {"todos": items})

def add_todo(request):
    if request.method == 'POST':
        todo_form = TodoForm(request.POST)
        weight_log_form = WeightLogForm(request.POST)
        if todo_form.is_valid() and weight_log_form.is_valid():
            todo = todo_form.save()
            weight_log = weight_log_form.save(commit=False)
            weight_log.todo = todo
            weight_log.save()
            return redirect('todos')
    else:
        todo_form = TodoForm()
        weight_log_form = WeightLogForm()
    return render(request, 'add_todo.html', {'todo_form': todo_form, 'weight_log_form': weight_log_form})

def edit_todo(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)
    if request.method == 'POST':
        todo_form = TodoForm(request.POST, instance=todo)
        weight_log_form = WeightLogForm(request.POST)
        if todo_form.is_valid() and weight_log_form.is_valid():
            todo_form.save()
            weight_log = weight_log_form.save(commit=False)
            weight_log.todo = todo
            weight_log.save()
            return redirect('todos')
    else:
        todo_form = TodoForm(instance=todo)
        weight_log_form = WeightLogForm()
    return render(request, 'edit_todo.html', {'todo_form': todo_form, 'weight_log_form': weight_log_form})

def delete_todo(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('todos')
    return render(request, 'delete_todo.html', {'todo': todo})

def progress_graph(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)
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

def delete_todo(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('todos')
    return render(request, 'delete_todo.html', {'todo': todo})

def progress_graph(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)
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

