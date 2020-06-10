from django.db import models
from Users.models import User
from Vendor.models import Vendor
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Sum, Avg
from Discount.models import PointsDiscount, PercentDiscount, AmountDiscount
import pandas as pd


class CustomerToken(models.Model):
    token = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.token


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    birthday = models.DateField()
    token = models.OneToOneField(CustomerToken, on_delete=models.CASCADE, related_name="customer", default=None, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="customers")
    points = models.IntegerField(default=0)
    imported = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.vendor.store_name, self.first_name + ' ' + self.last_name)

    @property
    def next_gift(self):
        discounts = list(self.vendor.discounts.filter(is_active=True, end_date__gte=timezone.now(), min_points__gt=self.points).values_list('min_points', flat=True))
        offers = list(self.vendor.offers.filter(is_active=True, end_date__gte=timezone.now(), cost__gt=self.points).values_list('cost', flat=True))
        all_points = discounts + offers or [0]
        return min(all_points) - self.points

    @property
    def name(self):
        return '{} {}'.format(self.first_name.capitalize(), self.last_name.capitalize())

    @property
    def visit_freq(self):
        if self.transactions.count() <= 0:
            return 0
        else:
            dates = self.transactions.filter(refunded=False).values_list('date', flat=True)
            df = pd.DataFrame(dates, columns=['Date'])
            pd.to_datetime(df['Date'])
            stat = df.groupby([df['Date'].dt.year, df['Date'].dt.month]).agg('count')
            return stat['Date'].mean()

    @property
    def last_visit(self):
        if self.transactions.count() <= 0:
            return None
        else:
            return self.transactions.filter(refunded=False).order_by('-date').first().date

    @property
    def total_expenses(self):
        if self.transactions.count() <= 0:
            return 0
        else:
            return self.transactions.filter(refunded=False).aggregate(Sum('amount'))['amount__sum']
    
    @property
    def avg_expenses(self):
        if self.transactions.count() <= 0:
            return 0
        else:
            return self.transactions.filter(refunded=False).aggregate(Avg('amount'))['amount__avg']


@receiver(post_save, sender=Customer)
def save_token(sender, instance, created, **kwargs):
    if created:
        from secrets import token_urlsafe
        instance.token = CustomerToken.objects.create(token=token_urlsafe(20))
        instance.save()


class CustomersList(models.Model):
    name = models.CharField(max_length=255)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="lists")
    customers = models.ManyToManyField(Customer, related_name="lists")
    #mail_campaigns = models.ManyToManyField(MailCampaign, related_name="lists")
    #sms_campaigns = models.ManyToManyField(MailCampaign, related_name="sms_lists")
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Liste {}'.format(self.name)


class Transaction(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="transactions")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="transactions")
    amount = models.FloatField()
    amount_discounted = models.FloatField()
    point_discount = models.ForeignKey(PointsDiscount, on_delete=models.SET_NULL, related_name="transactions", null=True, blank=True, default=None)
    amount_discount = models.ForeignKey(AmountDiscount, on_delete=models.SET_NULL, related_name="transactions", null=True, blank=True, default=None)
    percent_discount = models.ForeignKey(PercentDiscount, on_delete=models.SET_NULL, related_name="transactions", null=True, blank=True, default=None)
    refunded = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    date_refund = models.DateTimeField(default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.customer.points += self.amount_discounted
            self.customer.save()
        super(Transaction, self).save(*args, **kwargs)


    def __str__(self):
        return '{}{} chez {} le {}'.format('Remboursé - ' if self.refunded else '', self.customer, self.vendor.store_name, self.date)