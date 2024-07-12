from django import forms
from .models import UC

class UCCreateForm(forms.ModelForm):
    class Meta:
        model = UC
        fields = '__all__'