from django.contrib import admin
from .models import Customer, CustomerToken, CustomersList, Transaction

admin.site.register(Customer)
admin.site.register(Transaction)
admin.site.register(CustomerToken)
admin.site.register(CustomersList)