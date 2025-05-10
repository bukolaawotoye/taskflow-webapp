from django.shortcuts import render, redirect
from authentication.models import User
from . forms import TodoForm
from .models import Todo
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from datetime import datetime
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from helpers.decorators import auth_user_should_not_access
# Create your views here.
@login_required
def index(request):
    todos= Todo.objects.filter(owner=request.user)
    context = {
        'todos': todos
    }
    return render(request, 'todo/index.html',context)

def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.owner = request.user
            todo.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, "Todo created successfully!")
            return redirect(reverse("todo-detail", kwargs={'id': todo.pk}))
    else:
        form = TodoForm()
    return render(request, 'todo/create-todo.html', {'form': form})
@login_required
def todo_delete(request, id):
        todo = get_object_or_404(Todo, pk=id)
        context = {'todo': todo}
        if request.method == 'POST':
            # Check if the user is the owner of the todo
            if todo.owner != request.user:
                return HttpResponseForbidden("You are not allowed to delete this todo.")
            todo.delete()
            messages.success(request, "Todo deleted successfully!")
            return redirect('home')  # or whatever view shows the list of todos
        return render(request, 'todo/todo-delete.html', context)  # Add a template for confirmation

@login_required
def todo_edit(request, id):
    todo = get_object_or_404(Todo, pk=id)
    context = {
        'todo': todo
    }
    if request.method == 'POST':
        # Check if the user is the owner of the todo
        if todo.owner != request.user:
            return HttpResponseForbidden("You are not allowed to edit this todo.")
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            updated_todo = form.save(commit=False)
            updated_todo.save()
            form.save_m2m()  # Save assigned_users M2M data

            messages.success(request, "Todo updated successfully!")
            return HttpResponseRedirect(reverse("home"))
    else:
        form = TodoForm(instance=todo)

    context = {
        'todo': todo,
        'form': form
    }
    return render(request, 'todo/todo-edit.html', context)
@login_required 
def todo_detail(request, id):
    todo = get_object_or_404(Todo, pk=id)
    context = {
        'todo': todo
    }
    return render(request, 'todo/todo-detail.html', context)




#USER FUNCTIONS
@login_required
def user_tasks(request):
    """Displays tasks assigned to the logged-in user."""
    user = request.user
    tasks = Todo.objects.filter(assigned_users=user)  # ✅ Get tasks assigned to this user
    
    return render(request, "todo/user_tasks.html", {"tasks": tasks})
@login_required
def edit_user(request, id):
    task = get_object_or_404(Todo, pk=id)
    if request.method == 'POST':
        task.is_completed = request.POST.get('status') == "completed"
        task.save()
        messages.success(request, "Task status updated successfully!")
        return redirect('user-tasks')

    return render(request, 'todo/edit_user.html', {'task': task})
@login_required
def user_task_detail(request, id):
    """Displays details of a specific task."""
    task = get_object_or_404(Todo, pk=id)
    return render(request, "todo/user_task_detail.html", {"task": task})

