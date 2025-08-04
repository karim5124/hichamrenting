from django.db import models

# Create your models here.

from django.db import models

class Formulaire(models.Model):
    prenom = models.CharField("Prénom", max_length=100)
    nom = models.CharField("Nom", max_length=100)
    email = models.EmailField("Email")
    telephone = models.CharField("Téléphone", max_length=20, blank=True)

    # Subscription details
    date_debut = models.DateField("Date début")
    date_fin = models.DateField("Date fin")
    vehicule = models.CharField("Véhicule", max_length=100, blank=True)
    notes = models.TextField("Notes", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.email})"