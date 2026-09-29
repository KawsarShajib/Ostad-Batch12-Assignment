from django import forms
from .models import Property

# addition of image gallery for a property
# ----------------------------------------
from django.forms import inlineformset_factory
from .models import Property, PropertyImage





class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'property_type', 'location',
            'monthly_rent', 'bedrooms', 'bathrooms', 'image', 'is_available',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_monthly_rent(self):
        rent = self.cleaned_data['monthly_rent']
        if rent <= 0:
            raise forms.ValidationError("Monthly rent must be greater than zero.")
        return rent


class PropertySearchForm(forms.Form):
    location = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Search by location...'}))
    property_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + list(Property.PropertyType.choices),
        widget=forms.Select(attrs={'class': 'form-select'}))
    min_rent = forms.DecimalField(required=False, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Min rent'}))
    max_rent = forms.DecimalField(required=False, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Max rent'}))

    def clean(self):
        cleaned_data = super().clean()
        min_rent = cleaned_data.get('min_rent')
        max_rent = cleaned_data.get('max_rent')
        if min_rent is not None and max_rent is not None and min_rent > max_rent:
            raise forms.ValidationError("Minimum rent cannot be greater than maximum rent.")
        return cleaned_data


# addition of image gallery for a property
# ----------------------------------------
# Lets an owner upload several gallery photos alongside the property form.
# extra=3 shows 3 empty upload slots; can_delete=True lets them remove an
# existing gallery photo by ticking its "Remove this image" box.
PropertyImageFormSet = inlineformset_factory(
    Property,
    PropertyImage,
    fields=['image', 'caption'],
    extra=3,
    can_delete=True,
    widgets={
        'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional caption'}),
    },
)