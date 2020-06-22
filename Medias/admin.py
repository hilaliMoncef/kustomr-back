from django.contrib import admin
from .models import ArticleMedia, VendorMedia, DiscountMedia, TrainingMedia, EmailMedia, SocialMedia


admin.site.register(ArticleMedia)
admin.site.register(VendorMedia)
admin.site.register(DiscountMedia)
admin.site.register(TrainingMedia)
admin.site.register(EmailMedia)
admin.site.register(SocialMedia)