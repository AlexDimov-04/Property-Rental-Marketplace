from django import forms
from .models import BaseProperty ,Apartment, Villa, Office, Shop, Building

class BasePropertyForm(forms.ModelForm):
    class Meta:
        model = BaseProperty
        exclude = ('property',)

class ApartmentForm(BasePropertyForm):
    class Meta(BasePropertyForm.Meta):
        model = Apartment

class VillaForm(BasePropertyForm):
    class Meta(BasePropertyForm.Meta):
        model = Villa

class OfficeForm(BasePropertyForm):
    class Meta(BasePropertyForm.Meta):
        model = Office

class ShopForm(BasePropertyForm):
    class Meta(BasePropertyForm.Meta):
        model = Shop

class BuildingForm(BasePropertyForm):
    class Meta(BasePropertyForm.Meta):
        model = Building
