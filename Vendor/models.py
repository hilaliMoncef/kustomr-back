from django.db import models
from django.db.models import Count, Sum
from Users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from Medias.models import VendorMedia
import os


class Vendor(models.Model):
    """
        This model represents the Store manager. It is linked to a regular user account.
    """
    # Choices for store type
    STORE_TYPE_CHOICES = [
        ('AL', 'Alimentation'),
        ('BA', 'Banque et assurance'),
        ('MT', 'Multimédia/Technologie'),
        ('TH', 'Textile/Habillement/Chaussure'),
        ('SE', 'Services aux entreprises'),
        ('AU', 'Automobile'),
        ('AM', 'Ameublement'),
        ('AR', 'Art (Artisanat)'),
        ('CO', 'Commerce de détail'),
        ('EV', 'Evenementiel'),
        ('HR', 'Hôtellerie/Restauration'),
        ('SM', 'Santé/Médical'),
    ]
    # Choices for store type
    STORE_TYPES_VISITS_CHOICES = [
        ('SM', 'Entre 50 et 200'),
        ('MD', 'Entre 200 et 500'),
        ('LG', 'Entre 500 et 1000'),
        ('XL', '1000+'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor")
    store_name = models.CharField(max_length=255)
    store_type = models.CharField(max_length=2, choices=STORE_TYPE_CHOICES, default='AL')
    store_visits = models.CharField(max_length=2, choices=STORE_TYPES_VISITS_CHOICES, default="SM")

    # Store infos
    store_phone = models.CharField(blank=True, null=True, max_length=255)
    store_adress = models.TextField(blank=True, null=True)

    # Social links
    website = models.CharField(max_length=255, default='', null=True, blank=True)
    facebook = models.CharField(max_length=255, default='', null=True, blank=True)
    instagram = models.CharField(max_length=255, default='', null=True, blank=True)
    youtube = models.CharField(max_length=255, default='', null=True, blank=True)
    linkedin = models.CharField(max_length=255, default='', null=True, blank=True)
    pinterest = models.CharField(max_length=255, default='', null=True, blank=True)
    snapchat = models.CharField(max_length=255, default='', null=True, blank=True)
    tripadvisor = models.CharField(max_length=255, default='', null=True, blank=True)

    def __str__(self):
        return self.store_name

    @property
    def nb_clients(self):
        return self.customers.all().count()

    @property
    def slug(self):
        return slugify(self.store_name)


class VendorOpeningHours(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, related_name="opening_hours")
    monday = models.CharField(max_length=100, blank=True, default="-")
    tuesday = models.CharField(max_length=100, blank=True, default="-")
    wednesday = models.CharField(max_length=100, blank=True, default="-")
    thursday = models.CharField(max_length=100, blank=True, default="-")
    friday = models.CharField(max_length=100, blank=True, default="-")
    saturday = models.CharField(max_length=100, blank=True, default="-")
    sunday = models.CharField(max_length=100, blank=True, default="-")

    def __str__(self):
        return 'Heures d\'ouvertures de {}'.format(self.vendor.store_name)


class RewardCardLayout(models.Model):
    """
        This model represents a design of vendor's reward card, it will be used with Apple Wallet.
    """
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, null=True, blank=True, related_name="reward_card_layout")
    icon = models.ForeignKey(VendorMedia, on_delete=models.SET_NULL, related_name="icons", default=None, null=True, blank=True)
    logo = models.ForeignKey(VendorMedia, on_delete=models.SET_NULL, related_name="logos", default=None, null=True, blank=True)
    bg_color = models.CharField(max_length=7, default="#000000")
    text_color = models.CharField(max_length=7, default="#ffffff")

    def __str__(self):
        return 'Fidelity Card Layout for {}'.format(self.vendor)


@receiver(post_save, sender=Vendor)
def create_default_layout(sender, instance, created, **kwargs):
    """
        This function is connected to Vendor Modeal creation to create a default RewardCardLayout and a default Opening Hours
    """
    if created:
        VendorOpeningHours.objects.create(vendor=instance)
        RewardCardLayout.objects.create(vendor=instance)




class Discount(models.Model):
    """
        This model represents all discounts created by the Vendor. They can be applied to the Customers.
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="discounts")
    image = models.FileField(default=None, blank=True, null=True, upload_to="discounts/")
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=40)
    description = models.TextField()
    min_points = models.IntegerField(default=0)
    start_date = models.DateTimeField(default=None, null=True, blank=True)
    end_date = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return 'Réduction "{}" - {}'.format(self.name, self.status_text)

    @property
    def status_text(self):
        if self.is_active:
            if timezone.now() >= self.start_date and timezone.now() <= self.end_date:
                return 'Actif'
            elif timezone.now() < self.start_date:
                return 'A venir'
            else:
                return 'Expiré'
        else:
            return 'Désactivé'
        


class Offer(models.Model):
    """
        This model represents all offers created by the Vendor. They can be applied to the Customers using customers points.
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="offers")
    image = models.FileField(default=None, blank=True, null=True, upload_to="offers/")
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=40)
    description = models.TextField()
    cost = models.IntegerField()
    start_date = models.DateTimeField(default=None, null=True, blank=True)
    end_date = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return 'Offre "{}" - {}'.format(self.name, self.status_text)

    @property
    def status_text(self):
        if self.is_active:
            if timezone.now() >= self.start_date and timezone.now() <= self.end_date:
                return 'Actif'
            elif timezone.now() < self.start_date:
                return 'A venir'
            else:
                return 'Expiré'
        else:
            return 'Désactivé'