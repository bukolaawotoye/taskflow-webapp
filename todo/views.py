from django.shortcuts import render

from authentication.models import User
from . forms import TodoForm
from .models import Todo
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from datetime import datetime
from django.urls import reverse
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    return render(request, 'todo/index.html')
def create_todo(request):
    form = TodoForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_user_id = request.POST.get('assigned_user')
        due_date_str = request.POST.get('due_date')  # Capturing the due date input

        assigned_user = User.objects.get(id=assigned_user_id)

        if assigned_user.role != 'editor':
            return HttpResponseForbidden("You can only assign todos to editors.")

        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date() if due_date_str else None

        todo = Todo(title=title, description=description, assigned_user=assigned_user, due_date=due_date)
        todo.save()

        messages.add_message(request, messages.SUCCESS, "Todo created and assigned successfully!")
        return HttpResponseRedirect(reverse("todo", kwargs={'id': todo.pk}))
    return render(request, 'todo/create-todo.html', context)
#