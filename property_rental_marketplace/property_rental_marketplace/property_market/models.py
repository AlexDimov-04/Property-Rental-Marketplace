from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BaseProperty(models.Model):
    STATE_CHOICES = [
        ('For Sell', 'For Sell'),
        ('For Rent', 'For Rent'),
        ('Featured', 'Featured'),
    ]

    TYPE_CHOICES = [
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
        ('Office', 'Office'),
        ('Shop', 'Shop'),
        ('Building', 'Building')
    ]

    created_at = models.DateTimeField(default=timezone.now, editable=False)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties_created', default=1)

    property_state = models.CharField(
        max_length=10,
        choices=STATE_CHOICES
    )

    property_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )

    price = models.PositiveIntegerField()

    title = models.CharField(
        max_length=100
    )

    images = models.ImageField(
        upload_to='property_images',
        null=True,
        blank=True,
    )

    location = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.title

class Apartment(models.Model):
    property = models.OneToOneField(BaseProperty, on_delete=models.CASCADE)

    description = models.TextField(
        max_length=300
    )

    num_bedrooms = models.PositiveIntegerField()

    num_bathrooms = models.PositiveIntegerField()

    area_sqft  = models.PositiveIntegerField()

    floor_number = models.PositiveIntegerField()

    has_balcony = models.BooleanField()

    is_furnished = models.BooleanField()

    has_air_conditioning = models.BooleanField()

    def __str__(self):
        return f"Apartment: {self.property.title}"

class Villa(models.Model):
    property = models.OneToOneField(BaseProperty, on_delete=models.CASCADE)
    description = models.TextField()
    num_bedrooms = models.PositiveIntegerField()
    num_bathrooms = models.PositiveIntegerField()
    area_sqft = models.PositiveIntegerField()
    has_garden = models.BooleanField()
    has_pool = models.BooleanField()

    def __str__(self):
        return f"Villa: {self.property.title}" 

class Office(models.Model):
    property = models.OneToOneField(BaseProperty, on_delete=models.CASCADE)
    description = models.TextField()
    num_rooms = models.PositiveIntegerField()
    area_sqft = models.PositiveIntegerField()
    floor_number = models.PositiveIntegerField()
    has_parking = models.BooleanField()
    has_lift = models.BooleanField()

    def __str__(self):
        return f"Office: {self.property.title}"
    
class Shop(models.Model):
    property = models.OneToOneField(BaseProperty, on_delete=models.CASCADE)
    description = models.TextField()
    area_sqft = models.PositiveIntegerField()
    has_ac = models.BooleanField()
    has_cctv = models.BooleanField()

    def __str__(self):
        return f"Shop: {self.property.title}"
    
class Building(models.Model):
    property = models.OneToOneField(BaseProperty, on_delete=models.CASCADE)
    description = models.TextField()
    num_floors = models.PositiveIntegerField()
    total_area_sqft = models.PositiveIntegerField()
    has_lift = models.BooleanField()
    has_parking = models.BooleanField()

    def __str__(self):
        return f"Building: {self.property.title}"
    