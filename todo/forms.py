from django import forms
from .models import Todo
from authentication.models import User  # Ensure correct reference

class TodoForm(forms.ModelForm):
    assigned_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role="User"),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Assign Users"
    )

    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        label="Due Date"
    )

    class Meta:
        model = Todo
        fields = ['title', 'description', 'assigned_users', 'due_date', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
