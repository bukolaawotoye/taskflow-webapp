from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('create/', views.create_todo, name='create-todo'),
    path('todo-delete/<id>/', views.todo_delete, name='todo-delete'),
    path('todo-edit/<id>/', views.todo_edit, name='todo-edit'),
    path('todo-detail/<id>/', views.todo_detail, name='todo-detail'),
    path('user-tasks/', views.user_tasks, name='user-tasks'),
    path('edit-user/<id>/', views.edit_user, name='edit-user'),
    path('user-task-detail/<id>/', views.user_task_detail, name='user-task-detail'),
]