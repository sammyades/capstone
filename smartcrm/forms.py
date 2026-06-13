from django import forms
from .models import Lead, Activity, Deal, Task 

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        # Define which fields the user should fill out
        fields = ['amount', 'stage', 'status']
        
        # Add Bootstrap styling to the form fields
        widgets = {
            field: forms.TextInput(attrs={'class': 'form-control'}) 
            for field in fields
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # Define which fields the user should fill out
        fields = ['title', 'description', 'priority', 'status', 'due_date']
        
        # Add Bootstrap styling to the form fields
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Send Proposal'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Task details...'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['type', 'note']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'What happened?'}),
        }

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        # Fields the user should fill out
        fields = ['first_name', 'last_name', 'email', 'phone', 'company', 'industry', 'status', 'created_at']
        widgets = {
            # Add Bootstrap classes for a clean look
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'industry': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'created_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 

        }



