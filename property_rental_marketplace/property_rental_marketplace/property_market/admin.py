from django.contrib import admin
from property_rental_marketplace.property_market.models import BaseProperty, Apartment \
    ,Villa, Office, Shop, Building, PropertyEstimate

@admin.register(BaseProperty)
class BasePropertyAdmin(admin.ModelAdmin):
    pass

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Villa)
class VillaAdmin(admin.ModelAdmin):
    pass

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    pass

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    pass

@admin.register(PropertyEstimate)
class PropertyEstimateAdmin(admin.ModelAdmin):
    pass