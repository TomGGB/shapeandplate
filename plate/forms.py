# forms.py
from django import forms

class AllergyForm(forms.Form):
    allergies = forms.CharField(widget=forms.Textarea, required=False, help_text="Ingrese sus alergias separadas por comas.")