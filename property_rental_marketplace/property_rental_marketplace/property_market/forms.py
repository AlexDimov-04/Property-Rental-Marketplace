from django import forms
from .models import BaseProperty, SavedProperty, Apartment, Villa, Office, Shop, Building, PropertyEstimate

class PropertyEstimateForm(forms.ModelForm):
    class Meta:
        model = PropertyEstimate
        exclude = ('estimate_value',)

class SavePropertyForm(forms.ModelForm):
    class Meta:
        model = SavedProperty
        fields = ['property']

class BasePropertyForm(forms.ModelForm):
    class Meta:
        model = BaseProperty
        exclude = ("property", "owner", "created_at", "saved_by_users")

        widgets = {
            "price": forms.NumberInput(
                attrs={"placeholder": "Price"}
            ),

            "title": forms.TextInput(
                attrs={"placeholder": "Title"}
            ),

            "location": forms.TextInput(
                attrs={"placeholder": "Location"}
            ),
        }


class ApartmentForm(BasePropertyForm):
    class Meta(BasePropertyForm.Meta):
        model = Apartment

        widgets = {
            "description": forms.TextInput(
                attrs={"placeholder": "Apartment Description"}
            ),

            "num_bedrooms": forms.NumberInput(
                attrs={"placeholder": "Bedrooms"}
            ),

            "num_bathrooms": forms.NumberInput(
                attrs={"placeholder": "Bathrooms"}
            ),

            "area_sqft": forms.NumberInput(
                attrs={"placeholder": "Area Sqft"}
            ),

            "floor_number": forms.NumberInput(
                attrs={"placeholder": "Floor Number"}
            ),
        }


class VillaForm(BasePropertyForm):
    class Meta(BasePropertyForm.Meta):
        model = Villa

        widgets = {
            "description": forms.TextInput(
                attrs={"placeholder": "Villa Description"}
            ),

            "num_bedrooms": forms.NumberInput(
                attrs={"placeholder": "Bedrooms"}
            ),

            "num_bathrooms": forms.NumberInput(
                attrs={"placeholder": "Bathrooms"}
            ),

            "area_sqft": forms.NumberInput(
                attrs={"placeholder": "Area Sqft"}
            ),

            "floor_number": forms.NumberInput(
                attrs={"placeholder": "Floor Number"}
            ),  
        }


class OfficeForm(BasePropertyForm):
    class Meta(BasePropertyForm.Meta):
        model = Office

        widgets = {
            "description": forms.TextInput(
                attrs={"placeholder": "Office Description"}
            ),

            "num_rooms": forms.NumberInput(
                attrs={"placeholder": "Rooms"}
            ),

            "area_sqft": forms.NumberInput(
                attrs={"placeholder": "Area Sqft"}
            ),

            "floor_number": forms.NumberInput(
                attrs={"placeholder": "Floor Number"}
            ),  
        }


class ShopForm(BasePropertyForm):
    class Meta(BasePropertyForm.Meta):
        model = Shop

        widgets = {
            "description": forms.TextInput(
                attrs={"placeholder": "Shop Description"}
            ),

            "area_sqft": forms.NumberInput(
                attrs={"placeholder": "Area Sqft"}
            ),
        }


class BuildingForm(BasePropertyForm):
    class Meta(BasePropertyForm.Meta):
        model = Building

        widgets = {
            "description": forms.TextInput(
                attrs={"placeholder": "Building Description"}
            ),

            "num_floors": forms.NumberInput(
                attrs={"placeholder": "Number Of Floors"}
            ),

            "total_area_sqft": forms.NumberInput(
                attrs={"placeholder": "Total Area Sqft"}
            ),  
        }
