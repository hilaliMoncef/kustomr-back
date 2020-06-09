from django.contrib import admin
from .models import AmountDiscount, PercentDiscount, PointsDiscount


admin.site.register(AmountDiscount)
admin.site.register(PercentDiscount)
admin.site.register(PointsDiscount)
