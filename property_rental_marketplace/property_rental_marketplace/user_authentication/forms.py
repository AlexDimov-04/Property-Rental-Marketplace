from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from property_rental_marketplace.user_authentication.models import UserProfile

class UserRegistrationForm(auth_forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = (
                "form-control not-required"
                if field_name in ("first_name", "last_name")
                else "form-control"
            )

            field.widget.attrs["id"] = field_name

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.email = user.email
            profile.save()

        return user

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if email and User.objects.filter(email=email).exists():
            self.add_error("email", "This email address is already in use.")

        if User.objects.filter(username=username).exists():
            self.add_error("username", "This username is already taken.")

        if username:
            if len(username) < 2:
                self.add_error("username", "Username must be at least 2 characters long.")
            if username.isdigit() or username[0].isupper():
                self.add_error("username", "Invalid username.")

        if first_name:
            if len(first_name) < 2:
                self.add_error("first_name", " First name should be at least 2 characters long.")
            elif any(char.isdigit() for char in first_name):
                self.add_error("first_name", " First name cannot contain digits.")
            elif first_name[0].islower():
                self.add_error("first_name", " First name should start with an uppercase letter.")

        if last_name:
            if len(last_name) < 2:
                self.add_error("last_name", " Last name should be at least 2 characters long.")
            elif any(char.isdigit() for char in last_name):
                self.add_error("last_name", " Last name cannot contain digits.")
            elif last_name[0].islower():
                self.add_error("last_name", " Last name should start with an uppercase letter.")

        return cleaned_data


    class Meta(auth_forms.UserCreationForm.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )