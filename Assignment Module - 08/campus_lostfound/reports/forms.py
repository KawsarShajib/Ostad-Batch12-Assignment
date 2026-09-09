## Step 10 — Write `reports/forms.py` (new file)

# Forms turn raw HTML `<input>` submissions into validated Python data, and can also 
# auto-generate HTML fields from a model.



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


"""

**Three forms, three purposes:**

1. **`RegisterForm`** — instead of writing a username/password form from scratch, we extend Django's built-in `UserCreationForm` (which already handles password confirmation and hashing safely) and just add an `email` field on top. The `__init__` override loops over every field and adds Bootstrap's `form-control` CSS class, so it looks consistent without repeating `attrs={'class': ...}` on each field individually.

2. **`ReportForm`** is a **`ModelForm`** — instead of manually declaring 8 fields, we point it at the `Report` model and list which fields to expose: `fields = ['item_name', 'report_type', ...]`. Django reads each field's type from the model and auto-generates the right HTML input. Two fields are **deliberately excluded**: `owner` (set in the view from whoever's logged in — never something a user should type in themselves) and `status` (only changed through the dedicated "Resolve" action, covered in Step 12).

3. **`ReportSearchForm`** is a plain `forms.Form` (not tied to a model) — used only for the search bar. Every field has `required=False` so an empty search shows everything. `choices=[('', 'All')] + Report.TYPE_CHOICES` prepends a blank "All" option onto the model's real choices.


"""
