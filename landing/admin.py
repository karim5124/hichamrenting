from django.contrib import admin
from .models import Formulaire

@admin.register(Formulaire)
class FormulaireAdmin(admin.ModelAdmin):
    list_display = ("prenom", "nom", "email")
