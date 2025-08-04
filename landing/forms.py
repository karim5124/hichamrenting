from django import forms
from .models import Formulaire

class FormulaireForm(forms.ModelForm):
    class Meta:
        model = Formulaire
        fields = [
            'prenom', 'nom', 'email', 'telephone',
            'date_debut', 'date_fin', 'vehicule', 'notes'
        ]
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }