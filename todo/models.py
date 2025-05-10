from django.db import models
from authentication.models import User  # Ensure correct reference

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_users = models.ManyToManyField(User, related_name="assigned_todos")  # ✅ Allows multiple users
    due_date = models.DateField(null=True, blank=True)  # Allowing optional due dates
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_task")
    def __str__(self):
        return self.title