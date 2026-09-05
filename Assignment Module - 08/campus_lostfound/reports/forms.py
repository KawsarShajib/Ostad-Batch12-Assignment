from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Report


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})



class ReportForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Report
        fields = [
            'item_name', 'report_type', 'category', 'description',
            'location', 'date', 'contact_info', 'image',
        ]
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Student ID Card'}),
            'report_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                                   'placeholder': 'Describe the item in detail...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Library, 2nd Floor'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone or email'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ReportSearchForm(forms.Form):
    q = forms.CharField(required=False, label='Search',
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by item name...'}))
    report_type = forms.ChoiceField(required=False, label='Type',
                                     choices=[('', 'All')] + Report.TYPE_CHOICES,
                                     widget=forms.Select(attrs={'class': 'form-select'}))
    category = forms.ChoiceField(required=False, label='Category',
                                  choices=[('', 'All')] + Report.CATEGORY_CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    status = forms.ChoiceField(required=False, label='Status',
                                choices=[('', 'All')] + Report.STATUS_CHOICES,
                                widget=forms.Select(attrs={'class': 'form-select'}))

    