from django import forms
from .models import ArticleMedia, DiscountMedia, VendorMedia


class ArticleMediaUploadForm(forms.ModelForm):
    class Meta:
        model = ArticleMedia
        fields = ['file']


class DiscountMediaUploadForm(forms.ModelForm):
    class Meta:
        model = DiscountMedia
        fields = ['file']


class VendorMediaUploadForm(forms.ModelForm):
    class Meta:
        model = VendorMedia
        fields = ['file']
