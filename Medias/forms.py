from django import forms
from .models import ArticleMedia, DiscountMedia, VendorMedia, TrainingMedia, EmailMedia


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


class TrainingMediaUploadForm(forms.ModelForm):
    class Meta:
        model = TrainingMedia
        fields = ['file']


class EmailMediaUploadForm(forms.ModelForm):
    class Meta:
        model = EmailMedia
        fields = ['file']
