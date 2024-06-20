from django.shortcuts import render, get_object_or_404, redirect
from .models import TodoItem
from .forms import TodoForm

def home(request):
    return render(request, "home.html")

def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html", {"todos": items})

def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todos')  # Redirect to the todos view
    else:
        form = TodoForm()
    return render(request, 'add_todo.html', {'form': form})

def edit_todo(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todos')  # Redirect to the todos view
    else:
        form = TodoForm(instance=todo)
    return render(request, 'edit_todo.html', {'form': form})

def delete_todo(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('todos')  # Redirect to the todos view
    return render(request, 'delete_todo.html', {'todo': todo})
