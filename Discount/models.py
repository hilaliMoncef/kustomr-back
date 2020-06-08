from django.db import models
from django.utils import timezone
from Medias.models import DiscountMedia
from Vendor.models import Vendor


class PointsDiscount(models.Model):
    """
        This model represents all discounts created by the Vendor. They can be applied to the Customers.
    """
    AMOUNT_TYPE_CHOICES = [
        ('M', 'Euros'),
        ('P', 'Pourcentage')
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="point_discounts")
    image = models.ForeignKey(DiscountMedia, on_delete=models.SET_NULL, related_name="point_discounts", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=40)
    min_points = models.IntegerField()
    type_amount = models.CharField(max_length=1, choices=AMOUNT_TYPE_CHOICES)
    amount = models.FloatField()
    description = models.TextField()
    start_date = models.DateTimeField(default=None, null=True, blank=True)
    end_date = models.DateTimeField(default=None, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Réduction Points de Fidélité "{}" - {}'.format(self.name, self.status_text)

    @property
    def status(self):
        if self.is_active:
            if timezone.now() >= self.start_date and timezone.now() <= self.end_date:
                return 0
            elif timezone.now() < self.start_date:
                return 1
            else:
                return -1
        else:
            return -2


class AmountDiscount(models.Model):
    """
        This model represents all discounts created by the Vendor. They can be applied to the Customers.
    """
    AMOUNT_TYPE_CHOICES = [
        ('M', 'Euros'),
        ('P', 'Pourcentage')
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="amount_discounts")
    image = models.ForeignKey(DiscountMedia, on_delete=models.SET_NULL, related_name="amount_discounts", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=40)
    min_bill = models.IntegerField()
    type_amount = models.CharField(max_length=1, choices=AMOUNT_TYPE_CHOICES)
    amount = models.FloatField()
    description = models.TextField()
    start_date = models.DateTimeField(default=None, null=True, blank=True)
    end_date = models.DateTimeField(default=None, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Réduction Montant Fixe "{}" - {}'.format(self.name, self.status_text)

    @property
    def status(self):
        if self.is_active:
            if timezone.now() >= self.start_date and timezone.now() <= self.end_date:
                return 0 # Actif
            elif timezone.now() < self.start_date:
                return 1 # A venir
            else:
                return -1 # Expiré
        else:
            return -2 # Désactivé


class PercentDiscount(models.Model):
    """
        This model represents all discounts created by the Vendor. They can be applied to the Customers.
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="percent_discounts")
    image = models.ForeignKey(DiscountMedia, on_delete=models.SET_NULL, related_name="percent_discounts", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=40)
    amount = models.FloatField()
    description = models.TextField()
    start_date = models.DateTimeField(default=None, null=True, blank=True)
    end_date = models.DateTimeField(default=None, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Réduction Pourcentage "{}" - {}'.format(self.name, self.status_text)

    @property
    def status(self):
        if self.is_active:
            if timezone.now() >= self.start_date and timezone.now() <= self.end_date:
                return 0 # Actif
            elif timezone.now() < self.start_date:
                return 1 # A venir
            else:
                return -1 # Expiré
        else:
            return -2 # Désactivé