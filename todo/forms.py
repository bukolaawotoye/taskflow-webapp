from django import forms
from .models import Todo
from authentication.models import User  # Ensure correct reference

class TodoForm(forms.ModelForm):
    assigned_user = forms.ModelChoiceField(
        queryset=User.objects.all(),  # Lists all users for assignment
        required=True,
        label="Assign to User"
    )

    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        label="Due Date"
    )

    class Meta:
        model = Todo
        fields = ['title', 'description', 'assigned_user', 'due_date', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }