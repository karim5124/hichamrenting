from tabnanny import verbose
import uuid
from django.db import models
from django.core.files.base import ContentFile

from qr_code.qrcode.maker import make_qr_code_image
from qr_code.qrcode.utils import QRCodeOptions

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Client(TimeStampedModel):
    first_name = models.CharField("First Name", max_length=100, default='Amine')
    last_name = models.CharField("Last Name", max_length=100, default='')
    email = models.EmailField("Email Address", unique=True, default='')
    phone = models.CharField("Phone Number", max_length=20, blank=True, default='')
    verified = models.BooleanField("Verified", default=False)
    notes = models.TextField("Notes", blank=True, default='')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Vehicule(TimeStampedModel):
    marque = models.CharField("Marque", max_length=100)
    matricule = models.CharField("Immatriculation", max_length=20, unique=True)
    modele = models.CharField("Modèle", max_length=100, blank=True)
    production_date = models.DateField("Date de production")
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="vehicules",
        help_text="Le client propriétaire de ce véhicule"
    )

class Device(TimeStampedModel):
    code_qr = models.UUIDField(
        default=uuid.uuid4,  # auto-generate
        editable=False,  # can’t be changed by hand
        unique=True,  # no two devices share a code
        help_text="Unique identifier encoded in the QR code"
    )
    picture = models.ImageField(upload_to="devices/images/", blank=True)
    model = models.CharField(max_length=50)
    date_achat = models.DateField("Date Ahat")
    status = models.CharField(
        max_length=20,
        choices=[
            ("available", "Available"),
            ("in_use", "In Use"),
            ("maintenance", "Maintenance"),
            ("retired", "Retired"),
        ],
        default="available"
    )
    last_maintenance = models.DateField(blank=True, null=True)


    def save(self, *args, **kwargs):
        # Only generate once (when qr_image is empty)
        if not self.qr_image:
            # 1. Prepare the data and options
            data = str(self.code_qr)
            options = QRCodeOptions()  # uses sensible defaults :contentReference[oaicite:0]{index=0}

            # 2. Generate PNG bytes
            img_bytes: bytes = make_qr_code_image(data,
                                                  options)  # returns raw image bytes :contentReference[oaicite:1]{index=1}

            # 3. Wrap in a Django file and save to the ImageField (without committing yet)
            filename = f"qr_{self.code_qr}.png"
            self.qr_image.save(filename, ContentFile(img_bytes), save=False)

        # 4. Now call super to save both model and file
        super().save(*args, **kwargs)


class Subscription(TimeStampedModel):
    date_debut = models.DateTimeField(null=False, blank=False, verbose_name='Date debut du contrat')
    date_fin = models.DateTimeField(null=False, blank=False, verbose_name='Date debut du contrat')
    actual_date_debut = models.DateTimeField(null=True, blank=True, verbose_name='Date debut reel du contrat')
    actual_date_fin = models.DateTimeField(null=True, blank=True, verbose_name='Date fin reel du contrat')
    paid = models.BooleanField(default=False, verbose_name='Sousciption payee ?')
    deposit_paid = models.BooleanField(default=False, verbose_name='Avance payee ?')
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False, null=False)
    devices = models.ManyToManyField(Device, blank=False)
    pic_before_device = models.FileField(upload_to='subscriptions/before/', verbose_name='Image Avant sousciption')
    pic_after_device = models.FileField(upload_to='subscriptions/after/', verbose_name='Image Apres souscription')
    pic_on_vehicule = models.FileField(upload_to='subscriptions/vehicule/', verbose_name='Image de l"outils sur le vehicule')
    prix = models.FloatField(blank=True, null=True, verbose_name='Cout de la sousciption')
    incidents = models.TextField(null=True, blank=True, verbose_name='Incident a noter ?')
    notes = models.TextField(null=True, blank=True, verbose_name='Notes sur la souscription ?')
    late_days = models.IntegerField(null=True, blank=True, default=0, verbose_name='Nombre de jour en retard')





