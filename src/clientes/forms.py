from django import forms
from .models import Cliente

class ClienteCreateForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['__all__']
    
    def clean_name(self):
        nome = self.cleaned_data.get("nome")
        return nome