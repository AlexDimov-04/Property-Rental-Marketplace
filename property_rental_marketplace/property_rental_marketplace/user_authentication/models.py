from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserProfile(models.Model):

    GENDER_CHOICES = [
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
        ('Do not specify', 'Do not specify')
    ]

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(
        max_length=30, 
        null=True, 
        blank=True,
    )

    last_name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )

    email = models.EmailField(
        null=True,
        blank=True
    )

    birth_date = models.DateField(
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )

    country = models.CharField(
        null=True,
        blank=True
    )

    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        null=True,
        blank=True,
        help_text='Contact Phone Number'
    )

    bio = models.TextField(
        max_length=500,
        null=True, 
        blank=True
    )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username
    
class UserComment(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    comment = models.TextField(max_length=250)

    profession = models.CharField(
        max_length=30,
    )

    timestamp = models.DateTimeField(auto_now_add=True)

class UserPayment(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)

@receiver(post_save, sender=UserProfile)
def create_user_payment(sender, instance, created, **kwargs):
	if created:
		UserPayment.objects.create(user_profile=instance)
                