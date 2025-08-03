from django.contrib import admin
from .models import Client, Vehicule, Device, Subscription

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "verified")
    search_fields = ("first_name", "last_name", "email")

@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ("marque", "matricule", "modele", "production_date", "client")
    list_filter  = ("marque", "production_date")
    search_fields = ("matricule",)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("code_qr", "model", "status", "date_achat", "last_maintenance")
    list_filter  = ("status",)
    readonly_fields = ("code_qr",)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("client", "vehicule", "date_debut", "date_fin", "paid", "deposit_paid")
    list_filter  = ("paid", "deposit_paid", "client")
    filter_horizontal = ("devices",)
    readonly_fields = ("actual_date_debut", "actual_date_fin")
